// extract/primitives/gradient.js — 原生线性渐变基元(2026-07-27 P2 1.6, D2 已拍板)
// 当 config.nativeGradient === true 时,linear-gradient → 原生可编辑渐变形状;
// 否则(默认)回退到 capture 截图路径(行为不变)。
// 回退条件:radial/conic-gradient、色停含 alpha<1、解析失败 → 返回 false(交由 capture 接管)
(() => {
  const ns = (window.__htmlSlides = window.__htmlSlides || {});
  ns.primitives = ns.primitives || {};

  // 解析 linear-gradient(...) 返回 { angle, stops } 或 null(不可解析)
  // angle: CSS 度数(0=向上,顺时针);stops: [{pos(0-100), color(HEX)}]
  function parseLinearGradient(bgImage) {
    if (!bgImage || bgImage === "none") return null;
    const m = /^linear-gradient\(\s*(.+)\s*\)$/i.exec(bgImage);
    if (!m) return null;
    const inner = m[1];
    // 按逗号分割(但 rgb()/rgba() 内的逗号不算)
    const parts = [];
    let depth = 0, cur = "";
    for (const ch of inner) {
      if (ch === "(") depth++;
      else if (ch === ")") depth--;
      if (ch === "," && depth === 0) { parts.push(cur.trim()); cur = ""; }
      else cur += ch;
    }
    if (cur.trim()) parts.push(cur.trim());
    if (parts.length < 2) return null; // 至少要有一个色停(第一个可能是角度)

    let angle = 180; // CSS 默认:to bottom
    let stopParts = parts;
    const first = parts[0].toLowerCase();
    if (first.endsWith("deg")) {
      angle = parseFloat(first) || 180;
      stopParts = parts.slice(1);
    } else if (first.startsWith("to ")) {
      const dirs = first.replace(/^to\s+/, "").trim().split(/\s+/);
      const dirMap = { top: 0, right: 90, bottom: 180, left: 270 };
      if (dirs.length === 1 && dirMap[dirs[0]] !== undefined) {
        angle = dirMap[dirs[0]];
      } else if (dirs.length === 2) {
        // 对角:to top right = 45, to bottom right = 135, to bottom left = 225, to top left = 315
        const a = dirMap[dirs[0]], b = dirMap[dirs[1]];
        if (a === undefined || b === undefined) return null;
        // 取两个方向的中点(仅正交组合有效)
        if (Math.abs(a - b) === 90 || Math.abs(a - b) === 270) {
          angle = (a + b) / 2;
          if (angle < 0) angle += 360;
          if (angle >= 360) angle -= 360;
        } else return null;
      } else return null;
      stopParts = parts.slice(1);
    }

    if (stopParts.length < 1) return null;

    // 解析色停:每个 part 是 "color [position]"
    const stops = [];
    for (const sp of stopParts) {
      // 提取位置(百分比或 px):取最后一个空格后的内容
      const posMatch = sp.match(/\s+(-?\d+(?:\.\d+)?)(%|px)\s*$/);
      let pos = null;
      let colorPart = sp;
      if (posMatch) {
        const val = parseFloat(posMatch[1]);
        const unit = posMatch[2];
        if (unit === "%") pos = val;
        else if (unit === "px") pos = null; // px 位置暂不支持,按 null 处理(均分)
        colorPart = sp.slice(0, sp.length - posMatch[0].length).trim();
      }

      // 解析颜色:getComputedStyle 会把颜色规范为 rgb()/rgba()
      let color = null;
      let alpha = 1;
      const rgbM = /^rgba?\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*(?:,\s*([\d.]+))?\s*\)$/i.exec(colorPart);
      if (rgbM) {
        const r = parseInt(rgbM[1]), g = parseInt(rgbM[2]), b = parseInt(rgbM[3]);
        color = [r, g, b].map((v) => v.toString(16).padStart(2, "0")).join("").toUpperCase();
        if (rgbM[4] !== undefined) alpha = parseFloat(rgbM[4]);
      } else {
        // hex
        const hexM = /^#?([0-9a-fA-F]{3}|[0-9a-fA-F]{6})$/.exec(colorPart);
        if (hexM) {
          let h = hexM[1];
          if (h.length === 3) h = h.split("").map((c) => c + c).join("");
          color = h.toUpperCase();
        }
      }
      if (!color) return null;       // 颜色不可解析 → 回退
      if (alpha < 1) return null;    // alpha 超集 → 回退(D2 决策:保守,后续可增强)

      stops.push({ pos: pos, color }); // pos 可能为 null,后续补全
    }

    // 补全缺失的位置:全 null → 均匀分布;混合 → 首尾 0/100 + 中间插值
    if (stops.length >= 2) {
      const allNull = stops.every((s) => s.pos === null);
      if (allNull) {
        // 均匀分布(CSS 默认行为):N 个色停 → 0, 100/(N-1), ..., 100
        for (let i = 0; i < stops.length; i++)
          stops[i].pos = (i / (stops.length - 1)) * 100;
      } else {
        if (stops[0].pos === null) stops[0].pos = 0;
        if (stops[stops.length - 1].pos === null) stops[stops.length - 1].pos = 100;
        for (let i = 1; i < stops.length - 1; i++) {
          if (stops[i].pos === null) {
            const prev = stops[i - 1].pos || 0;
            const next = stops[i + 1].pos || 100;
            stops[i].pos = (prev + next) / 2;
          }
        }
      }
    }

    return { angle, stops };
  }

  // CSS 角度 → PPTX a:lin ang(60000ths of degree)
  // CSS: 0=up, 90=right, 180=down, 270=left (顺时针)
  // PPTX: 0=right, 90=down, 180=left, 270=up (顺时针)
  // 转换: pptxDeg = (cssDeg + 270) % 360
  function cssAngleToPptx(cssDeg) {
    return ((cssDeg + 270) % 360) * 60000;
  }

  ns.primitives.gradientBackground = {
    name: "native-gradient",
    emitsShape: true, // 命中后 border-strips 可执行(与非统一边框共存)
    tryEmit(box, cs, rect, collector, cfg) {
      if (!box.bg) return false;
      // 开关关 → 回退到 capture(默认行为)
      if (!cfg || !cfg.nativeGradient) return false;

      const parsed = parseLinearGradient(cs.backgroundImage);
      if (!parsed) return false; // 不可解析/radial/alpha → 回退

      collector.push({
        kind: "gradient",
        shape: box.shapeHint || (box.isRound ? "ellipse" : box.radius > 0 ? "roundRect" : "rect"),
        rect,
        angle: cssAngleToPptx(parsed.angle),
        stops: parsed.stops.map((s) => ({ pos: Math.round(s.pos * 1000), color: s.color })),
        border: box.uniform
          ? {
              hex: box.nonZero[0].color.hex,
              width: box.nonZero[0].w,
              ...(box.nonZero[0].style !== "solid" ? { dash: box.nonZero[0].style } : {}),
            }
          : null,
        radius: box.radius > 0 && !box.isRound ? box.radius : 0,
        shadow: box.shadow,
        ...(box.rotate ? { rotate: box.rotate } : {}),
      });
      return true;
    },
  };
})();
