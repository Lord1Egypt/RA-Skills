const constants = require("../config/constants");
const { requestApi, pollTaskResult } = require("../utils/request");
const { pickCost, pickTaskId } = require("../utils/cost");
const { SkillError } = require("../utils/errors");

/**
 * @returns {Promise<string|undefined>} Create 成功时的任务 id（uuid）；缺失则查询仅带业务字段
 */
async function createSearchTask(token, keyword, sort, time, duration, limit) {
  const response = await requestApi(
    "POST",
    "/api/kuaishou/search/keyword",
    { _: Date.now() },
    { keyword, sort, time, duration, limit },
    token,
    constants.CREATE_MAX_ATTEMPTS,
    "创建任务",
  );
  return pickTaskId(response);
}

/**
 * @param {string} [taskId] Create 返回的任务 id；有则查询只传 id（不带业务字段）
 * @returns {Promise<{ results: Array, cost?: number }>}
 */
async function getSearchTask(
  token,
  keyword,
  sort,
  time,
  duration,
  limit,
  taskId,
) {
  const params = taskId
    ? { id: taskId }
    : { keyword, sort, time, duration, limit };
  const response = await pollTaskResult(
    "/api/kuaishou/search/info",
    params,
    token,
    "查询任务",
  );
  const cost = pickCost(response);
  if (!Array.isArray(response.data)) {
    throw new SkillError("API_ERROR", "搜索结果格式错误: data 不是数组", true);
  }
  return { results: response.data, cost };
}

module.exports = {
  createSearchTask,
  getSearchTask,
};
