// extract/primitives/table.js — <table> → table 基元(2026-07-27 P1)
// 解析 tr/td(th):单元格文本(单样式)+ colspan/rowspan + 底纹 + 边框 + 对齐;
// 列宽/行高取首行单元格 offsetWidth / 各行最大 offsetHeight。渲染端转 pt/in。
(() => {
  const ns = (window.__htmlSlides = window.__htmlSlides || {});
  ns.primitives = ns.primitives || {};

  const valignMap = (v) => (v === "top" || v === "bottom" ? v : "middle");
  const alignMap = (a) => (["", "start", "normal"].includes(a) ? "left" : a);

  // 单元格边框 → pptxgenjs BorderProps(单值或 [t,r,b,l] 四元组)
  function cellBorder(tcs) {
    const sides = [
      { w: parseFloat(tcs.borderTopWidth) || 0, color: ns.rgb(tcs.borderTopColor), style: tcs.borderTopStyle },
      { w: parseFloat(tcs.borderRightWidth) || 0, color: ns.rgb(tcs.borderRightColor), style: tcs.borderRightStyle },
      { w: parseFloat(tcs.borderBottomWidth) || 0, color: ns.rgb(tcs.borderBottomColor), style: tcs.borderBottomStyle },
      { w: parseFloat(tcs.borderLeftWidth) || 0, color: ns.rgb(tcs.borderLeftColor), style: tcs.borderLeftStyle },
    ];
    const nonZero = sides.filter((s) => s.w > 0 && s.color);
    if (!nonZero.length) return null;
    const uniform =
      new Set(sides.map((s) => s.w)).size === 1 &&
      new Set(sides.map((s) => (s.color ? s.color.hex : "none"))).size === 1 &&
      new Set(sides.map((s) => (s.w > 0 ? s.style : "none"))).size === 1;
    const mk = (s) =>
      s && s.w > 0 && s.color
        ? { hex: s.color.hex, w: s.w, ...(s.style !== "solid" ? { dash: s.style } : {}) }
        : null;
    if (uniform) return { uniform: true, ...mk(nonZero[0]) };
    return { uniform: false, sides: sides.map(mk) };
  }

  // 2026-08-05 H12 修复:单元格底纹沿 td → tr → table 回溯。
  // background 写在 <tr>/<table> 上是表格底纹的主流写法,但 CSS background 不继承到 td,
  // getComputedStyle(td).backgroundColor 恒为 transparent → 深蓝表头/zebra 底纹全丢
  // (106-table-focus 锚定页一直如此;L3 免截纯原生页 → 视觉缺陷全程隐形)。
  // 回溯取第一个非透明背景;rgba(…,0) 视为无底纹。
  function cellBg(td) {
    let el = td;
    while (el && el.tagName !== "TABLE") {
      const b = ns.rgb(getComputedStyle(el).backgroundColor);
      if (b && b.alpha > 0) return b;
      el = el.parentElement;
    }
    return null;
  }

  ns.primitives.table = {
    name: "table",
    emit(el, cs, rect, collector, cfg) {
      const rows = [];
      const colWidths = [];
      const rowHeights = [];
      const trs = el.querySelectorAll("tr");
      trs.forEach((tr, ri) => {
        const cells = [];
        let rowH = 0;
        Array.from(tr.children).forEach((td, ci) => {
          const tcs = getComputedStyle(td);
          const bg = cellBg(td);
          const b = cellBorder(tcs);
          const fontFace = (tcs.fontFamily || "").split(",")[0].replace(/["']/g, "").trim();
          const fw = parseInt(tcs.fontWeight, 10);
          const cell = {
            text: (td.textContent || "").replace(/\s+/g, " ").trim() || " ",
            options: {
              align: alignMap(tcs.textAlign),
              valign: valignMap(tcs.verticalAlign),
              fontSize: Math.round(parseFloat(tcs.fontSize)),
              color: (ns.rgb(tcs.color) || { hex: cfg.defaultColorHex }).hex,
              bold: fw >= (cfg.boldThreshold || 600),
              fontFace,
              margin: 0.04, // ~3px 内边距
              ...(bg ? { fill: { color: bg.hex, transparency: 100 - bg.alpha } } : {}),
              ...(td.colSpan > 1 ? { colspan: td.colSpan } : {}),
              ...(td.rowSpan > 1 ? { rowspan: td.rowSpan } : {}),
              ...(b ? { border: b } : {}),
            },
          };
          cells.push(cell);
          if (ri === 0) colWidths[ci] = td.offsetWidth;
          rowH = Math.max(rowH, td.offsetHeight);
        });
        rowHeights[ri] = rowH;
        rows.push(cells);
      });
      if (!rows.length) return;
      collector.push({ kind: "table", rect, rows, colWidths, rowHeights });
    },
  };
})();
