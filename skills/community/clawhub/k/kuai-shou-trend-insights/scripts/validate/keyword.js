const utils = require("../utils/utils");

function isKeywordValid(keyword) {
  if (typeof keyword !== "string" || keyword.trim() === "") {
    utils.printError(`搜索关键词不能为空`);
    return false;
  }
  keyword = keyword.trim();
  if (keyword.length < 2) {
    utils.printError(`搜索关键词长度不能小于 2 个字符`);
    return false;
  }
  if (keyword.length > 50) {
    utils.printError(`搜索关键词长度不能超过 50 个字符`);
    return false;
  }
  if (/[<>\"'&]/g.test(keyword)) {
    utils.printError(`搜索关键词包含特殊字符, 请输入普通关键词, 例如: 新媒体`);
    return false;
  }
  if (keyword.includes("http")) {
    utils.printError(
      `搜索关键词包含 http 链接, 请输入普通关键词, 例如: 新媒体`,
    );
    return false;
  }
  return true;
}

function cleanKeyword(keyword) {
  if (typeof keyword !== "string") return "";
  return (
    keyword
      // 去控制字符与零宽字符
      .replace(/[\u0000-\u001f\u007f\u200b-\u200f\ufeff]/g, "")
      // 去 emoji 与杂项符号(保留文字类)
      .replace(/[\u{1F000}-\u{1FAFF}\u{2600}-\u{27BF}\u{FE00}-\u{FE0F}]/gu, "")
      // 多个空白收敛为一个
      .replace(/\s+/g, " ")
      .trim()
  );
}

function optionFormat(sort, time, duration, limit) {
  sort = sort || 0;
  time = time || 0;
  duration = duration || 0;
  limit = limit || 10;
  if (sort !== 0 && sort !== 1 && sort !== 2) {
    utils.printError(`排序 ${sort} 无效, 请使用 0, 1, 2。 默认值为 0`);
    sort = 0;
  }
  if (time !== 0 && time !== 1 && time !== 7 && time !== 30) {
    utils.printError(`发布时间 ${time} 无效, 请使用 0, 1, 7, 30。 默认值为 0`);
    time = 0;
  }
  if (duration !== 0 && duration !== 1 && duration !== 2 && duration !== 3) {
    utils.printError(
      `作品时长 ${duration} 无效, 请使用 0, 1, 2, 3。 默认值为 0`,
    );
    duration = 0;
  }
  if (limit <= 0 || limit > 10000) {
    utils.printError(`搜索数量 ${limit} 无效, 请使用 1-10000。 默认值为 10`);
    limit = 10;
  }
  return [sort, time, duration, limit];
}

module.exports = {
  cleanKeyword,
  isKeywordValid,
  optionFormat,
};
