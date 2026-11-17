const constants = require("../config/constants");
const { postJson, getJson } = require("../utils/request");
const { withRetry } = require("../utils/retry");
const utils = require("../utils/utils");

async function createCommentTask(token, url, limit) {
  return await withRetry(
    async () => {
      return await postJson(
        "/api/kuaishou/comment/url",
        { _: Date.now() },
        { url, limit },
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

async function getCommentTask(token, url, limit) {
  return await withRetry(
    async () => {
      const res = await getJson(
        "/api/kuaishou/comment/info",
        {
          _: Date.now(),
          url,
          limit,
        },
        token,
      );
      if (!Array.isArray(res.data)) {
        throw new Error(`评论结果格式错误: data 不是数组类型`);
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
  createCommentTask,
  getCommentTask,
};
