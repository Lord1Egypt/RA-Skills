/**
 * 步骤 1／4：探测单文件 HTML 原型各视图的真实像素高度
 *
 * 为什么必须先探测：不同视图内容量差很多，统一视口高度会把内容截断。
 * 实测同一原型四个视图分别是 1372 / 1549 / 1733 / 7221 px。
 *
 * 前置：静态服务已起、Chrome 已用 --remote-debugging-port=9222 启动（见手册第 3 节）
 * 用法：node 01_probe_views.mjs
 * 产出：probe.txt，把里面的 h 值填进 02_capture.mjs 的 height
 */
import { openSession, sleep } from './cdp.mjs';
import fs from 'node:fs';

// ==================== 配置区（只改这里） ====================
const CONFIG = {
  url: 'http://127.0.0.1:8766/demo.html',
  width: 1440,
  // 每个视图对应一段点击它的 JS，原型的导航按钮选择器按实际情况改
  views: [
    { name: 'week',    click: `Array.from(document.querySelectorAll('[data-view]')).find(b=>b.dataset.view==='week').click()` },
    { name: 'day',     click: `Array.from(document.querySelectorAll('[data-view]')).find(b=>b.dataset.view==='day').click()` },
    { name: 'month',   click: `Array.from(document.querySelectorAll('[data-view]')).find(b=>b.dataset.view==='month').click()` },
    { name: 'library', click: `Array.from(document.querySelectorAll('[data-view]')).find(b=>b.dataset.view==='library').click()` },
  ],
};
// ==========================================================

const s = await openSession();
await s.send('Emulation.setDeviceMetricsOverride',
  { width: CONFIG.width, height: 1000, deviceScaleFactor: 1, mobile: false });
await s.go(CONFIG.url);
await sleep(700);

const log = [`url = ${CONFIG.url}`, `viewport width = ${CONFIG.width}`, ''];
for (const v of CONFIG.views) {
  await s.evalJs(v.click);
  await sleep(350);
  const h = await s.evalJs('document.documentElement.scrollHeight');
  const w = await s.evalJs('document.documentElement.scrollWidth');
  const over = w > CONFIG.width ? '  ⚠ 横向溢出 ' + (w - CONFIG.width) + 'px' : '';
  log.push(`${v.name.padEnd(12)} h=${String(h).padEnd(6)} w=${w}${over}`);
}
log.push('');
log.push('把上面的 h 直接填进 02_capture.mjs 每个步骤的 height；超长页（如任务库）只截首屏即可。');

fs.writeFileSync('probe.txt', log.join('\n'), 'utf8');
s.close();
console.log('probe.txt written');
