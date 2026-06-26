const express = require('express');
const fs = require('fs');
const path = require('path');
const { getGeminiClient } = require('../utils/geminiClient');
const state = require('../config/state');
const { emitStreamLog } = require('../utils/streamer');

const router = express.Router();

router.post('/draft-image-prompt', async (req, res) => {
    const { id } = req.body;
    const safeId = state.sanitizeId(id);
    const sessionDir = path.join(state.downloadsDir, safeId);

    const scriptFile = path.join(sessionDir, 'script.txt');
    if (!fs.existsSync(scriptFile)) {
        return res.status(404).json({ error: "Script not found. Please draft the script first." });
    }

    try {
        // The SDK automatically pulls from process.env.GEMINI_API_KEY
        const ai = getGeminiClient();
        const scriptText = fs.readFileSync(scriptFile, 'utf8');

        emitStreamLog(safeId, { message: "Analyzing podcast script for visual concepts..." });
        
        const systemPrompt = `Write a highly descriptive, 1-sentence prompt for an AI image generator to create sleek modern podcast cover art based on this script excerpt. Do NOT include any text or words in the image design.`;

        const promptDesign = await ai.models.generateContent({
            model: 'gemini-2.5-flash',
            contents: `Script Excerpt:\n${scriptText.substring(0, 3000)}`,
            config: { systemInstruction: systemPrompt }
        });

        res.json({ success: true, prompt: promptDesign.text.trim() });
    } catch (error) {
        emitStreamLog(safeId, { status: 'error', message: error.message });
        res.status(500).json({ error: error.message });
    }
});

router.post('/generate-thumbnail', async (req, res) => {
    const { id, prompt } = req.body;
    const safeId = state.sanitizeId(id);
    const sessionDir = path.join(state.downloadsDir, safeId);

    if (!prompt) return res.status(400).json({ error: "Image prompt is required." });
    if (!fs.existsSync(sessionDir)) fs.mkdirSync(sessionDir, { recursive: true });

    try {
        // The SDK automatically pulls from process.env.GEMINI_API_KEY
        const ai = getGeminiClient();

        emitStreamLog(safeId, { message: "Rendering 16:9 image via Gemini 3.1 Flash Image Preview..." });
        
        const imageResponse = await ai.models.generateContent({
            model: 'gemini-3.1-flash-image-preview', 
            contents: prompt,
            config: { 
                responseModalities: ["IMAGE"],
                imageConfig: { aspectRatio: "16:9" }
            }
        });

        const base64Data = imageResponse.candidates[0].content.parts[0].inlineData.data;
        const imagePath = path.join(sessionDir, 'thumbnail.png');
        
        fs.writeFileSync(imagePath, Buffer.from(base64Data, 'base64'));

        emitStreamLog(safeId, { message: "Cover art successfully rendered and saved!" });
        res.json({ success: true, file: 'thumbnail.png' });
    } catch (error) {
        emitStreamLog(safeId, { status: 'error', message: error.message });
        res.status(500).json({ error: error.message });
    }
});

module.exports = router;