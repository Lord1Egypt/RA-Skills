const constants = require("../config/constants");
const { requestApi } = require("../utils/request");

/**
 * 获取文件上传的预签名URL和授权Headers
 * @param {string} token API令牌
 * @param {string} filename 文件完整路径
 * @returns {Promise<{url: string, headers: object} | null>} 预签名上传信息，包含url和headers；失败返回null
 * @throws {Error} 网络错误或认证失败时抛出
 */
async function getPresignedUrl(token, filename) {
  if (!token || typeof token !== "string") {
    throw new Error("token 必须是非空字符串");
  }
  if (!filename || typeof filename !== "string") {
    throw new Error("filename 必须是非空字符串");
  }

  const data = { file: filename };

  const response = await requestApi(
    "/api/video/presign",
    token,
    data,
    constants.CREATE_MAX_ATTEMPTS,
    "预上传",
  );
  if (response.data) {
    return response.data;
  } else {
    throw new Error("获取预签名上传信息失败");
  }
}

/**
 * 获取视频分析任务ID
 * @param {string} token API令牌
 * @param {string} url 视频上传后的URL（不含查询参数）
 * @returns {Promise<{id: string} | null>} 包含视频分析任务ID的对象；失败返回null
 * @throws {Error} 网络错误或认证失败时抛出
 */
async function getVideoId(token, url) {
  if (!token || typeof token !== "string") {
    throw new Error("token 必须是非空字符串");
  }
  if (!url || typeof url !== "string") {
    throw new Error("url 必须是非空字符串");
  }

  const data = { url };

  const response = await requestApi(
    "/api/video/id",
    token,
    data,
    constants.CREATE_MAX_ATTEMPTS,
    "视频ID",
  );
  if (response.data) {
    return response.data;
  } else {
    throw new Error("获取视频分析任务ID失败");
  }
}

/**
 * 获取视频分析文案
 * @param {string} token API令牌
 * @param {string} id 视频分析任务ID
 * @param {string} [prompt=""] 提示词，用于指导AI生成文案的风格或内容要求
 * @returns {Promise<{text: string} | null>} 包含视频文案的对象；失败返回null
 * @throws {Error} 网络错误或认证失败时抛出
 */
async function getVideoText(token, id, prompt = "") {
  if (!token || typeof token !== "string") {
    throw new Error("token 必须是非空字符串");
  }
  if (!id || typeof id !== "string") {
    throw new Error("id 必须是非空字符串");
  }

  const data = { id, prompt };

  const response = await requestApi(
    "/api/video/text",
    token,
    data,
    constants.QUERY_MAX_ATTEMPTS,
    "视频文案",
  );
  if (response.data) {
    return response.data;
  } else {
    throw new Error("获取视频文案失败");
  }
}

module.exports = {
  getPresignedUrl,
  getVideoId,
  getVideoText,
};
