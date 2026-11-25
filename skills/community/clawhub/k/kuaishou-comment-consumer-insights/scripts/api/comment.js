const constants = require("../config/constants");
const { requestApi, pollTaskResult } = require("../utils/request");
const { pickCost } = require("../utils/cost");
const { SkillError } = require("../utils/errors");

async function createCommentTask(token, url, limit) {
  return await requestApi(
    "POST",
    "/api/kuaishou/comment/url",
    { _: Date.now() },
    { url, limit },
    token,
    constants.CREATE_MAX_ATTEMPTS,
    "创建任务",
  );
}

async function getCommentTask(token, url, limit) {
  const response = await pollTaskResult(
    "/api/kuaishou/comment/info",
    { url, limit },
    token,
    "查询任务",
  );
  const cost = pickCost(response);
  if (!Array.isArray(response.data)) {
    throw new SkillError("API_ERROR", "评论结果格式错误: data 不是数组", true);
  }
  return { results: response.data, cost };
}

module.exports = {
  createCommentTask,
  getCommentTask,
};
