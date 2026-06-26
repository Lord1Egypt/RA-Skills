const { chromium } = require('playwright');

(async () => {
    console.log('🚀 自动化填写工时...');
    
    const browser = await chromium.launch({
        channel: 'chrome',
        headless: false,
        args: ['--disable-gpu', '--no-sandbox', '--disable-dev-shm-usage']
    });
    
    const context = await browser.newContext({ viewport: { width: 1920, height: 1080 } });
    const page = await context.newPage();
    
    try {
        // ===== 配置区域 =====
        // 请修改为你的真实账号密码，或使用环境变量
        const username = process.env.PMS_USERNAME || 'your_username@company.com';
        const password = process.env.PMS_PASSWORD || 'your_password';
        
        // 填写日期（格式：YYYY-MM-DD）
        const dates = ['2026-03-13'];  // 今天
        
        // 工时信息
        const workItem = 'IOT0225121104-1980';  // 事项编号
        const hours = '8';                       // 每天工时
        const description = '养虾';              // 工作说明
        
        // PMS 系统地址
        const pmsUrl = 'https://pms.aispeech.com.cn/workspace/workload/insight';
        
        // 截图保存目录
        const screenshotDir = '/Users/aispeech/.openclaw/workspace';
        // ===================
        
        // 登录
        console.log('🔐 登录...');
        await page.goto('https://pms.aispeech.com.cn', { waitUntil: 'networkidle', timeout: 60000 });
        await page.waitForTimeout(3000);
        
        await page.locator('input[name="account"]').first().fill(username);
        await page.locator('input[type="password"]').first().fill(password);
        await page.locator('button:has-text("登录")').first().click();
        
        // 等待登录完成 - 检查是否还在登录页
        console.log('  等待登录完成...');
        await page.waitForTimeout(15000);
        
        // 检查是否登录成功（看是否还有登录按钮）
        const loginBtn = page.locator('button:has-text("登录")');
        const isLoggedIn = !(await loginBtn.first().isVisible());
        
        if (!isLoggedIn) {
            console.log('  ⚠️  登录可能失败，仍尝试继续...');
            await page.screenshot({ path: `${screenshotDir}/pms_login_failed.png` });
        } else {
            console.log('  ✅ 登录成功');
        }
        
        // 导航到工时页面
        console.log('📍 导航到工时页面...');
        await page.goto(pmsUrl, { waitUntil: 'networkidle', timeout: 120000 });
        await page.waitForTimeout(15000);
        
        // 截图查看
        await page.screenshot({ path: `${screenshotDir}/pms_page.png` });
        console.log('📸 已保存页面截图');
        
        // 检查页面内容
        const pageTitle = await page.title();
        console.log(`  页面标题：${pageTitle}`);
        
        const url = page.url();
        console.log(`  当前 URL: ${url}`);
        
        // 截图查看当前页面
        await page.screenshot({ path: `${screenshotDir}/pms_page.png` });
        console.log('📸 已保存页面截图');
        
        // 列出所有按钮文本
        console.log('🔍 查找页面上的按钮...');
        const buttons = page.locator('button');
        const btnCount = await buttons.count();
        console.log(`  找到${btnCount}个按钮`);
        for (let j = 0; j < btnCount && j < 20; j++) {
            try {
                const text = await buttons.nth(j).textContent();
                if (text && text.trim()) {
                    console.log(`    [${j}] ${text.trim()}`);
                }
            } catch (e) {}
        }
        
        for (let i = 0; i < dates.length; i++) {
            const date = dates[i];
            console.log(`\n═══════════════════════════════════`);
            console.log(`📅 第${i+1}天：${date}`);
            console.log(`═══════════════════════════════════`);
            
            // 关闭弹窗
            await page.keyboard.press('Escape');
            await page.keyboard.press('Escape');
            await page.waitForTimeout(1000);
            
            // 点击登记工时 - 尝试多种选择器
            console.log('🔘 点击"登记工时"...');
            await page.waitForTimeout(2000);
            
            let clicked = false;
            const selectors = [
                'button:has-text("登记工时")',
                'button:has-text("登记")',
                'button:has-text("添加工时")',
                'button:has-text("添加")',
                '[class*="register"]',
                '[class*="add"]'
            ];
            
            for (const selector of selectors) {
                try {
                    const btn = page.locator(selector).first();
                    if (await btn.isVisible()) {
                        const text = await btn.textContent();
                        console.log(`  尝试选择器：${selector} (文本：${text?.trim()})`);
                        await btn.click({ force: true });
                        clicked = true;
                        console.log('  ✅ 点击成功');
                        break;
                    }
                } catch (e) {}
            }
            
            if (!clicked) {
                // 尝试点击第一个可见按钮
                try {
                    for (let j = 0; j < btnCount && !clicked; j++) {
                        const btn = buttons.nth(j);
                        if (await btn.isVisible()) {
                            const text = await btn.textContent();
                            if (text && (text.includes('登记') || text.includes('添加') || text.includes('工时'))) {
                                console.log(`  点击按钮 [${j}]: ${text.trim()}`);
                                await btn.click({ force: true });
                                clicked = true;
                            }
                        }
                    }
                } catch (e) {}
            }
            
            if (!clicked) {
                console.log('  ⚠️  未找到合适按钮，保存截图...');
                await page.screenshot({ path: `${screenshotDir}/pms_no_button.png` });
                throw new Error('未找到"登记工时"按钮，请查看截图');
            }
            
            await page.waitForTimeout(3000);
            
            // 等待表单加载
            await page.waitForSelector('[role="dialog"]', { timeout: 10000 });
            await page.waitForTimeout(2000);
            
            // ===== 1. 事项类型：选择"工作项" =====
            console.log('📋 1. 选择事项类型：工作项');
            
            await page.locator('text=产品需求').or(page.locator('text=工作项')).first().click({ force: true });
            await page.waitForTimeout(1500);
            
            await page.locator('text=工作项').first().click({ force: true });
            console.log('  ✅ 已选择"工作项"');
            await page.waitForTimeout(2000);
            
            // ===== 2. 事项：填写并选择 =====
            console.log(`📝 2. 填写事项：${workItem}`);
            
            await page.evaluate((item) => {
                const modal = document.querySelector('[role="dialog"]');
                if (!modal) return;
                
                const labels = Array.from(modal.querySelectorAll('label, .form-label'));
                for (const label of labels) {
                    if (label.textContent?.trim() === '事项' || label.textContent?.trim() === '事项 *') {
                        const container = label.parentElement;
                        if (container) {
                            const itemInput = container.querySelector('input[type="text"], input:not([type])');
                            if (itemInput) {
                                itemInput.value = item;
                                itemInput.dispatchEvent(new Event('input', { bubbles: true }));
                                itemInput.dispatchEvent(new Event('change', { bubbles: true }));
                                itemInput.focus();
                                break;
                            }
                        }
                    }
                }
            }, workItem);
            
            console.log('  ✅ 已填写事项编号');
            
            // 点击输入框激活下拉列表
            console.log('  点击输入框激活下拉列表...');
            await page.evaluate(() => {
                const modal = document.querySelector('[role="dialog"]');
                const labels = Array.from(modal.querySelectorAll('label, .form-label'));
                for (const label of labels) {
                    if (label.textContent?.trim() === '事项' || label.textContent?.trim() === '事项 *') {
                        const container = label.parentElement;
                        if (container) {
                            const itemInput = container.querySelector('input[type="text"], input:not([type])');
                            if (itemInput) {
                                itemInput.click();
                                break;
                            }
                        }
                    }
                }
            });
            
            // 等待下拉列表出现
            console.log('  ⏳ 等待下拉列表出现...');
            await page.waitForTimeout(3000);
            
            // 查找并点击下拉选项
            console.log('  查找下拉选项...');
            
            try {
                await page.waitForSelector(`text=${workItem}`, { timeout: 5000 });
                console.log('  ✅ 找到包含编号的选项');
                await page.locator(`text=${workItem}`).first().click({ force: true });
                console.log('  ✅ 已点击选项');
            } catch (e) {
                console.log('  ℹ️  未找到精确匹配，尝试其他方式...');
                
                const selectors = [
                    '.ant-select-item',
                    '.thy-select-option',
                    '.select-item',
                    '[class*="select"] [class*="item"]',
                    '.cdk-overlay-container span'
                ];
                
                let clicked = false;
                for (const selector of selectors) {
                    const options = page.locator(selector);
                    const count = await options.count();
                    if (count > 0) {
                        console.log(`  找到${count}个选项 (${selector})`);
                        await options.nth(0).click({ force: true });
                        clicked = true;
                        break;
                    }
                }
                
                if (!clicked) {
                    console.log('  ⚠️  未找到可点击的选项');
                }
            }
            
            await page.waitForTimeout(2000);
            
            // ===== 3. 工时 =====
            console.log(`⏱️  3. 填写工时：${hours}`);
            const hoursInput = page.locator('input[placeholder*="添加工时"], input[placeholder*="工时"]').first();
            await hoursInput.click({ force: true });
            await hoursInput.fill(hours);
            console.log('  ✅ 已填写工时');
            await page.waitForTimeout(500);
            
            // ===== 4. 日期 =====
            console.log(`📅 4. 填写日期：${date}`);
            const dateInput = page.locator('input[placeholder*="工作日期"], input[placeholder*="日期"]').first();
            await dateInput.click({ force: true });
            await dateInput.fill(date);
            console.log('  ✅ 已填写日期');
            await page.waitForTimeout(500);
            await page.keyboard.press('Escape');
            
            // ===== 5. 说明 =====
            console.log(`📝 5. 填写说明：${description}`);
            const editor = page.locator('[contenteditable="true"], .slate-editable-container').last();
            await editor.click({ force: true });
            await page.keyboard.type(description);
            console.log('  ✅ 已填写说明');
            await page.waitForTimeout(500);
            
            // 截图
            await page.screenshot({ path: `${screenshotDir}/day${i+1}_filled.png` });
            console.log('📸 已保存截图');
            
            // ===== 6. 点击确定提交 =====
            console.log('💾 6. 点击"确定"提交...');
            const submitBtn = page.locator('button:has-text("确定")').last();
            await submitBtn.click({ force: true });
            console.log('  ✅ 已提交');
            
            // 等待提交完成
            await page.waitForTimeout(5000);
            
            // 检查是否成功
            const isModalVisible = await page.locator('[role="dialog"]').first().isVisible();
            if (isModalVisible) {
                console.log('⚠️  表单仍然打开');
                await page.screenshot({ path: `${screenshotDir}/day${i+1}_error.png` });
            } else {
                console.log('✅ 提交成功！');
            }
            
            await page.screenshot({ path: `${screenshotDir}/day${i+1}_done.png` });
        }
        
        console.log('\n🎉 所有工时填写完成！');
        console.log(`📸 截图已保存到：${screenshotDir}/`);
        
        // 保持打开
        await page.waitForTimeout(120000);
        
    } catch (error) {
        console.error('❌ 错误:', error.message);
        await page.screenshot({ path: '/Users/aispeech/.openclaw/workspace/error.png' });
    } finally {
        await browser.close();
    }
})();
