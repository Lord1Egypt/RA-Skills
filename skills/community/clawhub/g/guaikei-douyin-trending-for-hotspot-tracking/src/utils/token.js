/**
 * TOKEN管理模块
 */
const utils = require("./utils");

/**
 * 验证 TOKEN 格式
 * @param {string} token - 待验证的 TOKEN
 * @returns {boolean} 是否有效
 */
function isValidToken(token) {
  if (!token || typeof token !== "string") return false;
  if (token.length < 16 || token.length > 256) return false;
  if (!/^[0-9a-zA-Z\_-]+$/.test(token)) return false;
  return true;
}

/**
 * 获取有效的技能令牌
 * @param {string|undefined} token - 环境变量中的技能令牌
 * @returns {string} 有效令牌
 */
function skillToken(token) {
  if (!isValidToken(token)) {
    utils.printWarn("警告: 你的 GUAIKEI_API_TOKEN 未正确配置,技能已暂停. ");
    utils.printSuccess("\t快速获取通道: www.guaikei.com");
    return "";
  }

  utils.printInfo("已使用配置的私有TOKEN");
  return token;
}

module.exports = {
  skillToken,
};
