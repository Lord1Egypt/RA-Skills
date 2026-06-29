#!/usr/bin/env node
/**
 * hanzi-center — 汉字视觉重心分析引擎
 *
 * 从 汉字视觉重心.html 移植到 Node.js，使用 node-canvas 做无头渲染。
 *
 * Usage:
 *   node analyze.js 永
 *   node analyze.js 永 --font=kai --weight=70 --density=60 --slant=40
 *   node analyze.js 永 --json
 *   node analyze.js 永 --compare 重,飞,不
 *   node analyze.js --fonts  列出可用字体
 */

const { createCanvas, registerFont } = require("canvas");
const path = require("path");
const os = require("os");

// ═══════════════════════════════════════════
// Constants
// ═══════════════════════════════════════════
const CANVAS_SIZE = 480;
const FONT_SIZE = 340;
const GRID = 28;
const CELL = CANVAS_SIZE / GRID;

// ═══════════════════════════════════════════
// Font definitions (matching the HTML version)
// ═══════════════════════════════════════════
const FONT_STYLES = [
  {
    key: "kai",
    label: "楷",
    name: "楷书",
    desc: "笔画起收分明，接近手写",
    stack: '"STKaiti","KaiTi","SimKai","Noto Serif SC","Kai",serif',
  },
  {
    key: "song",
    label: "宋",
    name: "宋体",
    desc: "横细竖粗，印刷正体",
    stack: '"STSong","SimSun","Songti SC","Noto Serif SC","NSimSun",serif',
  },
  {
    key: "hei",
    label: "黑",
    name: "黑体",
    desc: "笔画均匀，现代无衬线",
    stack: '"SimHei","STHeiti","Heiti SC","Microsoft YaHei","Noto Sans SC",sans-serif',
  },
  {
    key: "fangsong",
    label: "仿",
    name: "仿宋",
    desc: "楷体骨架，宋体笔形",
    stack: '"FangSong","STFangsong","FangSong_GB2312","Noto Serif SC",serif',
  },
  {
    key: "ming",
    label: "明",
    name: "明体",
    desc: "台湾标准印刷体",
    stack: '"PMingLiU","MingLiU","MingLiU_HKSCS","Noto Serif SC",serif',
  },
  {
    key: "noto",
    label: "思",
    name: "思源宋",
    desc: "Google 开源，跨平台一致",
    stack: '"Noto Serif SC","Source Han Serif SC","Songti SC",serif',
  },
];

// ═══════════════════════════════════════════
// Font registration helpers
// ═══════════════════════════════════════════
function getSystemFontDirs() {
  switch (os.platform()) {
    case "win32":
      return [path.join(process.env.WINDIR || "C:\\Windows", "Fonts")];
    case "darwin":
      return [
        "/System/Library/Fonts",
        "/Library/Fonts",
        path.join(os.homedir(), "Library/Fonts"),
      ];
    default:
      return ["/usr/share/fonts", "/usr/local/share/fonts", path.join(os.homedir(), ".fonts")];
  }
}

/**
 * Try to find and register a font file from the system.
 * node-canvas needs fonts registered explicitly for non-default families.
 * We try common font file names for each style.
 */
const FONT_FILE_MAP = {
  // Windows
  win32: {
    kai: ["STKAITI.TTF", "KaiTi.ttf", "simkai.ttf"],
    song: ["STSONG.TTF", "SimSun.ttc", "SimSun.ttf"],
    hei: ["SIMHEI.TTF", "STHEITI.TTF", "msyh.ttc"],
    fangsong: ["STFANGSO.TTF", "FangSong.ttf", "FangSong_GB2312.ttf"],
    ming: ["PMINGLIU.TTF", "MingLiU.ttc"],
    noto: ["NotoSerifSC-Regular.otf", "NotoSerifCJKsc-Regular.otf"],
  },
  // macOS
  darwin: {
    kai: ["STKaiti.ttc", "Kaiti.ttc"],
    song: ["STSong.ttc", "Songti.ttc"],
    hei: ["STHeiti.ttc", "Heiti.ttc"],
    fangsong: ["STFangsong.ttc"],
    ming: ["PMingLiU.ttf"],
    noto: ["NotoSerifSC-Regular.otf", "NotoSerifCJKsc-Regular.otf"],
  },
  // Linux
  linux: {
    kai: ["STKAITI.TTF", "KaiTi.ttf"],
    song: ["STSONG.TTF", "SimSun.ttf"],
    hei: ["SIMHEI.TTF", "STHEITI.TTF"],
    fangsong: ["STFANGSO.TTF", "FangSong.ttf"],
    ming: ["PMINGLIU.TTF", "MingLiU.ttf"],
    noto: ["NotoSerifSC-Regular.otf", "NotoSerifCJKsc-Regular.otf"],
  },
};

const registeredFonts = new Set();

function ensureFontRegistered(fontKey) {
  if (registeredFonts.has(fontKey)) return true;

  const platform = os.platform();
  const files = (FONT_FILE_MAP[platform] || FONT_FILE_MAP.linux)[fontKey];
  if (!files) return false;

  const fontDirs = getSystemFontDirs();

  for (const dir of fontDirs) {
    for (const file of files) {
      try {
        const fullPath = path.join(dir, file);
        // Check existence via fs
        const fs = require("fs");
        if (fs.existsSync(fullPath)) {
          registerFont(fullPath, { family: FONT_STYLES.find((f) => f.key === fontKey)?.stack.split(",")[0].replace(/["']/g, "") || fontKey });
          registeredFonts.add(fontKey);
          return true;
        }
      } catch (e) {
        // Try next
      }
    }
  }
  // Font not found — will rely on system default
  return false;
}

// ═══════════════════════════════════════════
// Core Analysis (ported from HTML, line 816-987)
// ═══════════════════════════════════════════
function analyzeChar(char, sliders, fontStack) {
  const canvas = createCanvas(CANVAS_SIZE, CANVAS_SIZE);
  const ctx = canvas.getContext("2d");

  ctx.clearRect(0, 0, CANVAS_SIZE, CANVAS_SIZE);
  ctx.fillStyle = "#000000";
  ctx.font = `${FONT_SIZE}px ${fontStack}`;
  ctx.textAlign = "center";
  ctx.textBaseline = "middle";
  ctx.fillText(char, CANVAS_SIZE / 2, CANVAS_SIZE / 2);

  const imageData = ctx.getImageData(0, 0, CANVAS_SIZE, CANVAS_SIZE);
  const pixels = imageData.data;

  // Find bounding box & collect dark pixels
  let minX = CANVAS_SIZE,
    maxX = 0,
    minY = CANVAS_SIZE,
    maxY = 0;
  const darkPixels = [];

  for (let y = 0; y < CANVAS_SIZE; y++) {
    for (let x = 0; x < CANVAS_SIZE; x++) {
      const idx = (y * CANVAS_SIZE + x) * 4;
      const alpha = pixels[idx + 3];
      if (alpha > 60) {
        const darkness = Math.min(alpha / 255, 1);
        const weight = darkness * (1 - pixels[idx] / 255);
        if (x < minX) minX = x;
        if (x > maxX) maxX = x;
        if (y < minY) minY = y;
        if (y > maxY) maxY = y;
        darkPixels.push({ x, y, weight });
      }
    }
  }

  if (darkPixels.length === 0) return null;

  const charWidth = maxX - minX;
  const charHeight = maxY - minY;
  const geoCX = (minX + maxX) / 2;
  const geoCY = (minY + maxY) / 2;

  // 1. Raw centroid (分量)
  let sumW = 0,
    sumWX = 0,
    sumWY = 0;
  for (const p of darkPixels) {
    sumW += p.weight;
    sumWX += p.weight * p.x;
    sumWY += p.weight * p.y;
  }
  const rawCX = sumWX / sumW;
  const rawCY = sumWY / sumW;

  // 2. Density grid (距离 / 中宫收紧)
  const densityGrid = new Float32Array(GRID * GRID);
  for (const p of darkPixels) {
    const gx = Math.min(Math.floor(p.x / CELL), GRID - 1);
    const gy = Math.min(Math.floor(p.y / CELL), GRID - 1);
    densityGrid[gy * GRID + gx] += p.weight;
  }
  let maxDensity = 0;
  for (let i = 0; i < densityGrid.length; i++) {
    if (densityGrid[i] > maxDensity) maxDensity = densityGrid[i];
  }

  // Density-weighted center
  let sumDW = 0,
    sumDWX = 0,
    sumDWY = 0;
  for (const p of darkPixels) {
    const gx = Math.min(Math.floor(p.x / CELL), GRID - 1);
    const gy = Math.min(Math.floor(p.y / CELL), GRID - 1);
    const localD = maxDensity > 0 ? densityGrid[gy * GRID + gx] / maxDensity : 1;
    const dw = p.weight * (1 + localD * 2.0);
    sumDW += dw;
    sumDWX += dw * p.x;
    sumDWY += dw * p.y;
  }
  const densityCX = sumDWX / sumDW;
  const densityCY = sumDWY / sumDW;

  // 3. Slant analysis (斜度) — Sobel-like gradient
  let slantOX = 0,
    slantOY = 0,
    slantN = 0;
  for (let i = 0; i < darkPixels.length; i += 5) {
    const p = darkPixels[i];
    if (p.x <= 1 || p.x >= CANVAS_SIZE - 1 || p.y <= 1 || p.y >= CANVAS_SIZE - 1) continue;

    const iT = ((p.y - 1) * CANVAS_SIZE + p.x) * 4;
    const iB = ((p.y + 1) * CANVAS_SIZE + p.x) * 4;
    const iL = (p.y * CANVAS_SIZE + (p.x - 1)) * 4;
    const iR = (p.y * CANVAS_SIZE + (p.x + 1)) * 4;

    const gx = (pixels[iR] - pixels[iL]) / 2;
    const gy = (pixels[iB] - pixels[iT]) / 2;
    const mag = Math.sqrt(gx * gx + gy * gy);

    if (mag > 3) {
      if (Math.abs(gy) < Math.abs(gx) * 0.7) {
        slantOY += Math.sign(gy) * mag * 0.3;
        slantOX -= Math.sign(gy) * mag * 0.15;
      } else if (Math.abs(gx) < Math.abs(gy) * 0.7) {
        slantOX += Math.sign(gx) * mag * 0.3;
      } else {
        slantOX += Math.sign(gx) * mag * 0.2;
        slantOY -= Math.sign(gy) * mag * 0.2;
      }
      slantN++;
    }
  }
  const avgSlantX = slantN > 0 ? slantOX / slantN : 0;
  const avgSlantY = slantN > 0 ? slantOY / slantN : 0;

  // 4. Apply slider weights
  const wW = sliders.weightFactor / 100;
  const wD = sliders.densityFactor / 100;
  const wS = sliders.slantFactor / 100;

  const blendedCX = rawCX + (densityCX - rawCX) * wW;
  const blendedCY = rawCY + (densityCY - rawCY) * wW;

  const densityShiftX = (densityCX - blendedCX) * wD;
  const densityShiftY = (densityCY - blendedCY) * wD;

  const slantShiftX = avgSlantX * wS;
  const slantShiftY = avgSlantY * wS;

  const upBiasPx = charHeight * (sliders.upBias / 100);
  const rightBiasPx = charWidth * (sliders.rightBias / 100);

  const visualCX = blendedCX + densityShiftX + slantShiftX + rightBiasPx;
  const visualCY = blendedCY + densityShiftY + slantShiftY - upBiasPx;

  // 5. Quadrant distribution
  const quads = { tl: 0, tr: 0, bl: 0, br: 0 };
  for (const p of darkPixels) {
    if (p.x < geoCX) {
      if (p.y < geoCY) quads.tl += p.weight;
      else quads.bl += p.weight;
    } else {
      if (p.y < geoCY) quads.tr += p.weight;
      else quads.br += p.weight;
    }
  }
  const totalQ = quads.tl + quads.tr + quads.bl + quads.br;
  const topPct = (((quads.tl + quads.tr) / totalQ) * 100).toFixed(1);
  const botPct = (((quads.bl + quads.br) / totalQ) * 100).toFixed(1);
  const leftPct = (((quads.tl + quads.bl) / totalQ) * 100).toFixed(1);
  const rightPct = (((quads.tr + quads.br) / totalQ) * 100).toFixed(1);

  // 6. Insight text
  const ox = visualCX - geoCX;
  const oy = visualCY - geoCY;
  let insight = "";
  if (Math.abs(ox) < 5 && Math.abs(oy) < 5) {
    insight = "重心接近几何中心，结构高度对称。可尝试增加「中宫收紧」权重观察变化。";
  } else if (oy < -12 && Math.abs(ox) < 8) {
    insight = '重心显著偏上，符合"上紧下松"的审美传统。启功云："中心部位笔画紧凑，而后向四方扩展，必然好看。"';
  } else if (ox > 10) {
    insight = '重心偏右，符合心理学"先小后大"的节奏感。姜夔《续书谱》谓顺其"真态"自然。';
  } else if (ox < -8) {
    insight = '重心偏左，可能是笔画天然分布使然。如"劉"字左重右轻，顺其自然即是美。';
  } else {
    insight = '重心偏移反映了笔画分布的自然态势。书法追求"不相等的东西获得相等"的杆秤式动态平衡。';
  }

  return {
    char,
    charWidth,
    charHeight,
    geoCX,
    geoCY,
    rawCX,
    rawCY,
    visualCX,
    visualCY,
    pixelCount: darkPixels.length,
    offsetX: ox,
    offsetY: oy,
    topPct,
    botPct,
    leftPct,
    rightPct,
    insight,
    densityGrid,
    maxDensity,
    dotX: ((visualCX - minX) / charWidth) * 80 + 10,
    dotY: ((visualCY - minY) / charHeight) * 80 + 10,
  };
}

// ═══════════════════════════════════════════
// Formatting helpers
// ═══════════════════════════════════════════
function directionLabel(ox, oy) {
  const h = ox > 3 ? "偏右" : ox < -3 ? "偏左" : "居中";
  const v = oy > 3 ? "偏下" : oy < -3 ? "偏上" : "居中";
  return `${h} · ${v}`;
}

function offsetStr(ox, oy) {
  return `${ox > 0 ? "+" : ""}${ox.toFixed(1)}, ${oy > 0 ? "+" : ""}${oy.toFixed(1)}`;
}

// ═══════════════════════════════════════════
// PNG generation — render visualization (like web demo)
// ═══════════════════════════════════════════
function drawVisualPNG(char, result, fontStack, outPath) {
  const fs = require("fs");
  const pad = 40;
  const size = CANVAS_SIZE + pad * 2;
  const canvas = createCanvas(size, size);
  const ctx = canvas.getContext("2d");

  // Paper background
  ctx.fillStyle = "#f7f3ea";
  ctx.fillRect(0, 0, size, size);

  // Grid
  ctx.strokeStyle = "rgba(180,160,120,0.12)";
  ctx.lineWidth = 1;
  const gs = 36;
  for (let x = pad; x <= size - pad; x += gs) {
    ctx.beginPath(); ctx.moveTo(x, pad); ctx.lineTo(x, size - pad); ctx.stroke();
  }
  for (let y = pad; y <= size - pad; y += gs) {
    ctx.beginPath(); ctx.moveTo(pad, y); ctx.lineTo(size - pad, y); ctx.stroke();
  }

  // Character
  ctx.fillStyle = "#1a1a1a";
  ctx.font = `${FONT_SIZE}px ${fontStack}`;
  ctx.textAlign = "center";
  ctx.textBaseline = "middle";
  ctx.fillText(char, size / 2, size / 2);

  const { geoCX, geoCY, rawCX, rawCY, visualCX, visualCY } = result;
  const ox = pad, oy = pad;

  // Geometric center (dashed diamond)
  ctx.strokeStyle = "rgba(0,0,0,0.22)";
  ctx.lineWidth = 1;
  ctx.setLineDash([4, 8]);
  ctx.beginPath();
  const gx = ox + geoCX, gy = oy + geoCY;
  ctx.moveTo(gx - 16, gy); ctx.lineTo(gx + 16, gy);
  ctx.moveTo(gx, gy - 16); ctx.lineTo(gx, gy + 16);
  ctx.stroke();
  ctx.setLineDash([]);
  // Diamond marker
  ctx.fillStyle = "rgba(0,0,0,0.28)";
  ctx.beginPath();
  ctx.moveTo(gx, gy - 5); ctx.lineTo(gx + 5, gy);
  ctx.lineTo(gx, gy + 5); ctx.lineTo(gx - 5, gy);
  ctx.closePath(); ctx.fill();

  // Raw centroid (blue)
  const rx = ox + rawCX, ry = oy + rawCY;
  ctx.fillStyle = "#4a7cc9";
  ctx.beginPath(); ctx.arc(rx, ry, 5, 0, Math.PI * 2); ctx.fill();
  ctx.strokeStyle = "rgba(74,124,201,0.4)";
  ctx.lineWidth = 2;
  ctx.setLineDash([]);
  ctx.beginPath(); ctx.arc(rx, ry, 10, 0, Math.PI * 2); ctx.stroke();

  // Connector line from raw to visual
  const vx = ox + visualCX, vy = oy + visualCY;
  ctx.strokeStyle = "rgba(0,0,0,0.18)";
  ctx.lineWidth = 1;
  ctx.setLineDash([3, 5]);
  ctx.beginPath();
  ctx.moveTo(rx, ry); ctx.lineTo(vx, vy);
  ctx.stroke();
  ctx.setLineDash([]);

  // Visual center glow
  const glow = ctx.createRadialGradient(vx, vy, 5, vx, vy, 20);
  glow.addColorStop(0, "rgba(184,58,31,0.5)");
  glow.addColorStop(0.5, "rgba(184,58,31,0.12)");
  glow.addColorStop(1, "rgba(184,58,31,0)");
  ctx.fillStyle = glow;
  ctx.beginPath(); ctx.arc(vx, vy, 20, 0, Math.PI * 2); ctx.fill();

  // Visual center dot
  ctx.fillStyle = "#b83a1f";
  ctx.beginPath(); ctx.arc(vx, vy, 7, 0, Math.PI * 2); ctx.fill();
  ctx.fillStyle = "#e85535";
  ctx.beginPath(); ctx.arc(vx, vy, 3.5, 0, Math.PI * 2); ctx.fill();

  // Outer ring
  ctx.strokeStyle = "#b83a1f";
  ctx.lineWidth = 2.5;
  ctx.setLineDash([]);
  ctx.beginPath(); ctx.arc(vx, vy, 13, 0, Math.PI * 2); ctx.stroke();

  // Crosshair
  ctx.strokeStyle = "rgba(184,58,31,0.55)";
  ctx.lineWidth = 1.3;
  ctx.beginPath();
  ctx.moveTo(vx - 24, vy); ctx.lineTo(vx + 24, vy);
  ctx.moveTo(vx, vy - 24); ctx.lineTo(vx, vy + 24);
  ctx.stroke();

  // Legend (top-left)
  ctx.fillStyle = "#b83a1f";
  ctx.font = 'bold 14px "Noto Serif SC","KaiTi",serif';
  ctx.textAlign = "left";
  ctx.fillText("视觉重心", 12, 24);
  ctx.fillStyle = "#4a7cc9";
  ctx.fillText("物理质心", 12, 44);
  ctx.fillStyle = "rgba(0,0,0,0.4)";
  ctx.fillText("几何中心", 12, 64);

  // Legend dots
  ctx.fillStyle = "#b83a1f"; ctx.beginPath(); ctx.arc(100, 19, 4, 0, Math.PI * 2); ctx.fill();
  ctx.fillStyle = "#4a7cc9"; ctx.beginPath(); ctx.arc(100, 39, 4, 0, Math.PI * 2); ctx.fill();
  ctx.fillStyle = "rgba(0,0,0,0.28)";
  ctx.beginPath(); ctx.moveTo(98, 59); ctx.lineTo(100, 55); ctx.lineTo(102, 59);
  ctx.lineTo(100, 63); ctx.closePath(); ctx.fill();

  // Info panel (top-right)
  ctx.fillStyle = "#4a3f2f";
  ctx.font = '12px "Noto Serif SC",serif';
  ctx.textAlign = "right";
  const infoX = size - 14;
  ctx.fillText(`${char} · ${result.charWidth}×${result.charHeight}`, infoX, 22);
  ctx.fillText(`偏移: ${result.offsetX > 0 ? "+" : ""}${result.offsetX.toFixed(1)}, ${result.offsetY > 0 ? "+" : ""}${result.offsetY.toFixed(1)}`, infoX, 40);
  ctx.fillText(`上:下 ${result.topPct}:${result.botPct}  左:右 ${result.leftPct}:${result.rightPct}`, infoX, 56);

  const buf = canvas.toBuffer("image/png");
  fs.writeFileSync(outPath, buf);
  return outPath;
}

function formatReport(r, fontName, sliders) {
  const lines = [];
  const w = 48;

  lines.push("┌" + "─".repeat(w) + "┐");
  const title = `${r.char} · ${fontName} · 视觉重心分析`;
  const padL = Math.floor((w - title.length) / 2);
  lines.push("│" + " ".repeat(padL) + title + " ".repeat(w - padL - title.length) + "│");
  lines.push("├" + "─".repeat(w) + "┤");

  const rows = [
    ["字符尺寸", `${r.charWidth} × ${r.charHeight} px`],
    ["笔画像素", r.pixelCount.toLocaleString()],
    ["几何中心", `(${r.geoCX.toFixed(1)}, ${r.geoCY.toFixed(1)})`],
    ["物理质心", `(${r.rawCX.toFixed(1)}, ${r.rawCY.toFixed(1)})`],
    ["视觉重心 🎯", `(${r.visualCX.toFixed(1)}, ${r.visualCY.toFixed(1)})`],
    ["偏移 Δx,Δy", offsetStr(r.offsetX, r.offsetY)],
    ["方向", directionLabel(r.offsetX, r.offsetY)],
    ["上 : 下", `${r.topPct} : ${r.botPct}`],
    ["左 : 右", `${r.leftPct} : ${r.rightPct}`],
  ];

  for (const [key, val] of rows) {
    const line = `│  ${key.padEnd(14)}│  ${val.padEnd(30)}│`;
    lines.push(line);
  }

  lines.push("├" + "─".repeat(w) + "┤");
  // Word-wrap insight
  const insightPrefix = "解读：";
  const maxInsightWidth = w - 4;
  let insightRemaining = insightPrefix + r.insight;
  while (insightRemaining.length > 0) {
    const chunk = insightRemaining.slice(0, maxInsightWidth);
    insightRemaining = insightRemaining.slice(maxInsightWidth);
    lines.push("│  " + chunk + " ".repeat(w - 2 - chunk.length) + "│");
  }

  // Parameter summary
  lines.push("├" + "─".repeat(w) + "┤");
  lines.push(
    "│  参数: 分量=" +
      sliders.weightFactor +
      "% 中宫=" +
      sliders.densityFactor +
      "% 斜度=" +
      sliders.slantFactor +
      "%" +
      " ".repeat(Math.max(0, w - 2 - 31)) +
      "│"
  );
  lines.push(
    "│        偏上=" +
      sliders.upBias.toFixed(1) +
      "% 偏右=" +
      sliders.rightBias.toFixed(1) +
      "%" +
      " ".repeat(Math.max(0, w - 2 - 22)) +
      "│"
  );

  lines.push("└" + "─".repeat(w) + "┘");
  return lines.join("\n");
}

// ═══════════════════════════════════════════
// Comparison mode — analyze multiple chars
// ═══════════════════════════════════════════
function analyzeCompare(chars, fontKey, sliders) {
  const fontStyle = FONT_STYLES.find((f) => f.key === fontKey) || FONT_STYLES[0];
  const results = [];

  for (const ch of chars) {
    const r = analyzeChar(ch, { ...sliders }, fontStyle.stack);
    if (r) results.push(r);
  }

  if (results.length === 0) return;

  console.log("\n┌" + "─".repeat(68) + "┐");
  console.log("│  多字对比 · " + fontStyle.name.padEnd(25) + " ".repeat(33) + "│");
  console.log("├" + "─".repeat(68) + "┤");
  console.log("│  字  │ 几何中心       │ 视觉重心       │ 偏移         │ 方向          │");
  console.log("├" + "─".repeat(68) + "┤");

  for (const r of results) {
    const geo = `(${r.geoCX.toFixed(1)}, ${r.geoCY.toFixed(1)})`.padEnd(14);
    const vis = `(${r.visualCX.toFixed(1)}, ${r.visualCY.toFixed(1)})`.padEnd(14);
    const off = offsetStr(r.offsetX, r.offsetY).padEnd(12);
    const dir = directionLabel(r.offsetX, r.offsetY).padEnd(14);
    console.log(`│  ${r.char}   │ ${geo} │ ${vis} │ ${off} │ ${dir} │`);
  }
  console.log("└" + "─".repeat(68) + "┘");
}

// ═══════════════════════════════════════════
// CLI Entry
// ═══════════════════════════════════════════
function parseArgs() {
  const args = process.argv.slice(2);
  const opts = {
    char: null,
    font: "kai",
    weight: 70,
    density: 60,
    slant: 40,
    upBias: 6.0,
    rightBias: 2.5,
    json: false,
    png: true,          // 默认生成图片
    noPng: false,       // --no-png 可关闭
    listFonts: false,
    compare: null,
    help: false,
  };

  // Helper: parse "--key=val" or "--key val"
  function getVal(arg, next) {
    const eq = arg.indexOf("=");
    if (eq !== -1) return arg.slice(eq + 1);
    return next;
  }
  function getKey(arg) {
    const eq = arg.indexOf("=");
    return eq !== -1 ? arg.slice(0, eq) : arg;
  }

  let i = 0;
  while (i < args.length) {
    const a = args[i];
    const k = getKey(a);
    const rawVal = args[i + 1];

    if (k === "--font" || k === "-f") {
      opts.font = getVal(a, rawVal) || "kai";
      if (a.indexOf("=") === -1) i++;
    } else if (k === "--weight" || k === "-w") {
      opts.weight = parseFloat(getVal(a, rawVal)) || 70;
      if (a.indexOf("=") === -1) i++;
    } else if (k === "--density" || k === "-d") {
      opts.density = parseFloat(getVal(a, rawVal)) || 60;
      if (a.indexOf("=") === -1) i++;
    } else if (k === "--slant" || k === "-s") {
      opts.slant = parseFloat(getVal(a, rawVal)) || 40;
      if (a.indexOf("=") === -1) i++;
    } else if (k === "--upbias" || k === "-u") {
      opts.upBias = parseFloat(getVal(a, rawVal)) ?? 6.0;
      if (a.indexOf("=") === -1) i++;
    } else if (k === "--rightbias" || k === "-r") {
      opts.rightBias = parseFloat(getVal(a, rawVal)) ?? 2.5;
      if (a.indexOf("=") === -1) i++;
    } else if (k === "--compare" || k === "-c") {
      opts.compare = (getVal(a, rawVal) || "").split(",").map((s) => s.trim()).filter(Boolean);
      if (a.indexOf("=") === -1) i++;
    } else if (a === "--json" || a === "-j") {
      opts.json = true;
    } else if (a === "--no-png") {
      opts.noPng = true;
      opts.png = false;
    } else if (a === "--png") {
      opts.png = true;
      opts.noPng = false;
    } else if (a === "--fonts") {
      opts.listFonts = true;
    } else if (a === "--help" || a === "-h") {
      opts.help = true;
    } else if (!a.startsWith("-")) {
      if (!opts.char) {
        opts.char = [...a][0];
      }
    }
    i++;
  }

  return opts;
}

function printHelp() {
  console.log(`
汉字视觉重心分析引擎 · hanzi-center

用法:
  node analyze.js <汉字> [选项]

选项:
  -f, --font <key>      字体: kai|song|hei|fangsong|ming|noto (默认: kai)
  -w, --weight <n>      笔画分量权重 0-100 (默认: 70)
  -d, --density <n>     中宫收紧权重 0-100 (默认: 60)
  -s, --slant <n>       斜度影响权重 0-100 (默认: 40)
  -u, --upbias <n>      视觉偏上偏差 0-15 (默认: 6.0)
  -r, --rightbias <n>   视觉偏右偏差 -5-10 (默认: 2.5)
  -c, --compare <字1,字2,字3>  多字对比模式
  -j, --json            输出 JSON 格式
  --png                 生成可视化图片 (默认开启)
  --no-png              不生成图片
  --fonts              列出可用字体
  -h, --help           显示帮助

示例:
  node analyze.js 永
  node analyze.js 永 --font=song --json
  node analyze.js 重 --compare 永,飞,不,中
  node analyze.js 我 --weight=100 --density=80
`);
}

function printFonts() {
  console.log("\n可用字体：");
  console.log("─".repeat(50));
  for (const f of FONT_STYLES) {
    console.log(`  ${f.key.padEnd(10)} ${f.label} · ${f.name.padEnd(8)} ${f.desc}`);
  }
  console.log("\n字体栈会自动 fallback，优先使用系统中安装的字体。");
}

// ═══════════════════════════════════════════
// Main
// ═══════════════════════════════════════════
function main() {
  const opts = parseArgs();

  if (opts.help) {
    printHelp();
    return;
  }

  if (opts.listFonts) {
    printFonts();
    return;
  }

  // Validate font key
  const fontStyle = FONT_STYLES.find((f) => f.key === opts.font);
  if (!fontStyle) {
    console.error(`错误: 未知字体 "${opts.font}"。用 --fonts 查看可用字体。`);
    process.exit(1);
  }

  // Try to register the font for better rendering
  ensureFontRegistered(opts.font);

  // Compare mode
  if (opts.compare && opts.compare.length > 0) {
    const chars = opts.char ? [opts.char, ...opts.compare.slice(0, 4)] : opts.compare.slice(0, 5);
    const sliders = {
      weightFactor: opts.weight,
      densityFactor: opts.density,
      slantFactor: opts.slant,
      upBias: opts.upBias,
      rightBias: opts.rightBias,
    };
    analyzeCompare(chars, opts.font, sliders);
    return;
  }

  // Single character mode
  if (!opts.char) {
    console.error('错误: 请提供一个汉字。例如: node analyze.js 永');
    console.error('使用 --help 查看完整帮助。');
    process.exit(1);
  }

  const sliders = {
    weightFactor: opts.weight,
    densityFactor: opts.density,
    slantFactor: opts.slant,
    upBias: opts.upBias,
    rightBias: opts.rightBias,
  };

  const result = analyzeChar(opts.char, sliders, fontStyle.stack);

  if (!result) {
    console.error(`错误: 无法分析 "${opts.char}"。请确认输入的是有效汉字。`);
    process.exit(1);
  }

  // Text report (skip if JSON only)
  if (!opts.json) {
    console.log(formatReport(result, fontStyle.name, sliders));
  }

  // PNG generation (default on, unless --no-png)
  if (opts.png && !opts.noPng) {
    const pngPath = `hanzi_${opts.char}_${opts.font}.png`;
    drawVisualPNG(opts.char, result, fontStyle.stack, pngPath);
    console.log(`\n📷 可视化图片已保存: ${pngPath}`);
  }

  if (opts.json) {
    console.log(
      JSON.stringify(
        {
          char: result.char,
          font: fontStyle.name,
          fontKey: opts.font,
          charSize: { width: result.charWidth, height: result.charHeight },
          geometricCenter: { x: +result.geoCX.toFixed(1), y: +result.geoCY.toFixed(1) },
          rawCentroid: { x: +result.rawCX.toFixed(1), y: +result.rawCY.toFixed(1) },
          visualCenter: { x: +result.visualCX.toFixed(1), y: +result.visualCY.toFixed(1) },
          offset: { dx: +result.offsetX.toFixed(1), dy: +result.offsetY.toFixed(1) },
          direction: directionLabel(result.offsetX, result.offsetY),
          quadrant: { topPct: +result.topPct, bottomPct: +result.botPct, leftPct: +result.leftPct, rightPct: +result.rightPct },
          pixelCount: result.pixelCount,
          insight: result.insight,
          parameters: sliders,
        },
        null,
        2
      )
    );
  }
}

main();
