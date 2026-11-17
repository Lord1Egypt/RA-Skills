// validate/dom-checks.js — 浏览器计算样式检查
// 该函数被序列化进页面执行(page.evaluate),必须保持自包含、无闭包依赖。
// 画布尺寸由调用方以单参数对象注入(page.evaluate(domChecks, {w, h});
// Playwright evaluate 只接受一个参数),勿在函数体内硬编码。
// 规则与旧 validate.js 逐字一致。
function domChecks(canvas) {
  const canvasW = canvas.w, canvasH = canvas.h;
  const issues = [];
  const container = document.querySelector(".slide-container");
  if (!container) return issues;
  const base = container.getBoundingClientRect();
  if (Math.round(base.width) !== canvasW || Math.round(base.height) !== canvasH)
    issues.push({ level: "ERROR", msg: `.slide-container 尺寸为 ${Math.round(base.width)}x${Math.round(base.height)},应为 ${canvasW}x${canvasH}`, fix: "检查容器 width/height 及缩放" });

  const INLINE = new Set(["SPAN", "BR", "B", "I", "STRONG", "EM", "A", "SUP", "SUB", "FONT"]);
  const hasBlockChild = (el) => Array.from(el.children).some((c) => !INLINE.has(c.tagName));

  // 1) 未标记 data-object 的可见元素(不在任何 data-object 之内) → 不会被提取
  //    Phase 2 起不再限绝对定位:流式/flex/grid 子级同样必须标记(测绘证实旧页零命中)
  document.querySelectorAll(".slide-container *").forEach((el) => {
    const cs = getComputedStyle(el);
    if (cs.display === "none" || cs.visibility === "hidden") return;
    if (el.closest('[data-object="true"]') !== el && el.closest('[data-object="true"]')) return; // 在被标记的祖先内,OK
    if (el.closest('[data-object="true"]')) return;
    // 布局容器的直接子级由 layout-checks 给出更具体的报错,此处不重复
    if (el.parentElement) {
      const pd = getComputedStyle(el.parentElement).display;
      if (pd.includes("flex") || pd.includes("grid")) return;
    }
    const r = el.getBoundingClientRect();
    if (r.width < 2 || r.height < 2) return;
    // 只看"自身"可见性:直接文本节点/自身背景。后代文字若在未标记后代里,后代会被各自检查;
    // 容器内已标记子级的文字不应让未标记容器本身误报(flex/grid 布局容器正是此形态)
    const directText = Array.from(el.childNodes).some((n) => n.nodeType === 3 && n.textContent.trim() !== "");
    const hasVisual = cs.backgroundColor !== "rgba(0, 0, 0, 0)" || (cs.backgroundImage && cs.backgroundImage !== "none") || directText;
    if (hasVisual)
      issues.push({ level: "ERROR", msg: `元素未标记 data-object="true",转换时会被忽略: <${el.tagName.toLowerCase()}> "${(el.textContent || "").trim().slice(0, 20)}"`, fix: "补上 data-object=\"true\" data-object-type=\"textbox|shape\"" });
  });

  // 2) 文本检查:多行无显式行高 / rgba 文字 / 非统一边框
  document.querySelectorAll('[data-object="true"]').forEach((el) => {
    const cs = getComputedStyle(el);
    const r = el.getBoundingClientRect();
    const fs = parseFloat(cs.fontSize) || 16;
    const isTextLeaf = !hasBlockChild(el) && (el.textContent || "").trim() !== "";
    if (isTextLeaf) {
      const lh = cs.lineHeight;
      // 仅在"可能折行"时才提示:估算文本宽度超过盒宽 且 盒高超过单行
      const text = el.textContent.trim();
      const estWidth = text.length * fs * 0.95;
      const mayWrap = estWidth > r.width * 1.05 && r.height > fs * 1.6;
      if (lh === "normal" && mayWrap)
        issues.push({ level: "WARN", msg: `多行文字未设显式 line-height,行距将不可控: "${text.slice(0, 20)}"`, fix: "给该文本加 line-height(如 1.5 或 31px)" });
      const m = /rgba\(([^)]+)\)/.exec(cs.color);
      if (m && parseFloat(m[1].split(",")[3]) < 1)
        issues.push({ level: "WARN", msg: `文字颜色带透明度,转换后变为纯色: "${el.textContent.trim().slice(0, 20)}" (${cs.color})`, fix: "改用不透明的混合色值(手算与底色的混合结果)" });
    }
    const bw = [cs.borderTopWidth, cs.borderRightWidth, cs.borderBottomWidth, cs.borderLeftWidth];
    const nonZero = bw.filter((w) => parseFloat(w) > 0);
    const radius = parseFloat(cs.borderTopLeftRadius) || 0;
    // 非统一边框已支持(逐边细条),但与圆角共存时不贴合 → 仅此时提示
    if (nonZero.length > 0 && new Set(bw).size > 1 && radius > 0)
      issues.push({ level: "WARN", msg: `圆角卡片使用非统一边框(${bw.join("/")}),逐边细条不贴合圆角`, fix: "圆角卡改用统一边框,或强调条用独立细长 shape" });
  });

  // 3) 容器背景为渐变/图片:PPTX 幻灯片背景只支持纯色(纯色容器背景会自动导出,无需处理)
  const ccs = getComputedStyle(container);
  if (ccs.backgroundImage && ccs.backgroundImage !== "none")
    issues.push({ level: "WARN", msg: ".slide-container 使用渐变/图片背景,幻灯片背景只支持纯色,该背景会丢失", fix: "加一个 1920x1080 全画布 data-object shape 铺渐变(将被截图还原)" });

  // 4) 完全在画布外的元素:不可见(部分超出的截图元素已自动取交集,无需处理)
  document.querySelectorAll('[data-object="true"]').forEach((el) => {
    const r = el.getBoundingClientRect();
    const relX = r.left - base.left, relY = r.top - base.top;
    if (relX + r.width <= 0 || relY + r.height <= 0 || relX >= canvasW || relY >= canvasH)
      issues.push({ level: "WARN", msg: `元素完全在画布外,不会显示: <${el.tagName.toLowerCase()}> "${(el.textContent || "").trim().slice(0, 20)}"`, fix: "移入 1920x1080 画布内,或删除" });
  });

  // 5) font-weight:500 会退化为常规体(PPTX 只有常规/粗体两档)
  document.querySelectorAll(".slide-container *").forEach((el) => {
    const hasDirectText = Array.from(el.childNodes).some((n) => n.nodeType === 3 && n.textContent.trim() !== "");
    if (!hasDirectText) return;
    const cs = getComputedStyle(el);
    if (parseInt(cs.fontWeight, 10) === 500)
      issues.push({ level: "WARN", msg: `font-weight:500 在 PPTX 中退化为常规体: "${el.textContent.trim().slice(0, 20)}"`, fix: "改用 400(常规)或 600(粗体)" });
  });

  // 6) 2026-07-27 P0/P1:静默消失类元素硬提示 / P2 2.6:video/audio 已支持(addMedia)
  // <canvas> 已支持(整体截图 / data-chart 原生图表)
  // video/audio:已支持原生嵌入(addMedia);video 建议 poster 属性(否则用截屏做封面)
  document.querySelectorAll(".slide-container iframe, .slide-container form").forEach((el) => {
    issues.push({ level: "ERROR", msg: `<${el.tagName.toLowerCase()}> 不支持转换,会被整个忽略`, fix: "内容拆成原生元素;表单改用静态展示" });
  });
  document.querySelectorAll(".slide-container video").forEach((el) => {
    if (!el.getAttribute("src") && !el.querySelector("source"))
      issues.push({ level: "WARN", msg: `<video> 未指定 src,将仅用封面图展示`, fix: "加 src 属性指向本地视频文件" });
    if (!el.getAttribute("poster") && !el.getAttribute("data-poster"))
      issues.push({ level: "WARN", msg: `<video> 未设 poster,将截取浏览器渲染帧做封面(可能黑屏)`, fix: "加 poster 属性指向封面图" });
  });
  document.querySelectorAll(".slide-container audio").forEach((el) => {
    if (!el.getAttribute("src") && !el.querySelector("source"))
      issues.push({ level: "WARN", msg: `<audio> 未指定 src,将被忽略`, fix: "加 src 属性指向本地音频文件" });
  });

  // 7) 容器必须位于视口原点:截图按视口坐标、基元按容器坐标,偏移会导致截图错位
  if (Math.abs(base.left) > 1 || Math.abs(base.top) > 1)
    issues.push({ level: "ERROR", msg: `.slide-container 未位于 (0,0)(实际 ${Math.round(base.left)},${Math.round(base.top)}),截图将与原生元素错位`, fix: "html,body 设 margin:0;padding:0;容器不要加 margin/位移" });

  // 8) 视觉效果类样式:2026-07-27 P1 起整体转截图(非编辑);特效元素内文字会丢失可编辑性
  document.querySelectorAll(".slide-container *").forEach((el) => {
    const cs = getComputedStyle(el);
    if (cs.mixBlendMode && cs.mixBlendMode !== "normal")
      issues.push({ level: "WARN", msg: `mix-blend-mode:${cs.mixBlendMode} 元素整体转截图(不可编辑)`, fix: "文字放在特效元素之外的独立 textbox 叠加" });
    if (cs.filter && cs.filter !== "none")
      issues.push({ level: "WARN", msg: `filter:${cs.filter} 元素整体转截图(不可编辑)`, fix: "文字放在特效元素之外的独立 textbox 叠加" });
    if (cs.backdropFilter && cs.backdropFilter !== "none")
      issues.push({ level: "WARN", msg: `backdrop-filter:${cs.backdropFilter} 元素整体转截图(不可编辑)`, fix: "文字放在特效元素之外的独立 textbox 叠加" });
    if (cs.clipPath && cs.clipPath !== "none")
      issues.push({ level: "WARN", msg: `clip-path:${cs.clipPath} 元素整体转截图(不可编辑)`, fix: "裁剪形状内的文字改放独立 textbox" });
    if (cs.outlineStyle && cs.outlineStyle !== "none" && parseFloat(cs.outlineWidth) > 0)
      issues.push({ level: "WARN", msg: "outline 不转换", fix: "改用 border(支持逐边/虚线)或独立细条 shape" });
  });

  // 9) transform 计算样式级语义检查(静态正则只覆盖内联字面量;此处兜住 matrix/类名写法)
  document.querySelectorAll(".slide-container *").forEach((el) => {
    const cs = getComputedStyle(el);
    const t = cs.transform;
    if (!t || t === "none") return;
    const m = /^matrix\(([^)]+)\)$/.exec(t);
    if (!m) return;
    const [a, b, c, d] = m[1].split(",").map((v) => parseFloat(v.trim()));
    const eps = 1e-6;
    const identity = Math.abs(a - 1) < eps && Math.abs(d - 1) < eps && Math.abs(b) < eps && Math.abs(c) < eps;
    if (identity) return; // 纯平移:无视觉变换
    const isRot = Math.abs(a - d) < 1e-4 && Math.abs(b + c) < 1e-4 && Math.abs(a * a + b * b - 1) < 1e-3;
    if (!isRot) {
      issues.push({ level: "ERROR", msg: `transform 含缩放/斜切(${t.slice(0, 40)}…),PPTX 中丢失: <${el.tagName.toLowerCase()}>`, fix: "仅支持纯旋转 rotate();尺寸用宽高表达,斜切图形改放图片背景" });
      return;
    }
    // 纯旋转:transform-origin 必须居中(PPTX 绕中心旋转)
    // 用 offsetWidth/Height(未旋转尺寸)判定;getBoundingClientRect 是旋转后包围盒,会误报
    const ori = (cs.transformOrigin || "").split(/\s+/);
    const ox = parseFloat(ori[0]), oy = parseFloat(ori[1]);
    if ((!isNaN(ox) && Math.abs(ox - el.offsetWidth / 2) > 1) || (!isNaN(oy) && Math.abs(oy - el.offsetHeight / 2) > 1))
      issues.push({ level: "WARN", msg: `旋转元素的 transform-origin 非居中(${cs.transformOrigin}),PPTX 将绕中心旋转,位置会有偏差`, fix: "改为 transform-origin:center,或旋转后用 left/top 重新对位" });
  });

  // 10) 2026-07-27 D6:<img> 必须显式声明 object-fit
  // 缺省时 CSS 默认 fill,与"我忘了写"无法区分 → 转换器按 fill(拉伸)处理,易出现非预期变形
  // 装饰图推荐 background-image(走截图路径);<img> 定位"内容照片/产品图"(原生可编辑图片)
  document.querySelectorAll(".slide-container img").forEach((el) => {
    const cs = getComputedStyle(el);
    if (cs.objectFit === "fill" && !el.style.objectFit && !el.getAttribute("object-fit"))
      issues.push({ level: "WARN", msg: `<img> 未显式声明 object-fit,默认按 fill(拉伸)处理,可能变形`, fix: "内容照片建议 object-fit:cover 或 contain;纯装饰图改用 background-image" });
  });

  // 11) 2026-07-27 P2 2.4:data-shape 预设几何白名单校验
  // data-shape 值必须是 pptxgenjs 支持的预设形状名;非法值会导致 addShape 报错
  const PRESET_SHAPES = new Set([
    "rect", "roundRect", "ellipse", "triangle", "rtTriangle", "diamond", "parallelogram",
    "trapezoid", "pentagon", "hexagon", "heptagon", "octagon", "decagon", "dodecagon",
    "pie", "chord", "teardrop", "frame", "halfFrame", "corner", "brackets", "brace",
    "leftArrow", "rightArrow", "upArrow", "downArrow", "stripedRightArrow", "notchedRightArrow",
    "bentArrow", "quadArrow", "leftRightArrow", "upDownArrow", "leftRightUpArrow",
    "quadArrowCallout", "bentArrowCallout", "chevron", "circularArrow", "homePlate",
    "curvedRightArrow", "curvedLeftArrow", "curvedUpArrow", "curvedDownArrow", "swooshArrow",
    "cube", "can", "lightningBolt", "heart", "sun", "moon", "smileyFace", "cloud",
    "star5", "star6", "star7", "star8", "star10", "star12", "star16", "star24", "star32",
    "plus", "minus", "multiply", "divide", "equals",
    "flowchartProcess", "flowchartDecision", "flowchartTerminator", "flowchartInput",
    "flowchartOutput", "flowchartPredefined", "flowchartDocument", "flowchartManualInput",
    "flowchartManualOperation", "flowchartConnector", "flowchartPreparation",
    "flowchartInternalStorage", "flowchartSort", "flowchartExtract", "flowchartMerge",
    "flowchartOr", "flowchartPunchedCard", "flowchartSummingJunction", "flowchartCollate",
    "flowchartStoredData", "flowchartDelay", "flowchartDisplay", "flowchartOffPageConnector",
    "flowchartMagneticDisk", "flowchartDirectAccessStorage", "flowchartSequentialAccess",
    "actionButtonBlank", "actionButtonHome", "actionButtonHelp", "actionButtonInformation",
    "actionButtonForwardNext", "actionButtonBackPrevious", "actionButtonEnd",
    "actionButtonBeginning", "actionButtonReturn", "actionButtonDocument",
  ]);
  document.querySelectorAll(".slide-container [data-shape]").forEach((el) => {
    const v = el.getAttribute("data-shape");
    if (!PRESET_SHAPES.has(v))
      issues.push({ level: "ERROR", msg: `data-shape="${v}" 不是 pptxgenjs 支持的预设形状名`, fix: "查 html-spec.md 5.4 节预设形状表,改用合法形状名(如 triangle/rightArrow/chevron/diamond)" });
  });

  // ══ 设计质量检查(2026-08-02 重构 D 期)══
  // design.tier 驱动;缺省档 presentation(2026-08-06 起默认开启),显式 tier:"" 才休眠
  const design = canvas.design || {};
  const tierOn = !!design.tier;
  // 判据阈值一律取自 config/default.config.js 的 design.thresholds(唯一事实源,2026-08-06 P2)。
  // 这里的 `|| {}` 与下方各处 `?? 默认值` 只是兜底(旧调用方未传 thresholds 时不至于崩),
  // **不是第二份事实源** —— 改阈值改配置表,别改这里的兜底值。
  const T = design.thresholds || {};

  // 12) 文字适配:仅查"作者固定高度"的盒子(inline style.height;方式 B/C 解析后也会写入 inline)。
  //    自动高度的 textbox 在浏览器里随内容生长,无溢出语义;CJK 字形超出 line-height 盒是常态(度量差),
  //    若对自动高度盒也查会系统性误报(封面大标题盒是典型)。
  //    溢出用 scrollHeight;欠载用"内容实际底边"(子级矩形/文本 Range 推算,绕开 scrollHeight 下界钳制)
  if (tierOn) {
    const contentBottomOf = (el, elTop) => {
      let bottom = 0;
      const push = (b) => { if (b > bottom) bottom = b; };
      Array.from(el.childNodes).forEach((n) => {
        if (n.nodeType === 1) {
          const r = n.getBoundingClientRect();
          if (r.height >= 1) push(r.bottom - elTop);
        } else if (n.nodeType === 3 && n.textContent.trim() !== "") {
          const range = document.createRange();
          range.selectNodeContents(n);
          const r = range.getBoundingClientRect();
          if (r.height >= 1) push(r.bottom - elTop);
        }
      });
      return bottom;
    };
    document.querySelectorAll('[data-object="true"]').forEach((el) => {
      const cs = getComputedStyle(el);
      if (cs.display === "none" || cs.visibility === "hidden") return;
      if (!el.style || !el.style.height) return; // 仅固定高度盒
      const text = (el.textContent || "").trim();
      if (!text) return;
      if (el.querySelector("table")) return; // 表格高度自适应,跳过
      const sh = el.scrollHeight, ch = el.clientHeight;
      if (ch < 10) return;
      // 溢出余量随字号缩放:CJK 字形超出 line-height 盒 ≈ 字号的 10-12%
      let maxFs = parseFloat(cs.fontSize) || 16;
      el.querySelectorAll("*").forEach((d) => {
        const f = parseFloat(getComputedStyle(d).fontSize) || 0;
        if (f > maxFs) maxFs = f;
      });
      const tolerance = Math.max(8, maxFs * 0.12);
      if (sh > ch + tolerance)
        issues.push({ level: "WARN", msg: `文字可能溢出容器(内容高约 ${Math.round(sh)}px > 盒高 ${Math.round(ch)}px): "${text.slice(0, 18)}"`, fix: "加高容器/减字/放大盒宽;PPT 端不会自动缩字" });
      else if (el.getAttribute("data-object-type") === "textbox" && ch >= 120) {
        const contentH = contentBottomOf(el, el.getBoundingClientRect().top);
        if (contentH > 0 && contentH < ch * 0.55)
          issues.push({ level: "WARN", msg: `文字欠载(内容高约 ${Math.round(contentH)}px < 盒高 ${Math.round(ch)}px 的 55%): "${text.slice(0, 18)}"`, fix: "放大字号/行距撑满(scale-to-fill),或收小盒高" });
      }
    });
  }

  // 13) 字号下限:绝对下限(默认 14px)+ 档内正文下限(启发:>20 字视为正文;
  //    底部注释区(top ≥ 840)且字号 ≥ 档内注释下限 → 豁免,那是来源标注不是正文)
  //    阈值源:design.thresholds.tierBodyMin / tierNoteMin / bodyHeuristicChars / noteZoneTop
  if (tierOn) {
    const bodyMin = (T.tierBodyMin || {})[design.tier] || T.bodyMinFallback || 16;
    const noteMin = (T.tierNoteMin || {})[design.tier] || T.noteMinFallback || 14;
    const bodyChars = T.bodyHeuristicChars || 20;
    const noteTop = T.noteZoneTop || 840;
    const floor = design.minBodyPx || 14;
    document.querySelectorAll(".slide-container *").forEach((el) => {
      const hasDirectText = Array.from(el.childNodes).some((n) => n.nodeType === 3 && n.textContent.trim() !== "");
      if (!hasDirectText) return;
      const cs = getComputedStyle(el);
      if (cs.display === "none" || cs.visibility === "hidden") return;
      const fs = parseFloat(cs.fontSize) || 16;
      const text = (el.textContent || "").trim();
      if (fs < floor - 0.01)
        issues.push({ level: "WARN", msg: `字号 ${fs}px 低于绝对下限 ${floor}px: "${text.slice(0, 18)}"`, fix: "任何文字(含页码/来源标注)不得小于绝对下限" });
      else if (fs < bodyMin - 0.01 && text.length > bodyChars) {
        const elTop = el.getBoundingClientRect().top - base.top;
        if (fs >= noteMin - 0.01 && elTop >= noteTop) return; // 底部注释区豁免
        issues.push({ level: "WARN", msg: `正文疑似过小:${fs}px 低于 ${design.tier} 档正文下限 ${bodyMin}px: "${text.slice(0, 18)}"`, fix: "升字号到档内区间;若它不是正文(标签/注释),精简到 20 字内" });
      }
    });
  }

  // 14) 画布填充(2026-08-06 第四轮 P3 重写):原判据只看"最低边",一根 1px 细线 + 16px 脚注
  //     就能骗过 —— 实测 96/104/105/106 全部"通过"却墨迹只占 29-52%、中间挖着 220-330px 空洞。
  //     现改三条并行判据(全部 WARN,互补而非替代):
  //       a. 墨迹行覆盖率 inkRow:内容带按 10px 分行,统计"有墨"行占比 <0.55 → 内容太稀
  //       b. 最大连续空洞 maxGap:内容带内部 ≥200px 连续无墨 → 断层(比"底部空"更普适:
  //          105-timeline 实测内容压在下半截 topShare=0.196,单看"上重下空"会漏)
  //       c. 分布偏斜 topShare:墨迹面积 ≥0.88 或 ≤0.12 集中在半边 → 一头沉
  //     页脚区(top ≥980)不计;airy 页(配置 airyPages / 深底 / 超大字少元素)整条豁免。
  //     阈值经全 44 页实测标定:airy 页实测区间 0.29-0.50 全部落在豁免侧,
  //     真实缺陷页(96/104/105/106/111)命中,已满页(01/02/110 = 1.0)不动。
  if (tierOn && !canvas.airy) {
    const TOP = T.contentTop || 320, BOT = T.contentBottom || 940, ROW = T.inkRowPx || 10;
    const rowN = Math.round((BOT - TOP) / ROW);
    const spans = Array.from({ length: rowN }, () => []);
    let maxBottom = 0, maxFs = 0, textObjCount = 0;
    const opaqueBg = (cs) => {
      const m = /rgba?\(([^)]+)\)/.exec(cs.backgroundColor || "");
      if (m) {
        const p = m[1].split(",");
        if (p.length < 4 || parseFloat(p[3]) > 0.05) return true;
      }
      return /gradient\(|url\(/.test(cs.backgroundImage || "none");
    };
    // 墨迹 = 直接文字 / 图表图形表格图片 / 不透明底色或渐变 / 有边框;整页底不算
    document.querySelectorAll(".slide-container *").forEach((el) => {
      const cs = getComputedStyle(el);
      if (cs.display === "none" || cs.visibility === "hidden" || parseFloat(cs.opacity) < 0.05) return;
      const r = el.getBoundingClientRect();
      const t = r.top - base.top, b = r.bottom - base.top;
      if (r.width < 2 || r.height < 2) return;
      const hasText = Array.from(el.childNodes).some((n) => n.nodeType === 3 && n.textContent.trim() !== "");
      const isFigure = /^(IMG|SVG|CANVAS|VIDEO|TABLE)$/.test(el.tagName) || el.hasAttribute("data-chart") || el.hasAttribute("data-shape");
      const fullBleed = r.width >= 0.98 * canvasW && r.height >= 0.98 * canvasH;
      const bordered =
        parseFloat(cs.borderTopWidth) + parseFloat(cs.borderBottomWidth) + parseFloat(cs.borderLeftWidth) + parseFloat(cs.borderRightWidth) > 0;
      const ink = hasText || isFigure || (!fullBleed && (opaqueBg(cs) || bordered));
      if (!ink) return;
      if (t < (T.footerZoneTop || 980) && b <= canvasH + 2) maxBottom = Math.max(maxBottom, b);
      if (hasText) { textObjCount++; maxFs = Math.max(maxFs, parseFloat(cs.fontSize) || 0); }
      if (b <= TOP || t >= BOT) return;
      const x0 = Math.max(r.left - base.left, 0), x1 = Math.min(r.right - base.left, canvasW);
      if (x1 - x0 < 2) return;
      const r0 = Math.max(0, Math.floor((t - TOP) / ROW));
      const r1 = Math.min(rowN - 1, Math.ceil((b - TOP) / ROW) - 1);
      for (let i = r0; i <= r1; i++) spans[i].push([x0, x1]);
    });
    // 逐行求横向并集宽度(重叠区不重复计)
    const occ = spans.map((s) => {
      const sorted = s.slice().sort((a, b) => a[0] - b[0]);
      let w = 0, cur = null;
      for (const seg of sorted) {
        if (!cur) cur = seg.slice();
        else if (seg[0] <= cur[1]) cur[1] = Math.max(cur[1], seg[1]);
        else { w += cur[1] - cur[0]; cur = seg.slice(); }
      }
      return cur ? w + (cur[1] - cur[0]) : w;
    });
    const bgm = /rgba?\(([^)]+)\)/.exec(ccs.backgroundColor || "");
    let dark = false;
    if (bgm) {
      const ch = bgm[1].split(",").map((v) => parseFloat(v));
      dark = (0.2126 * ch[0] + 0.7152 * ch[1] + 0.0722 * ch[2]) / 255 < 0.35;
    }
    const airyHeuristic = dark || (maxFs >= 64 && textObjCount <= 5);
    if (!airyHeuristic && occ.some((w) => w > 0)) {
      const inkRow = occ.filter((w) => w > 0).length / rowN;
      let gapRun = 0, maxGap = 0;
      occ.forEach((w) => { if (w === 0) { gapRun++; maxGap = Math.max(maxGap, gapRun); } else gapRun = 0; });
      const half = Math.floor(rowN / 2);
      const areaAll = occ.reduce((a, b) => a + b, 0);
      const topShare = areaAll ? occ.slice(0, half).reduce((a, b) => a + b, 0) / areaAll : 0;
      const FIX_FILL =
        "放大字号/行距/间距把内容撑满(scale-to-fill),或补足漏排内容;若为 airy 页(封面/分隔/大字/引用/收尾),把文件名加入 design.airyPages";
      if (inkRow < (T.inkRowMin ?? 0.55))
        issues.push({
          level: "WARN",
          msg: `内容区墨迹行占比 ${(inkRow * 100).toFixed(1)}%(阈值 ${((T.inkRowMin ?? 0.55) * 100).toFixed(0)}%),版面过稀`,
          fix: FIX_FILL,
        });
      if (maxGap * ROW >= (T.maxGapPx || 200))
        issues.push({
          level: "WARN",
          msg: `内容区有 ${maxGap * ROW}px 连续空白断层(阈值 ${T.maxGapPx || 200}px)`,
          fix: FIX_FILL,
        });
      const skewHi = T.skewMax ?? 0.88;
      if (topShare >= skewHi || topShare <= 1 - skewHi)
        issues.push({
          level: "WARN",
          msg: `墨迹 ${(Math.max(topShare, 1 - topShare) * 100).toFixed(0)}% 挤在${topShare >= skewHi ? "上" : "下"}半截,分布严重偏斜`,
          fix: FIX_FILL,
        });
    }
    // 保留原"最低边"判据(与上面三条并行;它对"整体偏上"最直观)
    const fillLine = (T.contentTop || 320) + ((T.contentBottom || 940) - (T.contentTop || 320)) * (design.fillThreshold || 0.85);
    if (!airyHeuristic && maxBottom > 0 && maxBottom < fillLine)
      issues.push({ level: "WARN", msg: `内容底边 ${Math.round(maxBottom)}px,底部留白过大(内容区 ${Math.round(fillLine)}px 线未达)`, fix: "放大字号/行距撑满(scale-to-fill),或检查是否漏排内容;若为 airy 页(封面/分隔/大字/引用),把文件名加入 design.airyPages" });
  }
  // 15) 字号层级(2026-08-06 第四轮 P3):字号阶只写在文档里,实测 96-107 段正文中位数
  //     几乎全部钉在 22px = 演讲档下限 —— 下限被当成了默认值,页内层级被压平。
  //     两条判据:页标题/正文比值 <1.6 → 层级不足;不同字号档 <3 → 缺少节奏。
  //     实测标定:93(1.00)命中;正常页 2.15-4.71 全部通过。
  //     正文样本**限内容区(top ≥320)** —— 否则长页标题自己 >20 字会被当成"正文",
  //     比值恒为 1.00(106-table-focus 实测踩过这个坑,它页内只有一个 56px 元素)。
  //     bodyMed=0(无 >20 字长文本的图示页,如 112-117)整条跳过 —— 无"正文"可比。
  if (tierOn) {
    const cbase = container.getBoundingClientRect();
    const samples = [];
    document.querySelectorAll(".slide-container *").forEach((el) => {
      const cs = getComputedStyle(el);
      if (cs.display === "none" || cs.visibility === "hidden") return;
      const own = Array.from(el.childNodes).filter((n) => n.nodeType === 3).map((n) => n.textContent).join("").trim();
      if (!own) return;
      const r = el.getBoundingClientRect();
      if (r.height < 2) return;
      samples.push({ fs: Math.round(parseFloat(cs.fontSize) || 0), len: own.length, top: r.top - cbase.top });
    });
    if (samples.length) {
      const body = samples.filter((s) => s.len > (T.bodyHeuristicChars || 20) && s.top >= (T.contentTop || 320)).map((s) => s.fs).sort((a, b) => a - b);
      const bodyMed = body.length ? body[Math.floor(body.length / 2)] : 0;
      const headFs = Math.max(0, ...samples.filter((s) => s.top < (T.contentTop || 320)).map((s) => s.fs));
      const distinct = new Set(samples.map((s) => s.fs)).size;
      const ratioMin = T.titleBodyRatioMin ?? 1.6;
      if (bodyMed > 0 && headFs > 0 && headFs / bodyMed < ratioMin)
        issues.push({
          level: "WARN",
          msg: `页标题 ${headFs}px 仅为正文 ${bodyMed}px 的 ${(headFs / bodyMed).toFixed(2)} 倍(阈值 ${ratioMin}),层级不足`,
          fix: "按 design-principles 字号阶拉开:页标题用 var(--text-title-page),正文 var(--text-body)",
        });
      if (distinct < (T.distinctSizesMin || 3) && samples.length >= (T.hierarchyMinSamples || 4))
        issues.push({
          level: "WARN",
          msg: `全页只有 ${distinct} 种字号,缺少视觉节奏`,
          fix: "至少分出页标题/块标题/正文三档(见 design-principles 第二章字号阶)",
        });
    }
  }

  // 16) 结构色面下限(2026-08-06 第四轮 P3;仅 balanced/rich 档):
  //     实测 96-107 段 10 页色面**恰好 0%**(纯白底 + 黑字 + 细线),110-117 段 11-72% ——
  //     "素雅单调"的量化根因就在这里。内容页(非 airy)要求至少一块结构色面:
  //     色带/深色面板/卡片底/表头底,面积 ≥1.5 万 px² 才计一块。
  //     口径:非画布色的不透明底或渐变;整页底不计(那是画布本身,不构成层次)。
  if (tierOn && !canvas.airy && /^(balanced|rich)$/.test(design.formProfile || "")) {
    const canvasBg = ccs.backgroundColor;
    let colorArea = 0, blocks = 0;
    document.querySelectorAll(".slide-container *").forEach((el) => {
      const cs = getComputedStyle(el);
      if (cs.display === "none" || cs.visibility === "hidden" || parseFloat(cs.opacity) < 0.05) return;
      const r = el.getBoundingClientRect();
      if (r.width < 2 || r.height < 2) return;
      if (r.width >= 0.98 * canvasW && r.height >= 0.98 * canvasH) return; // 整页底 = 画布
      const m = /rgba?\(([^)]+)\)/.exec(cs.backgroundColor || "");
      const opaque = m && (m[1].split(",").length < 4 || parseFloat(m[1].split(",")[3]) > 0.05);
      const grad = /gradient\(/.test(cs.backgroundImage || "none");
      if (!grad && !(opaque && cs.backgroundColor !== canvasBg)) return;
      const a = r.width * r.height;
      if (a >= (T.colorBlockMinArea || 15000)) { colorArea += a; blocks++; }
    });
    const colorPct = (colorArea / (canvasW * canvasH)) * 100;
    if (blocks === 0 && colorPct < (T.colorPctMin || 8))
      issues.push({
        level: "WARN",
        msg: `全页无结构色面(色带/深色面板/卡片底均无,色面占比 ${colorPct.toFixed(1)}%),观感偏素`,
        fix: "加一块承载信息的结构色面:章节色带 / 深色强调面板 / 卡片底色 / 表头底纹(见 design-principles 视觉形式三档;纯装饰形状不算)",
      });
  }

  // 17) 语义密度(2026-08-06 第五轮 P1):企业黑话检查。
  //     动机:规则 12-16 全是**几何统计量**。实测构造页"两块大色块 + 三行企业黑话"
  //     (赋能生态/持续深化/统筹推进…)可以 0 ERROR / 0 WARN 完整通过 —— 门禁在压制
  //     "小字堆上半截"的同时,为"大色块 + 空话"开了一条合法通道。这条规则堵它。
  //
  //     为什么只查黑话、不查"具体性":
  //       具体性(数字+单位)检测漏掉专有名词与命名实体 —— four-revolutions(农业/工业/信息/
  //       智能革命 + 机制描述)、05-four-questions(ISSB×ESRS×GRI、Scope 1/2/3)实测
  //       "具体标记 = 0",但它们内容扎实。按具体性判负会误伤这类页,故不做该判据。
  //
  //     两档词表(实测标定):
  //       一档 = 几乎永远是空话(赋能/抓手/提质增效/夯实基础…),计入判据;
  //       二档 = 有正当技术用法(对齐/协同/沉淀/闭环/打通),**不计** ——
  //         105 的"沉淀模板 v1.2"、05-four-questions 的"ISSB 对齐"、111 的"6 周闭环"都是实义。
  //     阈值:每千汉字 ≥40 次 **且** 绝对次数 ≥3。全 44 页实测最高 11.5/千字(94 页 1 个"赋能"),
  //     对照空话页 145.8/千字(7 次 / 48 字)—— 老页零命中,构造页必中。
  //     注意:**不设"最小字数"门限**。黑话密度在任何篇幅下都有意义,而图示型短页(113-cycle
  //     52 字)一档命中恒为 0,不需要靠字数门限保护;"≥3 次"这条已足够挡掉短页偶发误报。
  //     (`semanticMinCjk` 保留在配置里,供后续真的引入"具体性"判据时使用 —— 那个判据才需要它。)
  if (tierOn) {
    const BUZZ_T1 = [
      "赋能", "抓手", "提质增效", "全面提升", "持续优化", "打造标杆", "形成合力", "高度重视",
      "有效推进", "统筹推进", "夯实基础", "精准发力", "做大做强", "保驾护航", "全方位提升",
      "深度融合", "全面深化", "持续赋能", "生态闭环", "价值闭环",
    ];
    const cbase3 = container.getBoundingClientRect();
    let text = "";
    document.querySelectorAll(".slide-container *").forEach((el) => {
      const cs = getComputedStyle(el);
      if (cs.display === "none" || cs.visibility === "hidden") return;
      const own = Array.from(el.childNodes).filter((n) => n.nodeType === 3).map((n) => n.textContent).join("").trim();
      if (!own) return;
      const top = el.getBoundingClientRect().top - cbase3.top;
      if (top >= 320 && top < 980) text += own + " ";
    });
    const cjk = (text.match(/[一-龥]/g) || []).length;
    if (cjk > 0) {
      const hits = [];
      let n = 0;
      BUZZ_T1.forEach((w) => {
        const k = text.split(w).length - 1;
        if (k > 0) { n += k; hits.push(w); }
      });
      const perK = (n / cjk) * 1000;
      if (n >= (design.buzzMin || 3) && perK >= (design.buzzPerK || 40))
        issues.push({
          level: "WARN",
          msg: `内容区企业黑话密度过高(${n} 次 / ${cjk} 汉字 = ${perK.toFixed(0)}‰):${hits.slice(0, 5).join("、")}`,
          fix: "把空洞动宾换成可验证的事实:数字+单位、具体例子、专有名词、时间范围。版面达标不等于内容达标",
        });
    }
  }

  return issues;
}

module.exports = { domChecks };
