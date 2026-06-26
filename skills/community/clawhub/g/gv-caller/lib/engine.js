const puppeteer = require('puppeteer-core');
const fs = require('fs');

async function makeCall(targetNumber, audioPath) {
    console.log(`准备呼叫: ${targetNumber}`);
    
    const browser = await puppeteer.launch({
        executablePath: '/usr/bin/chromium',
        args: [
            '--no-sandbox',
            '--disable-setuid-sandbox',
            '--use-fake-ui-for-media-stream',
            '--use-fake-device-for-media-stream',
            `--use-file-for-fake-audio-capture=${audioPath}`, // 核心：将音频文件注入麦克风
            '--allow-file-access'
        ],
        headless: true
    });

    try {
        const page = await browser.newPage();
        const cookies = JSON.parse(fs.readFileSync('/root/.openclaw/workspace/google_voice_cookies.json', 'utf8'));
        await page.setCookie(...cookies);

        await page.goto('https://voice.google.com/u/0/calls', { waitUntil: 'networkidle2' });
        
        // 1. 等待拨号输入框出现 (根据截图中的占位符文字)
        const inputSelector = 'input[placeholder="输入姓名或电话号码"]';
        await page.waitForSelector(inputSelector);
        
        // 2. 输入目标号码
        await page.type(inputSelector, targetNumber);
        await page.keyboard.press('Enter');
        console.log("号码已输入，准备发起呼叫...");

        // 3. 点击绿色的呼叫按钮 (根据 aria-label 或特定的 class)
        // 注意：GV 的按钮结构复杂，这里通过文本或图标尝试定位
        await page.evaluate(() => {
            const buttons = Array.from(document.querySelectorAll('button'));
            const callBtn = buttons.find(b => b.innerText.includes('呼叫') || b.getAttribute('aria-label') === '呼叫');
            if (callBtn) callBtn.click();
        });

        // 4. 保持通话一段时间（比如 60 秒），让“虚拟麦克风”把音频放完
        console.log("正在通话中... 持续 60 秒以播放音频内容");
        await new Promise(r => setTimeout(r, (process.argv[4] || 60) * 1000)); 

        // 5. 通话结束截图留证
        await page.screenshot({ path: '/tmp/call_result.png' });
        console.log("通话结束，截图已保存。");

    } catch (error) {
        console.error("拨号过程出错:", error);
    } finally {
        await browser.close();
    }
}

// 获取命令行参数
const args = process.argv.slice(2);
const number = args[0] || 'YOUR_TEST_NUMBER';
const audio = args[1] || '/tmp/message.wav';

makeCall(number, audio);
