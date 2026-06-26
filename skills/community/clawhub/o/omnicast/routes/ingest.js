const express = require('express');
const fs = require('fs');
const path = require('path');
const multer = require('multer');
const axios = require('axios');
const cheerio = require('cheerio');
const ytdl = require('@distube/ytdl-core'); 
const { YoutubeTranscript } = require('youtube-transcript-plus');
const { getGeminiClient } = require('../utils/geminiClient'); 
const state = require('../config/state');
const { emitStreamLog } = require('../utils/streamer');
const { processLocalFile } = require('../utils/fileProcessor');
const dns = require('dns').promises; // NEW: Import DNS module

const router = express.Router();
const tempUploadsDir = path.join(state.downloadsDir, 'temp_uploads');
if (!fs.existsSync(tempUploadsDir)) fs.mkdirSync(tempUploadsDir, { recursive: true });
const upload = multer({ dest: tempUploadsDir, limits: { fileSize: 500 * 1024 * 1024 } });

// --- UPDATED SECURITY MIDDLEWARE (DNS Resolution) ---
const ssrfProtection = async (req, res, next) => {
    const { sourceType, url } = req.body;
    
    if (sourceType === 'url' && url) {
        try {
            const parsedUrl = new URL(url);
            
            // 1. Enforce safe protocols
            if (!['http:', 'https:'].includes(parsedUrl.protocol)) {
                return res.status(400).json({ error: "Security Exception: Only HTTP and HTTPS protocols are allowed." });
            }

            const hostname = parsedUrl.hostname;

            // 2. Resolve the hostname to its actual IP address to prevent DNS rebinding
            const lookup = await dns.lookup(hostname);
            const resolvedIp = lookup.address;

            // 3. Block local and private IP ranges
            const isLocalOrPrivate = /^(localhost|127\.0\.0\.1|0\.0\.0\.0|10\.\d+\.\d+\.\d+|192\.168\.\d+\.\d+|172\.(1[6-9]|2[0-9]|3[0-1])\.\d+\.\d+|169\.254\.\d+\.\d+|::1)$/i.test(resolvedIp) || hostname.toLowerCase() === 'localhost';
            
            if (isLocalOrPrivate) {
                return res.status(403).json({ error: "Security Exception: Access to local or private networks is strictly forbidden." });
            }
        } catch (err) {
            return res.status(400).json({ error: "Security Exception: Malformed URL or DNS resolution failed." });
        }
    }
    next();
};

router.post('/ingest', upload.single('file'), ssrfProtection, async (req, res) => {
    const { id, sourceType, url } = req.body;
    const safeId = state.sanitizeId(id);
    const sessionDir = path.join(state.downloadsDir, safeId);

    if (!fs.existsSync(sessionDir)) fs.mkdirSync(sessionDir, { recursive: true });
    
    let extractedText = "";

    try {
        emitStreamLog(safeId, { message: "Initializing ingestion engine..." });

        if (sourceType === 'url' && url) {
            const lowerUrl = url.toLowerCase();
            
            if (lowerUrl.endsWith('.mp4')) {
                const tempVideoPath = path.join(sessionDir, 'downloaded.mp4');
                const response = await axios({ method: 'GET', url: url, responseType: 'stream' });
                const writer = fs.createWriteStream(tempVideoPath);
                response.data.pipe(writer);
                await new Promise((resolve, reject) => { writer.on('finish', resolve); writer.on('error', reject); });
                
                extractedText = await processLocalFile(tempVideoPath, 'video/mp4', sessionDir, safeId);
                if (fs.existsSync(tempVideoPath)) fs.unlinkSync(tempVideoPath);
                
            } else if (lowerUrl.includes('youtube.com') || lowerUrl.includes('youtu.be')) {
                
                try {
                    // ATTEMPT 1: Fast transcript extraction
                    emitStreamLog(safeId, { message: "Fetching YouTube closed captions..." });
                    const transcriptData = await YoutubeTranscript.fetchTranscript(url);
                    extractedText = transcriptData.map(item => item.text).join(' ');
                    emitStreamLog(safeId, { message: "YouTube transcript successfully extracted!" });

                } catch (ytError) {
                    // ATTEMPT 2: Whisper Fallback (Video has no captions)
                    emitStreamLog(safeId, { message: "No captions found. Falling back to Whisper audio transcription..." });
                    
                    const tempAudioPath = path.join(sessionDir, 'yt_audio.mp4');
                    
                    await new Promise((resolve, reject) => {
                        // Download the highest quality audio stream available
                        const stream = ytdl(url, { filter: 'audioonly', quality: 'highestaudio' });
                        const writer = fs.createWriteStream(tempAudioPath);
                        stream.pipe(writer);
                        writer.on('finish', resolve);
                        stream.on('error', reject);
                    });

                    // Pass the downloaded YouTube audio into our existing Whisper chunking logic
                    extractedText = await processLocalFile(tempAudioPath, 'audio/mp4', sessionDir, safeId);
                    
                    if (fs.existsSync(tempAudioPath)) fs.unlinkSync(tempAudioPath);
                }

            } else {
                emitStreamLog(safeId, { message: "Scraping target URL..." });
                const response = await axios.get(url, { headers: { 'User-Agent': 'Mozilla/5.0' }, timeout: 10000 });
                const $ = cheerio.load(response.data);
                
                $('header, footer, nav, aside, script, style, noscript, svg, button').remove();
                let contentContainer = $('article').length > 0 ? $('article') : $('body');
                
                contentContainer.find('p, h1, h2, h3').each((i, el) => {
                    const text = $(el).text().trim();
                    if (text.length > 1) extractedText += text + "\n\n";
                });

                if (!extractedText.trim()) extractedText = contentContainer.text().replace(/\s+/g, ' ').trim();
            }
        } else if (req.file) {
            const tempPath = req.file.path;
            const mimeType = req.file.mimetype;
            emitStreamLog(safeId, { message: `Processing uploaded file...` });

            try {
                extractedText = await processLocalFile(tempPath, mimeType, sessionDir, safeId);
            } finally {
                if (fs.existsSync(tempPath)) fs.unlinkSync(tempPath);
            }
        }

        if (!extractedText.trim()) throw new Error("Could not extract meaningful text. The page might be protected or empty.");

        // Language Detection & Dual-Save Logic
        emitStreamLog(safeId, { message: "Analyzing language..." });
        
        const ai = getGeminiClient();
        
        const langPrompt = `What language is the following text predominantly written in? Respond with ONLY the English name of the language (e.g., "Spanish", "English", "Arabic", "French"). Do not include any other text.\n\nText: ${extractedText.substring(0, 1000)}`;
        const langRes = await ai.models.generateContent({ model: 'gemini-2.5-flash', contents: langPrompt });
        let detectedLanguage = langRes.text.trim().replace(/[^a-zA-Z]/g, '');

        let finalEnglishText = extractedText;

        if (detectedLanguage.toLowerCase() !== 'english') {
            emitStreamLog(safeId, { message: `Detected ${detectedLanguage}. Archiving original and translating to English...` });
            
            fs.writeFileSync(path.join(sessionDir, `original-${detectedLanguage.toLowerCase()}.txt`), extractedText);
            
            const translatePrompt = `Translate the following ${detectedLanguage} text into English. Output ONLY the English translation.\n\nText:\n${extractedText.substring(0, 30000)}`;
            const translateRes = await ai.models.generateContent({ model: 'gemini-2.5-flash', contents: translatePrompt });
            finalEnglishText = translateRes.text.trim();
        }

        fs.writeFileSync(path.join(sessionDir, 'original.txt'), finalEnglishText);

        emitStreamLog(safeId, { message: "Ingestion complete! Ready for script drafting." });
        res.json({ success: true, fullText: finalEnglishText, detectedLanguage });
    } catch (error) {
        emitStreamLog(safeId, { status: 'error', message: error.message });
        res.status(500).json({ error: error.message });
    }
});

module.exports = router;