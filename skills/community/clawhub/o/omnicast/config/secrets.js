require('dotenv').config();

module.exports = {
    getElevenLabsKey: () => process.env.ELEVENLABS_API_KEY
};