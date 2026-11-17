// test/lib/normalize.js — 规范化(递归键排序 + 浮点 4 位截断),golden.js 与布局等价测试共用
function normalize(v) {
  if (Array.isArray(v)) return v.map(normalize);
  if (v && typeof v === "object") {
    const o = {};
    for (const k of Object.keys(v).sort()) o[k] = normalize(v[k]);
    return o;
  }
  if (typeof v === "number" && !Number.isInteger(v)) return +v.toFixed(4);
  return v;
}
const stable = (v) => JSON.stringify(normalize(v), null, 1) + "\n";

module.exports = { normalize, stable };
