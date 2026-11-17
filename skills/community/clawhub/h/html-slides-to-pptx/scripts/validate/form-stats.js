// validate/form-stats.js — 页面视觉形式统计(2026-08-05 第三轮重构 D 期)
// 浏览器端自包含函数:validate/index.js 与 preview.js 通过 page.evaluate 序列化注入。
// 计数口径与 reference/design-principles.md 第五章一致:
//   计入 = 形状(最小边 ≥8px;全画布底色块除外)、内联 SVG 图标、data-chart/canvas、<table>、<img>
//   不计入 = 细线/中缝(最小边 <8px)、纯装饰、页眉页脚页码(文字本就不计)
// 返回:{ airy, form, nonText, counts } ;form ∈ text/diagram/chart/image/mixed
function formStats(opts) {
  const airyByConfig = !!(opts && opts.airy);
  const container = document.querySelector(".slide-container");
  const empty = { shape: 0, icon: 0, chart: 0, table: 0, image: 0 };
  if (!container) return { airy: true, form: "text", nonText: 0, counts: empty };
  const base = container.getBoundingClientRect();
  const CW = base.width, CH = base.height;
  const counts = { shape: 0, icon: 0, chart: 0, table: 0, image: 0 };
  let maxFs = 0, textObjCount = 0;
  const visible = (el) => {
    const cs = getComputedStyle(el);
    return cs.display !== "none" && cs.visibility !== "hidden";
  };
  const minSideOk = (r) => Math.min(r.width, r.height) >= 8;

  // 图标:每个可见 svg
  container.querySelectorAll("svg").forEach((el) => {
    if (!visible(el)) return;
    if (minSideOk(el.getBoundingClientRect())) counts.icon++;
  });
  // 图表:data-chart 声明 或 canvas 画布
  container.querySelectorAll("[data-chart], canvas").forEach((el) => {
    if (!visible(el)) return;
    if (minSideOk(el.getBoundingClientRect())) counts.chart++;
  });
  // 表格
  container.querySelectorAll("table").forEach((el) => {
    if (visible(el)) counts.table++;
  });
  // 图片:<img>
  container.querySelectorAll("img").forEach((el) => {
    if (!visible(el)) return;
    if (minSideOk(el.getBoundingClientRect())) counts.image++;
  });
  // 形状:bg 纯色/渐变(排除全画布底色块;排除自身已计入图表/图片的元素);
  // background-image:url(...) 的 shape 计为图片(全出血大图页即此形态)
  container.querySelectorAll('[data-object="true"]').forEach((el) => {
    if (!visible(el)) return;
    const cs = getComputedStyle(el);
    const r = el.getBoundingClientRect();
    if (r.width < 1 || r.height < 1) return;
    if ((el.textContent || "").trim()) {
      textObjCount++;
      maxFs = Math.max(maxFs, parseFloat(cs.fontSize) || 0);
    }
    if (el.hasAttribute("data-chart") || /^(img|canvas|table|svg)$/i.test(el.tagName)) return;
    const bgImg = cs.backgroundImage || "none";
    const hasUrl = /url\(/.test(bgImg);
    if (!minSideOk(r)) return; // 细线/中缝/装饰点
    if (hasUrl) { counts.image++; return; } // 全画布背景图也算(全出血大图正是页面主角)
    const bgc = cs.backgroundColor || "";
    const hasSolidFill = bgc !== "transparent" && !/rgba?\([^)]*,\s*0(\.0+)?\s*\)/.test(bgc);
    const hasGradient = /gradient\(/.test(bgImg);
    if (!hasSolidFill && !hasGradient) return;
    if (r.width >= CW * 0.98 && r.height >= CH * 0.98) return; // 全画布底色块
    counts.shape++;
  });

  // airy 判定:与 dom-checks 画布填充检查同款启发(配置名单 + 深底 + 超大字少元素)
  let dark = false;
  const m = /rgba?\(([^)]+)\)/.exec(getComputedStyle(container).backgroundColor || "");
  if (m) {
    const ch = m[1].split(",").map((v) => parseFloat(v));
    dark = (0.2126 * ch[0] + 0.7152 * ch[1] + 0.0722 * ch[2]) / 255 < 0.35;
  }
  const airy = airyByConfig || dark || (maxFs >= 64 && textObjCount <= 5);
  const nonText = counts.shape + counts.icon + counts.chart + counts.table + counts.image;
  const kinds = [];
  if (counts.shape + counts.icon > 0) kinds.push("diagram");
  if (counts.chart + counts.table > 0) kinds.push("chart");
  if (counts.image > 0) kinds.push("image");
  const form = kinds.length === 0 ? "text" : kinds.length === 1 ? kinds[0] : "mixed";
  return { airy, form, nonText, counts };
}

module.exports = { formStats };
