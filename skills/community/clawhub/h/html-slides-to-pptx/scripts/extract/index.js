// extract/index.js — 提取入口组装:window.__htmlSlides.extract(cfg)
// cfg 由 Node 端序列化传入(config.extract);缺省值与 default.config.js 一致。
(() => {
  const ns = (window.__htmlSlides = window.__htmlSlides || {});

  const FALLBACK = {
    boldThreshold: 600,
    singleLineFactor: 1.3,
    defaultColorHex: "1A1A1A",
    gridBlockifiesChildren: true,
    guardNestedObjects: true,
    nativeGradient: false, // P2 1.6:默认关,由 pipeline 从顶层 config 传入
  };

  ns.extract = function extract(cfg) {
    const config = Object.assign({}, FALLBACK, cfg || {});
    const container = document.querySelector(".slide-container");
    const base = container.getBoundingClientRect();

    const collector = ns.makeCollector();
    document.querySelectorAll('[data-object="true"]').forEach((el) => {
      // H2 护栏:嵌套 data-object 的内层不重复提取(外层 walk 会递归到达它)。
      // 测绘证实旧 29 页无嵌套,此护栏对基线零影响;嵌套写法在 validate 中为 ERROR。
      if (config.guardNestedObjects && el.parentElement && el.parentElement.closest('[data-object="true"]')) return;
      ns.walk(el, base, collector, config);
    });

    // 容器纯色底色 → 渲染侧用作 PPTX 幻灯片背景(默认白);
    // 渐变/图片容器背景无法用纯色表达,canvasBgImage 标记后由 validate 提示改用全画布 shape
    const ccs = getComputedStyle(container);
    const cbg = ns.rgb(ccs.backgroundColor);
    const canvasBg = cbg ? cbg.hex : "FFFFFF";
    const canvasBgImage = !!(ccs.backgroundImage && ccs.backgroundImage !== "none");

    const tpl = document.querySelector("template[data-slide-notes]");
    const notes = tpl ? tpl.content.textContent.trim() : "";

    return { prims: collector.prims, notes, canvasBg, canvasBgImage };
  };
})();
