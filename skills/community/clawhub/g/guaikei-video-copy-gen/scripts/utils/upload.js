const constants = require("../config/constants");
const helper = require("../utils/helper");
const utils = require("../utils/utils");
const https = require("https");
const fs = require("fs");

/**
 * 上传文件到安全空间，技能开发者、服务提供方，承诺上传后的视频，不外泄、不转存、不另作他用、仅用于视频转文案服务，且在视频转文案完成后自动删除
 */
async function uploadFileToOSS(filename, presignedUrl, headers) {
  const url = new URL(presignedUrl);
  if (url.protocol !== "https:") {
    throw new Error("上传URL必须是HTTPS协议");
  }
  return new Promise((resolve, reject) => {
    const fileStats = fs.statSync(filename);
    const totalSize = fileStats.size;
    let uploadedSize = 0;
    let settled = false;

    const fileStream = fs.createReadStream(filename);

    // 复制预签名 headers，并补充 OSS PUT 必需字段
    const uploadHeaders = Object.assign({}, headers);
    // 关键修复：明确 Content-Length，否则 Node 对流式 body 默认使用 chunked
    // Transfer-Encoding，阿里云 OSS 预签名 PUT 通常会拒绝而返回 400/403
    uploadHeaders["Content-Length"] = String(totalSize);
    if (!uploadHeaders["Content-Type"]) {
      uploadHeaders["Content-Type"] = "application/octet-stream";
    }

    const options = {
      host: url.hostname,
      path: url.pathname + url.search,
      method: "PUT",
      headers: uploadHeaders,
    };
    const req = https.request(
      { ...options, timeout: constants.REQUEST_TIMEOUT },
      (res) => {
        let body = "";
        res.on("data", (chunk) => (body += chunk));
        res.on("end", () => {
          if (settled) return;
          settled = true;
          fileStream.destroy();
          if (res.statusCode >= 200 && res.statusCode < 300) {
            helper.inlineLog(`文件上传成功, ${helper.byteHumanize(totalSize)}`);
            resolve(body);
          } else {
            reject(
              new Error(
                `文件上传失败, 状态码: ${res.statusCode}, 响应体: ${body}`,
              ),
            );
          }
        });
        res.on("error", (error) => {
          if (settled) return;
          settled = true;
          fileStream.destroy();
          req.destroy();
          utils.printError(`上传响应读取失败: ${error.message}`);
          reject(new Error(`上传响应读取失败: ${error.message}`));
        });
      },
    );
    fileStream.on("data", (chunk) => {
      uploadedSize += chunk.length;
      helper.inlineLog(
        `上传进度: ${helper.byteHumanize(uploadedSize)} / ${helper.byteHumanize(totalSize)}`,
      );
    });

    fileStream.on("error", (error) => {
      if (settled) return;
      settled = true;
      req.destroy();
      utils.printError(`上传读取文件失败: ${error.message}`);
      reject(error);
    });

    req.on("error", (error) => {
      if (settled) return;
      settled = true;
      fileStream.destroy();
      utils.printError(`上传请求失败: ${error.message}`);
      reject(error);
    });

    req.on("timeout", () => {
      if (settled) return;
      settled = true;
      fileStream.destroy();
      req.destroy();
      utils.printError(`上传请求超时: ${constants.REQUEST_TIMEOUT}ms`);
      reject(new Error("上传请求超时"));
    });

    fileStream.pipe(req);
  });
}

module.exports = { uploadFileToOSS };
