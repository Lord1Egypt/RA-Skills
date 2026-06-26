#!/usr/bin/env node
"use strict";

const fs = require("fs");
const os = require("os");
const path = require("path");
const crypto = require("crypto");
const http = require("http");
const https = require("https");
const { URL } = require("url");

function emit(type, data) {
  console.log(JSON.stringify({ type, ...data }));
}

function readArg(name) {
  const inline = process.argv.find((arg) => arg.startsWith(`--${name}=`));
  if (inline) {
    return inline.slice(name.length + 3);
  }

  const index = process.argv.findIndex((arg) => arg === `--${name}`);
  if (index >= 0) {
    return process.argv[index + 1] || "";
  }
  return "";
}

function expandHome(filePath) {
  if (!filePath) {
    return filePath;
  }
  if (filePath === "~") {
    return os.homedir();
  }
  if (filePath.startsWith("~/")) {
    return path.join(os.homedir(), filePath.slice(2));
  }
  return filePath;
}

function normalizeHeaders(rawHeaders, contentType) {
  const headers = {};
  if (rawHeaders) {
    let parsed;
    try {
      parsed = JSON.parse(rawHeaders);
    } catch (error) {
      throw new Error(`--headers 不是合法 JSON: ${error.message}`);
    }
    if (!parsed || typeof parsed !== "object" || Array.isArray(parsed)) {
      throw new Error("--headers 必须是 JSON object");
    }
    Object.keys(parsed).forEach((key) => {
      if (parsed[key] !== undefined && parsed[key] !== null) {
        headers[key] = String(parsed[key]);
      }
    });
  }

  if (contentType && !Object.keys(headers).some((key) => key.toLowerCase() === "content-type")) {
    headers["Content-Type"] = contentType;
  }
  return headers;
}

function statReadableFile(filePath) {
  let stat;
  try {
    stat = fs.statSync(filePath);
  } catch (error) {
    return null;
  }
  if (!stat.isFile()) {
    return null;
  }
  try {
    fs.accessSync(filePath, fs.constants.R_OK);
    return stat;
  } catch (error) {
    return null;
  }
}

function uniqPaths(paths) {
  return Array.from(new Set(paths.filter(Boolean)));
}

function resolveSourceFile(filePath, configuredTmpDir) {
  const directStat = statReadableFile(filePath);
  if (directStat) {
    return {
      resolvedPath: filePath,
      stat: directStat,
      usedFallback: false,
      candidates: [filePath],
    };
  }

  const fileName = path.basename(filePath);
  const candidateDirs = uniqPaths([
    path.dirname(filePath),
    configuredTmpDir,
    os.tmpdir(),
    "/tmp",
    "/var/tmp",
  ]);
  const candidates = [filePath];

  for (const dirPath of candidateDirs) {
    const candidatePath = path.join(dirPath, fileName);
    if (!candidates.includes(candidatePath)) {
      candidates.push(candidatePath);
    }
    const stat = statReadableFile(candidatePath);
    if (stat) {
      return {
        resolvedPath: candidatePath,
        stat,
        usedFallback: candidatePath !== filePath,
        candidates,
      };
    }
  }

  throw new Error(`找不到文件: ${filePath}`);
}

function stageFile(sourcePath, tmpDir) {
  fs.mkdirSync(tmpDir, { recursive: true });
  const fileName = path.basename(sourcePath);
  const stagedName = `${Date.now()}-${crypto.randomUUID()}-${fileName}`;
  const stagedPath = path.join(tmpDir, stagedName);
  fs.copyFileSync(sourcePath, stagedPath);
  return stagedPath;
}

function uploadFile({ uploadUrl, headers, filePath, size }) {
  const parsedUrl = new URL(uploadUrl);
  const client = parsedUrl.protocol === "https:" ? https : http;

  return new Promise((resolve, reject) => {
    const request = client.request(
      parsedUrl,
      {
        method: "PUT",
        headers: {
          ...headers,
          "Content-Length": String(size),
        },
      },
      (response) => {
        const chunks = [];
        response.on("data", (chunk) => chunks.push(chunk));
        response.on("end", () => {
          const body = Buffer.concat(chunks).toString("utf8");
          resolve({
            statusCode: response.statusCode || 0,
            headers: response.headers,
            body,
          });
        });
      },
    );

    request.on("error", (error) => {
      reject(error);
    });

    const fileStream = fs.createReadStream(filePath);
    fileStream.on("error", (error) => {
      request.destroy(error);
    });
    fileStream.pipe(request);
  });
}

async function main() {
  const sourceFile = expandHome(String(readArg("file") || "").trim());
  const uploadUrl = String(readArg("upload-url") || "").trim();
  const contentType = String(readArg("content-type") || "").trim();
  const rawHeaders = String(readArg("headers") || "").trim();
  const configuredTmpDir = expandHome(
    String(readArg("tmp-dir") || process.env.KEEP_UPLOAD_TMP_DIR || "~/.keepai/tmp").trim(),
  );
  const keepStagedFile = process.argv.includes("--keep-staged-file");

  if (!sourceFile) {
    emit("error", { message: "缺少 --file 参数" });
    process.exitCode = 1;
    return;
  }
  if (!uploadUrl) {
    emit("error", { message: "缺少 --upload-url 参数" });
    process.exitCode = 1;
    return;
  }

  let stat;
  let resolvedSourceFile = sourceFile;
  let probeCandidates = [];
  let stagedPath = "";
  try {
    const resolved = resolveSourceFile(sourceFile, configuredTmpDir);
    resolvedSourceFile = resolved.resolvedPath;
    stat = resolved.stat;
    probeCandidates = resolved.candidates;
    const headers = normalizeHeaders(rawHeaders, contentType);
    stagedPath = stageFile(resolvedSourceFile, configuredTmpDir);
    const stagedStat = fs.statSync(stagedPath);
    const response = await uploadFile({
      uploadUrl,
      headers,
      filePath: stagedPath,
      size: stagedStat.size,
    });

    if (response.statusCode < 200 || response.statusCode >= 300) {
      emit("error", {
        message: "PUT 上传失败",
        statusCode: response.statusCode,
        responseBody: response.body,
        stagedPath,
      });
      process.exitCode = 1;
      return;
    }

    emit("upload_success", {
      sourceFile,
      resolvedSourceFile,
      usedFallback: resolvedSourceFile !== sourceFile,
      probeCandidates,
      stagedPath,
      tmpDir: configuredTmpDir,
      bytes: stat.size,
      statusCode: response.statusCode,
    });
  } catch (error) {
    emit("error", {
      message: error && error.message ? error.message : String(error),
      sourceFile,
      resolvedSourceFile,
      probeCandidates,
      stagedPath,
      tmpDir: configuredTmpDir,
    });
    process.exitCode = 1;
  } finally {
    if (stagedPath && !keepStagedFile && fs.existsSync(stagedPath)) {
      try {
        fs.unlinkSync(stagedPath);
      } catch (error) {
        emit("warning", {
          message: `清理暂存文件失败: ${error.message}`,
          stagedPath,
        });
      }
    }
  }
}

main();
