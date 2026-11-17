const constants = require("../config/constants");
const utils = require("../utils/utils");
const { skillName } = require("../utils/name");
const https = require("https");
const querystring = require("querystring");

async function request(options, data = null) {
  return new Promise((resolve, reject) => {
    let timedOut = false;

    const req = https.request(
      { ...options, timeout: constants.REQUEST_TIMEOUT },
      (res) => {
        res.setEncoding("utf-8");
        let body = "";
        res.on("data", (chunk) => (body += chunk));
        res.on("end", () => {
          if (res.statusCode >= 200 && res.statusCode < 300) {
            try {
              const jsonBody = JSON.parse(body);
              if (jsonBody.errcode === 0) {
                resolve(jsonBody);
              } else {
                let e = new Error(
                  `请求失败, 错误码: ${jsonBody?.errcode || 1}, 错误信息: ${jsonBody?.errmsg || "未知错误"}`,
                );
                reject(e);
              }
            } catch (error) {
              reject(new Error(`响应解析失败: ${error.message}`));
            }
          } else if (res.statusCode === 401 || res.statusCode === 403) {
            const e = new Error(
              "GUAIKEI_API_TOKEN 无效, 请检查环境变量 或 联系微信: 13395823479 获取解决方案",
            );
            e.noRetry = true;
            reject(e);
          } else {
            reject(new Error(`请求失败 状态码: ${res.statusCode}`));
          }
        });
      },
    );

    req.on("error", (error) => {
      if (timedOut) {
        return;
      }
      if (error.code === "ETIMEDOUT" || error.code === "ECONNRESET") {
        reject(new Error("请求超时或连接被重置"));
      } else {
        reject(new Error(`网络错误: ${error.message}`));
      }
    });

    req.on("timeout", () => {
      timedOut = true;
      req.destroy();
      reject(new Error(`请求超时, ${constants.REQUEST_TIMEOUT}ms`));
    });

    if (data) {
      req.write(data);
    }
    req.end();
  });
}

async function postJson(path, token, data) {
  if (!path || typeof path !== "string") {
    throw new Error("路径 必须是非空字符串");
  }
  if (!token || typeof token !== "string") {
    throw new Error("token 必须是非空字符串");
  }
  if (!data || typeof data !== "object") {
    throw new Error("数据 必须是对象");
  }

  const params = { _: Date.now(), skill_name: skillName() };
  const fullPath = `${path}?${querystring.stringify(params)}`;
  const jsonData = JSON.stringify(data);

  const options = {
    host: constants.BASE_URL,
    path: fullPath,
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Content-Length": Buffer.byteLength(jsonData),
      TOKEN: token,
    },
  };

  return await request(options, jsonData);
}

async function withRetry(fn, maxAttempts, errorHandler) {
  let lastError;
  for (let attempt = 0; attempt < maxAttempts; attempt++) {
    try {
      return await fn(attempt);
    } catch (error) {
      lastError = error;
      if (error && error.noRetry) {
        throw error;
      }
      if (errorHandler) errorHandler(attempt, error);
      if (attempt < maxAttempts - 1) {
        const delay = Math.min(
          Math.pow(2, attempt) * constants.RETRY_INTERVAL,
          60000,
        );
        await new Promise((resolve) => setTimeout(resolve, delay));
      }
    }
  }
  throw lastError || new Error(`重试 ${maxAttempts} 次后失败`);
}

/**
 * 支持重试的API请求方法
 */
async function requestApi(path, token, data, maxAttempts, actionName) {
  return await withRetry(
    async () => {
      return await postJson(path, token, data);
    },
    maxAttempts,
    (attempt, error) => {
      utils.printError(
        `【${actionName}重试】${attempt + 1}/${maxAttempts} 次 - ${error.message}`,
      );
    },
  );
}
module.exports = { requestApi };
