// render/table-renderer.js — table 基元 → 原生可编辑表格(2026-07-27 P1)
// 单元格 fontSize px→pt;边框 w px→pt + type(dash);列宽/行高 px→in。
function renderTable(slide, p, units, config) {
  const colW = (p.colWidths || []).map((w) => units.px(w));
  const rowH = (p.rowHeights || []).map((h) => units.px(h));

  const mapFont = (ff) => (config.applyFontMap ? config.fontMap[ff] || ff : ff);
  const dashType = (d) => (d === "dashed" ? "dash" : d === "dotted" ? "sysDot" : undefined);

  const rows = p.rows.map((cells) =>
    cells.map((c) => {
      const o = { ...c.options };
      if (o.fontSize) o.fontSize = units.pt(o.fontSize);
      if (o.fontFace) o.fontFace = mapFont(o.fontFace);
      // 边框:统一 → 单 BorderProps;非统一 → [t,r,b,l] 四元组(空边 type:'none')
      if (o.border) {
        if (o.border.uniform) {
          const b = { pt: units.pt(o.border.w), color: o.border.hex };
          const dt = dashType(o.border.dash);
          if (dt) b.type = o.border.dash === "dashed" ? "dash" : "solid";
          o.border = b;
        } else {
          o.border = o.border.sides.map((s) =>
            s ? { pt: units.pt(s.w), color: s.hex, ...(s.dash ? { type: s.dash === "dashed" ? "dash" : "solid" } : {}) } : { type: "none" }
          );
        }
      }
      return { text: c.text, options: o };
    })
  );

  slide.addTable(rows, {
    x: units.px(p.rect.x),
    y: units.px(p.rect.y),
    colW,
    rowH,
    autoPage: false,
    fontFace: config.applyFontMap ? mapFont("Noto Sans SC") : "Noto Sans SC",
  });
}

module.exports = { renderTable };
