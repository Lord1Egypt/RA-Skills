const state = require('../config/state');

function emitStreamLog(id, payload) {
    // Log to the backend Node.js terminal
    const time = new Date().toLocaleTimeString();
    const logMsg = payload.message || payload.error || payload.status || "Processing...";
    console.log(`[${time}] [Session: ${id}] ${logMsg}`);

    // Stream to the frontend UI
    if (state.sseClients[id]) {
        state.sseClients[id].write(`data: ${JSON.stringify(payload)}\n\n`);
    }
}

const delay = (ms) => new Promise(resolve => setTimeout(resolve, ms));

module.exports = { emitStreamLog, delay };