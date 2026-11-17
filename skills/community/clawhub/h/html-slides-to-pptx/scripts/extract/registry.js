// extract/registry.js — 基元注册表:新增基元类型 = 往对应族里挂发射器,核心 walk 不变
// 族语义:
//   backgrounds  —— 每元素按序尝试,第一个命中的终止该族(渐变/图片 XOR 纯色 shape)
//   afterShape   —— 仅当 backgrounds 中 emitsShape 的发射器命中后执行(如逐边细条)
//   textLeaf     —— 第一个 applies 的发射器接管该元素并停止递归(文字叶子)
(() => {
  const ns = (window.__htmlSlides = window.__htmlSlides || {});
  const p = ns.primitives;

  ns.registry = {
    backgrounds: [p.gradientBackground, p.captureBackground, p.solidShape],
    afterShape: [p.borderStrips],
    textLeaf: [p.textLeaf],
  };
})();
