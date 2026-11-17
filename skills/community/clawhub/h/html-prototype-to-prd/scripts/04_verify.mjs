/**
 * 步骤 4／4：验收成品 PRD
 *
 * 必查两件事：
 *  1) 8 张图有没有坏图（base64 没接上 / 路径填错的典型症状）
 *  2) 结构数字对不对（章节数、表格数、页面块数）
 *
 * 前置：把成品 HTML 复制到静态服务目录下（脚本里叫 prd_view.html）
 * 用法：node 04_verify.mjs
 * 产出：verify.log（文本）+ verify/ 下抽查截图
 */
import { openSession, sleep } from './cdp.mjs';
import fs from 'node:fs';

// ==================== 配置区（只改这里） ====================
const CONFIG = {
  url: 'http://127.0.0.1:8766/prd_view.html',
  width: 1440,
  height: 1060,
  outDir: 'verify',
  // 期望值：从模板里数出来，别猜
  expect: { images: 8, pageBlocks: 8, sections: 6 },
  // 抽查截图的锚点
  probes: ['#p31'],
};
// ==========================================================

fs.mkdirSync(CONFIG.outDir, { recursive: true });
const s = await openSession();
await s.send('Emulation.setDeviceMetricsOverride',
  { width: CONFIG.width, height: CONFIG.height, deviceScaleFactor: 1, mobile: false });
await s.go(CONFIG.url);
await sleep(1000);

const raw = await s.evalJs(`(()=>{
  const a=[...document.images];
  return JSON.stringify({
    images: a.length,
    broken: a.filter(i=>!i.complete||i.naturalWidth===0).map(i=>i.alt||'(no alt)'),
    pageBlocks: document.querySelectorAll('.page-block').length,
    sections: document.querySelectorAll('section').length,
    tables: document.querySelectorAll('table').length,
    height: document.documentElement.scrollHeight
  });
})()`);
const got = JSON.parse(raw);

const log = [];
let fail = 0;
const chk = (name, ok, detail) => { if (!ok) fail++; log.push(`${ok ? 'PASS' : 'FAIL'}  ${name}  ${detail}`); };

chk('图片总数', got.images === CONFIG.expect.images, `got=${got.images} want=${CONFIG.expect.images}`);
chk('无坏图', got.broken.length === 0, got.broken.length ? '坏了: ' + got.broken.join(', ') : 'broken=[]');
chk('页面块数', got.pageBlocks === CONFIG.expect.pageBlocks, `got=${got.pageBlocks} want=${CONFIG.expect.pageBlocks}`);
chk('章节数', got.sections === CONFIG.expect.sections, `got=${got.sections} want=${CONFIG.expect.sections}`);
log.push(`INFO  表格=${got.tables} 文档高=${got.height}px`);

await s.shot(`${CONFIG.outDir}/00_top.png`);
for (const sel of CONFIG.probes) {
  await s.evalJs(`document.querySelector('${sel}').scrollIntoView({block:'start'})`);
  await sleep(500);
  await s.shot(`${CONFIG.outDir}/${sel.replace(/[#.]/g, '')}.png`);
}
log.push('');
log.push(fail ? `${fail} 项未通过` : '全部通过');

fs.writeFileSync('verify.log', log.join('\n'), 'utf8');
s.close();
console.log(log.join('\n'));
if (fail) process.exitCode = 1;
