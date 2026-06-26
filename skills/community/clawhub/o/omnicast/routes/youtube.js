const express = require('express');
const fs = require('fs');
const path = require('path');
const { google } = require('googleapis');
const state = require('../config/state');
const { emitStreamLog } = require('../utils/streamer');

const router = express.Router();

router.post('/upload-youtube', async (req, res) => {
    const { id, title, description, accessToken } = req.body;
    const safeId = state.sanitizeId(id);
    const sessionDir = path.join(state.downloadsDir, safeId);
    
    const videoPath = path.join(sessionDir, 'linkedin_podcast.mp4');

    if (!accessToken) return res.status(401).json({ error: "YouTube Access Token is required." });
    if (!fs.existsSync(videoPath)) return res.status(404).json({ error: "Video not found. Please generate the video package first." });

    try {
        emitStreamLog(safeId, { message: "Authenticating with YouTube API..." });

        const oauth2Client = new google.auth.OAuth2();
        oauth2Client.setCredentials({ access_token: accessToken });

        const youtube = google.youtube({ version: 'v3', auth: oauth2Client });
        const fileSize = fs.statSync(videoPath).size;

        emitStreamLog(safeId, { message: `Uploading video to YouTube (${(fileSize / (1024 * 1024)).toFixed(2)} MB). This may take a moment...` });

        const uploadRes = await youtube.videos.insert({
            part: 'snippet,status',
            notifySubscribers: false, 
            requestBody: {
                snippet: {
                    title: title,
                    description: description,
                    categoryId: '24' 
                },
                status: {
                    privacyStatus: 'private', 
                    selfDeclaredMadeForKids: false
                }
            },
            media: {
                body: fs.createReadStream(videoPath)
            }
        });

        emitStreamLog(safeId, { status: 'done', message: "YouTube upload complete!" });
        res.json({ success: true, videoId: uploadRes.data.id });

    } catch (error) {
        const errorMessage = error.response?.data?.error?.message || error.message;
        emitStreamLog(safeId, { status: 'error', message: "YouTube upload failed: " + errorMessage });
        res.status(500).json({ error: errorMessage });
    }
});

module.exports = router;