// layout/resolver.js — data-layout 解析器:校验 + 把子级改写为绝对定位
// validate 与 convert 注入同一文件,保证"预检所见 = 转换所得":
//   validateAll(root) → issues[](level/msg/fix),供 validate.js 收集
//   resolveAll(root)  → 改写 DOM(子级补上 inline position/left/top/width/height),
//                       非法布局直接 throw(convert 侧 fail fast);无 data-layout 时恒等 no-op
(() => {
  const ns = (window.__htmlSlides = window.__htmlSlides || {});
  ns.layout = ns.layout || {};

  const KNOWN_CONTAINER_ATTRS = new Set(["data-layout", "data-layout-gap", "data-layout-cols"]);
  const KNOWN_CHILD_ATTRS = new Set(["data-layout-h", "data-layout-w"]);
  const num = (v) => {
    const m = /^(\d+(?:\.\d+)?)(px)?$/.exec(String(v == null ? "" : v).trim());
    return m ? parseFloat(m[1]) : null;
  };
  const label = (el) => `<${el.tagName.toLowerCase()} data-layout="${el.getAttribute("data-layout")}">`;

  function containers(root) {
    return Array.from((root || document).querySelectorAll("[data-layout]"));
  }

  // 收集一个容器的校验问题;errs 为输出数组(元素: {level,msg,fix})
  function checkContainer(c, issues) {
    const strategyName = (c.getAttribute("data-layout") || "").trim();
    const strat = ns.layout.strategies[strategyName];
    const at = `容器 ${label(c)}`;
    if (!strat) {
      issues.push({
        level: "ERROR",
        msg: `未知 data-layout 策略: "${strategyName}"(${at})`,
        fix: "v1 支持: stack(纵向堆叠) / columns(横向分栏) / grid(等宽网格)",
      });
      return null;
    }

    // 未知属性(typo 防线)
    Array.from(c.attributes).forEach((a) => {
      if (a.name.startsWith("data-layout-") && !KNOWN_CONTAINER_ATTRS.has(a.name))
        issues.push({ level: "WARN", msg: `未知的容器布局属性 ${a.name}(${at}),将被忽略`, fix: `可用: data-layout-gap / data-layout-cols` });
    });

    // 嵌套 data-layout:任何祖先带 data-layout 即非法(v1)
    if (c.parentElement && c.parentElement.closest("[data-layout]"))
      issues.push({ level: "ERROR", msg: `data-layout 容器不允许嵌套(${at})`, fix: "拆成两个并列容器,或内层改用 flex/grid(方式 B)" });

    // 容器自身定位:必须绝对定位 + 显式宽度(columns 还要显式高度)
    if ((c.style.position || "") !== "absolute")
      issues.push({ level: "ERROR", msg: `data-layout 容器必须 position:absolute(${at})`, fix: "容器 style 加 position:absolute;left/top 指定画布内位置" });
    if (!(c.style.width || "").trim())
      issues.push({ level: "ERROR", msg: `data-layout 容器缺少显式 width(${at})`, fix: "容器 style 加 width:……px" });
    if (strat.needsHeight && !(c.style.height || "").trim())
      issues.push({ level: "ERROR", msg: `columns 容器缺少显式 height(${at})`, fix: "容器 style 加 height:……px(子级高度=容器高)" });

    const gap = num(c.getAttribute("data-layout-gap"));
    if (c.getAttribute("data-layout-gap") != null && gap == null)
      issues.push({ level: "ERROR", msg: `data-layout-gap 非法(${at})`, fix: "写像素数,如 data-layout-gap=\"24\"" });

    let cols = null;
    if (strat.needsCols) {
      cols = num(c.getAttribute("data-layout-cols"));
      if (cols == null || cols < 1)
        issues.push({ level: "ERROR", msg: `grid 容器缺少合法的 data-layout-cols(${at})`, fix: "写列数,如 data-layout-cols=\"4\"" });
    }

    // 子级检查
    const kids = Array.from(c.children);
    if (!kids.length)
      issues.push({ level: "WARN", msg: `data-layout 容器没有子级(${at})`, fix: "删除空容器或补上子级" });
    kids.forEach((k) => {
      Array.from(k.attributes).forEach((a) => {
        if (a.name.startsWith("data-layout-") && !KNOWN_CHILD_ATTRS.has(a.name))
          issues.push({ level: "WARN", msg: `未知的子级布局属性 ${a.name}(${label(c)} 的子级),将被忽略`, fix: "可用: data-layout-h / data-layout-w" });
      });
      if (k.getAttribute("data-object") !== "true")
        issues.push({ level: "ERROR", msg: `data-layout 容器的子级未标记 data-object="true": <${k.tagName.toLowerCase()}> "${(k.textContent || "").trim().slice(0, 20)}"`, fix: "补 data-object=\"true\" data-object-type=\"textbox|shape\"" });
      if (k.hasAttribute("data-layout"))
        issues.push({ level: "ERROR", msg: `data-layout 容器不允许嵌套(子级自身也是布局容器): <${k.tagName.toLowerCase()}>`, fix: "拆成两个并列容器,或内层改用 flex/grid(方式 B)" });
      // 混写几何:子级的定位与尺寸一律由解析器计算
      const ks = k.style;
      const mixed = ["position", "left", "top", "width", "height"].filter((p) => (ks[p] || "").trim() !== "");
      if (mixed.length)
        issues.push({ level: "ERROR", msg: `data-layout 子级混写了几何属性(${mixed.join("/")}): <${k.tagName.toLowerCase()}> "${(k.textContent || "").trim().slice(0, 16)}"`, fix: "几何交给 data-layout-h/w;视觉样式(背景/padding/圆角)照常写" });
      // 策略级子级属性校验(复用 readChild 的报错)
      if (strat) strat.readChild(k, issues);
    });

    return { strat, gap: gap || 0, cols: cols || 0 };
  }

  // validate 侧:收集全部容器的 issues
  ns.layout.validateAll = function (root) {
    const issues = [];
    containers(root).forEach((c) => checkContainer(c, issues));
    return issues;
  };

  // convert/golden 侧:校验(有问题即 throw)+ 改写子级为绝对定位
  ns.layout.resolveAll = function (root) {
    const list = containers(root);
    if (!list.length) return { containers: 0, children: 0 }; // 无 data-layout:恒等 no-op

    const issues = [];
    const plans = [];
    list.forEach((c) => {
      const before = issues.length;
      const plan = checkContainer(c, issues);
      if (issues.length === before && plan) plans.push({ c, ...plan });
    });
    const errs = issues.filter((i) => i.level === "ERROR");
    if (errs.length) throw new Error(`data-layout 布局非法:\n  - ${errs.map((e) => e.msg).join("\n  - ")}`);

    let n = 0;
    for (const { c, strat, gap, cols } of plans) {
      const width = parseFloat(c.style.width);
      const height = strat.needsHeight ? parseFloat(c.style.height) : 0;
      const childErrs = [];
      const children = Array.from(c.children).map((k) => strat.readChild(k, childErrs));
      if (childErrs.length) throw new Error(`data-layout 布局非法:\n  - ${childErrs.join("\n  - ")}`);
      const rects = strat.layout({ width, height, gap, cols, children });
      children.forEach((child, i) => {
        const r = rects[i];
        const s = child.el.style;
        s.position = "absolute";
        s.left = r.x + "px";
        s.top = r.y + "px";
        s.width = r.w + "px";
        s.height = r.h + "px";
        n++;
      });
    }
    return { containers: plans.length, children: n };
  };
})();
