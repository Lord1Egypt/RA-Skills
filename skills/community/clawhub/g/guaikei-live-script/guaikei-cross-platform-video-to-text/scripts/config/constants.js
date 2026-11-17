const pkg = require("../../package.json");
module.exports = {
  BASE_URL: "www.guaikei.com",
  REQUEST_TIMEOUT: 20000, // 请求超时时间（毫秒）
  CREATE_MAX_ATTEMPTS: 3, // 创建操作最大重试次数
  QUERY_MAX_ATTEMPTS: 30, // 查询视频分析文案最大重试次数, 异步任务，最多重试30次
  RETRY_INTERVAL: 2000, // 重试基础间隔（毫秒）
  EXPIRE_TIME: 60 * 60 * 24, // 临时文件过期时间 = 24小时
  VERSION: pkg.version,
};
