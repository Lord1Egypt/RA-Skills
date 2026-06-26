const express = require('express');
const fs = require('fs');
const path = require('path');
const ffmpeg = require('fluent-ffmpeg');
const OpenAI = require('openai');
const axios = require('axios');
const rateLimit = require('express-rate-limit');
const state = require('../config/state');
const secrets = require('../config/secrets'); 
const { emitStreamLog, delay } = require('../utils/streamer');

const router = express.Router();
const synthesizeLimiter = rateLimit({ windowMs: 60 * 60 * 1000, max: 10 });

function formatVTTTime(totalSeconds) {
    const totalMs = Math.round(totalSeconds * 1000);
    const h = Math.floor(totalMs / 3600000);
    const m = Math.floor((totalMs % 3600000) / 60000);
    const s = Math.floor((totalMs % 60000) / 1000);
    const ms = totalMs % 1000;
    const pad = (num, size) => num.toString().padStart(size, '0');
    return `${pad(h, 2)}:${pad(m, 2)}:${pad(s, 2)}.${pad(ms, 3)}`;
}

router.post('/synthesize', synthesizeLimiter, async (req, res) => {
    const { id, script, host1 = 'Alex', host2 = 'Sam', ttsEngine = 'openai', host1VoiceId, host2VoiceId } = req.body;
    const safeId = state.sanitizeId(id);
    const sessionDir = path.join(state.downloadsDir, safeId);
    
    if (!script) return res.status(400).json({ error: "Script content required" });
    if (!fs.existsSync(sessionDir)) fs.mkdirSync(sessionDir, { recursive: true });

    const sanitizedScript = script.replace(/<[^>]*>?/gm, '').replace(/\*\*/g, '').replace(/\*/g, '').replace(/^[-•]\s*/gm, '').replace(/^\d+\.\s*/gm, '').replace(/\r\n/g, '\n').trim();
    const regex = /^([a-zA-Z0-9_ ]+)\s*:\s*([\s\S]*?)(?=^[a-zA-Z0-9_ ]+\s*:|\s*$)/gm;
    let match;
    const segments = [];
    while ((match = regex.exec(sanitizedScript)) !== null) {
        if (match[2].trim().length > 0) segments.push({ s: match[1].trim(), t: match[2].trim() });
    }

    if (segments.length === 0) return res.status(400).json({ error: "No valid dialogue found." });

    state.jobs[safeId] = { status: 'queued', message: 'Queued for processing...', timestamp: Date.now() };
    res.json({ success: true, message: "Synthesis started." });

    const pcmPath = path.join(sessionDir, 'temp.pcm');
    const finalAudioPath = path.join(sessionDir, 'podcast.m4a');
    const vttPath = path.join(sessionDir, 'podcast.vtt');
    
    const openai = new OpenAI(); 

    try {
        const writeStream = fs.createWriteStream(pcmPath);
        let vttContent = "WEBVTT\n\n";
        let currentTime = 0.0;
        const silenceDuration = 0.5;
        const sampleRate = 24000;
        const silenceBytes = Buffer.alloc(sampleRate * 2 * silenceDuration);

        for (let i = 0; i < segments.length; i++) {
            const lineText = segments[i].t;
            const isHost2 = segments[i].s.toLowerCase().includes(host2.toLowerCase());
            const msg = `Synthesizing chunk ${i + 1} of ${segments.length} via ${ttsEngine.toUpperCase()}...`;
            
            emitStreamLog(safeId, { status: 'processing', message: msg });
            
            let audioData = null;
            let attempt = 0;
            while (attempt <= 3) {
                try {
                    if (ttsEngine === 'elevenlabs') {
                        const targetVoiceId = isHost2 ? host2VoiceId : host1VoiceId;
                        const response = await axios({
                            method: 'POST',
                            url: `https://api.elevenlabs.io/v1/text-to-speech/${targetVoiceId}?output_format=pcm_24000`,
                            headers: { 'xi-api-key': secrets.getElevenLabsKey(), 'Content-Type': 'application/json' },
                            data: { text: lineText, model_id: "eleven_multilingual_v2" },
                            responseType: 'arraybuffer'
                        });
                        audioData = Buffer.from(response.data);
                    } else {
                        const response = await openai.audio.speech.create({
                            model: "tts-1", voice: isHost2 ? "echo" : "shimmer", input: lineText, response_format: "pcm"
                        });
                        audioData = Buffer.from(await response.arrayBuffer());
                    }
                    break;
                } catch (err) {
                    attempt++;
                    if (attempt > 3) throw err;
                    await delay(Math.pow(2, attempt) * 1000);
                }
            }

            writeStream.write(audioData);
            const duration = audioData.length / (sampleRate * 2);
            vttContent += `${formatVTTTime(currentTime)} --> ${formatVTTTime(currentTime + duration)}\n<v ${segments[i].s}>${lineText}\n\n`;
            currentTime += duration;
            writeStream.write(silenceBytes);
            currentTime += silenceDuration;
        }

        writeStream.end();
        fs.writeFileSync(vttPath, vttContent);

        emitStreamLog(safeId, { status: 'processing', message: 'Compiling high-quality audio...' });

        ffmpeg(pcmPath)
            .inputOptions(['-f s16le', '-ar 24000', '-ac 1'])
            .outputOptions(['-c:a aac', '-b:a 128k'])
            .save(finalAudioPath)
            .on('end', () => {
                if (fs.existsSync(pcmPath)) fs.unlinkSync(pcmPath);
                emitStreamLog(safeId, { status: 'done', file: 'podcast.m4a', message: 'Audio compilation complete!' });
                state.jobs[safeId].status = 'done';
            })
            .on('error', (err) => emitStreamLog(safeId, { status: 'error', message: err.message }));

    } catch (err) {
        emitStreamLog(safeId, { status: 'error', message: err.message });
    }
});
module.exports = router;