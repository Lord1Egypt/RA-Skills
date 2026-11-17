// extract/context.js — 浏览器端共享工具(注入页面,挂 window.__htmlSlides)
// 迁移自旧 extract.js:rgb 解析、rectOf、盒模型样式分析、遍历判定。行为逐行保持。
(() => {
  const ns = (window.__htmlSlides = window.__htmlSlides || {});

  // getComputedStyle 已把 var()/颜色名都解析成 rgb()/rgba()
  ns.rgb = (s) => {
    const m = /rgba?\(([^)]+)\)/.exec(s || "");
    if (!m) return null;
    const p = m[1].split(",").map((x) => x.trim());
    const [r, g, b] = p.map((n) => parseInt(n, 10));
    const a = p[3] !== undefined ? parseFloat(p[3]) : 1;
    if (a === 0) return null; // 完全透明视作无
    const hex = [r, g, b].map((n) => n.toString(16).padStart(2, "0")).join("").toUpperCase();
    return { hex, alpha: Math.round(a * 100) };
  };

  // 元素相对画布容器的矩形
  ns.rectOf = (base, el) => {
    const r = el.getBoundingClientRect();
    return { x: r.left - base.left, y: r.top - base.top, w: r.width, h: r.height };
  };

  // 盒模型视觉分析:背景/填充/圆角/四边边框/统一性(旧 pushShapeIfVisible 的读取部分)
  ns.analyzeBox = (cs, rect) => {
    const bg = cs.backgroundImage && cs.backgroundImage !== "none";
    // 元素整体透明度 → 折算进填充透明度(红线⑦)
    const op = parseFloat(cs.opacity);
    const opacity = isNaN(op) ? 1 : op;
    const fill0 = ns.rgb(cs.backgroundColor);
    const fill = fill0 ? { hex: fill0.hex, alpha: Math.round(fill0.alpha * opacity) } : null;
    const radius = parseFloat(cs.borderTopLeftRadius) || 0;
    // border-radius:50% 在 CSS 中即椭圆(与宽高比无关),直接映射 ellipse;
    // px 半径达到半高时,只有宽高接近的盒子才是正圆 —— 长方形盒(胶囊/stadium)保持 roundRect
    const pctRound = cs.borderRadius.includes("50%");
    const nearSquare = Math.abs(rect.w - rect.h) <= Math.min(rect.w, rect.h) * 0.2;
    const isRound = pctRound || (radius * 2 >= Math.min(rect.w, rect.h) && nearSquare);

    const sides = [
      { w: parseFloat(cs.borderTopWidth) || 0, color: ns.rgb(cs.borderTopColor), style: cs.borderTopStyle },
      { w: parseFloat(cs.borderRightWidth) || 0, color: ns.rgb(cs.borderRightColor), style: cs.borderRightStyle },
      { w: parseFloat(cs.borderBottomWidth) || 0, color: ns.rgb(cs.borderBottomColor), style: cs.borderBottomStyle },
      { w: parseFloat(cs.borderLeftWidth) || 0, color: ns.rgb(cs.borderLeftColor), style: cs.borderLeftStyle },
    ];
    const nonZero = sides.filter((s) => s.w > 0 && s.color);
    const uniform =
      nonZero.length > 0 &&
      new Set(sides.map((s) => s.w)).size === 1 &&
      new Set(sides.map((s) => (s.color ? s.color.hex : "none"))).size === 1 &&
      // 虚线/点线参与统一性判定(2026-07-27):4 边同宽同色但样式不同 → 非统一 → 逐边还原
      new Set(sides.map((s) => (s.w > 0 ? s.style : "none"))).size === 1;

    return { bg, fill, radius, isRound, sides, nonZero, uniform, shadow: ns.parseShadow(cs.boxShadow) };
  };

  // box-shadow 解析(2026-07-27 P0:从"固定近似"升级为真实值):
  // 取第一个非 inset 层;返回 {angle, distance(px), blur(px), color, opacity(0-1)};
  // 无阴影/全 inset 返回 false(与旧基线 "shadow": false 保持一致,避免全量 L1 diff)。
  // spread 无 pptxgenjs 对应物,忽略(视觉近似);多层阴影只还原第一层。
  ns.parseShadow = (cssShadow) => {
    if (!cssShadow || cssShadow === "none") return false;
    const layers = cssShadow.split(/,(?![^()]*\))/); // 颜色函数内的逗号不分层
    for (const layer of layers) {
      const l = layer.trim();
      if (/(^|\s)inset(\s|$)/.test(l)) continue; // inset 不支持,看下一层
      let rest = l;
      let colorStr = null;
      const cm = l.match(/rgba?\([^)]*\)|#[0-9a-fA-F]{3,8}\b/);
      if (cm) {
        colorStr = cm[0];
        rest = l.replace(cm[0], " ");
      }
      // 计算样式中长度恒为 px:[x, y, blur?, spread?]
      const nums = (rest.match(/-?\d+(?:\.\d+)?px/g) || []).map((v) => parseFloat(v));
      const [x = 0, y = 0, blur = 0] = nums;
      const c = colorStr ? ns.rgb(colorStr) : null;
      return {
        angle: Math.round(((Math.atan2(y, x) * 180) / Math.PI + 360) % 360),
        distance: Math.round(Math.hypot(x, y) * 100) / 100,
        blur,
        color: c ? c.hex : "000000",
        opacity: c ? Math.min(100, c.alpha) / 100 : 0.4,
      };
    }
    return false; // 全是 inset → 不支持
  };

  // transform 旋转角提取(2026-07-27 P0:解禁纯旋转):
  // 返回角度(0-359,顺时针);非纯旋转(缩放/斜切)返回 0 并交由 validate 拦截。
  ns.rotationOf = (cs) => {
    const t = cs.transform;
    if (!t || t === "none") return 0;
    const m = /^matrix\(([^)]+)\)$/.exec(t);
    if (!m) return 0;
    const [a, b, c, d] = m[1].split(",").map((v) => parseFloat(v.trim()));
    const eps = 1e-6;
    // 恒等/纯平移:无视觉旋转
    if (Math.abs(a - 1) < eps && Math.abs(d - 1) < eps && Math.abs(b) < eps && Math.abs(c) < eps) return 0;
    // 纯旋转:a=d=cosθ, b=sinθ, c=-sinθ(容差内)
    const isRot = Math.abs(a - d) < 1e-4 && Math.abs(b + c) < 1e-4 && Math.abs(a * a + b * b - 1) < 1e-3;
    if (!isRot) return 0;
    const deg = Math.round(((Math.atan2(b, a) * 180) / Math.PI + 360) % 360);
    return deg === 360 ? 0 : deg;
  };

  // 未旋转几何:offset 链还原 transform 前的位置/尺寸(PPTX rotate 绕中心旋转未旋转盒)
  // offsetWidth/Height 为整数(亚像素误差 ≤0.5px,可接受);链断时回退 getBoundingClientRect
  ns.unrotatedRectOf = (base, el) => {
    let x = 0, y = 0, n = el, ok = true;
    while (n && !(n.classList && n.classList.contains("slide-container"))) {
      x += n.offsetLeft;
      y += n.offsetTop;
      if (!n.offsetParent) { ok = false; break; }
      n = n.offsetParent;
    }
    if (!ok || !n) return ns.rectOf(base, el);
    return { x, y, w: el.offsetWidth, h: el.offsetHeight };
  };

  // 内联标签集合:这些不算"块级子节点"
  // 2026-07-27 P1:补 CODE/KBD/SAMP/TT/VAR —— 代码/键位/样例内联,不应被当块级拆散
  // 2026-08-05 H10 修复:补全短语内容(phrasing content)行内标签。
  // 原集合漏了 U/S/DEL/INS/MARK 等 → 直接写 <u>/<s> 时 hasBlockChild 误判 li 有块级子元素,
  // 导致 ①li 丢原生 bullet ②<u> 之前的文本节点被 walk 跳过而丢字(复杂度压测实测)。
  ns.INLINE_TAGS = new Set(["SPAN", "BR", "B", "I", "STRONG", "EM", "A", "SUP", "SUB", "FONT", "CODE", "KBD", "SAMP", "TT", "VAR", "U", "S", "DEL", "INS", "MARK", "SMALL", "ABBR", "CITE", "Q", "DFN", "BDO", "WBR", "LABEL", "BUTTON", "SELECT", "TEXTAREA", "OUTPUT", "PROGRESS", "METER"]);

  // 图标字体判定(2026-07-27 P1):font-family 命中 config.iconFonts 任一子串即视为图标文字
  // → 整体转截图,避免 PPTX 端字体缺失导致 glyph 错字
  ns.isIconFont = (cs, cfg) => {
    const list = (cfg && cfg.iconFonts) || [];
    if (!list.length) return false;
    const ff = (cs.fontFamily || "").toLowerCase();
    return list.some((f) => ff.includes(String(f).toLowerCase()));
  };

  // flex/grid 容器的所有元素子级都会被块级化(flex item / grid item),即使标签是 span,
  // 也必须逐个递归提取(保留各自的位置/换行),不能拍平成一行。(红线⑥ + H4)
  ns.hasBlockChild = (el, cs, cfg) => {
    const blockified = cs.display.includes("flex") || ((cfg || {}).gridBlockifiesChildren && cs.display.includes("grid"));
    if (blockified) return el.children.length > 0;
    return Array.from(el.children).some((c) => !ns.INLINE_TAGS.has(c.tagName));
  };

  // 基元收集器:z 发号在此统一,发射顺序即 PPTX 叠放序(H3:DOM 遍历序)
  ns.makeCollector = () => {
    let zSeq = 0;
    return {
      prims: [],
      push(p) {
        this.prims.push({ ...p, z: zSeq++ });
      },
    };
  };
})();
