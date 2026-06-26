/**
 * Browser-injected DOM analyzer for extract_slides.js.
 * Defines window.__extractSlideData() — runs in Puppeteer page context.
 */
(function () {
  window.__extractSlideData = function () {
    const VW = document.documentElement.scrollWidth || 1280;
    const VH = document.documentElement.scrollHeight || 720;
    const regions = [];
    const elementsToHide = [];

    const { SKIP_TAGS, INLINE_TAGS } = window.__pptLib.K;
    const { toHexAlpha: parseColorWithAlpha } = window.__pptLib.color;
    const T = window.__pptLib.text;
    const {
      isDecorativeElement, isBlockLevel, getAllVisibleText,
      hasGradientFill, parseGradientStops, resolveGradientFromComputed,
      resolveTextColor, resolveActualFont, buildRunsForBlock,
      containsArrowChar, extractArrowDirection, hasCssBullet,
      rgbToHex, pxToPt,
    } = T;
    
    function collectLeafBlocks(el) {
      if (!el || !el.tagName) return;
      if (SKIP_TAGS.has(el.tagName)) return;
    
      const style = window.getComputedStyle(el);
      if (style.display === "none" || style.visibility === "hidden" || parseFloat(style.opacity) === 0) return;
      if (isDecorativeElement(el)) return;
    
      const isBlock = isBlockLevel(style);
      const text = getAllVisibleText(el).trim();
    
      if (isBlock && text) {
        const rect = el.getBoundingClientRect();
        if (rect.width < 3 || rect.height < 3) return;
        if (rect.right < 0 || rect.bottom < 0) return;
        if (rect.left > VW || rect.top > VH) return;
    
        // Check if any direct block child has text — if so, recurse instead.
        // flex/grid containers "blockify" inline children (CSS Display L3 §2.5).
        const parentIsFlex = style.display === "flex" || style.display === "inline-flex"
          || style.display === "grid" || style.display === "inline-grid";
        let hasBlockChildWithText = false;
        for (const child of el.children) {
          if (SKIP_TAGS.has(child.tagName)) continue;
          const cs2 = window.getComputedStyle(child);
          if (cs2.display === "none" || cs2.visibility === "hidden") continue;
          if (isBlockLevel(cs2) && getAllVisibleText(child).trim()) {
            if (parentIsFlex && INLINE_TAGS.has(child.tagName)) {
              const childRole = (child.getAttribute("data-pptx-role") || "").toLowerCase();
              if (childRole === "content" || childRole === "content-icon") {
                // Explicitly tagged content should not be skipped
              } else {
                const childBg = cs2.backgroundColor || "";
                const hasOwnBg = childBg && childBg !== "rgba(0, 0, 0, 0)"
                  && childBg !== "transparent" && childBg !== "color(srgb 0 0 0 / 0)";
                if (!hasOwnBg) continue;
              }
            }
            hasBlockChildWithText = true;
            break;
          }
        }
    
        if (hasBlockChildWithText) {
          // Mixed content: block element has both block children AND direct
          // text nodes / inline child elements. Extract them as separate
          // regions before recursing into block children.
          for (const cnode of el.childNodes) {
            if (cnode.nodeType === 3) {
              const raw = cnode.textContent.trim();
              if (!raw) continue;
              const rng = document.createRange();
              rng.selectNodeContents(cnode);
              const rects = rng.getClientRects();
              if (!rects.length) continue;
              let minX = Infinity, minY = Infinity, maxX = -Infinity, maxY = -Infinity;
              for (const r of rects) {
                if (r.width < 1) continue;
                minX = Math.min(minX, r.left);
                minY = Math.min(minY, r.top);
                maxX = Math.max(maxX, r.right);
                maxY = Math.max(maxY, r.bottom);
              }
              if (!isFinite(minX)) continue;
              const tnFontSize = parseFloat(style.fontSize) || 16;
              const tnFontWeight = parseInt(style.fontWeight) || 400;
              const tnColor = resolveTextColor(el, style);
              let tnAlpha = null;
              if (tnColor.alpha < 0.999) tnAlpha = Math.round(tnColor.alpha * 100000);
              const tnFamily = resolveActualFont(style.fontFamily, tnFontSize);
              let tnAlign = "left";
              if (style.textAlign === "center") tnAlign = "center";
              else if (style.textAlign === "right") tnAlign = "right";
              const tnW = maxX - minX;
              const tnH = maxY - minY;
              elementsToHide.push(el);
              regions.push({
                text: raw,
                x: Math.max(0, minX), y: Math.max(0, minY),
                w: tnW, h: tnH,
                lineCount: 1, maxLineWidth: tnW,
                fontSizePx: tnFontSize,
                fontSizePt: pxToPt(tnFontSize),
                fontFamily: tnFamily,
                lineHeightRatio: parseFloat(style.lineHeight) / tnFontSize || 1.2,
                letterSpacingEm: parseFloat(style.letterSpacing) / tnFontSize || 0,
                color: tnColor.hex, colorAlpha: tnAlpha,
                opacity: null,
                bold: tnFontWeight >= 600, italic: style.fontStyle === "italic",
                textTransform: style.textTransform !== "none" ? style.textTransform : null,
                align: tnAlign, vAlign: "top",
                arrowDirection: null, gradient: null,
                shadow: null, glow: null, outline: null, runs: null,
              });
              continue;
            }
            if (cnode.nodeType !== 1) continue;
            if (SKIP_TAGS.has(cnode.tagName)) continue;
            if (isDecorativeElement(cnode)) continue;
            const inCs = window.getComputedStyle(cnode);
            if (inCs.display === "none" || inCs.visibility === "hidden") continue;
            if (isBlockLevel(inCs)) continue;
            const inText = getAllVisibleText(cnode).trim();
            if (!inText) continue;
            const inRect = cnode.getBoundingClientRect();
            if (inRect.width < 2 || inRect.height < 2) continue;
            const inFontSize = parseFloat(inCs.fontSize) || 16;
            const inFontWeight = parseInt(inCs.fontWeight) || 400;
            const inColor = resolveTextColor(cnode, inCs);
            let inAlpha = null;
            if (inColor.alpha < 0.999) inAlpha = Math.round(inColor.alpha * 100000);
            const inFamily = resolveActualFont(inCs.fontFamily, inFontSize);
            let inAlign = "left";
            if (inCs.textAlign === "center") inAlign = "center";
            else if (inCs.textAlign === "right") inAlign = "right";
            elementsToHide.push(cnode);
            regions.push({
              text: inText,
              x: Math.max(0, inRect.left), y: Math.max(0, inRect.top),
              w: inRect.width, h: inRect.height,
              lineCount: 1, maxLineWidth: inRect.width,
              fontSizePx: inFontSize,
              fontSizePt: pxToPt(inFontSize),
              fontFamily: inFamily,
              lineHeightRatio: parseFloat(inCs.lineHeight) / inFontSize || 1.2,
              letterSpacingEm: parseFloat(inCs.letterSpacing) / inFontSize || 0,
              color: inColor.hex, colorAlpha: inAlpha,
              opacity: null,
              bold: inFontWeight >= 600, italic: inCs.fontStyle === "italic",
              textTransform: inCs.textTransform !== "none" ? inCs.textTransform : null,
              align: inAlign, vAlign: "top",
              arrowDirection: null, gradient: null,
              shadow: null, glow: null, outline: null, runs: null,
            });
          }
        }
    
        if (!hasBlockChildWithText) {
          const fontSize = parseFloat(style.fontSize) || 16;
          const fontWeight = parseInt(style.fontWeight) || 400;
          const fontFamily = resolveActualFont(style.fontFamily, fontSize);
    
          let align = "left";
          if (style.textAlign === "center") align = "center";
          else if (style.textAlign === "right") align = "right";
    
          const isGradient = hasGradientFill(el, style);
          let gradient = null;
          if (isGradient) {
            gradient = resolveGradientFromComputed(el);
            if (!gradient) gradient = parseGradientStops(el, style);
          }
    
          let textColor = "FFFFFF";
          let textColorAlpha = null;
          if (!isGradient) {
            const colorObj = resolveTextColor(el, style);
            textColor = colorObj.hex;
            if (colorObj.alpha < 0.999) textColorAlpha = Math.round(colorObj.alpha * 100000);
          }
    
          let shadow = null;
          let glow = null;
          const rawShadow = style.textShadow;
          if (rawShadow && rawShadow !== "none") {
            const sm = rawShadow.match(/rgba?\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)(?:\s*,\s*([\d.]+))?\)\s+([-\d.]+)px\s+([-\d.]+)px\s+([\d.]+)px/);
            if (sm) {
              const sColor = [sm[1], sm[2], sm[3]].map(v => parseInt(v).toString(16).padStart(2, "0")).join("").toUpperCase();
              const sAlpha = sm[4] !== undefined ? Math.round(parseFloat(sm[4]) * 100000) : 100000;
              const ox = parseFloat(sm[5]);
              const oy = parseFloat(sm[6]);
              const blur = parseFloat(sm[7]);
    
              if (Math.abs(ox) < 0.5 && Math.abs(oy) < 0.5 && blur > 0) {
                glow = { radiusPx: blur, color: sColor, alpha: sAlpha };
              } else {
                shadow = { offsetX: ox, offsetY: oy, blurPx: blur, color: sColor, alpha: sAlpha };
              }
            }
          }
    
          if (!shadow && !glow) {
            const rawFilter = style.filter || style.webkitFilter || "";
            const dsRe = /drop-shadow\(\s*rgba?\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)(?:\s*,\s*([\d.]+))?\)\s+([-\d.]+)px\s+([-\d.]+)px\s+([\d.]+)px\s*\)/gi;
            const dsMatches = [...rawFilter.matchAll(dsRe)];
            for (const dm of dsMatches) {
              const dsColor = [dm[1], dm[2], dm[3]].map(v => parseInt(v).toString(16).padStart(2, "0")).join("").toUpperCase();
              const dsAlpha = dm[4] !== undefined ? Math.round(parseFloat(dm[4]) * 100000) : 100000;
              const ox = parseFloat(dm[5]);
              const oy = parseFloat(dm[6]);
              const blur = parseFloat(dm[7]);
    
              if (Math.abs(ox) < 0.5 && Math.abs(oy) < 0.5 && blur > 0 && !glow) {
                glow = { radiusPx: blur, color: dsColor, alpha: dsAlpha };
              } else if (!shadow) {
                shadow = { offsetX: ox, offsetY: oy, blurPx: blur, color: dsColor, alpha: dsAlpha };
              }
            }
          }
    
          let outline = null;
          const strokeW = parseFloat(style.webkitTextStrokeWidth) || 0;
          if (strokeW > 0) {
            const strokeColor = rgbToHex(style.webkitTextStrokeColor);
            if (strokeColor) {
              outline = { widthPx: strokeW, color: strokeColor };
            }
          }
    
          let runs = null;
          if (!isGradient) {
            runs = buildRunsForBlock(el);
          }
    
          let arrowDir = null;
          if (containsArrowChar(text)) {
            arrowDir = extractArrowDirection(text);
          }
    
          let vAlign = "top";
          const dp = style.display;
          const ai = style.alignItems;
          if (dp === "flex" || dp === "inline-flex" || dp === "grid" || dp === "inline-grid") {
            if (ai === "center") vAlign = "middle";
            else if (ai === "flex-end" || ai === "end") vAlign = "bottom";
          }
    
          const textTransform = style.textTransform;
    
          const range = document.createRange();
          range.selectNodeContents(el);
          const lineRects = range.getClientRects();
          const uniqueLines = [];
          for (const lr of lineRects) {
            if (lr.width < 2 || lr.height < 2) continue;
            const existing = uniqueLines.find(u => Math.abs(u.top - lr.top) < fontSize * 0.3);
            if (existing) {
              existing.right = Math.max(existing.right, lr.right);
              existing.left = Math.min(existing.left, lr.left);
            } else {
              uniqueLines.push({ top: lr.top, left: lr.left, right: lr.right });
            }
          }
    
          let lineCount = Math.max(1, uniqueLines.length);
          let maxLineWidth = rect.width;
          if (uniqueLines.length > 1) {
            let maxLW = 0;
            for (const line of uniqueLines) {
              const lw = line.right - line.left;
              if (lw > maxLW) maxLW = lw;
            }
            maxLineWidth = maxLW;
          } else if (uniqueLines.length === 1) {
            maxLineWidth = uniqueLines[0].right - uniqueLines[0].left;
          }
    
          let compositeOpacity = 1;
          let opNode = el;
          while (opNode && opNode !== document.body) {
            const opStyle = window.getComputedStyle(opNode);
            const opVal = parseFloat(opStyle.opacity);
            if (!isNaN(opVal)) compositeOpacity *= opVal;
            opNode = opNode.parentElement;
          }
          compositeOpacity = Math.round(compositeOpacity * 1000) / 1000;
    
          const bullet = hasCssBullet(el);
          const finalText = bullet ? (bullet + " " + text) : text;
    
          elementsToHide.push(el);
          regions.push({
            text: finalText,
            x: Math.max(0, rect.left),
            y: Math.max(0, rect.top),
            w: rect.width,
            h: rect.height,
            lineCount,
            maxLineWidth,
            fontSizePx: fontSize,
            fontSizePt: pxToPt(fontSize),
            fontFamily,
            lineHeightRatio: parseFloat(style.lineHeight) / fontSize || 1.2,
            letterSpacingEm: parseFloat(style.letterSpacing) / fontSize || 0,
            color: textColor,
            colorAlpha: textColorAlpha,
            opacity: compositeOpacity < 0.999 ? compositeOpacity : null,
            bold: fontWeight >= 600,
            italic: style.fontStyle === "italic",
            textTransform: textTransform !== "none" ? textTransform : null,
            align,
            vAlign,
            arrowDirection: arrowDir,
            gradient,
            shadow,
            glow,
            outline,
            runs,
          });
          return;
        }
      }
    
      for (const child of el.children) {
        collectLeafBlocks(child);
      }
    }
    
    collectLeafBlocks(document.body);
    
    // --- Shape extraction: border boxes, lines, separators ---
    const shapeRegions = [];
    
    function collectDecoShapes(el) {
      if (!el || !el.tagName) return;
      if (SKIP_TAGS.has(el.tagName)) return;
    
      const style = window.getComputedStyle(el);
      if (style.display === "none" || style.visibility === "hidden") return;
    
      const role = (el.getAttribute("data-pptx-role") || "").toLowerCase();
      if (role === "content-icon") return;
      const rect = el.getBoundingClientRect();
    
      if (rect.width < 5 || rect.height < 5) {
        for (const child of el.children) collectDecoShapes(child);
        return;
      }
      if (rect.right < 0 || rect.bottom < 0 || rect.left > VW || rect.top > VH) return;
    
      const bTop = parseFloat(style.borderTopWidth) || 0;
      const bRight = parseFloat(style.borderRightWidth) || 0;
      const bBottom = parseFloat(style.borderBottomWidth) || 0;
      const bLeft = parseFloat(style.borderLeftWidth) || 0;
      const borderSides = [bTop, bRight, bBottom, bLeft].filter(b => b > 0.5).length;
      const hasBorder = borderSides >= 3 && (bTop + bRight + bBottom + bLeft) > 1.5;
      const borderRadius = parseFloat(style.borderRadius) || 0;
    
      const isHR = el.tagName === "HR";
      const bgStr = style.backgroundColor || "";
      const bgImg = style.backgroundImage || "";
      const bgClip = style.backgroundClip || style.webkitBackgroundClip || "";
      const isTextGradient = bgClip === "text" || bgClip === "-webkit-text";
      const hasVisibleBG = (bgStr && bgStr !== "rgba(0, 0, 0, 0)"
        && bgStr !== "transparent" && bgStr !== "color(srgb 0 0 0 / 0)")
        || (bgImg && bgImg !== "none" && !isTextGradient);
      const hasDoubleBorder = borderSides >= 2 && (bTop + bRight + bBottom + bLeft) > 1;
      const isCardLike = hasBorder || hasDoubleBorder || (hasVisibleBG && borderRadius > 0);
      const isBigEnough = rect.width >= 40 && rect.height >= 20;
      const isDecoRole = role === "decoration" || role === "watermark";
      const isContentRole = role === "content";
      const hasVisualAppearance = isCardLike || hasVisibleBG;
      const shouldExtract = isDecoRole
        ? false
        : isContentRole
          ? hasVisualAppearance
          : (isCardLike && isBigEnough);
    
      if (shouldExtract || isHR) {
        // Pick border color from the side that actually has width.
        // PPTX shapes have uniform borders; when only one side is styled
        // (e.g. border-left accent bar), using borderTopColor yields a
        // wrong default color. Ref: CSS borderXColor spec.
        const sides = [
          { w: bTop,    color: style.borderTopColor },
          { w: bRight,  color: style.borderRightColor },
          { w: bBottom, color: style.borderBottomColor },
          { w: bLeft,   color: style.borderLeftColor },
        ];
        const activeSides = sides.filter(s => s.w > 0.5);
        const thickest = activeSides.length > 0
          ? activeSides.reduce((a, b) => b.w > a.w ? b : a)
          : { w: 0, color: style.borderTopColor || "" };
        const rawBorderColor = thickest.color || style.borderTopColor || "";
        const borderParsed = parseColorWithAlpha(rawBorderColor);
        const borderColor = borderParsed.hex || "FFFFFF";
        const borderAlpha = borderParsed.alpha;
    
        const bgParsed = parseColorWithAlpha(style.backgroundColor);
        const bgColor = bgParsed.hex;
        const bgOpacity = parseFloat(style.opacity) || 1;
        const bgAlpha = bgParsed.alpha;

        // Detect single-side accent border (e.g. border-left: 3px solid yellow)
        // PPTX cannot model per-side borders. Emit the main shape without border,
        // plus a separate narrow rectangle for the accent stripe.
        const isSingleSideAccent = borderSides === 1 && thickest.w >= 2;
    
        const shape = {
          type: borderRadius >= 4 ? "roundedRect" : "rect",
          role: role || null,
          x: Math.max(0, rect.left),
          y: Math.max(0, rect.top),
          w: rect.width,
          h: rect.height,
          borderWidthPx: isSingleSideAccent ? 0 : Math.max(bTop, bRight, bBottom, bLeft),
          borderColor: isSingleSideAccent ? "000000" : borderColor,
          borderAlpha: isSingleSideAccent ? 0 : Math.round(borderAlpha * 100000),
          borderRadius: borderRadius,
        };
    
        if (bgColor && bgAlpha > 0.01) {
          shape.fillColor = bgColor;
          shape.fillAlpha = Math.round(bgAlpha * bgOpacity * 100000);
        } else if (bgImg && bgImg !== "none" && bgImg.includes("gradient")) {
          const gradColors = bgImg.match(/rgba?\(\s*\d+\s*,\s*\d+\s*,\s*\d+(?:\s*,\s*[\d.]+)?\s*\)/g)
            || bgImg.match(/color\(\s*srgb\s+[\d.]+\s+[\d.]+\s+[\d.]+(?:\s*\/\s*[\d.]+)?\s*\)/g);
          if (gradColors && gradColors.length >= 1) {
            const parsed = parseColorWithAlpha(gradColors[0]);
            if (parsed.hex) {
              shape.fillColor = parsed.hex;
              shape.fillAlpha = Math.round(parsed.alpha * bgOpacity * 100000);
              shape.gradientStops = gradColors.map(c => {
                const p = parseColorWithAlpha(c);
                return { hex: p.hex, alpha: p.alpha };
              });
            }
          }
        }
    
        if (isHR || (rect.height < 4 && rect.width > 20)) {
          shape.type = "line";
        }
    
        const innerText = getAllVisibleText(el).trim();
        if (innerText && innerText.length <= 8 && role !== "content") {
          const cs = window.getComputedStyle(el);
          const colorObj = resolveTextColor(el, cs);
          shape.shapeText = innerText;
          shape.textColor = colorObj.hex;
          shape.textColorAlpha = colorObj.alpha < 0.999 ? Math.round(colorObj.alpha * 100000) : null;
          shape.textSizePx = parseFloat(cs.fontSize) || 14;
          shape.textSizePt = pxToPt(shape.textSizePx);
          shape.textBold = (parseInt(cs.fontWeight) || 400) >= 600;
          shape.textAlign = "center";
        }

        shapeRegions.push(shape);

        if (isSingleSideAccent) {
          const accentParsed = parseColorWithAlpha(thickest.color);
          const accentW = thickest.w;
          const accent = {
            type: "rect",
            borderWidthPx: 0, borderColor: "000000", borderAlpha: 0,
            borderRadius: 0,
            fillColor: accentParsed.hex || borderColor,
            fillAlpha: Math.round((accentParsed.alpha || 1) * bgOpacity * 100000),
          };
          if (bLeft > 0.5 && bRight < 0.5 && bTop < 0.5 && bBottom < 0.5) {
            accent.x = Math.max(0, rect.left);
            accent.y = Math.max(0, rect.top);
            accent.w = accentW;
            accent.h = rect.height;
          } else if (bRight > 0.5 && bLeft < 0.5 && bTop < 0.5 && bBottom < 0.5) {
            accent.x = Math.max(0, rect.right - accentW);
            accent.y = Math.max(0, rect.top);
            accent.w = accentW;
            accent.h = rect.height;
          } else if (bTop > 0.5 && bBottom < 0.5 && bLeft < 0.5 && bRight < 0.5) {
            accent.x = Math.max(0, rect.left);
            accent.y = Math.max(0, rect.top);
            accent.w = rect.width;
            accent.h = accentW;
          } else if (bBottom > 0.5 && bTop < 0.5 && bLeft < 0.5 && bRight < 0.5) {
            accent.x = Math.max(0, rect.left);
            accent.y = Math.max(0, rect.bottom - accentW);
            accent.w = rect.width;
            accent.h = accentW;
          }
          if (accent.x !== undefined) {
            shapeRegions.push(accent);
          }
        }
    
        el.style.setProperty("border", "none", "important");
        el.style.setProperty("outline", "none", "important");
        if (shape.fillColor || (bgImg !== "none" && !isTextGradient)) {
          el.style.setProperty("background-color", "transparent", "important");
          el.style.setProperty("background-image", "none", "important");
          el.style.setProperty("box-shadow", "none", "important");
          el.style.setProperty("backdrop-filter", "none", "important");
          el.style.setProperty("-webkit-backdrop-filter", "none", "important");
        }
      }
    
      for (const child of el.children) {
        collectDecoShapes(child);
      }
    }
    
    collectDecoShapes(document.body);

    // Table extraction delegated to table-extractor.js (window.__pptLib.table)
    const tableRegions = window.__pptLib.table.extractTables();

    function hideTextElement(node) {
      node.style.setProperty("color", "transparent", "important");
      node.style.setProperty("-webkit-text-fill-color", "transparent", "important");
      node.style.setProperty("text-shadow", "none", "important");
      node.style.setProperty("-webkit-text-stroke", "0", "important");
      node.style.setProperty("filter", "none", "important");
      const cs = window.getComputedStyle(node);
      if (cs.backgroundClip === "text" || cs.webkitBackgroundClip === "text") {
        node.style.setProperty("background", "none", "important");
        node.style.setProperty("-webkit-background-clip", "border-box", "important");
        node.style.setProperty("background-clip", "border-box", "important");
      }
    }
    
    for (const el of elementsToHide) {
      hideTextElement(el);
      for (const child of el.querySelectorAll("*")) hideTextElement(child);
    }
    
    const rootStyle = window.getComputedStyle(document.documentElement);
    const cssVarPalette = {};
    const varNames = ["--bg-primary", "--bg-secondary", "--bg-card",
      "--accent-1", "--accent-2", "--accent-3",
      "--text-primary", "--text-secondary", "--text-dim"];
    for (const v of varNames) {
      const val = rootStyle.getPropertyValue(v).trim();
      if (val) cssVarPalette[v] = val;
    }
    
    // SVG style inlining delegated to svg-utils.js (window.__pptLib.svg)
    const { inlineSvgStyles } = window.__pptLib.svg;
    
    const svgExtracts = [];
    const iconSet = new Set(document.querySelectorAll('[data-pptx-role="content-icon"]'));
    const iconElements = Array.from(iconSet);
    for (const iconEl of iconElements) {
      let rect = iconEl.getBoundingClientRect();
      const text = iconEl.textContent.trim();
      const hasEmoji = /[\u{1F300}-\u{1F9FF}\u{2600}-\u{26FF}\u{2700}-\u{27BF}]/u.test(text);
      const svgChild = iconEl.querySelector("svg");
      const hasSVG = svgChild !== null;
      const isSVG = iconEl.tagName === "SVG" || iconEl.tagName === "svg";
      const hasImg = iconEl.querySelector("img") !== null;
      // CSS-only graphics (conic-gradient donut, radial-gradient dial, etc.)
      // are visual decorations even without SVG/img children.
      // When a conic-gradient is found, parse its stops into chartData
      // so assemble_pptx.py can emit a native PPTX doughnut chart.
      let hasCssGraphic = false;
      let chartData = null;
      const parseConic = (bgStr) => {
        // Extract conic-gradient body with nested parentheses support.
        // getComputedStyle returns resolved values like:
        //   conic-gradient(rgb(251, 191, 36) 0%, rgb(251, 191, 36) 72%, ...)
        const idx0 = bgStr.indexOf("conic-gradient(");
        if (idx0 < 0) return null;
        let depth = 0, start = idx0 + "conic-gradient".length, end = start;
        for (let ci = start; ci < bgStr.length; ci++) {
          if (bgStr[ci] === "(") depth++;
          else if (bgStr[ci] === ")") { depth--; if (depth === 0) { end = ci; break; } }
        }
        const body = bgStr.slice(start + 1, end);
        // Split by top-level commas (not inside parentheses)
        const parts = [];
        let part = "", pd = 0;
        for (let ci = 0; ci < body.length; ci++) {
          if (body[ci] === "(") pd++;
          else if (body[ci] === ")") pd--;
          if (body[ci] === "," && pd === 0) { parts.push(part.trim()); part = ""; }
          else part += body[ci];
        }
        if (part.trim()) parts.push(part.trim());
        // Parse each color stop: "rgba(...) 0% 72%" or "rgb(...) 72%"
        const stops = [];
        for (const p of parts) {
          const pctMatches = [...p.matchAll(/([\d.]+)%/g)].map(mm => parseFloat(mm[1]));
          const colorPart = p.replace(/([\d.]+)%/g, "").trim();
          if (pctMatches.length >= 1 && colorPart) {
            stops.push({ color: colorPart, p1: pctMatches[0], p2: pctMatches.length > 1 ? pctMatches[1] : null });
          }
        }
        if (stops.length < 2) return null;
        const segments = [];
        for (let i = 0; i < stops.length; i++) {
          const sStart = stops[i].p1;
          const sEnd = stops[i].p2 !== null ? stops[i].p2 : (i + 1 < stops.length ? stops[i + 1].p1 : 100);
          const pct = sEnd - sStart;
          if (pct > 0) {
            let rawColor = stops[i].color;
            if (rawColor.startsWith("var(")) {
              const varName = rawColor.replace(/var\(|\)/g, "").trim();
              rawColor = getComputedStyle(document.documentElement).getPropertyValue(varName).trim();
            }
            segments.push({ pct, color: rawColor });
          }
        }
        return segments.length >= 1 ? segments : null;
      };
      let chartRect = null;
      (() => {
        const checkAndParse = (el) => {
          const cs = window.getComputedStyle(el);
          const bg = cs.backgroundImage || "";
          if (/conic-gradient/.test(bg) && bg !== "none") {
            const segs = parseConic(bg);
            if (segs) {
              chartData = { type: "doughnut", segments: segs };
              const cr = el.getBoundingClientRect();
              chartRect = { x: cr.left, y: cr.top, w: cr.width, h: cr.height };
            }
            const mask = cs.webkitMask || cs.mask || "";
            if (/radial-gradient/.test(mask)) {
              const holeM = mask.match(/([\d.]+)px/);
              if (holeM && chartData) {
                const holeRadius = parseFloat(holeM[1]);
                const outerRadius = Math.min(el.getBoundingClientRect().width, el.getBoundingClientRect().height) / 2;
                chartData.holePct = Math.round((holeRadius / outerRadius) * 100);
              }
            }
            return true;
          }
          // Only conic-gradient triggers extraction (data charts).
          // Pure radial-gradient is decorative and stays in the background.
          return false;
        };
        if (checkAndParse(iconEl)) { hasCssGraphic = true; return; }
        for (const child of iconEl.querySelectorAll("*")) {
          if (checkAndParse(child)) { hasCssGraphic = true; return; }
        }
      })();
      const isVisual = hasEmoji || hasSVG || isSVG || hasImg || hasCssGraphic;
    
      if (rect.width < 10 || rect.height < 10) continue;
      if (rect.x + rect.width < 0 || rect.y + rect.height < 0) continue;
      if (rect.x > VW || rect.y > VH) continue;

      // When a container wraps a single SVG that is smaller than the
      // container (e.g. absolutely-positioned narrow SVG in a wider wrapper),
      // store the SVG's actual bbox to avoid stretching in PPTX.
      let svgActualRect = null;
      if (hasSVG && !isSVG) {
        const svgRect = svgChild.getBoundingClientRect();
        if (svgRect.width > 0 && svgRect.height > 0 &&
            (svgRect.width < rect.width * 0.7 || svgRect.height < rect.height * 0.7)) {
          svgActualRect = { x: svgRect.left, y: svgRect.top, w: svgRect.width, h: svgRect.height };
        }
      }
    
      let svgMarkup = null;
      if (isSVG || hasSVG) {
        const targetSvg = isSVG ? iconEl : svgChild;
        inlineSvgStyles(targetSvg);
        const NON_SVG_PROPS = [
          "color", "-webkit-text-fill-color", "text-shadow",
          "-webkit-text-stroke", "-webkit-text-stroke-width",
          "-webkit-text-stroke-color", "filter",
        ];
        function cleanSvgElement(el) {
          for (const p of NON_SVG_PROPS) el.style.removeProperty(p);
        }
        cleanSvgElement(targetSvg);
        for (const c of targetSvg.querySelectorAll("*")) cleanSvgElement(c);
        svgMarkup = targetSvg.outerHTML;
      }
    
      const cs = window.getComputedStyle(iconEl);
      const bgColor = cs.backgroundColor;
      const borderColor = cs.borderColor;
      const borderWidth = parseFloat(cs.borderWidth) || 0;
      const borderRadius = cs.borderRadius;
      const isCircular = borderRadius && (borderRadius === "50%" || parseFloat(borderRadius) >= Math.min(rect.width, rect.height) / 2 - 1);
      const csBgImg = cs.backgroundImage || "";
      const hasCssBg = bgColor && bgColor !== "rgba(0, 0, 0, 0)" && bgColor !== "transparent";
      const hasCssGradient = csBgImg && csBgImg !== "none" && csBgImg.includes("gradient");
      let containerStyle = null;
      if (hasCssBg || hasCssGradient) {
        let effectiveBg = bgColor;
        if (!hasCssBg && hasCssGradient) {
          const gradMatch = csBgImg.match(/rgba?\(\s*\d+\s*,\s*\d+\s*,\s*\d+(?:\s*,\s*[\d.]+)?\s*\)/g)
            || csBgImg.match(/color\(\s*srgb\s+[\d.]+\s+[\d.]+\s+[\d.]+(?:\s*\/\s*[\d.]+)?\s*\)/g);
          effectiveBg = gradMatch ? gradMatch[0] : "rgba(128,128,128,0.5)";
        }
        containerStyle = {
          bgColor: effectiveBg,
          borderColor: borderWidth > 0 ? borderColor : null,
          borderWidth,
          isCircular: !!isCircular,
          w: rect.width,
          h: rect.height,
        };
      }

      const svgIdx = svgExtracts.length;
      iconEl.setAttribute("data-svg-idx", String(svgIdx));
      let textStyle = null;
      if (text && !hasSVG && !isSVG && !hasImg) {
        const { resolveTextColor, pxToPt } = window.__pptLib.text;
        const textCs = window.getComputedStyle(iconEl);
        const colorObj = resolveTextColor(iconEl, textCs);
        textStyle = {
          color: colorObj.hex,
          colorAlpha: colorObj.alpha,
          sizePt: pxToPt(parseFloat(textCs.fontSize) || 14),
          bold: (parseInt(textCs.fontWeight) || 400) >= 600,
        };
      }

      svgExtracts.push({
        idx: svgIdx,
        x: rect.left, y: rect.top, w: rect.width, h: rect.height,
        isVisual, isSVG: isSVG || hasSVG,
        svgMarkup,
        text: text.slice(0, 10),
        textStyle,
        svgActualRect,
        chartData,
        chartRect,
        containerStyle,
      });
    }
    
    for (const iconEl of iconElements) {
      if (iconEl.hasAttribute("data-svg-idx")) {
        iconEl.setAttribute("data-extract-icon", "1");
        iconEl.style.setProperty("visibility", "hidden", "important");
      }
    }
    
    return { regions, shapeRegions, svgExtracts, tableRegions, viewportW: VW, viewportH: VH, cssVarPalette };
  };
})();
