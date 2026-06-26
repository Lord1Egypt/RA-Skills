#!/usr/bin/env node

/**
 * notice-monitor - 通用公告监控引擎 v2
 * 修复：页面加载和层级切换逻辑
 */

const puppeteer = require('puppeteer');
const fs = require('fs');
const path = require('path');
const yaml = require('yaml');
const { program } = require('commander');

program
    .name('notice-monitor')
    .description('通用公告监控工具')
    .version('1.0.0')
    .option('-c, --config <path>', '配置文件路径')
    .option('-t, --task <name>', '执行指定任务')
    .option('--dry-run', '测试运行，不发送通知')
    .parse(process.argv);

const options = program.opts();

function loadConfig(configPath) {
    const fullPath = path.resolve(configPath || '~/.openclaw/workspace/notice-monitor-config.yaml').replace('~', process.env.HOME);
    if (!fs.existsSync(fullPath)) {
        console.error(`❌ 配置文件不存在：${fullPath}`);
        process.exit(1);
    }
    return yaml.parse(fs.readFileSync(fullPath, 'utf-8'));
}

class StateManager {
    constructor(stateDir) {
        this.stateDir = stateDir;
        if (!fs.existsSync(stateDir)) fs.mkdirSync(stateDir, { recursive: true });
    }
    load(taskName) {
        const file = path.join(this.stateDir, `pushed-${taskName.toLowerCase().replace(/[^a-z0-9]/g, '-')}.json`);
        return fs.existsSync(file) ? JSON.parse(fs.readFileSync(file, 'utf-8')) : [];
    }
    save(taskName, ids) {
        const file = path.join(this.stateDir, `pushed-${taskName.toLowerCase().replace(/[^a-z0-9]/g, '-')}.json`);
        fs.writeFileSync(file, JSON.stringify(ids.slice(-1000), null, 2));
    }
}

class Notifier {
    static async send(config, message) {
        if (config.type === 'dingtalk') {
            try {
                const { execSync } = require('child_process');
                execSync(`openclaw message send --target "${config.target}" --message "${message.replace(/"/g, '\\"')}"`, { stdio: 'pipe' });
                console.log('✅ 消息已发送');
            } catch (e) {
                console.error('❌ 发送失败:', e.message);
                console.log(message);
            }
        } else {
            console.log(message);
        }
    }
}

async function main() {
    console.log('🔍 notice-monitor v1.0.0');
    const config = loadConfig(options.config);
    const stateManager = new StateManager(path.join(__dirname, '..', 'state'));
    
    let browser;
    try {
        browser = await puppeteer.launch({
            headless: 'new',
            args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage', '--disable-gpu']
        });
        
        const page = await browser.newPage();
        await page.setViewport({ width: 1920, height: 1080 });
        await page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0 Safari/537.36');

        const tasks = options.task ? config.tasks.filter(t => t.name === options.task) : config.tasks;
        
        for (const task of tasks) {
            console.log(`\n🚀 任务：${task.name}`);
            console.log(`   URL: ${task.url}`);
            
            const pushedIds = stateManager.load(task.name);
            const newNotices = {};
            const levels = task.levels || [{ name: '默认', selector: null }];

            for (const level of levels) {
                console.log(`   📍 ${level.name}...`);
                
                try {
                    // 加载页面
                    await page.goto(task.url, { waitUntil: 'domcontentloaded', timeout: 90000 });
                    // 等待表格数据出现
                    await page.waitForFunction(() => {
                        const rows = document.querySelectorAll('table tbody tr');
                        return rows.length > 0;
                    }, { timeout: 30000 }).catch(() => {});
                    await new Promise(r => setTimeout(r, 2000));

                    // 点击层级（省级通常默认显示，不需要点击）
                    if (level.selector && level.name !== '省级') {
                        const clicked = await page.evaluate((sel) => {
                            const els = Array.from(document.querySelectorAll('span, div, a, button'));
                            const target = els.find(e => {
                                const t = e.textContent?.trim();
                                return t === sel || t.includes(sel);
                            });
                            if (target?.click) { target.click(); return true; }
                            return false;
                        }, level.selector);
                        console.log(`      点击：${clicked ? '✅' : '❌'}`);
                        await new Promise(r => setTimeout(r, 3000));
                    } else if (level.selector) {
                        console.log(`      默认层级，跳过点击`);
                    }

                    // 提取数据
                    const notices = await page.evaluate(() => {
                        const rows = [];
                        document.querySelectorAll('table tbody tr').forEach(row => {
                            const cells = row.querySelectorAll('td');
                            if (cells.length >= 4) {
                                const title = cells[2]?.querySelector('a')?.textContent?.trim() || cells[2]?.textContent?.trim() || '';
                                const area = cells[3]?.textContent?.trim() || '';
                                const date = cells[4]?.textContent?.trim() || '';
                                if (title) rows.push({ title, area, date, id: `${date}_${title.slice(0, 30)}` });
                            }
                        });
                        return rows;
                    });

                    console.log(`      公告：${notices.length} 条`);
                    
                    // 过滤
                    newNotices[level.name] = [];
                    const keywords = task.keywords || [];
                    for (const n of notices) {
                        const matches = keywords.some(k => n.title.includes(k));
                        if (matches && !pushedIds.includes(n.id)) {
                            newNotices[level.name].push(n);
                            pushedIds.push(n.id);
                        }
                    }
                    console.log(`      新增：${newNotices[level.name].length} 条`);

                } catch (e) {
                    console.error(`      失败：${e.message}`);
                }
            }

            stateManager.save(task.name, pushedIds);
            
            const total = Object.values(newNotices).reduce((s, a) => s + a.length, 0);
            
            if (total > 0 && !options.dryRun) {
                await Notifier.send(task.notify, generateReport(task.name, newNotices));
            } else if (options.dryRun) {
                console.log('\n📝 报告:\n' + generateReport(task.name, newNotices));
            } else {
                console.log('   ✅ 无新增');
            }
        }

    } catch (e) {
        console.error('❌ 错误:', e.message);
        process.exit(1);
    } finally {
        if (browser) await browser.close();
    }
}

function generateReport(taskName, notices) {
    const today = new Date().toLocaleDateString('zh-CN');
    let r = `📢 ${taskName} 日报\n📅 ${today}\n\n`;
    for (const [level, items] of Object.entries(notices)) {
        r += `【${level}】${items.length}条\n${'━'.repeat(35)}\n`;
        if (items.length === 0) { r += '\n'; continue; }
        items.forEach((n, i) => {
            r += `${i+1}️⃣ ${n.title}\n   📍 ${n.area} | 🕐 ${n.date}\n\n`;
        });
    }
    const total = Object.values(notices).reduce((s, a) => s + a.length, 0);
    r += `${'━'.repeat(35)}\n✅ 今日新增：${total}条`;
    return r;
}

main();
