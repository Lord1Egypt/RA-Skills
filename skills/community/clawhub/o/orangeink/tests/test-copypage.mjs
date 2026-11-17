// test-copypage.mjs — 复制页微调栏冒烟测试（jsdom 执行页面内联脚本）
// 用法: node test-copypage.mjs <复制页.html>
import fs from 'fs';
import { JSDOM } from 'jsdom';

const file = process.argv[2];
if (!file) { console.error('用法: node test-copypage.mjs <复制页.html>'); process.exit(1); }
const html = fs.readFileSync(file, 'utf-8');

// 信任边界（响应 ClawHub "Missing User Warnings"）：本测试以 runScripts:'dangerously' 执行
// 页面内联脚本，【仅限 orangeink render.mjs 自产的复制页】。任何第三方/不可信 HTML 一律拒绝——
// 缺少 oimd 品牌标记的文件直接退出，不进入 jsdom，防止任意代码借测试进程执行。
if (!html.includes('orangeink · oimd v')) {
  console.error('拒绝执行：输入缺少 orangeink · oimd 品牌标记，不是本工具自产的复制页。');
  console.error('本测试仅信任 scripts/render.mjs 生成的输出文件，不加载不可信 HTML。');
  process.exit(2);
}

const dom = new JSDOM(html, { runScripts: 'dangerously', url: 'http://localhost/' });
const { window } = dom;
const doc = window.document;
const fail = [];
const ok = (cond, name) => { console.log((cond ? 'PASS ' : 'FAIL ') + name); if (!cond) fail.push(name); };

const api = window.__oimd;
ok(!!api, '暴露 window.__oimd 接口');
const stage = doc.getElementById('stage');
const orig = api.original();
ok(stage.innerHTML === orig, '初始状态 = 原始渲染（未应用任何变换）');
ok(doc.getElementById('optTheme').value === 'orangeink', '主题下拉默认 orangeink');
ok(doc.getElementById('optZoom').value === '1', '字号下拉默认标准');
ok(doc.getElementById('optPad').value === '14', '边距下拉默认窄 14');
ok(/orangeink · oimd v\d+\.\d+\.\d+/.test(doc.getElementById('bar').textContent), '品牌位：顶部 orangeink · oimd 版本号');
ok(/github\.com\/aladooo\/orangeink/.test(doc.getElementById('foot').textContent), '品牌位：底部引流链接');
ok(!doc.getElementById('hint'), '近似提示已移除（不暴露 CLI 细节给最终读者）');
ok(doc.getElementById('optPhone').checked === true && doc.body.className === 'phone', '手机预览默认开启');

// ① 主题切换 → 墨蓝
api.state.theme = 'inkblue'; api.apply();
let h = stage.innerHTML;
ok(h.indexOf('#bf3b1e') !== -1 && h.indexOf('#ff5a00') === -1, '① 主题→墨蓝：主色已映射');
ok(h.indexOf('#2f4d6e') !== -1 && h.indexOf('#c94a00') === -1, '① 主题→墨蓝：EMBER 已映射');

// ② 深色（夜读配色）
api.state.theme = 'orangeink'; api.state.dark = true; api.apply();
h = stage.innerHTML;
ok(h.indexOf('#d8d2c8') !== -1 && h.indexOf('#ece7de') !== -1, '② 深色：正文/标题换夜读配色');
ok(h.indexOf('background:#141312') !== -1, '② 深色：根部注入深底');

// ③ 字号 ×1.06
api.state.dark = false; api.state.zoom = 1.06; api.apply();
h = stage.innerHTML;
ok(h.indexOf('font-size:17px') !== -1, '③ 字号×1.06：16px→17px');
ok(h.indexOf('font-size:16px') === -1, '③ 字号×1.06：原 16px 已全部缩放');

// ④ 边距 → 22
api.state.zoom = 1; api.state.pad = 22; api.apply();
h = stage.innerHTML;
ok(h.indexOf('<section style="padding:0 22px;box-sizing:border-box"') === 0, '④ 边距→22：根部 padding 已改');

// ⑤ 边距 → 0（剥离分支）
api.state.pad = 0; api.apply();
h = stage.innerHTML;
ok(h.indexOf('<section style="box-sizing:border-box"') === 0, '⑤ 边距→0：根部 padding 已剥离');

// ⑥ 恢复默认 → 与原始逐字节一致（恒等性）
api.state.theme = 'orangeink'; api.state.dark = false; api.state.zoom = 1; api.state.pad = 14; api.apply();
ok(stage.innerHTML === orig, '⑥ 恢复默认后与原始渲染逐字节一致');

// ⑦ 手机预览（默认开；仅切 class，不影响复制内容）
api.state.phone = false; api.apply();
ok(doc.body.className === '' && stage.innerHTML === orig, '⑦ 手机预览关闭：class 清空，正文不变');
api.state.phone = true; api.apply();
ok(doc.body.className === 'phone' && stage.innerHTML === orig, '⑦ 手机预览开启：仅切 class，正文不变');

console.log(fail.length ? 'FAIL 共 ' + fail.length + ' 项' : 'PASS 复制页微调栏全部通过');
process.exit(fail.length ? 1 : 0);
