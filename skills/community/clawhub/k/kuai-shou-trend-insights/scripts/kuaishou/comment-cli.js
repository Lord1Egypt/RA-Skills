#!/usr/bin/env node

const constants = require("../config/constants");
const log = require("../utils/log");
const comment = require("../api/comment");
const token = require("../utils/token");
const utils = require("../utils/utils");
const validator = require("../validate/url");
const { parseArgs, buildHelp } = require("../utils/args");

const SCHEMA = {
  flags: {
    "--url": {
      alias: "-U",
      key: "url",
      type: "string",
      required: true,
      desc: "快手视频URL或视频ID",
    },
    "--limit": {
      alias: "-L",
      key: "limit",
      type: "number",
      default: 10,
      transform: (v) => Number(v),
      desc: "评论数量, 0-10000",
    },
  },
  positionalKey: "url",
};

function printHelp() {
  console.error(
    buildHelp(
      SCHEMA,
      "node scripts/kuaishou/comment-cli.js <视频URL或视频ID> [选项]",
      [
        "node scripts/kuaishou/comment-cli.js -U 3xxxx",
        'node scripts/kuaishou/comment-cli.js -U "https://www.kuaishou.com/short-video/3xxxx"',
        "node scripts/kuaishou/comment-cli.js --url 3xxxx --limit 100",
      ],
    ),
  );
}

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
  if (!validator.isVideoUrl(url)) {
    utils.printError(`URL格式错误: ${url}`);
    printHelp();
    process.exit(1);
  }
  url = validator.normalizeUrl(url);
  utils.printInfo(`规范后的URL: ${url}`);
  if (limit < 1 || limit > 10000) {
    utils.printError(`评论数量参数错误: ${limit}`);
    printHelp();
    process.exit(1);
  }

  const tokenValue = token.skillToken(process.env.GUAIKEI_API_TOKEN);
  if (tokenValue === "") process.exit(3);

  let commentTask = null;
  try {
    commentTask = await comment.createCommentTask(tokenValue, url, limit);
    utils.printSuccess("获取评论任务创建成功, 正在查询中...");

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
      skill_metadata: {
        skill_version: constants.VERSION,
        runtime_version: process.versions.node,
        execution_time: Date.now() - startTime,
      },
      results: null,
    };
    process.stdout.write(JSON.stringify(errorOutput, null, 2) + "\n", () =>
      process.exit(1),
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
      skill_metadata: {
        skill_version: constants.VERSION,
        runtime_version: process.versions.node,
        execution_time: Date.now() - startTime,
      },
      results: null,
    };
    process.stdout.write(JSON.stringify(emptyOutput, null, 2) + "\n", () =>
      process.exit(1),
    );
    return;
  }

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
    skill_metadata: {
      skill_version: constants.VERSION,
      runtime_version: process.versions.node,
      execution_time: Date.now() - startTime,
    },
    results: commentTask,
  };
  console.log(JSON.stringify(finalOutput, null, 2));
  utils.printSuccess(`获取评论任务完成, 共获取 ${commentTask.length} 条评论`);

  url = validator.url2Name(url);
  await log.taskWrite(
    `${startTime}_${url}_comment.json`,
    JSON.stringify(finalOutput, null, 2),
  );
}

main().catch((error) => {
  utils.printError(error.message);
  process.exit(1);
});
