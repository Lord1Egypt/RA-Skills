const utils = require("../utils/utils");

/**
 * 规范抖音视频URL
 * @param {string} url - 输入的URL
 * @returns {string} 规范后的URL
 */
function douyinPostUrl(url) {
  url = url.trim();
  if (url.includes("https://www.douyin.com/note/")) {
    url = url.substring(url.indexOf("https://www.douyin.com/note/"));
  } else if (url.includes("https://www.douyin.com/video/")) {
    url = url.substring(url.indexOf("https://www.douyin.com/video/"));
  } else {
    url = url.replace(/[^a-zA-Z0-9_ -]/g, "");
  }

  if (url.includes(" ")) {
    url = url.substring(0, url.indexOf(" "));
  }
  return url;
}

function optionFormat(limit) {
  limit = Number(limit);
  if (limit < 1 || limit > 10000) {
    utils.printError("获取的评论数量必须在1-10000之间");
    limit = 10;
  }
  return limit;
}

module.exports = {
  douyinPostUrl,
  optionFormat,
};
