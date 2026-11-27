/**
 * 检查搜索关键词。长度 1-50，不能是链接，不含 < > " '。
 * @param {string} keyword
 * @returns {boolean}
 */
function isKeywordValid(keyword) {
  if (typeof keyword !== "string" || keyword.trim() === "") {
    return false;
  }
  keyword = keyword.trim();
  if (keyword.length < 1 || keyword.length > 50) {
    return false;
  }
  if (/[<>"']/.test(keyword)) {
    return false;
  }
  if (/https?:\/\//i.test(keyword) || /www\./i.test(keyword)) {
    return false;
  }
  return true;
}

/**
 * 去掉控制字符、零宽字符和 emoji，连续空白收敛为一个空格。
 * @param {string} keyword
 * @returns {string}
 */
function normalizeKeyword(keyword) {
  if (typeof keyword !== "string") return "";
  return keyword
    .replace(/[\u0000-\u001f\u007f\u200b-\u200f\ufeff]/g, "")
    .replace(/[\u{1F000}-\u{1FAFF}\u{2600}-\u{27BF}\u{FE00}-\u{FE0F}]/gu, "")
    .replace(/\s+/g, " ")
    .trim();
}

function assertChoice(value, allowed, label) {
  const n = Number(value);
  if (!allowed.includes(n)) {
    throw new Error(`${label} ${value} 无效, 允许值: ${allowed.join(", ")}`);
  }
  return n;
}

function assertIntegerRange(value, min, max, label) {
  const n = Number(value);
  if (!Number.isInteger(n) || n < min || n > max) {
    throw new Error(`${label} ${value} 无效, 允许 ${min}-${max} 的整数`);
  }
  return n;
}

/**
 * 校验搜索选项。非法值直接失败，不改写成默认值。
 * @returns {[number, number, number, number]}
 */
function assertSearchOptions(sort, time, duration, limit) {
  sort = assertChoice(sort, [0, 1, 2], "排序 sort");
  time = assertChoice(time, [0, 1, 7, 30], "发布时间 time");
  duration = assertChoice(duration, [0, 1, 2, 3], "视频时长 duration");
  limit = assertIntegerRange(limit, 1, 10000, "搜索数量 limit");
  return [sort, time, duration, limit];
}

module.exports = {
  normalizeKeyword,
  isKeywordValid,
  assertSearchOptions,
  assertChoice,
  assertIntegerRange,
};
