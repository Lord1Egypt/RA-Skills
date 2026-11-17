/**
 * 步骤 2／4：按步骤批量截图
 *
 * 核心规则：
 *  1) 每一步单独定高，不要统一视口高度（高度从 01_probe_views.mjs 的 probe.txt 拿）
 *  2) 需要交互态（抽屉、弹窗、切换身份）的，把操作写进该步的 before 数组，截图前会依次执行
 *  3) 超长页只截首屏，别整页截，比例会崩
 *
 * 前置：静态服务已起、Chrome 已用 --remote-debugging-port=9222 启动
 * 用法：node 02_capture.mjs
 * 产出：shots/ 下若干 PNG
 */
import { openSession, sleep } from './cdp.mjs';
import fs from 'node:fs';

// ==================== 配置区（只改这里） ====================
const TOP = `window.scrollTo(0,0)`;
const goView = v => `Array.from(document.querySelectorAll('[data-view]')).find(b=>b.dataset.view==='${v}').click()`;

const CONFIG = {
  url: 'http://127.0.0.1:8766/demo.html',
  outDir: 'shots',
  width: 1440,
  scale: 1,                    // 1 就够；要更清晰可设 1.25，但文件会大 50%
  steps: [
    { file: '01_week.png',    height: 1400, before: [goView('week'), TOP] },
    { file: '02_day.png',     height: 1600, before: [goView('day'), TOP] },
    { file: '03_month.png',   height: 1780, before: [goView('month'), TOP] },
    { file: '04_library.png', height: 1340, before: [goView('library'), TOP] },
    // 交互态：先回到日视图点开任务详情抽屉
    { file: '05_detail.png',  height: 1020, before: [goView('day'), TOP, `document.querySelector('.task-row').click()`], wait: 600 },
    // 弹层：关掉抽屉再点新增
    { file: '06_new.png',     height: 1020, before: [goView('day'), TOP, `document.querySelector('#add-event').click()`], wait: 500 },
    // 切换到另一个身份 + 全部人员范围
    { file: '07_head.png',    height: 1400, before: [
        `(function(){const el=document.querySelector('#identity');el.value='boss';el.dispatchEvent(new Event('change',{bubbles:true}))})()`,
        `(function(){const el=document.querySelector('#scope');el.value='all';el.dispatchEvent(new Event('change',{bubbles:true}))})()`,
        goView('week'), TOP ] },
    // 检索态
    { file: '08_search.png',  height: 950,  before: [
        goView('library'), TOP,
        `(function(){const el=document.querySelector('#lib-search');el.value='广告';el.dispatchEvent(new Event('input',{bubbles:true}))})()` ], wait: 600 },
  ],
};
// ==========================================================

fs.mkdirSync(CONFIG.outDir, { recursive: true });
const s = await openSession();
const log = [];

async function size(h) {
  await s.send('Emulation.setDeviceMetricsOverride',
    { width: CONFIG.width, height: h, deviceScaleFactor: CONFIG.scale, mobile: false });
  await sleep(280);
}

await size(1000);
await s.go(CONFIG.url);
await sleep(800);

for (const step of CONFIG.steps) {
  for (const js of (step.before || [])) { await s.evalJs(js); await sleep(200); }
  await size(step.height);
  await sleep(step.wait || 300);
  await s.shot(`${CONFIG.outDir}/${step.file}`);
  // 自检：截到空白图多半是选择器没命中，这里报一下页面主体长度
  const len = await s.evalJs(`(document.querySelector('main,#main-view,.shell')||document.body).innerHTML.length`);
  log.push(`${step.file.padEnd(18)} h=${String(step.height).padEnd(6)} mainLen=${len}`);
}

fs.writeFileSync('capture.log', log.join('\n'), 'utf8');
s.close();
console.log(log.join('\n'));
