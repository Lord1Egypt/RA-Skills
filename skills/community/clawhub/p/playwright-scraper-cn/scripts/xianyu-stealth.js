#!/usr/bin/env node
/**
 * 闲鱼增强版爬虫 - 更多反反爬措施
 */

const { chromium } = require('playwright');

const url = process.argv[2] || 'https://www.goofish.com';

(async () => {
    console.log('🔥 闲鱼增强版爬虫启动...');
    
    const browser = await chromium.launch({
        headless: true,  // 无头模式（服务器没有X server）
        args: [
            '--no-sandbox',
            '--disable-setuid-sandbox',
            '--disable-blink-features=AutomationControlled',
            '--disable-web-security',
            '--disable-features=IsolateOrigins,site-per-process',
            '--disable-infobars',
            '--disable-dev-shm-usage',
            '--disable-accelerated-2d-canvas',
            '--no-first-run',
            '--no-zygote',
            '--disable-gpu',
        ],
    });
    
    const context = await browser.newContext({
        userAgent: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        viewport: { width: 1920, height: 1080 },
        locale: 'zh-CN',
        timezoneId: 'Asia/Shanghai',
        extraHTTPHeaders: {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Cache-Control': 'max-age=0',
        },
    });
    
    // 完整的反检测脚本
    await context.addInitScript(() => {
        // 隐藏webdriver
        Object.defineProperty(navigator, 'webdriver', { get: () => false });
        
        // 伪造chrome对象
        window.chrome = { 
            runtime: {},
            loadTimes: function() {},
            csi: function() {},
            app: {}
        };
        
        // 伪造permissions
        const originalQuery = window.navigator.permissions.query;
        window.navigator.permissions.query = (parameters) => (
            parameters.name === 'notifications' ?
                Promise.resolve({ state: Notification.permission }) :
                originalQuery(parameters)
        );
        
        // 伪造plugins
        Object.defineProperty(navigator, 'plugins', {
            get: () => [1, 2, 3, 4, 5]
        });
        
        // 伪造languages
        Object.defineProperty(navigator, 'languages', {
            get: () => ['zh-CN', 'zh', 'en']
        });
        
        // 伪造platform
        Object.defineProperty(navigator, 'platform', {
            get: () => 'MacIntel'
        });
        
        // 伪造hardwareConcurrency
        Object.defineProperty(navigator, 'hardwareConcurrency', {
            get: () => 8
        });
        
        // 伪造deviceMemory
        Object.defineProperty(navigator, 'deviceMemory', {
            get: () => 8
        });
        
        // 隐藏自动化痕迹
        const originalToString = Function.prototype.toString;
        Function.prototype.toString = function() {
            if (this === navigator.permissions.query) {
                return 'function query() { [native code] }';
            }
            return originalToString.call(this);
        };
    });
    
    const page = await context.newPage();
    
    // 模拟人类鼠标移动
    await page.mouse.move(100, 200);
    await page.waitForTimeout(500);
    await page.mouse.move(200, 300);
    await page.waitForTimeout(300);
    
    console.log(`📱 正在访问: ${url}`);
    
    try {
        const response = await page.goto(url, {
            waitUntil: 'networkidle',
            timeout: 60000,
        });
        
        console.log(`📡 HTTP Status: ${response.status()}`);
        
        // 等待页面加载
        await page.waitForTimeout(5000);
        
        // 检查是否需要登录
        const currentUrl = page.url();
        console.log(`🔗 当前URL: ${currentUrl}`);
        
        // 截图
        await page.screenshot({ path: '/tmp/xianyu_result.png', fullPage: true });
        console.log('📸 截图已保存: /tmp/xianyu_result.png');
        
        // 获取页面内容
        const content = await page.evaluate(() => {
            return {
                title: document.title,
                url: window.location.href,
                bodyText: document.body.innerText.substring(0, 3000),
                hasLoginForm: document.querySelector('input[type="text"]') !== null,
                itemCount: document.querySelectorAll('[class*="item"]').length,
            };
        });
        
        console.log('\n📊 页面信息:');
        console.log(JSON.stringify(content, null, 2));
        
        // 如果需要登录，等待用户手动登录
        if (content.url.includes('login') || content.hasLoginForm) {
            console.log('\n⚠️  需要登录！');
            console.log('请在浏览器窗口中手动登录，登录后按回车继续...');
            
            // 等待用户输入（在终端）
            await new Promise(resolve => {
                process.stdin.once('data', resolve);
            });
            
            // 登录后再次获取内容
            await page.waitForTimeout(3000);
            const afterLogin = await page.evaluate(() => {
                return {
                    title: document.title,
                    url: window.location.href,
                    bodyText: document.body.innerText.substring(0, 3000),
                };
            });
            console.log('\n✅ 登录后内容:');
            console.log(JSON.stringify(afterLogin, null, 2));
        }
        
    } catch (error) {
        console.error(`❌ 错误: ${error.message}`);
    }
    
    await browser.close();
})();
