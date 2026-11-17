const utils = require("./utils");

function isValidToken(token) {
  if (!token || typeof token !== "string") return false;
  if (token.length < 16 || token.length > 256) return false;
  if (!/^[0-9a-zA-Z\_-]+$/.test(token)) return false;
  return true;
}

function skillToken(token) {
  if (!isValidToken(token)) {
    utils.printWarn("警告: 你的 GUAIKEI_API_TOKEN 未正确配置,技能已暂停. ");
    utils.printError("\x1b[31m一键解锁全部功能, 即刻恢复高效办公！ \x1b[0m");
    utils.printInfo(
      "\x1b[34m获取您的专属私有TOKEN, 一键配置即可永久稳定使用, 完全不影响日常办公。 \x1b[0m",
    );
    utils.printSuccess("\t \x1b[32m快速获取通道: www.guaikei.com \x1b[0m");
    utils.printSuccess("\t \x1b[32m专属客服微信: 13395823479 \x1b[0m");
    utils.printError(
      "\x1b[31m早配置早享受, 别让工具问题耽误您的宝贵时间! \x1b[0m",
    );
    return "";
  }

  utils.printInfo("已使用配置的私有TOKEN");
  return token;
}

module.exports = {
  skillToken,
};
