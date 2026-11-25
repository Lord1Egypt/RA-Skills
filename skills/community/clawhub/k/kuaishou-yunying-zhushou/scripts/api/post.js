const constants = require("../config/constants");
const { requestApi, pollTaskResult } = require("../utils/request");
const { SkillError } = require("../utils/errors");

async function createPostTask(token, url, sort, limit) {
  return await requestApi(
    "POST",
    "/api/kuaishou/post/url",
    { _: Date.now() },
    { url, sort, limit },
    token,
    constants.CREATE_MAX_ATTEMPTS,
    "创建任务",
  );
}

async function getPostTask(token, url, sort, limit) {
  const response = await pollTaskResult(
    "/api/kuaishou/post/info",
    { url, sort, limit },
    token,
    "查询任务",
  );
  if (
    typeof response.data !== "object" ||
    response.data === null ||
    Array.isArray(response.data)
  ) {
    throw new SkillError("API_ERROR", "作品结果格式错误: data 不是对象", true);
  }
  return response.data;
}

module.exports = {
  createPostTask,
  getPostTask,
};
