require('dotenv').config();
const express = require('express');
const fs = require('fs');
const path = require('path');
const rateLimit = require('express-rate-limit');

const state = require('./config/state');
const ingestRoutes = require('./routes/ingest');
const draftRoutes = require('./routes/draft');
const synthesizeRoutes = require('./routes/synthesize');
const utilityRoutes = require('./routes/utilities');
const imageRoutes = require('./routes/images');
const linkedinRoutes = require('./routes/linkedin');
const youtubeRoutes = require('./routes/youtube'); 

const app = express();
const port = process.env.PORT || 7860;

app.use(express.static('public'));

// Security: Restrict static file access strictly to the local machine
app.use('/downloads', (req, res, next) => {
    const isLocal = req.ip === '127.0.0.1' || req.ip === '::ffff:127.0.0.1' || req.ip === '::1';
    if (!isLocal) {
        return res.status(403).json({ error: "Security Exception: Remote file access forbidden." });
    }
    next();
}, express.static(state.downloadsDir));

app.use(express.json({ limit: '50mb' }));

app.use('/api', ingestRoutes);
app.use('/api', draftRoutes);
app.use('/api', synthesizeRoutes);
app.use('/api', utilityRoutes);
app.use('/api', imageRoutes);
app.use('/api', linkedinRoutes);
app.use('/api', youtubeRoutes);

app.get('/api/stream-logs', (req, res) => {
    const { id } = req.query;
    res.writeHead(200, { 'Content-Type': 'text/event-stream', 'Cache-Control': 'no-cache', 'Connection': 'keep-alive' });
    state.sseClients[id] = res;
    res.write(`data: ${JSON.stringify({ message: "Connection established." })}\n\n`);
    req.on('close', () => { delete state.sseClients[id]; });
});

// Security: Explicitly bind to localhost to prevent external network access
app.listen(port, '127.0.0.1', () => console.log(`🚀 Studio running securely at http://127.0.0.1:${port}`));