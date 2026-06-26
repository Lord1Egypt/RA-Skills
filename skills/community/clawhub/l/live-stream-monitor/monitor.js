#!/usr/bin/env node

/**
 * Live Stream Monitor with Real-time Speech Recognition
 * Uses Web Speech API to transcribe what the streamer says
 * 
 * IMPORTANT: Run with --headed mode for speech recognition to work!
 */

const { chromium } = require('playwright');

// Platform configurations
const PLATFORMS = {
  bilibili: {
    name: 'Bilibili',
    baseUrl: 'https://live.bilibili.com',
    getUrl: (roomId) => `https://live.bilibili.com/${roomId}`,
    checkLive: async (page) => {
      const content = await page.content();
      return !content.includes('未开播') && !content.includes('直播间不存在');
    }
  },
  youtube: {
    name: 'YouTube',
    baseUrl: 'https://www.youtube.com',
    getUrl: (videoId) => `https://www.youtube.com/watch?v=${videoId}`,
    checkLive: async (page) => {
      const content = await page.content();
      return content.includes('直播') || content.includes('LIVE') || content.includes('正在观看');
    }
  }
};

// CLI mode
if (require.main === module) {
  const args = process.argv.slice(2);
  
  if (args[0] === '--monitor' && args[1] && args[2]) {
    const platform = args[1];
    const id = args[2];
    const name = args[3] || 'Streamer';
    const duration = parseInt(args[4]) || 10; // Default 10 seconds
    
    const config = PLATFORMS[platform];
    if (!config) {
      console.log('❌ Unknown platform:', platform);
      console.log('Supported: bilibili, youtube');
      process.exit(1);
    }
    
    (async () => {
      console.log('\n🚀 Starting Live Stream Monitor with Speech Recognition...\n');
      
      // IMPORTANT: Use headed mode for speech recognition!
      const browser = await chromium.launch({ 
        headless: false,  // Must be false for speech recognition!
        args: ['--use-fake-ui-for-media-stream'] 
      });
      
      const page = await browser.newPage();
      const url = config.getUrl(id);
      
      console.log(`📺 Opening: ${name} (${platform})`);
      console.log(`🔗 URL: ${url}\n`);
      
      await page.goto(url, { waitUntil: 'networkidle', timeout: 30000 });
      await page.waitForTimeout(5000);
      
      const isLive = await config.checkLive(page);
      console.log(`📡 Status: ${isLive ? '🔴 LIVE' : '🟢 Offline'}\n`);
      
      if (!isLive) {
        await browser.close();
        process.exit(0);
      }
      
      console.log('🎤 Starting speech recognition...');
      console.log('⏳ Listening for', duration, 'seconds...\n');
      
      // Inject speech recognition
      await page.evaluate((listenTime) => {
        return new Promise((resolve) => {
          if (!('webkitSpeechRecognition' in window || 'SpeechRecognition' in window)) {
            console.log('❌ Speech Recognition not supported in this browser');
            resolve();
            return;
          }
          
          const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
          const recognition = new SpeechRecognition();
          
          recognition.continuous = true;
          recognition.interimResults = true;
          recognition.lang = 'en-US';
          
          let transcriptCount = 0;
          
          recognition.onresult = (event) => {
            for (let i = event.resultIndex; i < event.results.length; i++) {
              if (event.results[i].isFinal) {
                const text = event.results[i][0].transcript.trim();
                if (text) {
                  console.log(`🗣️ [${++transcriptCount}] ${text}`);
                }
              }
            }
          };
          
          recognition.onerror = (event) => {
            console.log('❌ Speech Error:', event.error);
          };
          
          recognition.onend = () => {
            console.log('\n🛑 Speech recognition ended');
            resolve();
          };
          
          recognition.start();
          console.log('✅ Speech recognition started! Allow microphone access if prompted.\n');
          
          // Stop after duration
          setTimeout(() => {
            recognition.stop();
          }, listenTime * 1000);
        });
      }, duration);
      
      console.log('\n👋 Done! Closing browser...');
      await browser.close();
    })();
  } else {
    console.log(`
🎯 Live Stream Monitor with Speech Recognition

📖 Usage:
  node monitor.js --monitor <platform> <id> [name] [duration]

📌 Examples:
  node monitor.js --monitor youtube gCNeDWCI0vo "Al Jazeera" 60
  node monitor.js --monitor bilibili 1985112908 "CS2夏天" 30

⚠️  IMPORTANT:
  - Must run in headed mode (not headless) for speech recognition
  - Browser will open and you may need to allow microphone access
  - Speech recognition requires speakers to be ON to hear the stream

🌐 Supported Platforms:
  - youtube
  - bilibili
`);
  }
}

module.exports = { PLATFORMS };
