// validate/static-checks.js — 源码级检查(可给行号)
// 规则消息与旧 validate.js 逐字一致;新增规则一律进 layout-checks.js 并受基线门禁约束。
function staticChecks(file, src) {
  const issues = [];
  // <template data-slide-notes> 是演讲者备注,其内容是自然语言文本,不是 HTML/CSS —
  // 不应参与样式检查(备注里提到 "transform:rotate" 等字样会被正则误判)。
  // 用等量空行替换 template 内容,保留行号准确(后续行的 line number 不变)。
  const srcNoTemplate = src.replace(/<template\b[^>]*>[\s\S]*?<\/template>/gi, (m) => "\n".repeat(m.split("\n").length - 1));
  const lines = srcNoTemplate.split("\n");
  const lineOf = (idx) => srcNoTemplate.slice(0, idx).split("\n").length;

  if (!src.includes("slide-container"))
    issues.push({ level: "ERROR", line: 1, msg: "缺少 .slide-container 根容器", fix: "用 <div class=\"slide-container\" style=\"position:relative;width:1920px;height:1080px;overflow:hidden;\"> 包裹全部内容" });

  lines.forEach((line, i) => {
    const ln = i + 1;
    // <img> 已支持(2026-07-27 P1):原生 image 基元;不再报 ERROR
    // transform(2026-07-27 起放行纯旋转):rotate(deg) 原生还原;缩放/斜切/平移仍会丢 → ERROR
    // 负向后行排除 text-transform(大小写变换是文字规则,与几何 transform 无关)
    const tm = /(?<![\w-])transform\s*:\s*([^;]+)/i.exec(line);
    if (tm && !/^\s*\/\//.test(line)) {
      const v = tm[1].trim();
      const isRotateOnly = /^(none|rotate\(\s*-?[\d.]+(deg)?\s*\))$/i.test(v);
      if (!isRotateOnly)
        issues.push({ level: "ERROR", line: ln, msg: "transform 仅支持纯旋转 rotate()(缩放/斜切/平移在 PPTX 中丢失)", fix: "纯旋转可保留;尺寸用宽高直接表达,斜切/缩放图形改放图片背景" });
    }
    if (/box-shadow\s*:/i.test(line) && !/box-shadow\s*:\s*none/i.test(line))
      issues.push({ level: "WARN", line: ln, msg: "box-shadow 只还原第一层非 inset 阴影(spread 与多层不还原)", fix: "如需精确阴影,改用渐变/多层形状模拟" });
    if (/writing-mode\s*:/i.test(line))
      issues.push({ level: "WARN", line: ln, msg: "竖排文字为实验性支持(eaVert)", fix: "逐字 <br> 换行是更稳的替代" });
  });
  return issues;
}

module.exports = { staticChecks };
