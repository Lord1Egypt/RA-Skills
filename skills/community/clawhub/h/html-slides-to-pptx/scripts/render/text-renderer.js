// render/text-renderer.js — text 基元 → 原生可编辑文本框
// 行距用绝对磅值 spcPts(红线②);单行不换行,避免窄盒因替换字体变宽而折行。
// run 级富样式(italic/underline/strike/link/fontFace)仅在存在时写入,
// 保证旧页面(无这些键)L2 XML 与基线逐字节一致。
function renderText(slide, p, units, config) {
  const mapFont = (ff) =>
    config.applyFontMap ? config.fontMap[ff] || ff : ff; // H1:默认映射,可配置关闭
  const boxFontFace = mapFont(p.fontFace);

  const textArr = p.runs.map((r) => ({
    text: r.text,
    options: {
      color: r.color,
      fontSize: units.pt(r.size),
      bold: r.bold,
      breakLine: !!r.breakLine,
      fontFace: r.fontFace ? mapFont(r.fontFace) : boxFontFace,
      // 2026-07-27 P2 2.3:run 级 charSpacing 优先,回退到 box 级
      charSpacing: r.charSpacing ? units.pt(r.charSpacing) : p.letterSpacing ? units.pt(p.letterSpacing) : undefined,
      ...(r.italic ? { italic: true } : {}),
      ...(r.underline ? { underline: { style: "sng" } } : {}),
      ...(r.strike ? { strike: "sngStrike" } : {}),
      ...(r.link ? { hyperlink: { url: r.link } } : {}),
      ...(r.bullet ? { bullet: r.bullet } : {}),
      // 2026-07-27 P2 2.3:上下标(pptxgenjs 原生支持)
      ...(r.sup ? { superscript: true } : {}),
      ...(r.sub ? { subscript: true } : {}),
    },
  }));
  // 行距:多行才设绝对磅值,单行交给 valign 居中
  const lineSpacing = p.singleLine || !p.lineHeightPx ? undefined : units.pt(p.lineHeightPx);
  slide.addText(textArr, {
    x: units.px(p.rect.x),
    y: units.px(p.rect.y),
    w: units.px(p.rect.w),
    h: units.px(p.rect.h),
    align: p.align,
    valign: p.valign,
    margin: 0,
    wrap: !p.singleLine,
    autoFit: false,
    shrinkText: false,
    lineSpacing,
    ...(p.vertical ? { vert: "eaVert" } : {}),
    ...(p.rotate ? { rotate: p.rotate } : {}),
  });
}

module.exports = { renderText };
