#!/usr/bin/env node
const clean = require("../utils/clean");
const helper = require("../utils/helper");
const token = require("../utils/token");
const upload = require("../utils/upload");
const utils = require("../utils/utils");
const validator = require("../utils/validator");
const video = require("../api/video");
const constants = require("../config/constants");
const { parseArgs, buildHelp } = require("../utils/args");
const fs = require("fs");
const path = require("path");

const SCHEMA = {
  flags: {
    "--file": {
      alias: "-F",
      key: "file",
      type: "string",
      default: "",
      desc: "本地 mp4，或可直接下载的 mp4 直链",
    },
    "--id": {
      alias: "-I",
      key: "id",
      type: "string",
      default: "",
      desc: "历史视频分析任务ID；传 'last' 可复用上一次任务ID",
    },
    "--prompt": {
      alias: "-P",
      key: "prompt",
      type: "string",
      default: "",
      desc: "视频文案提取/生成的 AI 提示词（总结/改写/金句/翻译等）",
    },
  },
  positionalKey: "file",
};

function printHelp() {
  console.log(
    buildHelp(SCHEMA, "node scripts/video2text/index.js <URL or PATH> [选项]", [
      "node scripts/video2text/index.js -F 'https://cdn.example.com/video.mp4'",
      "node scripts/video2text/index.js 'D:\\video.mp4' -P '总结这个视频的核心观点'",
      "node scripts/video2text/index.js -I last -P '提取视频中的所有金句'",
    ]),
  );
}

function sourceKeyOf(file) {
  if (validator.isUrl(file)) return file.trim();
  return path.resolve(file);
}

function canReusePending(pending, sourceKey, file) {
  if (!pending || pending.sourceKey !== sourceKey || !pending.ossUrl) {
    return false;
  }
  if (Date.now() - Number(pending.savedAt || 0) > constants.EXPIRE_TIME * 1000) {
    return false;
  }
  if (validator.isUrl(file)) return true;
  try {
    const stat = fs.statSync(file);
    return stat.size === pending.size && stat.mtimeMs === pending.mtimeMs;
  } catch (_) {
    return false;
  }
}

function removeTempDownload(filePath) {
  const root = path.resolve(utils.downloadPath());
  const target = path.resolve(filePath);
  if (target !== root && target.startsWith(root + path.sep)) {
    try {
      fs.unlinkSync(target);
    } catch (_) {}
  }
}

async function prepareLocalFile(file) {
  if (!fs.existsSync(file)) {
    throw new Error("文件不存在: " + file);
  }
  if (!validator.isFilePath(file)) {
    throw new Error("不是有效的视频文件: " + file);
  }
  const stat = fs.statSync(file);
  if (stat.size <= 0) {
    throw new Error("视频文件为空: " + file);
  }
  validator.presignFileName(file);
  return { file, stat };
}

async function downloadVideo(file) {
  const filepath = utils.downloadPath();
  await fs.promises.mkdir(filepath, { recursive: true });
  const downloadResult = await helper.download(file, filepath);
  let tempFilePath = downloadResult?.filePath || "";
  if (tempFilePath === "") {
    throw new Error("下载失败: 未返回文件路径");
  }
  tempFilePath = validator.ensureDownloadExtension(tempFilePath);
  try {
    validator.presignFileName(tempFilePath);
  } catch (error) {
    removeTempDownload(tempFilePath);
    throw error;
  }
  const stat = fs.statSync(tempFilePath);
  if (stat.size <= 0) {
    removeTempDownload(tempFilePath);
    throw new Error("下载结果为空");
  }
  utils.printInfo("网络视频已下载到本地: " + tempFilePath);
  return { file: tempFilePath, stat };
}

async function uploadAndRemember(tokenValue, sourceKey, localFile, stat) {
  const fileName = validator.presignFileName(localFile);
  const presignedUrl = await video.getPresignedUrl(tokenValue, fileName);
  if (!presignedUrl || !presignedUrl.url) {
    throw new Error("获取预签名URL失败，请反馈给开发者");
  }
  utils.printInfo("上传文件到安全空间...");
  await upload.uploadFileToOSS(localFile, presignedUrl.url, presignedUrl.headers);
  utils.printInfo("文件上传到安全空间成功，获取视频分析任务ID");
  if (presignedUrl.url.indexOf("?") === -1) {
    throw new Error("预签名URL格式错误，请反馈给开发者");
  }
  const ossUrl = presignedUrl.url.substring(0, presignedUrl.url.indexOf("?"));
  utils.savePendingUpload({
    sourceKey,
    ossUrl,
    size: stat.size,
    mtimeMs: stat.mtimeMs,
    savedAt: Date.now(),
  });
  return ossUrl;
}

async function bindTaskId(tokenValue, ossUrl) {
  try {
    const task = await video.getVideoId(tokenValue, ossUrl);
    if (!task || !task.id) {
      throw new Error("获取视频分析任务ID失败，请反馈给开发者");
    }
    utils.clearPendingUpload();
    utils.saveLastTask(task.id);
    utils.printInfo(
      "视频分析任务 ID: " +
        task.id +
        "。可用 --id 或 --id last 继续查询；更换提示词会重新解析并计费",
    );
    return task.id;
  } catch (error) {
    if (error && error.noRetry) utils.clearPendingUpload();
    throw error;
  }
}

function printStillProcessing(id, prompt) {
  utils.saveLastTask(id);
  utils.printError("视频仍在处理中。本轮轮询已结束，任务会在服务端继续");
  utils.printInfo("任务 ID: " + id);
  const cmd = prompt
    ? `node scripts/video2text/index.js --id last --prompt ${JSON.stringify(prompt)}`
    : "node scripts/video2text/index.js --id last";
  utils.printInfo("请使用相同提示词继续等待，更换提示词会重新解析并计费:");
  utils.printInfo(cmd);
}

async function main() {
  try {
    await clean.deleteExpire();
  } catch (_) {}

  const args = process.argv.slice(2);
  if (args.length === 0) {
    printHelp();
    process.exit(1);
  }

  let parsed;
  try {
    parsed = parseArgs(args, SCHEMA);
  } catch (error) {
    utils.printError(`参数解析错误: ${error.message || String(error)}`);
    printHelp();
    process.exit(1);
  }
  if (parsed._help) {
    printHelp();
    process.exit(0);
  }
  if (Array.isArray(parsed._warnings)) {
    parsed._warnings.forEach((warning) => utils.printWarn(warning));
  }

  let { file, id, prompt } = parsed;

  if (id === "last") {
    const last = utils.loadLastTask();
    if (!last) {
      utils.printError("未找到上一次的视频分析任务ID，请先使用 --file 处理一个视频");
      process.exit(1);
    }
    id = last;
  }

  if (id && file) {
    utils.printWarn("同时传入 --file 与 --id，以 --id 为准，已忽略 --file");
  }

  if ([...prompt].length > 1000) {
    utils.printError("提示词不能超过 1000 个字符");
    process.exit(1);
  }

  utils.printBanner();

  const tokenValue = token.skillToken(process.env.GUAIKEI_API_TOKEN);
  if (tokenValue === "") process.exit(3);

  if (!id) {
    if (!file) {
      utils.printError("缺少视频来源：请通过 --file 指定 mp4 直链或本地 mp4，或通过 --id 指定历史任务ID");
      process.exit(1);
    }

    const sourceKey = sourceKeyOf(file);
    const pending = utils.loadPendingUpload();
    try {
      let ossUrl = "";
      if (canReusePending(pending, sourceKey, file)) {
        ossUrl = pending.ossUrl;
        utils.printInfo("上次文件已上传，继续获取视频分析任务 ID");
      } else {
        const prepared = validator.isUrl(file)
          ? await downloadVideo(file)
          : await prepareLocalFile(file);
        ossUrl = await uploadAndRemember(
          tokenValue,
          sourceKey,
          prepared.file,
          prepared.stat,
        );
      }
      id = await bindTaskId(tokenValue, ossUrl);
    } catch (error) {
      utils.printError(
        "视频分析任务ID获取失败: " + (error.message || String(error)),
      );
      process.exit(1);
    }
  }

  try {
    const text = await video.getVideoText(tokenValue, id, prompt);
    utils.saveLastTask(id);
    utils.printInfo("视频文案获取成功，文案内容如下：");
    console.log(text.text);
  } catch (error) {
    if (error && error.code === "STILL_PROCESSING") {
      printStillProcessing(id, prompt);
      process.exit(2);
    }
    utils.printError(error.message || String(error));
    process.exit(1);
  }
}

main().catch((error) => {
  utils.printError(error.message || String(error));
  process.exit(1);
});
