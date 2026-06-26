const ffmpeg = require('fluent-ffmpeg');

console.log("🔍 Checking the bridge between Node.js and FFmpeg...");

// Ask FFmpeg for its list of available codecs
ffmpeg.getAvailableCodecs((err, codecs) => {
    if (err) {
        console.error("\n❌ FAILED: Node.js cannot communicate with FFmpeg.");
        console.error("Error details:", err.message);
        console.error("\nTroubleshooting:");
        console.error("1. Did you install the actual FFmpeg software on your OS? (Run: brew install ffmpeg)");
        console.error("2. If on Windows, did you add the FFmpeg /bin folder to your System PATH variables?");
        console.error("3. Try restarting your terminal to refresh the PATH.");
    } else {
        console.log("\n✅ SUCCESS: FFmpeg is installed and communicating with Node.js!");
        
        // Check for specific codecs we rely on
        const hasMp3 = codecs['libmp3lame'] !== undefined;
        const hasAac = codecs['aac'] !== undefined;
        
        console.log(`📦 Found ${Object.keys(codecs).length} available audio/video codecs.`);
        console.log(`🎵 MP3 Encoding Support (Whisper prep): ${hasMp3 ? '✅ Yes' : '❌ No (Missing libmp3lame)'}`);
        console.log(`🎵 AAC Encoding Support (Final podcast): ${hasAac ? '✅ Yes' : '❌ No (Missing aac)'}`);
        
        if (hasMp3 && hasAac) {
            console.log("\n🚀 All systems go! You are ready to run: npm start");
        } else {
            console.warn("\n⚠️ FFmpeg is responding, but you are missing essential audio encoders. Reinstall a full build of FFmpeg.");
        }
    }
});
