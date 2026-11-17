// extract/primitives/text.js — 文字叶子基元(runs/行高/对齐/竖排)
// 红线①②⑥的提取半:行高记录绝对 px 值(渲染侧转 spcPts 磅值),flex 子级不拍平。
// 增强:①background-clip:text 渐变文字转 capture(连文字一起截图);
//      ②rgba 半透明文字与背景色自动混合为不透明 hex;
//      ③font-weight:500 + 大间距(letter-spacing ≥ 3.2px) 智能降级为粗体;
//      ④run 级富样式:italic/underline/strike/hyperlink/fontFace(2026-07-27 P0);
//      ⑤text-transform 按计算样式逐 run 变换文本(2026-07-27 P0)。
(() => {
  const ns = (window.__htmlSlides = window.__htmlSlides || {});
  ns.primitives = ns.primitives || {};

  // 把 rgba(r,g,b,a) 与背景色混合为不透明 hex。
  // 例外:接近纯白的颜色(亮度 > 250)混合后人眼无法区分,直接返回 FFFFFF,
  // 避免与历史基线(旧转换器对 rgba 直接取不透明)产生差异。
  function blendWithBackground(el, r, g, b, a) {
    if (a >= 1) return ns.rgb(`rgb(${r},${g},${b})`);
    // 近白色(亮度>250 且饱和度<10)直接返回白色,保持与旧基线一致
    const max = Math.max(r, g, b), min = Math.min(r, g, b);
    if (max > 250 && (max - min) < 10) return { hex: "FFFFFF" };
    // 向上找第一个非透明背景色作为混合底色
    let bg = { r: 5, g: 7, b: 15 }; // 兜底:#05070f(与项目常用深色一致)
    let el_ = el;
    while (el_ && el_ !== document.documentElement) {
      const bgc = getComputedStyle(el_).backgroundColor;
      if (bgc && bgc !== "rgba(0, 0, 0, 0)" && bgc !== "transparent") {
        const m = bgc.match(/rgba?\(([^)]+)\)/);
        if (m) {
          const parts = m[1].split(",").map(Number);
          if (parts.length >= 3) {
            bg = { r: parts[0], g: parts[1], b: parts[2] };
            break;
          }
        }
      }
      el_ = el_.parentElement;
    }
    const mix = (fg, bgc) => Math.round(a * fg + (1 - a) * bgc);
    const hex = (v) => v.toString(16).padStart(2, "0");
    return { hex: `#${hex(mix(r, bg.r))}${hex(mix(g, bg.g))}${hex(mix(b, bg.b))}` };
  }

  // 从渐变色中提取第一个色停作为纯色 hex。如 linear-gradient(135deg,#64d2ff,#5e5ce6) → 64D2FF
  function gradientFirstColor(el) {
    const bg = getComputedStyle(el).backgroundImage;
    if (!bg || bg === "none") return null;
    const m = bg.match(/#[0-9a-fA-F]{3,6}/);
    if (!m) return null;
    let h = m[0].substring(1);
    if (h.length === 3) h = h.split("").map(c => c + c).join("");
    return h.toUpperCase();
  }
  function extractColor(el, cs) {
    const m = cs.color.match(/rgba?\(([^)]+)\)/);
    if (m) {
      const parts = m[1].split(",").map(Number);
      if (parts.length >= 4) return blendWithBackground(el, parts[0], parts[1], parts[2], parts[3]);
      if (parts.length >= 3) return ns.rgb(cs.color);
    }
    return ns.rgb(cs.color);
  }

  // 判断是否为粗体(支持 font-weight:500 + 大间距智能降级)
  function isBold(cs, cfg) {
    const fw = parseInt(cs.fontWeight, 10);
    if (fw >= cfg.boldThreshold) return true;
    // 500 + 大间距(≥3.2px):Keynote 风格中用作"加粗强调"的替代
    if (fw === 500) {
      const ls = parseFloat(cs.letterSpacing) || 0;
      if (ls >= 3.2) return true;
    }
    return false;
  }

  // 字体栈首族(与渲染侧 fontMap 的键空间一致)
  function firstFamily(ff) {
    return (ff || "").split(",")[0].replace(/["']/g, "").trim();
  }

  // text-transform 逐 run 变换。capitalize 按 Unicode 词边界首字母大写(近似 CSS);
  // full-width/full-size-kana 罕用,不处理(原样输出)。
  function applyTransform(t, mode) {
    if (!mode || mode === "none") return t;
    if (mode === "uppercase") return t.toUpperCase();
    if (mode === "lowercase") return t.toLowerCase();
    if (mode === "capitalize") return t.replace(/(^|\s)(\p{L})/gu, (m, ws, ch) => ws + ch.toUpperCase());
    return t;
  }

  ns.primitives.textLeaf = {
    name: "text",
    // 文字叶子判定:没有块级子元素 且 有文字
    applies(el, cs, cfg) {
      return !ns.hasBlockChild(el, cs, cfg) && el.textContent.trim() !== "";
    },

    emit(el, cs, rect, collector, cfg) {
      // ① background-clip:text 渐变文字:检测子元素中的 background-clip:text
      // 情况A:整个 textbox 就是 background-clip:text → 整个转 capture
      const bgClip = (cs.webkitBackgroundClip || cs.backgroundClip || "").toLowerCase();
      if (bgClip === "text") {
        el.setAttribute("data-keep-text", "true");
        collector.push({ kind: "capture", rect, reason: "gradient-text" });
        return;
      }

      // 情况B:textbox 内部有 background-clip:text 的 span → 不再转为 capture,而是提取
      // 渐变色的第一个色停作为纯色 run,保证同一 textbox 内所有文字对齐(避免错位/重叠)。

      const baseColor = extractColor(el, cs) || { hex: cfg.defaultColorHex };
      // 规范化:基线颜色统一为大写 hex(无 #),与 golden 基线格式对齐。
      // 注意:FFFFFE(254,254,254)与 FFFFFF(255,255,255)视为等价——浏览器子像素渲染差异。
      function normColor(c) {
        if (!c || !c.hex) return c;
        let h = c.hex.replace(/^#/, "").toUpperCase();
        // FFFFFE → FFFFFF(浏览器子像素差异,历史基线统一为 FFFFFF)
        if (h === "FFFFFE") h = "FFFFFF";
        return { hex: h };
      }
      const baseColorN = normColor(baseColor) || { hex: cfg.defaultColorHex };
      const baseBold = isBold(cs, cfg);
      const baseSize = Math.round(parseFloat(cs.fontSize));

      // 混合字号行(如 130px 数字 + 44px 单位):浏览器的行盒高度由最大的 run 决定,
      // 无单位 line-height 会作为系数继承到每个 run。div 自身的计算行高(按自身字号算)
      // 不能代表整行 —— 先取后代最大字号,再推算有效行高。
      let maxFontSize = baseSize;
      el.querySelectorAll("*").forEach((n) => {
        const s = parseFloat(getComputedStyle(n).fontSize);
        if (s > maxFontSize) maxFontSize = s;
      });

      // 行高:记录 CSS 计算后的绝对行高(px)。PPTX 用绝对磅值(spcPts)精确还原,
      // 避免百分比行距随替换字体的自然行高漂移。"normal" 时无绝对值 → 交回默认。
      const lhPx = parseFloat(cs.lineHeight); // NaN when "normal"
      const specifiedLh = (el.style.lineHeight || "").trim();
      const unitlessLh = /^[\d.]+$/.test(specifiedLh) ? parseFloat(specifiedLh) : null;
      // 无单位行高:系数 × 最大 run 字号;绝对 px 行高:对所有 run 一致;normal:最大字号 × 1.2
      const effectiveLhPx = unitlessLh ? unitlessLh * maxFontSize : lhPx || maxFontSize * 1.2;
      const lineHeightPx = lhPx ? effectiveLhPx : null;
      const oneLineH = effectiveLhPx;
      // 单行判定按**内容高**而非 border box 高(2026-08-07 修复):
      // rect.h 是 border box,padding 与 border 会把它撑高。胶囊标签
      // (padding:3px 16px + border:1px,line-height 21px)盒高 29px,
      // 29 ≤ 21×1.3(27.3) 为 false → 被判多行 → valign:"top" + wrap:"square",
      // 于是 PPTX 里文字顶对齐、不居中(浏览器与预览截图都正常,只有 PPTX 错)。
      // 扣掉 padding+border 后 content=21px ≤ 27.3 → 正确判为单行。
      // 只影响判定,不动 rect —— 几何输出逐字节不变。
      // ⚠️ 只在**上下 padding 对称**时才扣除。理由:valign:"middle" 是在 border box 内居中,
      // 只有对称 padding 才与浏览器渲染等价。非对称(如 08.html 的 `padding-top:25px`,
      // 盒高 47.4 / 行高 22.4)浏览器把文字压在下半部,若判为单行居中会上移 12.5px —— 反而弄坏。
      const padT = parseFloat(cs.paddingTop) || 0, padB = parseFloat(cs.paddingBottom) || 0;
      const bdT = parseFloat(cs.borderTopWidth) || 0, bdB = parseFloat(cs.borderBottomWidth) || 0;
      const symmetricV = Math.abs(padT - padB) < 0.5 && Math.abs(bdT - bdB) < 0.5;
      const contentH = symmetricV ? rect.h - padT - padB - bdT - bdB : rect.h;
      const isSingleLine = contentH <= oneLineH * cfg.singleLineFactor;

      // 横向内缩到 content box(2026-08-07 修复的另一半):
      // 文字在浏览器里从 content box 左边起排,而 PPTX 的 lIns=0 让它从 border box 左边起排,
      // 于是整体左偏「左 padding + 左边框」。胶囊 padding:0 16px + border:1px → 左偏 17px。
      // 横向无需对称性守卫:文字永远排不进 padding,内缩对 algn 的 l/ctr/r 都与浏览器等价。
      // ⚠️ rect 与 shape 基元共用同一对象引用(walk.js 把它同时传给 shape 与 text),
      //    必须新建对象,直接改会连带改坏已 push 的 shape 几何。
      const padL = parseFloat(cs.paddingLeft) || 0, padR = parseFloat(cs.paddingRight) || 0;
      const bdL = parseFloat(cs.borderLeftWidth) || 0, bdR = parseFloat(cs.borderRightWidth) || 0;
      const insetH = padL + padR + bdL + bdR;
      // 居中 + 左右对称 padding 时,在 border box 内居中与在 content box 内居中**视觉等价**,
      // 内缩纯属基线扰动 → 跳过。其余情况(左/右对齐,或非对称 padding)内缩才是必需的。
      const centeredAndSymmetric =
        (cs.textAlign === "center" || (cs.display.includes("flex") && cs.justifyContent === "center")) &&
        Math.abs(padL - padR) < 0.5 && Math.abs(bdL - bdR) < 0.5;
      if (insetH > 0 && rect.w - insetH > 1 && !centeredAndSymmetric) {
        rect = { x: rect.x + padL + bdL, y: rect.y, w: rect.w - insetH, h: rect.h };
      }

      // 递归收集 runs,保留 span 颜色/粗细/斜体/下划线/删除线/超链接/字体 和 <br> 换行。
      // text-decoration 不由 getComputedStyle 继承(视觉上却沿祖先传播),
      // 因此 underline/strike 沿递归链手动累积;<u>/<s>/<del> 等标签的 UA 样式在元素自身
      // 计算样式上体现,累积逻辑天然覆盖。
      // 新样式键只在非默认时写入 run(italic/underline/strike/link/fontFace),
      // 保证不含这些写法的旧页面 L1 基线零 diff。
      const runs = [];
      const boxFontFace = firstFamily(cs.fontFamily);
      const boxLetterSpacing = parseFloat(cs.letterSpacing) || 0;
      const mkRun = (text, st) => {
        const r = { text, color: st.color, bold: st.bold, size: st.size };
        if (st.italic) r.italic = true;
        if (st.underline) r.underline = true;
        if (st.strike) r.strike = true;
        if (st.link) r.link = st.link;
        if (st.fontFace && st.fontFace !== boxFontFace) r.fontFace = st.fontFace;
        // 2026-07-27 P2 2.3:上下标 + run 级字距(条件写入,旧页零 diff)
        if (st.sup) r.sup = true;
        if (st.sub) r.sub = true;
        if (st.charSpacing && st.charSpacing !== boxLetterSpacing) r.charSpacing = st.charSpacing;
        return r;
      };
      function collect(node, inherited) {
        node.childNodes.forEach((n) => {
          if (n.nodeType === 3) {
            // pre/code 等保留空白(2026-07-27 P1):white-space:pre/pre-wrap 不折叠
            const pws = n.parentElement ? getComputedStyle(n.parentElement).whiteSpace : "";
            const pre = pws && pws.startsWith("pre");
            const raw = pre ? n.textContent : n.textContent.replace(/\s+/g, " ");
            if (raw.trim() !== "" || raw === " ")
              runs.push(mkRun(applyTransform(raw, inherited.transform), inherited));
          } else if (n.nodeType === 1) {
            if (n.tagName === "BR") {
              if (runs.length) runs[runs.length - 1].breakLine = true;
              return;
            }
            const s = getComputedStyle(n);
            const dl = (s.textDecorationLine || "").toLowerCase();
            // 2026-07-27 P2 2.3:上下标检测(SUP/SUB 标签 或 vertical-align:super/sub)
            const va = (s.verticalAlign || "").toLowerCase();
            const isSup = n.tagName === "SUP" || va === "super";
            const isSub = n.tagName === "SUB" || va === "sub";
            const next = {
              color: inherited.color,
              bold: isBold(s, cfg),
              size: Math.round(parseFloat(s.fontSize)),
              italic: inherited.italic || s.fontStyle === "italic" || s.fontStyle === "oblique",
              underline: inherited.underline || dl.includes("underline"),
              strike: inherited.strike || dl.includes("line-through"),
              link: n.tagName === "A" && n.getAttribute("href") ? n.getAttribute("href") : inherited.link,
              fontFace: firstFamily(s.fontFamily) || inherited.fontFace,
              transform: s.textTransform !== "none" ? s.textTransform : inherited.transform,
              sup: inherited.sup || isSup,
              sub: inherited.sub || isSub,
              charSpacing: parseFloat(s.letterSpacing) || 0,
            };
            // background-clip:text 的 span:提取渐变第一个色停作为纯色 run,保持同一 textbox 内对齐
            const nClip = (s.webkitBackgroundClip || s.backgroundClip || "").toLowerCase();
            if (nClip === "text") {
              const gradColor = gradientFirstColor(n);
              collect(n, { ...next, color: gradColor || "0A84FF" });
              return;
            }
            const nodeColor = extractColor(n, s);
            collect(n, {
              ...next,
              color: nodeColor ? nodeColor.hex.replace(/^#/, "").toUpperCase() : inherited.color,
            });
          }
        });
      }
      const baseDl = (cs.textDecorationLine || "").toLowerCase();
      const baseVa = (cs.verticalAlign || "").toLowerCase();
      collect(el, {
        color: baseColorN.hex,
        bold: baseBold,
        size: baseSize,
        italic: cs.fontStyle === "italic" || cs.fontStyle === "oblique",
        underline: baseDl.includes("underline"),
        strike: baseDl.includes("line-through"),
        link: el.tagName === "A" && el.getAttribute("href") ? el.getAttribute("href") : null,
        fontFace: boxFontFace,
        transform: cs.textTransform !== "none" ? cs.textTransform : null,
        sup: el.tagName === "SUP" || baseVa === "super",
        sub: el.tagName === "SUB" || baseVa === "sub",
        charSpacing: boxLetterSpacing,
      });

      // 对齐/竖排推断
      let align = cs.textAlign;
      if (["", "start", "normal"].includes(align)) align = "left";
      if (cs.display.includes("flex")) {
        if (cs.justifyContent === "center") align = "center";
        if (cs.justifyContent === "flex-end") align = "right";
      }
      // 垂直对齐:flex 居中 / 单行盒子(常用于固定高度徽章) → middle,多行 → top
      const flexMiddle = cs.display.includes("flex") && cs.alignItems === "center";
      const valign = flexMiddle || isSingleLine ? "middle" : "top";

      // 列表项(2026-07-27 P1;2026-08-05 H11 修复):LI 直接含文字 → 首个实质 run 挂原生 bullet
      // UL → 圆点(U+2022);OL → 阿拉伯数字;嵌套层数 → 缩进。文字位置近似(详见 html-spec)
      // ⚠️ pptxgenjs 序列化是 type 优先:bullet.type 存在且非 "number" 时 characterCode 分支永不执行
      //   (旧写法 {type:"bullet",characterCode} → 永远不产 buChar,PPTX 无项目符号,实测 H11)。
      //   UL 不写 type;OL 用 {type:"number", style} —— style 才是 buAutoNum 的字段名(numberType 无效)。
      if (el.tagName === "LI") {
        const isOl = el.parentElement && el.parentElement.tagName === "OL";
        const bullet = isOl
          ? { type: "number", style: "arabicPeriod", indent: 14 }
          : { characterCode: "2022", indent: 14 };
        const firstReal = runs.find((r) => r.text && r.text.trim() !== "");
        if (firstReal) firstReal.bullet = bullet;
        else if (runs[0]) runs[0].bullet = bullet;
      }

      // 纯旋转:仅当 walk 已按"无背景"路径换成未旋转几何时附着(与 walk 判定同源:
      // 渐变/图片背景元素走截图包围盒,文字再旋转会二次错位 —— 那种组合不支持)
      const rotForText = ns.rotationOf(cs);
      const hasBgImg = cs.backgroundImage && cs.backgroundImage !== "none";

      collector.push({
        kind: "text",
        rect,
        runs,
        align,
        valign,
        letterSpacing: parseFloat(cs.letterSpacing) || 0,
        lineHeightPx, // 绝对行高(px),渲染侧转 spcPts 绝对磅值
        singleLine: isSingleLine,
        vertical: cs.writingMode.startsWith("vertical"),
        fontFace: cs.fontFamily.split(",")[0].replace(/["']/g, "").trim(),
        ...(rotForText && !hasBgImg ? { rotate: rotForText } : {}),
      });
    },
  };
})();
