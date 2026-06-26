/**
 * Text extraction utilities for browser-injected DOM analysis.
 * Helper functions used by collectLeafBlocks in dom-analyzer.js.
 *
 * Exposed on window.__pptLib.text — consumed by dom-analyzer.js.
 *
 * Ref: CSS Display L3 §2.5 (blockification)
 * Ref: CSS Backgrounds §5.11 (background-clip: text)
 */
(function () {
  "use strict";

  const ns = (window.__pptLib = window.__pptLib || {});
  const { SKIP_TAGS, BLOCK_DISPLAYS, INLINE_TAGS, ARROW_CHARS, pxToPt } = ns.K;
  const { toHex: rgbToHex, toHexAlpha: parseColorWithAlpha } = ns.color;

  // ── Element classification ─────────────────────────────────────

  function classifyElement(el) {
    let cur = el;
    while (cur && cur !== document.body) {
      if (cur.getAttribute) {
        const pptxRole = cur.getAttribute("data-pptx-role");
        if (pptxRole === "decoration" || pptxRole === "watermark") return "decoration";
        if (pptxRole === "content-icon") return "content-icon";
        if (pptxRole === "content") return "content";
        if (cur.getAttribute("data-decorative") === "true") return "decoration";
      }
      cur = cur.parentElement;
    }
    return "auto";
  }

  function isDecorativeByHeuristic(el, style) {
    const opacity = parseFloat(style.opacity);
    if (opacity > 0 && opacity <= 0.15) return true;
    const fontSize = parseFloat(style.fontSize) || 16;
    if (fontSize >= 160) return true;
    const blendMode = style.mixBlendMode;
    if (blendMode && blendMode !== "normal") return true;
    return false;
  }

  function containsArrowChar(text) {
    for (const ch of text) {
      if (ARROW_CHARS.has(ch)) return true;
    }
    return false;
  }

  function extractArrowDirection(text) {
    for (const ch of text) {
      if ("\u2191\u21D1\u25B2\u25B3\u2B06".includes(ch)) return "up";
      if ("\u2193\u21D3\u25BC\u25BD\u2B07".includes(ch)) return "down";
      if ("\u2190\u21D0\u25C0\u25C1\u2B05".includes(ch)) return "left";
      if ("\u2192\u21D2\u25B6\u25B7\u27A1".includes(ch)) return "right";
      if ("\u2195\u21D5".includes(ch)) return "updown";
      if ("\u2194\u21D4".includes(ch)) return "leftright";
    }
    return null;
  }

  function isDecorativeElement(el) {
    const classification = classifyElement(el);
    if (classification === "decoration") {
      // Fallback: arrows should be role="content" per prompt rule 8.
      // If LLM mislabels an arrow as decoration, rescue it for text extraction.
      const text = getAllVisibleText(el).trim();
      if (containsArrowChar(text)) return false;
      return true;
    }
    if (classification === "content-icon") return true;
    if (classification === "content") return false;

    const style = window.getComputedStyle(el);

    if (isDecorativeByHeuristic(el, style)) {
      return true;
    }

    return false;
  }

  function isBlockLevel(style) {
    return (
      BLOCK_DISPLAYS.has(style.display) ||
      style.position === "absolute" ||
      style.position === "fixed"
    );
  }

  function getAllVisibleText(el) {
    let text = "";
    for (const child of el.childNodes) {
      if (child.nodeType === Node.TEXT_NODE) {
        text += child.textContent;
      } else if (child.nodeType === Node.ELEMENT_NODE) {
        if (SKIP_TAGS.has(child.tagName)) continue;
        const cs = window.getComputedStyle(child);
        if (cs.display === "none" || cs.visibility === "hidden" || parseFloat(cs.opacity) === 0) continue;
        text += getAllVisibleText(child);
      }
    }
    return text.replace(/\s+/g, " ");
  }

  // ── Gradient parsing ───────────────────────────────────────────

  function hasGradientFill(el, style) {
    return style.backgroundClip === "text" || style.webkitBackgroundClip === "text";
  }

  function parseGradientStops(el, style) {
    const bg = style.backgroundImage || style.background || "";
    const m = bg.match(/linear-gradient\(([^)]+)\)/);
    if (!m) return null;

    const parts = m[1].split(",").map(function (s) { return s.trim(); });
    let angleDeg = 180;
    let colorStart = 0;

    const angleMatch = parts[0].match(/([\d.]+)deg/);
    if (angleMatch) {
      angleDeg = parseFloat(angleMatch[1]);
      colorStart = 1;
    } else if (parts[0].startsWith("to ")) {
      colorStart = 1;
    }

    const stops = [];
    for (let i = colorStart; i < parts.length; i++) {
      const part = parts[i];
      const posMatch = part.match(/([\d.]+)%/);
      const pos = posMatch ? parseInt(parseFloat(posMatch[1]) * 1000) : Math.round((i - colorStart) / Math.max(1, parts.length - colorStart - 1) * 100000);

      let hex = "";
      const hexMatch = part.match(/#([0-9a-fA-F]{3,8})/);
      if (hexMatch) {
        let h = hexMatch[1].toUpperCase();
        if (h.length === 3) h = h[0] + h[0] + h[1] + h[1] + h[2] + h[2];
        hex = h.slice(0, 6);
      } else {
        const rgbMatch = part.match(/rgba?\(([^)]+)\)/);
        if (rgbMatch) {
          const nums = rgbMatch[1].split(",").map(function (s) { return s.trim(); });
          if (nums.length >= 3) {
            hex = [nums[0], nums[1], nums[2]].map(function (v) { return parseInt(v).toString(16).padStart(2, "0"); }).join("").toUpperCase();
          }
        }
      }

      if (!hex) {
        const varMatch = part.match(/var\(([^)]+)\)/);
        if (varMatch) {
          const resolved = window.getComputedStyle(el).getPropertyValue(varMatch[1].split(",")[0].trim()).trim();
          hex = rgbToHex(resolved);
        }
      }

      if (hex) stops.push({ pos: pos, color: hex });
    }

    if (stops.length < 2) return null;
    return { angleDeg: angleDeg, stops: stops };
  }

  function resolveGradientFromComputed(el) {
    const style = window.getComputedStyle(el);
    const bg = style.backgroundImage;
    if (!bg || !bg.includes("linear-gradient")) return null;

    const gradStart = bg.indexOf("linear-gradient(");
    if (gradStart === -1) return null;
    const contentStart = gradStart + "linear-gradient(".length;
    let depth = 1;
    let gradEnd = -1;
    for (let i = contentStart; i < bg.length; i++) {
      if (bg[i] === "(") depth++;
      else if (bg[i] === ")") {
        depth--;
        if (depth === 0) { gradEnd = i; break; }
      }
    }
    if (gradEnd === -1) return null;

    const inner = bg.substring(contentStart, gradEnd);
    let angleDeg = 180;
    const angleMatch = inner.match(/^([\d.]+)deg/);
    if (angleMatch) angleDeg = parseFloat(angleMatch[1]);

    const stopRegex = /rgba?\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)(?:\s*,\s*[\d.]+)?\)\s*(?:([\d.]+)%)?/g;
    const rawStops = [];
    let sm;
    while ((sm = stopRegex.exec(inner)) !== null) {
      const hex = [sm[1], sm[2], sm[3]].map(function (v) { return parseInt(v).toString(16).padStart(2, "0"); }).join("").toUpperCase();
      const hasPos = sm[4] !== undefined;
      const pos = hasPos ? Math.round(parseFloat(sm[4]) * 1000) : -1;
      rawStops.push({ color: hex, pos: pos, hasPos: hasPos });
    }

    if (rawStops.length < 2) return null;

    const stops = rawStops.map(function (s, idx) {
      return {
        color: s.color,
        pos: s.hasPos ? s.pos : Math.round(idx / (rawStops.length - 1) * 100000),
      };
    });

    return { angleDeg: angleDeg, stops: stops };
  }

  // ── Text color / font / runs ───────────────────────────────────

  function resolveTextColor(el, style) {
    const fillColor = style.webkitTextFillColor;
    if (fillColor && fillColor !== "transparent" && fillColor !== "inherit" && fillColor !== "initial" && fillColor !== "currentcolor") {
      const parsed = parseColorWithAlpha(fillColor);
      if (parsed.hex) return parsed;
    }
    const parsed = parseColorWithAlpha(style.color);
    if (parsed.hex) return parsed;
    return { hex: "FFFFFF", alpha: 1 };
  }

  const _fontCache = {};
  const _CJK_FALLBACKS = [
    "Noto Sans CJK SC", "Noto Sans CJK TC", "Noto Sans CJK JP",
    "Source Han Sans SC", "Source Han Sans CN",
    "WenQuanYi Micro Hei", "Droid Sans Fallback",
    "Microsoft YaHei", "PingFang SC", "Hiragino Sans GB",
  ];
  const _LATIN_FALLBACKS = [
    "DejaVu Sans", "Liberation Sans", "Noto Sans", "Arial",
  ];

  function resolveActualFont(cssFontFamily, sizePx) {
    const key = cssFontFamily;
    if (_fontCache[key]) return _fontCache[key];

    const candidates = (cssFontFamily || "").split(",").map(function (f) { return f.trim().replace(/['"]/g, ""); });
    const generic = new Set(["sans-serif", "serif", "monospace", "system-ui", "-apple-system", "cursive", "fantasy", "ui-sans-serif", "ui-serif"]);
    const canvas = document.createElement("canvas");
    const ctx = canvas.getContext("2d");
    const testStr = "ABCDE\u6D4B\u8BD5\u5B57\u4F53012";
    ctx.font = sizePx + 'px "____NoSuchFont9999____"';
    const fallbackW = ctx.measureText(testStr).width;

    function isRealFont(name) {
      ctx.font = sizePx + 'px "' + name + '"';
      return Math.abs(ctx.measureText(testStr).width - fallbackW) > 0.3;
    }

    for (var fi = 0; fi < candidates.length; fi++) {
      var f = candidates[fi];
      if (generic.has(f)) continue;
      if (isRealFont(f)) { _fontCache[key] = f; return f; }
    }

    var probes = _CJK_FALLBACKS.concat(_LATIN_FALLBACKS);
    for (var pi = 0; pi < probes.length; pi++) {
      if (isRealFont(probes[pi])) { _fontCache[key] = probes[pi]; return probes[pi]; }
    }

    _fontCache[key] = "sans-serif";
    return _fontCache[key];
  }

  function collectInlineRuns(el, parentStyle) {
    const elStyle = window.getComputedStyle(el);
    const elIsFlex = elStyle.display === "flex" || elStyle.display === "inline-flex"
      || elStyle.display === "grid" || elStyle.display === "inline-grid";
    const runs = [];
    for (const child of el.childNodes) {
      if (child.nodeType === Node.TEXT_NODE) {
        const t = child.textContent.replace(/\s+/g, " ");
        if (!t || !t.trim()) continue;
        runs.push({ text: t, fromParent: true });
      } else if (child.nodeType === Node.ELEMENT_NODE) {
        if (SKIP_TAGS.has(child.tagName)) continue;
        const cs = window.getComputedStyle(child);
        if (cs.display === "none" || cs.visibility === "hidden" || parseFloat(cs.opacity) === 0) continue;
        if (isBlockLevel(cs) && !(elIsFlex && INLINE_TAGS.has(child.tagName))) continue;
        const childRuns = collectInlineRuns(child, cs);
        for (const cr of childRuns) {
          if (cr.fromParent) {
            const colorObj = resolveTextColor(child, cs);
            const fw = parseInt(cs.fontWeight) || 400;
            const childFs = parseFloat(cs.fontSize) || 16;
            const childFf = resolveActualFont(cs.fontFamily, childFs);
            const entry = {
              text: cr.text,
              color: colorObj.hex,
              bold: fw >= 600,
              italic: cs.fontStyle === "italic",
              fontSizePx: childFs,
              fontSizePt: pxToPt(childFs),
              fontFamily: childFf,
              fromParent: false,
            };
            if (colorObj.alpha < 0.999) entry.colorAlpha = Math.round(colorObj.alpha * 100000);
            runs.push(entry);
          } else {
            runs.push(cr);
          }
        }
      }
    }
    return runs;
  }

  function buildRunsForBlock(el) {
    const parentStyle = window.getComputedStyle(el);
    const parentColorObj = resolveTextColor(el, parentStyle);
    const parentBold = (parseInt(parentStyle.fontWeight) || 400) >= 600;
    const parentItalic = parentStyle.fontStyle === "italic";

    const rawRuns = collectInlineRuns(el, parentStyle);
    const finalRuns = [];

    for (let ri = 0; ri < rawRuns.length; ri++) {
      const r = rawRuns[ri];
      let text = r.text ? r.text.replace(/\s+/g, " ") : "";
      if (!text || !text.trim()) continue;
      if (ri === 0) text = text.trimStart();
      if (ri === rawRuns.length - 1) text = text.trimEnd();
      if (!text) continue;
      if (r.fromParent) {
        const entry = {
          text: text,
          color: parentColorObj.hex,
          bold: parentBold,
          italic: parentItalic,
        };
        if (parentColorObj.alpha < 0.999) entry.colorAlpha = Math.round(parentColorObj.alpha * 100000);
        finalRuns.push(entry);
      } else {
        const entry = {
          text: text,
          color: r.color || parentColorObj.hex,
          bold: r.bold !== undefined ? r.bold : parentBold,
          italic: r.italic !== undefined ? r.italic : parentItalic,
        };
        if (r.colorAlpha !== undefined) entry.colorAlpha = r.colorAlpha;
        else if (!r.color && parentColorObj.alpha < 0.999) entry.colorAlpha = Math.round(parentColorObj.alpha * 100000);
        if (r.fontSizePx) entry.fontSizePx = r.fontSizePx;
        if (r.fontSizePt) entry.fontSizePt = r.fontSizePt;
        if (r.fontFamily) entry.fontFamily = r.fontFamily;
        finalRuns.push(entry);
      }
    }

    if (finalRuns.length === 0) return null;

    const allSame = finalRuns.every(function (r) {
      return r.color === finalRuns[0].color &&
        r.bold === finalRuns[0].bold &&
        r.italic === finalRuns[0].italic &&
        (r.colorAlpha || 100000) === (finalRuns[0].colorAlpha || 100000) &&
        (r.fontSizePx || 0) === (finalRuns[0].fontSizePx || 0);
    });
    if (allSame) return null;

    return finalRuns;
  }

  // ── CSS bullets ────────────────────────────────────────────────

  function hasCssBullet(el) {
    const LI_TAGS = new Set(["LI", "DT", "DD"]);
    if (!LI_TAGS.has(el.tagName)) return null;
    const before = window.getComputedStyle(el, "::before");
    if (!before) return null;
    const cnt = before.content;
    if (cnt === "none" || cnt === "normal") return null;
    const w = parseFloat(before.width);
    const h = parseFloat(before.height);
    if (cnt === '""' || cnt === "''") {
      if (w > 2 && h > 2) return "\u2022";
      return null;
    }
    if (cnt && cnt.length >= 3 && cnt.startsWith('"') && cnt.endsWith('"')) {
      const ch = cnt.slice(1, -1);
      if (ch.length <= 2) return ch;
    }
    return null;
  }

  // ── Export ─────────────────────────────────────────────────────

  ns.text = {
    classifyElement: classifyElement,
    isDecorativeElement: isDecorativeElement,
    isBlockLevel: isBlockLevel,
    getAllVisibleText: getAllVisibleText,
    hasGradientFill: hasGradientFill,
    parseGradientStops: parseGradientStops,
    resolveGradientFromComputed: resolveGradientFromComputed,
    resolveTextColor: resolveTextColor,
    resolveActualFont: resolveActualFont,
    buildRunsForBlock: buildRunsForBlock,
    containsArrowChar: containsArrowChar,
    extractArrowDirection: extractArrowDirection,
    hasCssBullet: hasCssBullet,
    rgbToHex: rgbToHex,
    pxToPt: pxToPt,
  };
})();
