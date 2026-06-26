// ============================================================
// generate-pptx.cjs — PresentationSchema → Professional .pptx
// Midnight Executive 主题 · 电影级视觉层次 · 可编辑
// ============================================================

const pptxgen = require("pptxgenjs");
const fs = require("fs");
const path = require("path");
const React = require("react");
const ReactDOMServer = require("react-dom/server");
const sharp = require("sharp");
const {
  FaRocket, FaBullseye, FaLightbulb, FaChartLine, FaCogs,
  FaExclamationTriangle, FaCheckCircle, FaTimesCircle,
  FaArrowRight, FaClock, FaQuoteRight, FaQuestionCircle,
  FaComments, FaLayerGroup, FaCode, FaShieldAlt, FaUsers,
  FaStar, FaBook, FaGlobe, FaTools, FaBrain, FaHandshake,
  FaChartBar, FaChartPie, FaDatabase, FaServer, FaMobileAlt,
  FaSearch, FaSync, FaLock, FaKey, FaEnvelope,
} = require("react-icons/fa");

// ─── 路径配置 ────────────────────────────────────────────
const SCHEMA_PATH = process.argv[2] || path.join(__dirname, "presentation-schema.json");
const OUTPUT_PATH = process.argv[3] || path.join(process.cwd(), "output.pptx");

// ─── Midnight Executive 配色 ─────────────────────────────
const C = {
  navy:       "1E2761",   // 主色 — 深海军蓝（封面/章节/强调）
  navyDark:   "151D4A",   // 更深 — 封面背景
  ice:        "E8EEFA",   // 冰蓝 — 亮色幻灯片背景
  white:      "FFFFFF",   // 纯白 — 卡片
  text:       "1A1F36",   // 正文 — 近黑蓝
  textMuted:  "6B7394",   // 弱化文字
  accent:     "F59E0B",   // 琥珀金 — 强调/高亮
  accentGreen:"10B981",   // 翠绿 — 正向
  accentRed:  "EF4444",   // 红 — 负向
  iceDark:    "CADCFC",   // 冰蓝深 — 分割线/边框
  cardBg:     "FFFFFF",   // 卡片
  thesisBg:   "F0F3FA",   // 论点区背景
  navyLight:  "2D3A8C",   // 海军蓝浅
  gold:       "D97706",   // 深金
};

// ─── 字体 ────────────────────────────────────────────────
const F = {
  heading: "Georgia",     // 标题 — 衬线体，有性格
  body:    "Calibri",     // 正文 — 易读
  quote:   "Georgia",     // 引文 — 衬线
  accent:  "Georgia",     // 强调数字 — 衬线
};

// ─── 布局常量（16:9 = 10" × 5.625"） ────────────────────
const L = {
  ml: 0.65,               // 左边距
  mr: 0.65,               // 右边距
  mt: 0.4,                // 上边距
  contentW: 8.7,          // 内容区宽度 = 10 - ml - mr
  titleY: 0.35,
  titleH: 0.65,
  bodyY: 1.2,
  bodyH: 3.9,
  pageNumY: 5.15,
  dataCardW: 2.15,        // 数据卡片宽度
};

// ─── 工具 ────────────────────────────────────────────────

const makeShadow = () => ({ type: "outer", color: "000000", blur: 6, offset: 2, angle: 135, opacity: 0.1 });
const makeCardShadow = () => ({ type: "outer", color: "000000", blur: 4, offset: 1, angle: 135, opacity: 0.06 });

function pageNum(slide, n, total, color = C.textMuted) {
  slide.addText(`${n} / ${total}`, {
    x: 8.7, y: L.pageNumY, w: 1, h: 0.28,
    fontSize: 8, color, fontFace: F.body, align: "right", margin: 0,
  });
}

function topAccentLine(slide) {
  slide.addShape("line", {
    x: L.ml, y: 0.1, w: L.contentW, h: 0,
    line: { color: C.iceDark, width: 0.5 },
  });
}

function renderIcon(Icon, colorHex = "#1E2761", size = 256) {
  const svg = ReactDOMServer.renderToStaticMarkup(
    React.createElement(Icon, { color: colorHex, size: String(size) })
  );
  return sharp(Buffer.from(svg)).png().toBuffer();
}

async function iconBase64(Icon, colorHex, size = 256) {
  const buf = await renderIcon(Icon, colorHex, size);
  return "image/png;base64," + buf.toString("base64");
}

function iconCache() {
  const cache = {};
  return async (Icon, colorHex = "#1E2761", size = 256) => {
    const key = `${Icon.name || Icon.render?.name || "icon"}_${colorHex}_${size}`;
    if (!cache[key]) cache[key] = await iconBase64(Icon, colorHex, size);
    return cache[key];
  };
}

// ─── 通用装饰 ────────────────────────────────────────────

// 深色背景装饰：四角放射 + 顶部金色细线
function darkBgDecor(slide) {
  slide.background = { color: C.navyDark };
  // 右上角放射
  slide.addShape("rect", {
    x: 7, y: -1.5, w: 6, h: 4, rotate: 25,
    fill: { color: C.navy, transparency: 50 },
  });
  // 左下角放射
  slide.addShape("rect", {
    x: -3, y: 3.5, w: 7, h: 4, rotate: -20,
    fill: { color: C.navyLight, transparency: 65 },
  });
  // 顶部金色细线
  slide.addShape("line", {
    x: L.ml, y: 0.35, w: 3.5, h: 0,
    line: { color: C.accent, width: 1.5 },
  });
  // 底部金色细线
  slide.addShape("line", {
    x: 6.5, y: 5.25, w: 2.8, h: 0,
    line: { color: C.accent, width: 1.5 },
  });
}

// 内容页装饰
function contentDecor(slide) {
  // 顶部金色 accent 线
  slide.addShape("line", {
    x: L.ml, y: 0.08, w: 1.6, h: 0,
    line: { color: C.accent, width: 2 },
  });
  // 顶部全域细线
  slide.addShape("line", {
    x: L.ml, y: 0.12, w: L.contentW, h: 0,
    line: { color: C.iceDark, width: 0.3 },
  });
}

// ─── Slide 生成函数 ──────────────────────────────────────

async function generateCover(pres, meta, getIcon) {
  const slide = pres.addSlide();
  darkBgDecor(slide);

  // 左侧大号色块
  slide.addShape("rect", {
    x: 0, y: 0, w: 0.1, h: 5.625,
    fill: { color: C.accent },
  });

  // 右侧装饰几何
  slide.addShape("rect", {
    x: 8.2, y: 1.0, w: 0.04, h: 3.6,
    fill: { color: C.iceDark, transparency: 50 },
  });
  slide.addShape("rect", {
    x: 8.5, y: 1.8, w: 0.04, h: 2.0,
    fill: { color: C.iceDark, transparency: 70 },
  });

  // 标题区域 — 大号衬线
  slide.addText(meta.title.toUpperCase(), {
    x: 1.2, y: 1.2, w: 6.8, h: 1.8,
    fontSize: 30, fontFace: F.heading, color: C.white,
    bold: true, align: "left", valign: "bottom",
    lineSpacingMultiple: 1.15, margin: 0,
  });

  // 分隔线（金色）
  slide.addShape("line", {
    x: 1.2, y: 3.2, w: 2.5, h: 0,
    line: { color: C.accent, width: 2.5 },
  });

  // 副标题
  if (meta.subtitle) {
    slide.addText(meta.subtitle, {
      x: 1.2, y: 3.45, w: 6.8, h: 0.55,
      fontSize: 14, fontFace: F.body, color: C.iceDark,
      align: "left", valign: "top", margin: 0,
    });
  }

  // 演讲者信息区块
  slide.addShape("rect", {
    x: 1.2, y: 4.25, w: 0.05, h: 0.8,
    fill: { color: C.navyLight },
  });
  slide.addText(meta.speaker, {
    x: 1.5, y: 4.25, w: 4, h: 0.35,
    fontSize: 14, fontFace: F.body, color: C.white, bold: true, margin: 0,
  });
  if (meta.speakerRole) {
    slide.addText(meta.speakerRole, {
      x: 1.5, y: 4.55, w: 4, h: 0.25,
      fontSize: 10, fontFace: F.body, color: C.textMuted, margin: 0,
    });
  }
  slide.addText(meta.date, {
    x: 1.5, y: 4.78, w: 4, h: 0.25,
    fontSize: 10, fontFace: F.body, color: C.textMuted, margin: 0,
  });

  // 右下图标
  try {
    const rocketData = await getIcon(FaRocket, "#F59E0B", 128);
    slide.addImage({ data: rocketData, x: 8.0, y: 4.4, w: 0.5, h: 0.5 });
  } catch (_) { /* fallback */ }
}

async function generateSection(pres, data, num, total, getIcon) {
  const slide = pres.addSlide();
  darkBgDecor(slide);

  // 左侧金色条
  slide.addShape("rect", {
    x: 0, y: 0, w: 0.1, h: 5.625,
    fill: { color: C.accent },
  });

  const startY = data.chapterNumber ? 1.2 : 1.8;

  // 章节号 — 超大
  if (data.chapterNumber) {
    slide.addText(data.chapterNumber, {
      x: 1.2, y: startY, w: 2.5, h: 1.5,
      fontSize: 80, fontFace: F.heading, color: C.iceDark,
      bold: true, align: "left", valign: "middle", margin: 0,
      transparency: 30,
    });
  }

  // 章节标题
  slide.addText(data.chapterTitle.toUpperCase(), {
    x: 1.2, y: startY + 1.2, w: 7.5, h: 0.9,
    fontSize: 26, fontFace: F.heading, color: C.white,
    bold: true, align: "left", valign: "top", margin: 0,
  });

  // 分隔线
  slide.addShape("line", {
    x: 1.2, y: startY + 2.25, w: 2, h: 0,
    line: { color: C.accent, width: 2 },
  });

  // 论点
  if (data.thesis) {
    slide.addText(data.thesis, {
      x: 1.2, y: startY + 2.55, w: 7.5, h: 0.6,
      fontSize: 13, fontFace: F.body, color: C.iceDark,
      align: "left", valign: "top", margin: 0,
    });
  }

  // 时长
  if (data.duration) {
    try {
      const clockData = await getIcon(FaClock, "#CADCFC", 64);
      slide.addImage({ data: clockData, x: 1.2, y: startY + 3.3, w: 0.22, h: 0.22 });
    } catch (_) {}
    slide.addText(data.duration, {
      x: 1.55, y: startY + 3.24, w: 3, h: 0.3,
      fontSize: 10, fontFace: F.body, color: C.textMuted, margin: 0,
    });
  }

  pageNum(slide, num, total, "64748B");
}

async function generateContent(pres, data, num, total, getIcon) {
  const slide = pres.addSlide();
  slide.background = { color: C.ice };
  contentDecor(slide);

  // 标题（衬线大写）
  slide.addText(data.title.toUpperCase(), {
    x: L.ml, y: L.titleY, w: L.contentW, h: L.titleH,
    fontSize: 22, fontFace: F.heading, color: C.navy,
    bold: true, align: "left", valign: "middle", margin: 0,
  });

  let curY = 1.15;

  // 核心论点（金色强调）
  if (data.thesis) {
    const th = 0.48;
    slide.addShape("rect", {
      x: L.ml, y: curY, w: L.contentW, h: th,
      fill: { color: C.thesisBg },
    });
    slide.addShape("rect", {
      x: L.ml, y: curY, w: 0.06, h: th,
      fill: { color: C.accent },
    });

    try {
      const bulbData = await getIcon(FaLightbulb, "#F59E0B", 64);
      slide.addImage({ data: bulbData, x: L.ml + 0.2, y: curY + 0.09, w: 0.28, h: 0.28 });
    } catch (_) {}

    slide.addText(data.thesis, {
      x: L.ml + 0.6, y: curY, w: L.contentW - 0.65, h: th,
      fontSize: 13, fontFace: F.body, color: C.navy, bold: true,
      align: "left", valign: "middle", margin: 0,
    });
    curY += th + 0.2;
  }

  const hasData = data.dataHighlights && data.dataHighlights.length > 0;
  const hasBullets = data.bullets && data.bullets.length > 0;

  // 数据卡片（右侧列）
  if (hasData) {
    const count = data.dataHighlights.length;
    const cardW = L.dataCardW;
    const cardH = Math.min(1.2, (L.bodyH - 0.3) / count);
    const gap = 0.1;
    const rightX = L.ml + L.contentW - cardW;
    const startY = curY;

    const icons = [FaChartLine, FaStar, FaUsers, FaChartBar, FaCogs, FaRocket];

    for (let i = 0; i < count; i++) {
      const dh = data.dataHighlights[i];
      const cy = startY + i * (cardH + gap);

      // 卡片背景
      slide.addShape("rect", {
        x: rightX, y: cy, w: cardW, h: cardH,
        fill: { color: C.white }, shadow: makeCardShadow(),
      });

      // 顶部金色细条
      slide.addShape("line", {
        x: rightX + 0.15, y: cy + 0.06, w: cardW - 0.3, h: 0,
        line: { color: C.accent, width: 1 },
      });

      // 大数值（衬线 golden）
      slide.addText(dh.value, {
        x: rightX, y: cy + 0.15, w: cardW, h: cardH * 0.52,
        fontSize: 34, fontFace: F.accent, color: C.accent,
        bold: true, align: "center", valign: "bottom", margin: 0,
      });

      // 标签
      const label = dh.unit ? `${dh.label} ${dh.unit}` : dh.label;
      slide.addText(label, {
        x: rightX, y: cy + cardH * 0.62, w: cardW, h: cardH * 0.32,
        fontSize: 9, fontFace: F.body, color: C.textMuted,
        align: "center", valign: "top", margin: 0,
      });

      // 图标（微弱）
      try {
        const ic = await getIcon(icons[i % icons.length], "#CADCFC", 48);
        slide.addImage({ data: ic, x: rightX + cardW - 0.48, y: cy + cardH - 0.48, w: 0.35, h: 0.35, transparency: 70 });
      } catch (_) {}
    }
  }

  // 要点列表（左侧）
  if (hasBullets) {
    const bulletW = hasData ? L.contentW - L.dataCardW - 0.35 : L.contentW;

    // 图标映射（第一层要点用图标替代默认圆点）
    const itemsWithIcons = [];
    for (let i = 0; i < data.bullets.length; i++) {
      const b = data.bullets[i];
      const prefix = b.iconChar || (b.emphasis === "strong" ? "◆" : "▸");
      itemsWithIcons.push({
        text: `${prefix}  ${b.text}`,
        options: {
          breakLine: i < data.bullets.length - 1,
          fontSize: 13,
          fontFace: F.body,
          color: b.emphasis === "strong" ? C.navy : C.text,
          bold: b.emphasis === "strong",
          paraSpaceAfter: 10,
        },
      });
    }

    slide.addText(itemsWithIcons, {
      x: L.ml + 0.05, y: curY + 0.05, w: bulletW, h: L.bodyY + L.bodyH - curY,
      valign: "top", margin: [0, 0, 0, 8],
    });
  }

  // 标注
  if (data.caption) {
    slide.addText(data.caption, {
      x: L.ml, y: 5.0, w: L.contentW, h: 0.25,
      fontSize: 8, fontFace: F.body, color: C.textMuted,
      italic: true, align: "left", margin: 0,
    });
  }

  pageNum(slide, num, total);

  if (data.speakerNotes) {
    slide.addNotes(data.speakerNotes);
  }
}

async function generateAgenda(pres, data, num, total, getIcon) {
  const slide = pres.addSlide();
  slide.background = { color: C.ice };
  contentDecor(slide);

  slide.addText(data.title.toUpperCase(), {
    x: L.ml, y: L.titleY, w: L.contentW, h: L.titleH,
    fontSize: 22, fontFace: F.heading, color: C.navy,
    bold: true, align: "left", valign: "middle", margin: 0,
  });

  const items = data.items;
  const itemH = Math.min(0.55, 3.6 / items.length);
  const gap = 0.06;
  const startY = 1.15;

  const icons = [FaRocket, FaCogs, FaChartLine, FaShieldAlt, FaBrain, FaTools, FaLightbulb, FaStar];

  for (let i = 0; i < items.length; i++) {
    const item = items[i];
    const y = startY + i * (itemH + gap);

    // 卡片背景
    slide.addShape("rect", {
      x: L.ml, y, w: L.contentW, h: itemH,
      fill: { color: C.white }, shadow: makeCardShadow(),
    });

    // 序号圆（金色）
    slide.addShape("oval", {
      x: L.ml + 0.15, y: y + itemH / 2 - 0.17, w: 0.34, h: 0.34,
      fill: { color: C.navy },
    });
    slide.addText(item.chapter || `${i + 1}`, {
      x: L.ml + 0.15, y: y, w: 0.34, h: itemH,
      fontSize: 11, fontFace: F.heading, color: C.white,
      bold: true, align: "center", valign: "middle", margin: 0,
    });

    // 图标
    try {
      const ic = await getIcon(icons[i % icons.length], "#F59E0B", 48);
      slide.addImage({ data: ic, x: L.ml + 0.65, y: y + itemH / 2 - 0.14, w: 0.28, h: 0.28 });
    } catch (_) {}

    // 标题
    slide.addText(item.title, {
      x: L.ml + 1.05, y: y, w: 5.5, h: itemH,
      fontSize: 13, fontFace: F.body, color: C.text,
      bold: true, align: "left", valign: "middle", margin: 0,
    });

    // 时长（右侧）
    if (item.duration) {
      slide.addText(item.duration, {
        x: 7.0, y: y, w: 1.2, h: itemH,
        fontSize: 10, fontFace: F.body, color: C.textMuted,
        align: "left", valign: "middle", margin: 0,
      });
    }

    // 论点（小字）
    if (item.thesis) {
      slide.addText(item.thesis, {
        x: L.ml + 1.05, y: y + itemH * 0.55, w: 7, h: itemH * 0.4,
        fontSize: 9, fontFace: F.body, color: C.textMuted,
        align: "left", valign: "top", margin: 0,
      });
    }
  }

  pageNum(slide, num, total);
}

async function generateQuote(pres, data, num, total, getIcon) {
  const slide = pres.addSlide();
  slide.background = { color: C.navy };
  darkBgDecor(slide);

  // 大号引号装饰
  slide.addText("\u201C", {
    x: 0.5, y: -0.3, w: 3, h: 3,
    fontSize: 160, fontFace: F.quote, color: C.navyLight,
    transparency: 40, align: "left", valign: "top", margin: 0,
  });

  // 引文
  slide.addText(data.quote, {
    x: 1.5, y: 1.2, w: 7, h: 2.4,
    fontSize: 24, fontFace: F.quote, color: C.white,
    italic: true, align: "left", valign: "middle",
    lineSpacingMultiple: 1.3, margin: 0,
  });

  // 金色分割线
  slide.addShape("line", {
    x: 1.5, y: 3.7, w: 2, h: 0,
    line: { color: C.accent, width: 2 },
  });

  // 上下文
  if (data.context) {
    slide.addText(data.context, {
      x: 1.5, y: 3.95, w: 7, h: 0.45,
      fontSize: 13, fontFace: F.body, color: C.iceDark,
      align: "left", valign: "top", margin: 0,
    });
  }
  if (data.source) {
    slide.addText(`\u2014 ${data.source}`, {
      x: 1.5, y: 4.35, w: 7, h: 0.35,
      fontSize: 11, fontFace: F.body, color: C.textMuted,
      align: "left", valign: "top", margin: 0,
    });
  }

  // 右下图标
  try {
    const qData = await getIcon(FaQuoteRight, "#F59E0B", 64);
    slide.addImage({ data: qData, x: 7.8, y: 4.5, w: 0.35, h: 0.35, transparency: 40 });
  } catch (_) {}

  pageNum(slide, num, total, "64748B");
}

function generateTable(pres, data, num, total) {
  const slide = pres.addSlide();
  slide.background = { color: C.ice };
  contentDecor(slide);

  slide.addText(data.title.toUpperCase(), {
    x: L.ml, y: L.titleY, w: L.contentW, h: L.titleH,
    fontSize: 22, fontFace: F.heading, color: C.navy,
    bold: true, align: "left", valign: "middle", margin: 0,
  });

  const rows = data.rows;
  const cols = data.columns;
  const colW = cols.map(() => L.contentW / cols.length);
  const rowH = 0.38;

  // 表头
  const headerRow = cols.map((col, ci) => ({
    text: col.toUpperCase(),
    options: {
      fill: { color: C.navy },
      color: C.white,
      bold: true,
      fontSize: 9,
      fontFace: F.body,
      align: ci === 0 ? "left" : "center",
      valign: "middle",
      charSpacing: 1.5,
    },
  }));

  // 数据行（交替）
  const dataRows = rows.map((row, ri) =>
    row.map((cell, ci) => ({
      text: cell,
      options: {
        fill: { color: ri % 2 === 0 ? C.white : C.ice },
        color: ri === 0 ? C.accent : C.text,
        bold: ri === 0,
        fontSize: 10,
        fontFace: F.body,
        align: ci === 0 ? "left" : "center",
        valign: "middle",
      },
    }))
  );

  const tableH = (rows.length + 1) * rowH;
  const tableY = 1.3;

  slide.addTable([headerRow, ...dataRows], {
    x: L.ml, y: tableY, w: L.contentW,
    colW, rowH: [rowH, ...rows.map(() => rowH)],
    border: { pt: 0.3, color: C.iceDark },
    margin: [4, 8, 4, 8],
  });

  if (data.caption) {
    slide.addText(data.caption, {
      x: L.ml, y: tableY + tableH + 0.1, w: L.contentW, h: 0.25,
      fontSize: 8, fontFace: F.body, color: C.textMuted,
      italic: true, align: "center", margin: 0,
    });
  }

  pageNum(slide, num, total);
}

function generateDiagram(pres, data, num, total) {
  const slide = pres.addSlide();
  slide.background = { color: C.ice };
  contentDecor(slide);

  slide.addText(data.title.toUpperCase(), {
    x: L.ml, y: L.titleY, w: L.contentW, h: L.titleH,
    fontSize: 22, fontFace: F.heading, color: C.navy,
    bold: true, align: "left", valign: "middle", margin: 0,
  });

  // 占位区域
  slide.addShape("rect", {
    x: 2, y: 1.5, w: 6, h: 3.2,
    fill: { color: C.white },
    line: { color: C.accent, width: 1, dashType: "dash" },
  });

  slide.addShape("oval", {
    x: 4.65, y: 2.4, w: 0.7, h: 0.7,
    fill: { color: C.iceDark, transparency: 50 },
  });
  slide.addText("📊", {
    x: 4.65, y: 2.4, w: 0.7, h: 0.7,
    fontSize: 28, align: "center", valign: "middle", margin: 0,
  });

  slide.addText([
    { text: "在 PowerPoint 中插入 Mermaid 图表", options: { breakLine: true, fontSize: 12, color: C.textMuted, bold: true } },
    { text: "推荐插件: Mermaid for PowerPoint / 截图粘贴", options: { fontSize: 9, color: C.textMuted } },
  ], {
    x: 2, y: 3.25, w: 6, h: 1, align: "center", valign: "top",
  });

  pageNum(slide, num, total);
}

async function generateComparison(pres, data, num, total, getIcon) {
  const slide = pres.addSlide();
  slide.background = { color: C.ice };
  contentDecor(slide);

  slide.addText(data.title.toUpperCase(), {
    x: L.ml, y: L.titleY, w: L.contentW, h: L.titleH,
    fontSize: 22, fontFace: F.heading, color: C.navy,
    bold: true, align: "left", valign: "middle", margin: 0,
  });

  const panelW = 3.8;
  const panelH = 3.0;
  const panelY = 1.3;
  const leftX = L.ml;
  const rightX = L.ml + panelW + 1.1;
  const midX = leftX + panelW + 0.32;

  // ─── 左侧面板 ───
  const lAccent = data.leftSide.accent === "negative" ? C.accentRed : C.navy;
  slide.addShape("rect", {
    x: leftX, y: panelY, w: panelW, h: panelH,
    fill: { color: C.white }, shadow: makeCardShadow(),
  });
  // 顶部色条
  slide.addShape("rect", {
    x: leftX, y: panelY, w: panelW, h: 0.08,
    fill: { color: lAccent },
  });
  // 标签
  slide.addText(data.leftSide.label.toUpperCase(), {
    x: leftX + 0.2, y: panelY + 0.2, w: panelW - 0.4, h: 0.35,
    fontSize: 12, fontFace: F.heading, color: lAccent,
    bold: true, align: "left", valign: "middle", margin: 0,
  });
  // 列表
  slide.addText(
    data.leftSide.items.map((item, i) => ({
      text: `▸  ${item}`,
      options: {
        breakLine: i < data.leftSide.items.length - 1,
        fontSize: 11, fontFace: F.body, color: C.text,
        paraSpaceAfter: 8,
      },
    })),
    { x: leftX + 0.2, y: panelY + 0.65, w: panelW - 0.4, h: panelH - 0.75, valign: "top", margin: [0, 0, 0, 6] }
  );

  // ─── 中间箭头 ───
  slide.addShape("oval", {
    x: midX, y: panelY + panelH / 2 - 0.25, w: 0.5, h: 0.5,
    fill: { color: C.accent },
    shadow: makeCardShadow(),
  });

  try {
    const arrowData = await getIcon(FaArrowRight, "#FFFFFF", 64);
    slide.addImage({ data: arrowData, x: midX + 0.09, y: panelY + panelH / 2 - 0.16, w: 0.32, h: 0.32 });
  } catch (_) {
    slide.addText("→", {
      x: midX, y: panelY + panelH / 2 - 0.25, w: 0.5, h: 0.5,
      fontSize: 18, fontFace: F.body, color: C.white,
      bold: true, align: "center", valign: "middle", margin: 0,
    });
  }

  // ─── 右侧面板 ───
  const rAccent = data.rightSide.accent === "negative" ? C.accentRed : C.accentGreen;
  slide.addShape("rect", {
    x: rightX, y: panelY, w: panelW, h: panelH,
    fill: { color: C.white }, shadow: makeCardShadow(),
  });
  slide.addShape("rect", {
    x: rightX, y: panelY, w: panelW, h: 0.08,
    fill: { color: rAccent },
  });
  slide.addText(data.rightSide.label.toUpperCase(), {
    x: rightX + 0.2, y: panelY + 0.2, w: panelW - 0.4, h: 0.35,
    fontSize: 12, fontFace: F.heading, color: rAccent,
    bold: true, align: "left", valign: "middle", margin: 0,
  });
  slide.addText(
    data.rightSide.items.map((item, i) => ({
      text: `▸  ${item}`,
      options: {
        breakLine: i < data.rightSide.items.length - 1,
        fontSize: 11, fontFace: F.body, color: C.text,
        paraSpaceAfter: 8,
      },
    })),
    { x: rightX + 0.2, y: panelY + 0.65, w: panelW - 0.4, h: panelH - 0.75, valign: "top", margin: [0, 0, 0, 6] }
  );

  // ─── 结论 ───
  if (data.verdict) {
    slide.addShape("rect", {
      x: L.ml, y: panelY + panelH + 0.12, w: L.contentW, h: 0.4,
      fill: { color: C.thesisBg },
    });
    slide.addShape("rect", {
      x: L.ml, y: panelY + panelH + 0.12, w: 0.06, h: 0.4,
      fill: { color: C.accent },
    });
    slide.addText(data.verdict, {
      x: L.ml + 0.2, y: panelY + panelH + 0.12, w: L.contentW - 0.25, h: 0.4,
      fontSize: 12, fontFace: F.body, color: C.navy, bold: true,
      align: "left", valign: "middle", margin: 0,
    });
  }

  pageNum(slide, num, total);
}

async function generateQA(pres, data, num, total, getIcon) {
  const slide = pres.addSlide();
  slide.background = { color: C.ice };

  // 标题（居中）
  slide.addText(data.isEndQA ? "Q & A" : "预期问答".toUpperCase(), {
    x: L.ml, y: 0.4, w: L.contentW, h: 0.6,
    fontSize: 28, fontFace: F.heading, color: C.navy,
    bold: true, align: "center", valign: "middle", margin: 0,
  });

  // 金色分割线
  slide.addShape("line", {
    x: 4.0, y: 1.05, w: 2, h: 0,
    line: { color: C.accent, width: 2 },
  });

  const questions = data.questions;
  const qaH = Math.min(0.9, 3.2 / questions.length);
  const qaGap = 0.08;
  const qaY = 1.25;

  try {
    const qIconData = await getIcon(FaQuestionCircle, "#1E2761", 64);
    const aIconData = await getIcon(FaComments, "#F59E0B", 64);

    for (let i = 0; i < questions.length; i++) {
      const qa = questions[i];
      const cy = qaY + i * (qaH + qaGap);

      slide.addShape("rect", {
        x: 1.5, y: cy, w: 7, h: qaH,
        fill: { color: C.white }, shadow: makeCardShadow(),
      });

      // Q icon
      slide.addImage({ data: qIconData, x: 1.65, y: cy + 0.12, w: 0.28, h: 0.28 });

      slide.addText([
        { text: qa.question, options: { breakLine: true, bold: true, fontSize: 12, color: C.navy } },
        { text: `→ ${qa.answerDirection}`, options: { fontSize: 10, color: C.textMuted } },
      ], {
        x: 2.05, y: cy, w: 6.2, h: qaH,
        fontFace: F.body, align: "left", valign: "middle", margin: [6, 6, 6, 6],
      });
    }
  } catch (_) {
    // 无图标降级
    for (let i = 0; i < questions.length; i++) {
      const qa = questions[i];
      const cy = qaY + i * (qaH + qaGap);

      slide.addShape("rect", {
        x: 1.5, y: cy, w: 7, h: qaH,
        fill: { color: C.white }, shadow: makeCardShadow(),
      });
      slide.addText([
        { text: `Q: ${qa.question}`, options: { breakLine: true, bold: true, fontSize: 12, color: C.navy } },
        { text: `→ ${qa.answerDirection}`, options: { fontSize: 10, color: C.textMuted } },
      ], {
        x: 1.7, y: cy, w: 6.6, h: qaH,
        fontFace: F.body, align: "left", valign: "middle", margin: [6, 6, 6, 6],
      });
    }
  }

  pageNum(slide, num, total);
}

async function generateEnd(pres, data, num, total, getIcon) {
  const slide = pres.addSlide();
  darkBgDecor(slide);

  // 左侧金色条
  slide.addShape("rect", {
    x: 0, y: 0, w: 0.1, h: 5.625,
    fill: { color: C.accent },
  });

  // 中央金色分割线
  slide.addShape("line", {
    x: 3.8, y: 2.4, w: 2.4, h: 0,
    line: { color: C.accent, width: 2.5 },
  });

  // 结束语
  slide.addText((data.message || "谢谢").toUpperCase(), {
    x: 1, y: 2.6, w: 8, h: 1,
    fontSize: 36, fontFace: F.heading, color: C.white,
    bold: true, align: "center", valign: "middle", margin: 0,
  });

  // 联系方式
  if (data.contactInfo) {
    slide.addText(data.contactInfo, {
      x: 1, y: 3.6, w: 8, h: 0.5,
      fontSize: 14, fontFace: F.body, color: C.iceDark,
      align: "center", valign: "middle", margin: 0,
    });
  }

  // 底部图标
  try {
    const starData = await getIcon(FaStar, "#F59E0B", 64);
    slide.addImage({ data: starData, x: 4.7, y: 4.25, w: 0.4, h: 0.4, transparency: 60 });
  } catch (_) {}

  pageNum(slide, num, total, "64748B");
}

// ─── 主入口 ──────────────────────────────────────────────

async function main() {
  if (!process.argv[2]) {
    console.log("用法: node generate-pptx.cjs <schema.json> [output.pptx]");
    process.exit(1);
  }
  console.log("📄 读取 Schema:", SCHEMA_PATH);
  const schema = JSON.parse(fs.readFileSync(SCHEMA_PATH, "utf-8"));
  const { meta, slides } = schema;
  const total = slides.length;

  const pres = new pptxgen();
  pres.layout = "LAYOUT_16x9";
  pres.author = meta.speaker;
  pres.title = meta.title;
  pres.subject = meta.subtitle || "";

  const getIcon = iconCache();

  console.log(`🎨 主题: Midnight Executive 深蓝金`);
  console.log(`📊 共 ${total} 张幻灯片，开始生成...\n`);

  for (let i = 0; i < slides.length; i++) {
    const data = slides[i];
    const n = i + 1;
    process.stdout.write(`  [${n}/${total}] ${data.type}... `);

    try {
      switch (data.type) {
        case "cover":
          await generateCover(pres, meta, getIcon);
          break;
        case "section":
          await generateSection(pres, data, n, total, getIcon);
          break;
        case "content":
          await generateContent(pres, data, n, total, getIcon);
          break;
        case "agenda":
          await generateAgenda(pres, data, n, total, getIcon);
          break;
        case "quote":
          await generateQuote(pres, data, n, total, getIcon);
          break;
        case "table":
          generateTable(pres, data, n, total);
          break;
        case "diagram":
          generateDiagram(pres, data, n, total);
          break;
        case "comparison":
          await generateComparison(pres, data, n, total, getIcon);
          break;
        case "qa":
          await generateQA(pres, data, n, total, getIcon);
          break;
        case "end":
          await generateEnd(pres, data, n, total, getIcon);
          break;
        default:
          process.stdout.write("⏭ 跳过\n");
          continue;
      }
      console.log("✅");
    } catch (err) {
      console.log(`❌ ${err.message}`);
    }
  }

  await pres.writeFile({ fileName: OUTPUT_PATH });
  console.log(`\n✅ 生成完成: ${OUTPUT_PATH}`);
  console.log(`   共 ${total} 张幻灯片`);
  console.log(`   主题: Midnight Executive 深蓝金`);
  console.log(`   可在 PowerPoint / Keynote / WPS 中打开编辑`);
}

main().catch((err) => {
  console.error("\n❌ 致命错误:", err.message);
  process.exit(1);
});