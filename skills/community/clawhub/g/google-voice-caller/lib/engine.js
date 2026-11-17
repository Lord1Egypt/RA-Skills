const puppeteer = require('puppeteer-core');
const fs = require('fs');
const path = require('path');

async function makeCall(targetNumber, audioPath, duration) {
    const skillDir = path.join(__dirname, '..');
    const cookiePath = process.env.GV_COOKIE_PATH || path.join(skillDir, 'google_voice_cookies.json');
    const recordingPath = '/tmp/gv_recorded_incoming.webm';

    console.log(`[GoogleVoice] 拨打任务开始: ${targetNumber}`);
    
    const browser = await puppeteer.launch({
        executablePath: '/usr/bin/chromium',
        args: [
            '--no-sandbox', '--disable-setuid-sandbox',
            '--use-fake-ui-for-media-stream', '--use-fake-device-for-media-stream',
            `--use-file-for-fake-audio-capture=${audioPath}`,
            '--allow-file-access'
        ],
        headless: true
    });

    try {
        const page = await browser.newPage();
        await page.setViewport({ width: 1280, height: 800 });
        const cookies = JSON.parse(fs.readFileSync(cookiePath, 'utf8'));
        await page.setCookie(...cookies);

        await page.goto('https://voice.google.com/u/0/calls', { waitUntil: 'networkidle2', timeout: 60000 });
        await new Promise(r => setTimeout(r, 5000));

        // 1. 拨号
        const inputSelector = 'input[placeholder*="号码"]';
        await page.waitForSelector(inputSelector);
        await page.type(inputSelector, targetNumber);
        await page.keyboard.press('Enter');
        await new Promise(r => setTimeout(r, 2000));

        // 2. 呼叫
        await page.evaluate(() => {
            const btns = Array.from(document.querySelectorAll('button'));
            const callBtn = btns.find(b => (b.getAttribute('aria-label') || '').includes('呼叫'));
            if (callBtn) callBtn.click();
        });

        console.log("✅ 通话已发起，正在激活录音系统...");

        // 3. 录音：通过 MediaRecorder 捕获标签页音频流
        await page.evaluate(async () => {
            window.chunks = [];
            try {
                // 捕获浏览器生成的音频流
                const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
                const recorder = new MediaRecorder(stream);
                recorder.ondataavailable = (e) => { if (e.data.size > 0) window.chunks.push(e.data); };
                recorder.start();
                window.myRecorder = recorder;
            } catch (err) { console.error("Recorder init failed: " + err.message); }
        });

        // 通话保持
        const timeLimit = parseInt(duration) || 60;
        await new Promise(r => setTimeout(r, timeLimit * 1000));

        // 4. 提取录音
        const base64Audio = await page.evaluate(async () => {
            if (!window.myRecorder) return null;
            window.myRecorder.stop();
            await new Promise(r => setTimeout(r, 1500));
            const blob = new Blob(window.chunks, { type: 'audio/webm' });
            return new Promise(resolve => {
                const reader = new FileReader();
                reader.onloadend = () => resolve(reader.result.split(',')[1]);
                reader.readAsDataURL(blob);
            });
        });

        if (base64Audio) {
            fs.writeFileSync(recordingPath, Buffer.from(base64Audio, 'base64'));
            console.log(`💾 录音已保存至 ${recordingPath}`);
        }

    } catch (error) {
        console.error("拨号过程出错:", error.message);
    } finally {
        await browser.close();
    }
}

const args = process.argv.slice(2);
makeCall(args[0], args[1], args[2]);
