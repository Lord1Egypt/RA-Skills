const constants = require("../config/constants");
const { requestApi, pollTaskResult } = require("../utils/request");
const { pickCost, pickTaskId } = require("../utils/cost");
const { SkillError } = require("../utils/errors");

/**
 * @returns {Promise<string|undefined>} Create 成功时的任务 id（uuid）
 */
async function createPostTask(token, url, sort, limit) {
  const response = await requestApi(
    "POST",
    "/api/kuaishou/post/url",
    { _: Date.now() },
    { url, sort, limit },
    token,
    constants.CREATE_MAX_ATTEMPTS,
    "创建任务",
  );
  return pickTaskId(response);
}

/**
 * @param {string} [taskId] Create 返回的任务 id；有则查询只传 id（不带业务字段）
 * @returns {Promise<{ results: object, cost?: number }>}
 */
async function getPostTask(token, url, sort, limit, taskId) {
  const params = taskId ? { id: taskId } : { url, sort, limit };
  const response = await pollTaskResult(
    "/api/kuaishou/post/info",
    params,
    token,
    "查询任务",
  );
  const cost = pickCost(response);
  if (
    typeof response.data !== "object" ||
    response.data === null ||
    Array.isArray(response.data)
  ) {
    throw new SkillError("API_ERROR", "作品结果格式错误: data 不是对象", true);
  }
  return { results: response.data, cost };
}

module.exports = {
  createPostTask,
  getPostTask,
};
