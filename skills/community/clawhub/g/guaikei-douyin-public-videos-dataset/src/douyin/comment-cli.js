#!/usr/bin/env node

const constants = require("../config/constants");
const comment = require("../api/comment");
const log = require("../utils/log");
const token = require("../utils/token");
const utils = require("../utils/utils");
const validator = require("../validate/comment");
const { ApiError } = require("../utils/errors");
const { parseArgs, buildHelp } = require("../utils/args");

const SCHEMA = {
  flags: {
    "--url": {
      alias: "-u",
      key: "url",
      type: "string",
      required: true,
      desc: "抖音视频(或图文)URL或aweme_id",
    },
    "--limit": {
      alias: "-l",
      key: "limit",
      type: "number",
      default: 10,
      transform: (v) => Number(v),
      desc: "评论数量, 1-10000",
    },
  },
  positionalKey: "url",
};

function printHelp() {
  console.log(
    buildHelp(SCHEMA, "node src/douyin/comment-cli.js <url> [选项]", [
      "node src/douyin/comment-cli.js https://www.douyin.com/video/xxx",
      "node src/douyin/comment-cli.js --url https://www.douyin.com/note/xxx --limit 20",
      "node src/douyin/comment-cli.js -u xxx --limit 100",
    ]),
  );
}

/**
 * 主函数 - 获取抖音作品的评论列表
 */
async function main() {
  const startTime = Date.now();
  const args = process.argv.slice(2);
  if (args.length === 0) {
    printHelp();
    process.exit(0);
  }

  let parsed;
  try {
    parsed = parseArgs(args, SCHEMA);
  } catch (error) {
    utils.printError(`参数解析错误: ${error.message}`);
    printHelp();
    process.exit(1);
  }
  if (parsed._help) {
    printHelp();
    process.exit(0);
  }

  let { url, limit } = parsed;

  utils.printBanner();
  utils.printInfo(`原始URL: ${url}`);
  url = validator.douyinPostUrl(url);
  utils.printInfo(`规范后的URL: ${url}`);
  limit = validator.optionFormat(limit);
  const tokenValue = token.skillToken(process.env.GUAIKEI_API_TOKEN);
  if (tokenValue === "") process.exit(3);
  let commentTask = null;
  try {
    const status = await comment.createCommentTask(tokenValue, url, limit);
    utils.printSuccess(`获取评论任务创建成功, 正在获取评论中...`);

    commentTask = await comment.getCommentTask(tokenValue, url, limit);
  } catch (error) {
    utils.printError(`获取评论失败: ${error.message}`);
    const errorOutput = {
      status: "error",
      error_code: error.code || "UNKNOWN",
      message: error.message,
      timestamp: new Date().toLocaleString(),
      request: {
        command: "comment",
        url: url,
        limit: limit,
      },
      metadata: {
        skill_version: constants.VERSION,
        runtime_version: process.versions.node,
        execution_time: Date.now() - startTime,
      },
      results: null,
    };
    const exitCode = error.name === "AuthError" ? 3 : 1;
    process.stdout.write(JSON.stringify(errorOutput, null, 2) + "\n", () =>
      process.exit(exitCode),
    );
    return;
  }

  if (!commentTask || !Array.isArray(commentTask) || commentTask.length === 0) {
    utils.printError(`获取评论任务没有返回结果, 请稍后重试或联系开发者`);
    const emptyOutput = {
      status: "empty",
      error_code: "NO_MATCH",
      message: "没有找到匹配的评论",
      timestamp: new Date().toLocaleString(),
      request: {
        command: "comment",
        url: url,
        limit: limit,
      },
      metadata: {
        skill_version: constants.VERSION,
        runtime_version: process.versions.node,
        execution_time: Date.now() - startTime,
      },
      results: null,
    };
    process.stdout.write(JSON.stringify(emptyOutput, null, 2) + "\n", () =>
      process.exit(0),
    );
    return;
  }

  // 输出评论结果
  const finalOutput = {
    status: "success",
    error_code: "OK",
    message: "获取评论任务完成",
    timestamp: new Date().toLocaleString(),
    request: {
      command: "comment",
      url: url,
      limit: limit,
    },
    metadata: {
      skill_version: constants.VERSION,
      runtime_version: process.versions.node,
      execution_time: Date.now() - startTime,
    },
    results: commentTask,
  };
  console.log(JSON.stringify(finalOutput, null, 2));
  utils.printSuccess(
    `获取评论任务完成, 共返回 ${finalOutput.results.length} 条结果`,
  );

  url = url.replace(/[^a-zA-Z0-9_-]/g, "");
  url = url.replace("httpswwwdouyincomvideo", "");
  url = url.replace("httpswwwdouyincomnote", "");
  await log.taskWrite(
    `${startTime}_${url}_comment.json`,
    JSON.stringify(finalOutput, null, 2),
  );
}

main().catch((error) => {
  utils.printError(error.message);
  process.exit(1);
});
