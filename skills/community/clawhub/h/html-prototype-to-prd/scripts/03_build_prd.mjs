/**
 * 步骤 3／4：把截图以 base64 内嵌进 PRD 模板，产出单文件 HTML
 *
 * 为什么内嵌：交付出去的 PRD 要能单独发人、拷到任何电脑都能打开，不能依赖外部图片目录。
 *
 * 前置：模板里图片位置留了 __IMG_01__ 这类占位符；shots/ 下有对应 PNG
 * 用法：node 03_build_prd.mjs
 * 产出：单文件 HTML（含内联样式 + base64 图片）
 */
import fs from 'node:fs';

// ==================== 配置区（只改这里） ====================
const CONFIG = {
  template: 'prd_template.html',
  output: '产品需求文档PRD.html',
  images: {
    '__IMG_01__': 'shots/01_week.png',
    '__IMG_02__': 'shots/02_day.png',
    '__IMG_03__': 'shots/03_month.png',
    '__IMG_04__': 'shots/04_library.png',
    '__IMG_05__': 'shots/05_detail.png',
    '__IMG_06__': 'shots/06_new.png',
    '__IMG_07__': 'shots/07_head.png',
    '__IMG_08__': 'shots/08_search.png',
  },
};
// ==========================================================

let out = fs.readFileSync(CONFIG.template, 'utf8');
const report = [];

for (const [key, file] of Object.entries(CONFIG.images)) {
  if (!fs.existsSync(file)) { report.push('MISSING  ' + file); continue; }
  const b64 = fs.readFileSync(file).toString('base64');
  const before = out.length;
  // 必须用 split/join，不要用 replace：base64 里的 $& $1 会被当成替换模式
  out = out.split(key).join('data:image/png;base64,' + b64);
  report.push(`${key}  <-  ${file}  (${(b64.length / 1024).toFixed(0)}KB, +${out.length - before} chars)`);
}

const left = (out.match(/__IMG_\d+__/g) || []).length;
report.push('');
report.push('未替换占位符 = ' + left + (left === 0 ? '  ✓' : '  ✗ 模板里的图片位没配全'));

fs.writeFileSync(CONFIG.output, out, 'utf8');
report.push('输出文件 = ' + CONFIG.output);
report.push('字节数 = ' + fs.statSync(CONFIG.output).size);

fs.writeFileSync('build.log', report.join('\n'), 'utf8');
console.log(report.join('\n'));
if (left !== 0) process.exitCode = 1;
