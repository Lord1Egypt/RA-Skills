// merge.js — 配置合并(纯函数,不可变)
// 项目级 slides.config.json 只允许覆盖白名单内的叶子键;未知键/类型不符在加载边界 fail fast。
const DEFAULTS = require("./default.config.js");

const isPlainObject = (v) => v !== null && typeof v === "object" && !Array.isArray(v);

// 开放字典:允许新增键(值必须为字符串),如 fontMap 的自定义字体映射
const OPEN_DICTS = new Set(["fontMap"]);

function deepMerge(base, override, pathPrefix = "") {
  const out = { ...base };
  for (const key of Object.keys(override)) {
    const path = pathPrefix ? `${pathPrefix}.${key}` : key;
    if (!(key in base)) {
      if (OPEN_DICTS.has(pathPrefix)) {
        if (typeof override[key] !== "string")
          throw new Error(`配置键类型不符: ${path}(开放字典 ${pathPrefix} 的值必须为字符串)`);
        out[key] = override[key];
        continue;
      }
      throw new Error(`slides.config.json 含未知配置键: ${path}`);
    }
    const b = base[key], o = override[key];
    if (isPlainObject(b) && isPlainObject(o)) out[key] = deepMerge(b, o, path);
    else if (isPlainObject(b) !== isPlainObject(o))
      throw new Error(`配置键类型不符: ${path}(期望${isPlainObject(b) ? "对象" : typeof b},得到 ${Array.isArray(o) ? "array" : typeof o})`);
    else if (typeof b !== typeof o || Array.isArray(b) !== Array.isArray(o))
      // 叶子键类型必须一致(null/数组/标量互不兼容),防静默行为漂移
      throw new Error(`配置键类型不符: ${path}(期望 ${Array.isArray(b) ? "array" : typeof b},得到 ${Array.isArray(o) ? "array" : typeof o})`);
    else out[key] = o;
  }
  return out;
}

// 返回新的冻结配置;overrides 为空时返回默认配置本身
function resolveConfig(overrides) {
  if (!overrides || Object.keys(overrides).length === 0) return DEFAULTS;
  const merged = deepMerge(DEFAULTS, overrides);
  Object.values(merged).forEach((v) => isPlainObject(v) && Object.freeze(v));
  return Object.freeze(merged);
}

module.exports = { resolveConfig };
