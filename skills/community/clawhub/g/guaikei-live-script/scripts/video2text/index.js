#!/usr/bin/env node
const clean = require("../utils/clean");
const helper = require("../utils/helper");
const token = require("../utils/token");
const upload = require("../utils/upload");
const utils = require("../utils/utils");
const validator = require("../utils/validator");
const video = require("../api/video");
const { parseArgs, buildHelp } = require("../utils/args");
const fs = require("fs");

const SCHEMA = {
  flags: {
    "--file": {
      alias: "-F",
      key: "file",
      type: "string",
      default: "",
      desc: "视频 URL 或本地文件路径",
    },
    "--id": {
      alias: "-I",
      key: "id",
      type: "string",
      default: "",
      desc: "历史视频分析任务ID；传 'last' 可复用上一次成功获取的任务ID",
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
      "node scripts/video2text/index.js -F 'http://v18.xhscdn.com/stream/.*.mp4'",
      "node scripts/video2text/index.js -F 'D:\\video2txt.mp4' -P '总结这个视频的核心观点'",
      "node scripts/video2text/index.js -I last -P '提取视频中的所有金句'",
    ]),
  );
}

async function main() {
  // 清理临时文件（非关键，吞掉异常，避免影响主流程）
  try {
    await clean.deleteExpire();
  } catch (_) {}

  const args = process.argv.slice(2);
  if (args.length === 0) {
    printHelp();
    return;
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

  let { file, id, prompt } = parsed;

  // 解析 --id last：复用上一次成功获取的任务ID
  if (id === "last") {
    const last = utils.loadLastTask();
    if (!last) {
      utils.printError("未找到上一次的视频分析任务ID，请先使用 --file 处理一个视频");
      process.exit(1);
    }
    id = last;
  }

  utils.printBanner();

  const tokenValue = token.skillToken(process.env.GUAIKEI_API_TOKEN);
  if (tokenValue === "") process.exit(3);

  // 没有任务ID时，需要先下载（仅 URL）+ 上传，获取任务ID
  if (!id) {
    if (!file) {
      utils.printError("缺少视频来源：请通过 --file 指定视频链接/路径，或通过 --id 指定历史任务ID");
      process.exit(1);
    }

    if (validator.isUrl(file)) {
      const filepath = utils.downloadPath();
      try {
        await fs.promises.mkdir(filepath, { recursive: true });
      } catch (error) {
        utils.printError("临时下载目录创建失败: " + (error.message || String(error)));
        process.exit(1);
      }

      try {
        const downloadResult = await helper.download(file, filepath);
        let tempFilePath = downloadResult?.filePath || "";
        if (tempFilePath === "") {
          utils.printError("下载失败: 未返回文件路径");
          process.exit(1);
        }
        // 下载文件缺少扩展名时统一补 .mp4，便于服务端识别视频类型
        if (tempFilePath.indexOf(".") === -1) {
          try {
            fs.renameSync(tempFilePath, tempFilePath + ".mp4");
            tempFilePath += ".mp4";
          } catch (renameError) {
            utils.printWarn("文件重命名失败: " + renameError.message);
          }
        }
        utils.printInfo("网络视频已下载到本地: " + tempFilePath);
        file = tempFilePath;
      } catch (error) {
        utils.printError("下载失败: " + (error.message || String(error)));
        process.exit(1);
      }
    } else if (!validator.isFilePath(file)) {
      utils.printError("无效的文件路径或URL");
      process.exit(1);
    }

    if (!fs.existsSync(file)) {
      utils.printError("文件不存在: " + file);
      process.exit(1);
    }

    try {
      const presignedUrl = await video.getPresignedUrl(tokenValue, file);
      if (!presignedUrl || !presignedUrl?.url || presignedUrl.url === "") {
        throw new Error("获取预签名URL失败，请反馈给开发者");
      }

      utils.printInfo("上传文件到安全空间...");
      await upload.uploadFileToOSS(file, presignedUrl.url, presignedUrl.headers);
      utils.printInfo("文件上传到安全空间成功，获取视频分析任务ID");

      if (presignedUrl.url.indexOf("?") === -1) {
        throw new Error("预签名URL格式错误，请反馈给开发者");
      }
      const url = presignedUrl.url.substring(0, presignedUrl.url.indexOf("?"));
      const task = await video.getVideoId(tokenValue, url);
      if (!task || !task?.id || task.id === "") {
        throw new Error("获取视频分析任务ID失败，请反馈给开发者");
      }
      utils.printInfo(
        "视频分析任务ID获取成功: 【" +
          task.id +
          "】，一小时内可复用该任务ID基于不同提示词再次分析",
      );
      // 记录最近一次任务ID，支持 --id last
      utils.saveLastTask(task.id);
      id = task.id;
    } catch (error) {
      utils.printError(
        "视频分析任务ID获取失败: " + (error.message || String(error)),
      );
      process.exit(1);
    }
  }

  // 已有任务ID，获取视频文案（核心输出）
  try {
    const text = await video.getVideoText(tokenValue, id, prompt);
    if (!text || !text?.text || text.text === "") {
      throw new Error("获取视频文案失败，请反馈给开发者");
    }
    utils.printInfo("视频文案获取成功，文案内容如下：");
    console.log(text.text);
  } catch (error) {
    utils.printError(error.message || String(error));
    process.exit(1);
  }
}

main().catch((error) => {
  utils.printError(error.message || String(error));
  process.exit(1);
});
