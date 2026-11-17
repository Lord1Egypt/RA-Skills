const constants = require("../config/constants");
const { postJson, getJson } = require("../utils/request");
const { withRetry } = require("../utils/retry");
const utils = require("../utils/utils");

async function createPostTask(token, url, sort, limit) {
  return await withRetry(
    async () => {
      return await postJson(
        "/api/kuaishou/post/url",
        { _: Date.now() },
        { url, sort, limit },
        token,
      );
    },
    constants.CREATE_MAX_ATTEMPTS,
    (attempt, err) => {
      utils.printError(
        `【创建任务重试】 ${attempt + 1}/${constants.CREATE_MAX_ATTEMPTS} 次 - ${err.message}`,
      );
    },
  );
}

async function getPostTask(token, url, sort, limit) {
  return await withRetry(
    async () => {
      const res = await getJson(
        "/api/kuaishou/post/info",
        {
          _: Date.now(),
          url,
          sort,
          limit,
        },
        token,
      );
      if (typeof res.data !== "object" || res.data === null) {
        throw new Error(`作品结果格式错误: data 不是对象类型`);
      }
      return res.data;
    },
    constants.QUERY_MAX_ATTEMPTS,
    (attempt, err) => {
      utils.printError(
        `【查询任务重试】 ${attempt + 1}/${constants.QUERY_MAX_ATTEMPTS} 次 - ${err.message}`,
      );
    },
  );
}

module.exports = {
  createPostTask,
  getPostTask,
};
