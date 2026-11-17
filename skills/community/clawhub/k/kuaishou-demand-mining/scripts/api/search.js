const constants = require("../config/constants");
const { requestApi, pollTaskResult } = require("../utils/request");
const { SkillError } = require("../utils/errors");

async function createSearchTask(token, keyword, sort, time, duration, limit) {
  return await requestApi(
    "POST",
    "/api/kuaishou/search/keyword",
    { _: Date.now() },
    { keyword, sort, time, duration, limit },
    token,
    constants.CREATE_MAX_ATTEMPTS,
    "创建任务",
  );
}

async function getSearchTask(token, keyword, sort, time, duration, limit) {
  const response = await pollTaskResult(
    "/api/kuaishou/search/info",
    { keyword, sort, time, duration, limit },
    token,
    "查询任务",
  );
  if (!Array.isArray(response.data)) {
    throw new SkillError("API_ERROR", "搜索结果格式错误: data 不是数组", true);
  }
  return response.data;
}

module.exports = {
  createSearchTask,
  getSearchTask,
};
