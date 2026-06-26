const express = require('express');
const fs = require('fs');
const path = require('path');
const archiver = require('archiver');
const { GoogleGenAI } = require('@google/genai'); 
const state = require('../config/state');

const router = express.Router();

const getValidatedSessionDir = (rawId) => {
    if (!rawId) throw new Error("ID is required.");
    const safeId = state.sanitizeId(rawId);
    const baseDir = path.resolve(state.downloadsDir);
    const targetDir = path.resolve(baseDir, safeId);
    if (!targetDir.startsWith(baseDir + path.sep)) throw new Error("Forbidden: Invalid path traversal detected.");
    return targetDir;
};

// --- NEW SESSION MANAGEMENT ENDPOINTS ---

// List all sessions (folders in downloads directory)
router.get('/sessions', (req, res) => {
    try {
        if (!fs.existsSync(state.downloadsDir)) return res.json({ success: true, sessions: [] });
        
        const dirs = fs.readdirSync(state.downloadsDir, { withFileTypes: true })
            .filter(dirent => dirent.isDirectory() && dirent.name !== 'temp_uploads') // Ignore temp folder
            .map(dirent => dirent.name)
            .sort((a, b) => {
                const statA = fs.statSync(path.join(state.downloadsDir, a));
                const statB = fs.statSync(path.join(state.downloadsDir, b));
                return statB.mtime.getTime() - statA.mtime.getTime(); // Sort Newest First
            });
        res.json({ success: true, sessions: dirs });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

// Load the text content of a specific session
router.get('/session-data', (req, res) => {
    try {
        const sessionDir = getValidatedSessionDir(req.query.id);
        if (!fs.existsSync(sessionDir)) return res.status(404).json({error: "Session not found"});
        
        const readIfExists = (filename) => {
            const p = path.join(sessionDir, filename);
            return fs.existsSync(p) ? fs.readFileSync(p, 'utf8') : null;
        };

        res.json({
            success: true,
            originalText: readIfExists('original.txt'),
            script: readIfExists('script.txt'),
            prompt: readIfExists('prompt.txt'),
            linkedinPost: readIfExists('linkedin_post.txt'),
            hasAudio: fs.existsSync(path.join(sessionDir, 'podcast.m4a')),
            hasImage: fs.existsSync(path.join(sessionDir, 'thumbnail.png')),
            hasVideo: fs.existsSync(path.join(sessionDir, 'linkedin_podcast.mp4'))
        });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

// Clear all sessions
router.delete('/delete-all-sessions', (req, res) => {
    try {
        if (!fs.existsSync(state.downloadsDir)) return res.json({ success: true });

        const dirs = fs.readdirSync(state.downloadsDir, { withFileTypes: true })
            .filter(dirent => dirent.isDirectory() && dirent.name !== 'temp_uploads')
            .map(dirent => dirent.name);
        
        for (const dir of dirs) {
            fs.rmSync(path.join(state.downloadsDir, dir), { recursive: true, force: true });
        }
        res.json({ success: true, message: "All sessions cleared." });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

// --- EXISTING ENDPOINTS ---

router.post('/save-file', (req, res) => {
    try {
        const { id, type, content } = req.body;
        const sessionDir = getValidatedSessionDir(id);
        if (!fs.existsSync(sessionDir)) return res.status(404).json({error: "Session not found."});

        let filename;
        if (type === 'script') filename = 'script.txt';
        else if (type === 'prompt') filename = 'prompt.txt';
        else if (type === 'linkedin') filename = 'linkedin_post.txt';
        else return res.status(400).json({error: "Invalid file type."});

        fs.writeFileSync(path.join(sessionDir, filename), content);
        res.json({ success: true, message: "Saved successfully!" });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

router.post('/translate-original', async (req, res) => {
    try {
        const { id, targetLanguage } = req.body;
        const sessionDir = getValidatedSessionDir(id);
        const originalFile = path.join(sessionDir, 'original.txt');
        
        if (!fs.existsSync(originalFile)) return res.status(404).json({error: "Original text not found."});
        const originalText = fs.readFileSync(originalFile, 'utf8');

        if (targetLanguage === 'English') return res.json({ text: originalText });

        const ai = new GoogleGenAI({ apiKey: process.env.GEMINI_API_KEY });
        const prompt = `Translate the following text into ${targetLanguage}. Output ONLY the translated text.\n\nText:\n${originalText.substring(0, 25000)}`;
        const response = await ai.models.generateContent({ model: 'gemini-2.5-flash', contents: prompt });
        
        res.json({ text: response.text.trim() });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

router.get('/download-zip', (req, res) => {
    try {
        const sessionDir = getValidatedSessionDir(req.query.id);
        if (!fs.existsSync(sessionDir)) return res.status(404).send("Session not found.");
        const safeAttachmentName = `omnicast_session_${path.basename(sessionDir)}.zip`;
        res.attachment(safeAttachmentName);
        const archive = archiver('zip', { zlib: { level: 9 } });
        archive.pipe(res);
        archive.directory(sessionDir, false);
        archive.finalize();
    } catch (error) {
        const status = error.message.includes('Forbidden') ? 403 : 400;
        res.status(status).send(error.message);
    }
});

router.delete('/delete-folder', (req, res) => {
    try {
        const sessionDir = getValidatedSessionDir(req.body.id);
        if (fs.existsSync(sessionDir)) fs.rmSync(sessionDir, { recursive: true, force: true });
        res.json({ success: true, message: "Folder safely removed." });
    } catch (error) {
        const status = error.message.includes('Forbidden') ? 403 : 400;
        res.status(status).json({ success: false, error: error.message });
    }
});

// --- NEW CONFIG ENDPOINT ---
router.get('/config', (req, res) => {
    res.json({ googleClientId: process.env.GOOGLE_CLIENT_ID || null });
});

module.exports = router;