// validate/palette-checks.js — 用色纪律(2026-08-17 第九轮 P3;浏览器端自包含函数)
//
// 为什么需要它(实测,见 .claude/plans/palette-and-determinism.md):
// theme.css 一直被称作"约束",但**校验器从不读它** —— 1104 行 validate 里没有任何规则
// 认识色板。后果在真实 deck 上量到了:
//   · 34 页的 deck:var() 用量 0、裸色声明 1074 处,所用色板逐值等于**另一套**预设
//     (theme.css 是联想红/深蓝,页面全是 Apple 蓝灰)—— 今天 0 ERROR 通过;
//   · 41 个色板外色里 60% 的用法只是"某色板色 × 白混合",本该是变量(P1 已补齐梯级);
//   · 近似重打成灾:#0A2C63 vs #0A2E5C(ΔRGB 7)、#1D1D1F vs #1F1F1F(2.8)——
//     肉眼同色、值不同,PPTX 里是不同填充色,永远无法整体换肤。
//
// 边界(刻意不查的):
//   · `<svg>` 内的着色:H7 要求图标显式着色(currentColor 会被截图规则变透明),
//     属性形态与 CSS 属性形态都合法,不在本规则管辖内;
//   · 渐变色停与 rgba 阴影:P1 未提供渐变梯级令牌,留待后续轮次;
//   · **不判断"这个颜色好不好看"** —— 只判断"它是否来自色板",越位就成了品味审查。
//
// 与转换保真的关系:提取器读**计算样式**,var() 与裸 hex 对 PPTX 输出完全等价。
// 所以本规则全部是 WARN(可维护性/一致性问题,不是转换错误),不做 ERROR。
function paletteChecks(arg) {
  const design = (arg && arg.design) || {};
  const palette = new Set((arg && arg.palette) || []);
  const T = design.thresholds || {};
  const issues = [];
  if (!design.tier) return issues; // 与其余设计检查同例:tier 为空 = 休眠
  if (!palette.size) return issues; // 解析不到色板(无 theme.css)→ 不判,避免全页误报

  const container = document.querySelector(".slide-container");
  if (!container) return issues;

  const TOL = T.paletteTolerance != null ? T.paletteTolerance : 6;
  const OFF_MAX = T.offPaletteMax != null ? T.offPaletteMax : 3;
  const MIN_DECLS = T.paletteMinDecls != null ? T.paletteMinDecls : 4;
  const VAR_PCT_MIN = T.paletteVarPctMin != null ? T.paletteVarPctMin : 70;

  const norm = (h) => {
    let s = h.replace("#", "").toUpperCase();
    if (s.length === 3) s = s.split("").map((c) => c + c).join("");
    return "#" + s.slice(0, 6);
  };
  const rgb = (h) => [1, 3, 5].map((i) => parseInt(norm(h).slice(i, i + 2), 16));
  const dist = (a, b) => Math.sqrt(a.reduce((s, v, i) => s + (v - b[i]) ** 2, 0));
  const nearest = (hex) => {
    let best = null;
    for (const p of palette) {
      const d = dist(rgb(hex), rgb(p));
      if (!best || d < best.d) best = { p, d };
    }
    return best;
  };

  // 统计对象:只看**作者写在 style 属性/内联 <style> 里的声明**,不看计算样式 ——
  // 计算样式里 var() 已被解析成具体色,无法区分"写了变量"与"写了 hex"(这正是要区分的东西)。
  let declTotal = 0, rawTotal = 0;
  const offPalette = new Map(); // hex -> {count, sample}
  const COLOR_PROPS = /(?:^|;)\s*(background|background-color|color|border-color|border-top-color|border-bottom-color|border-left-color|border-right-color|fill|stroke)\s*:\s*([^;]+)/gi;

  const scan = (styleText, sampleText) => {
    if (!styleText) return;
    for (const m of styleText.matchAll(COLOR_PROPS)) {
      const value = m[2].trim();
      // 渐变/图片:本轮不查(见文件头边界)
      if (/gradient|url\(/i.test(value)) continue;
      declTotal++;
      const hexes = value.match(/#[0-9A-Fa-f]{3,8}/g);
      if (!hexes) continue; // var() / 关键字(transparent/inherit)→ 记入总数,不计裸色
      rawTotal++;
      for (const h of hexes) {
        const hex = norm(h);
        if (palette.has(hex)) continue; // 值在色板内(写死了但至少同色板)——由 R2 的占比来管
        const prev = offPalette.get(hex);
        if (prev) prev.count++;
        else offPalette.set(hex, { count: 1, sample: (sampleText || "").trim().slice(0, 16) });
      }
    }
  };

  Array.from(container.querySelectorAll("*")).forEach((el) => {
    if (el.tagName === "TEMPLATE" || el.closest("template")) return; // 备注不显示给观众
    if (el.tagName.toLowerCase() === "svg" || el.closest("svg")) return; // H7 豁免
    const cs = getComputedStyle(el);
    if (cs.display === "none" || cs.visibility === "hidden") return;
    scan(el.getAttribute("style"), el.textContent);
  });

  // R1 · 色板外用色:逐色报(带"应该改成哪个变量"的具体建议,便于弱模型一次改对)
  for (const [hex, info] of offPalette) {
    const n = nearest(hex);
    const near = n && n.d <= TOL;
    issues.push({
      level: "WARN",
      msg: near
        ? `色板外用色 ${hex}(用 ${info.count} 次)与色板色 ${n.p} 肉眼同色但值不同 —— 近似重打,PPTX 里会成为两个不同填充色${info.sample ? `: "${info.sample}"` : ""}`
        : `色板外用色 ${hex}(用 ${info.count} 次)不在 theme.css 色板内${info.sample ? `: "${info.sample}"` : ""}`,
      fix: n
        ? `改用最接近的色板变量(${n.p} 对应的变量,ΔRGB ${Math.round(n.d)});确有新色需求 → 先加进 theme.css 与 16 套预设(tools/gen-ladder.js)`
        : "改用 theme.css 的色板变量",
    });
  }

  // R1b · 整页脱离色板:去重后色板外色过多 = 不是个别硬编码,是整页按另一套色画的
  if (offPalette.size >= OFF_MAX)
    issues.push({
      level: "WARN",
      msg: `本页有 ${offPalette.size} 种色板外颜色(上限 ${OFF_MAX})—— 疑似整页脱离 theme.css 色板`,
      fix: "对照 theme.css 逐一换成色板变量;若是刻意换色板,应改 theme.css 本身(或复制 assets/presets/ 的预设),而不是逐页写死",
    });

  // R2 · var() 占比:样张实测中位 95%,零 var() 的 deck 是 0%。
  //     只在色声明足够多时判(样本太小的页容易误报)。
  if (declTotal >= MIN_DECLS) {
    const varPct = Math.round(((declTotal - rawTotal) / declTotal) * 100);
    if (varPct < VAR_PCT_MIN)
      issues.push({
        level: "WARN",
        msg: `用色几乎不走变量:${declTotal} 处色声明里只有 ${varPct}% 用 var()(下限 ${VAR_PCT_MIN}%)`,
        fix: "把 background/color/border-color 的 hex 改成 theme.css 变量 —— 否则换色板要逐页改,且色值会逐页漂",
      });
  }

  return issues;
}

module.exports = { paletteChecks };
