const { chromium } = require('playwright');

const phone = '15982192571';

(async () => {
    console.log('🔥 闲鱼登录流程启动...');
    
    const browser = await chromium.launch({ 
        headless: true,
        args: ['--no-sandbox', '--disable-setuid-sandbox']
    });
    
    const context = await browser.newContext({
        userAgent: 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1',
        viewport: { width: 375, height: 812 },
        locale: 'zh-CN',
    });
    
    // 反检测
    await context.addInitScript(() => {
        Object.defineProperty(navigator, 'webdriver', { get: () => false });
        window.chrome = { runtime: {} };
    });
    
    const page = await context.newPage();
    
    // 1. 访问登录页
    console.log('📱 正在访问闲鱼登录页...');
    await page.goto('https://www.goofish.com', { waitUntil: 'networkidle', timeout: 30000 });
    await page.waitForTimeout(2000);
    
    // 截图看当前状态
    await page.screenshot({ path: '/tmp/xianyu_step1.png' });
    console.log('📸 步骤1截图: /tmp/xianyu_step1.png');
    
    // 2. 点击登录按钮
    console.log('🔍 查找登录按钮...');
    const loginBtn = await page.$('text=登录');
    if (loginBtn) {
        await loginBtn.click();
        await page.waitForTimeout(2000);
        await page.screenshot({ path: '/tmp/xianyu_step2.png' });
        console.log('📸 步骤2截图: /tmp/xianyu_step2.png');
    }
    
    // 3. 查找手机号输入框
    console.log('🔍 查找手机号输入框...');
    const phoneInput = await page.$('input[type="tel"], input[placeholder*="手机"], input[placeholder*="号码"]');
    
    if (phoneInput) {
        await phoneInput.fill(phone);
        console.log('✅ 已输入手机号:', phone);
        await page.waitForTimeout(1000);
        await page.screenshot({ path: '/tmp/xianyu_step3.png' });
        console.log('📸 步骤3截图: /tmp/xianyu_step3.png');
        
        // 4. 点击获取验证码
        console.log('🔍 查找验证码按钮...');
        const codeBtn = await page.$('text=获取验证码, text=发送验证码');
        if (codeBtn) {
            await codeBtn.click();
            console.log('✅ 已点击获取验证码');
            await page.waitForTimeout(2000);
            await page.screenshot({ path: '/tmp/xianyu_step4.png' });
            console.log('📸 步骤4截图: /tmp/xianyu_step4.png');
        }
    }
    
    // 等待用户输入验证码
    console.log('\n⏳ 请等待验证码短信，然后告诉我验证码...');
    
    // 保存当前页面状态
    const currentUrl = page.url();
    const content = await page.evaluate(() => document.body.innerText.substring(0, 1000));
    
    console.log('\n当前页面URL:', currentUrl);
    console.log('页面内容预览:', content);
    
    // 保持浏览器打开，等待后续操作
    // 由于是自动化脚本，这里需要等待用户输入
    
    await browser.close();
})();
