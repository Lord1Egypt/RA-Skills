#!/usr/bin/env node

const log = require("../utils/log");
const comment = require("../api/comment");
const token = require("../utils/token");
const utils = require("../utils/utils");
const validator = require("../validate/url");
const { assertIntegerRange } = require("../validate/keyword");
const { parseArgs, buildHelp } = require("../utils/args");
const {
  emitError,
  emitEmpty,
  printSuccessEnvelope,
  emitUncaught,
} = require("../utils/output");

const SCHEMA = {
  flags: {
    "--url": {
      alias: "-u",
      key: "url",
      type: "string",
      required: true,
      desc: "快手视频链接或 3x 视频 id",
    },
    "--limit": {
      alias: "-l",
      key: "limit",
      type: "number",
      default: 10,
      transform: (v) => Number(v),
      desc: "评论数量, 1-10000；包月 Token 实际最多 60",
    },
  },
  positionalKey: "url",
};

const AUTH_MESSAGE =
  "GUAIKEI_API_TOKEN 未配置或格式无效。须为 16-256 位字母、数字、下划线或连字符";

function printHelp() {
  process.stderr.write(
    buildHelp(
      SCHEMA,
      "node scripts/kuaishou/comment-cli.js <视频链接或视频id> [选项]",
      [
        'node scripts/kuaishou/comment-cli.js --url "https://www.kuaishou.com/short-video/3xabc" --limit 40',
        "node scripts/kuaishou/comment-cli.js --url 3xabc --limit 40",
      ],
    ) +
      "\n\n注意:\n" +
      "  - 这是视频链接或 3x 视频 id，不是博主主页，也不是纯数字 user_id\n" +
      "  - 数量 1-10000；包月 Token 实际最多 60，超限返回 PLAN_LIMIT\n" +
      "  - 数量若不在 1-10000，命令会直接失败，不会改成默认值后继续请求\n",
  );
}

async function main() {
  const startTime = Date.now();
  const args = process.argv.slice(2);
  if (args.length === 0) {
    printHelp();
    emitError("comment", "INVALID_ARGS", "缺少命令参数", 2, startTime);
    return;
  }

  let parsed;
  try {
    parsed = parseArgs(args, SCHEMA);
  } catch (error) {
    utils.printError(`参数解析错误: ${error.message}`);
    printHelp();
    emitError(
      "comment",
      "INVALID_ARGS",
      `参数解析错误: ${error.message}`,
      2,
      startTime,
    );
    return;
  }
  if (parsed._help) {
    printHelp();
    return;
  }

  let { url, limit } = parsed;
  const urlRaw = url;

  utils.printBanner();
  utils.printInfo(`原始链接: ${urlRaw}`);
  try {
    url = validator.resolveVideoUrl(url);
  } catch (error) {
    utils.printError(error.message);
    emitError("comment", "INVALID_URL", error.message, 1, startTime, {
      command: "comment",
      url_raw: urlRaw,
    });
    return;
  }
  utils.printInfo(`规范后的链接: ${url}`);
  try {
    limit = assertIntegerRange(limit, 1, 10000, "评论数量 limit");
  } catch (error) {
    utils.printError(error.message);
    emitError("comment", "INVALID_ARGS", error.message, 2, startTime, {
      command: "comment",
      url_raw: urlRaw,
      url,
      limit,
    });
    return;
  }
  utils.printInfo(`评论数量: ${limit}`);

  const tokenValue = token.skillToken(process.env.GUAIKEI_API_TOKEN);
  if (tokenValue === "") {
    emitError("comment", "AUTH_REQUIRED", AUTH_MESSAGE, 3, startTime, {
      command: "comment",
      url_raw: urlRaw,
      url,
      limit,
    });
    return;
  }

  const commentRequest = {
    command: "comment",
    url_raw: urlRaw,
    url,
    limit,
  };
  let commentTask = null;
  try {
    await comment.createCommentTask(tokenValue, url, limit);
    utils.printSuccess("获取评论任务创建成功, 正在查询中...");
    commentTask = await comment.getCommentTask(tokenValue, url, limit);
  } catch (error) {
    utils.printError(`获取评论失败: ${error.message}`);
    emitError(
      "comment",
      error.code || "UNKNOWN",
      error.message,
      error.name === "AuthError" ? 3 : 1,
      startTime,
      commentRequest,
    );
    return;
  }

  if (!Array.isArray(commentTask) || commentTask.length === 0) {
    utils.printInfo("没有找到匹配的评论");
    emitEmpty("没有找到匹配的评论", startTime, commentRequest);
    return;
  }

  const { text } = printSuccessEnvelope(
    "获取评论任务完成",
    startTime,
    commentRequest,
    commentTask,
  );
  utils.printSuccess(`获取评论任务完成, 共获取 ${commentTask.length} 条评论`);

  await log.taskWrite(
    `${startTime}_${validator.url2Name(url)}_comment.json`,
    text,
  );
}

main().catch((error) => {
  utils.printError(error.message || String(error));
  emitUncaught("comment", error);
});
