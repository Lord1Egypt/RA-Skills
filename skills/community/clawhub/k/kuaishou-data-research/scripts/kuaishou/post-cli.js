#!/usr/bin/env node

const post = require("../api/post");
const token = require("../utils/token");
const utils = require("../utils/utils");
const validator = require("../validate/url");
const { assertChoice, assertIntegerRange } = require("../validate/keyword");
const { parseArgs, buildHelp } = require("../utils/args");
const {
  emitError,
  emitEmpty,
  buildSuccessEnvelope,
  finishSuccess,
  emitUncaught,
} = require("../utils/output");

const SCHEMA = {
  flags: {
    "--url": {
      alias: "-u",
      key: "url",
      type: "string",
      required: true,
      desc: "快手博主主页链接或数字 user_id",
    },
    "--sort": {
      alias: "-s",
      key: "sort",
      type: "number",
      default: 1,
      transform: (v) => Number(v),
      desc: "排序, 0: 最新, 1: 最热(默认)",
    },
    "--limit": {
      alias: "-l",
      key: "limit",
      type: "number",
      default: 10,
      transform: (v) => Number(v),
      desc: "作品数量, 0-10000；包月 Token 实际最多 50；0 表示只取博主信息和互动数据",
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
      "node scripts/kuaishou/post-cli.js <博主主页或user_id> [选项]",
      [
        'node scripts/kuaishou/post-cli.js --url "https://www.kuaishou.com/profile/3xabc" --limit 20',
        "node scripts/kuaishou/post-cli.js --url 123456 --sort 0 --limit 20",
        "node scripts/kuaishou/post-cli.js --url 123456 --limit 0",
      ],
    ) +
      "\n\n注意:\n" +
      "  - 这是博主主页或数字 user_id，不是视频链接，也不是裸的 3x 视频 id\n" +
      "  - 不传 --sort 时是 1（最热）。要最近发布请显式传 --sort 0\n" +
      "  - --limit 0 只返回博主信息和互动数据\n" +
      "  - 数量 0-10000；包月 Token 实际最多 50，超限返回 PLAN_LIMIT\n" +
      "  - 排序和数量若不在允许范围内，命令会直接失败，不会改成默认值后继续请求\n",
  );
}

function isEmptyPost(task) {
  if (!task || typeof task !== "object") return true;
  const hasPosts = Array.isArray(task.post) && task.post.length > 0;
  const hasUser = task.user && Object.keys(task.user).length > 0;
  return !hasPosts && !hasUser;
}

async function main() {
  const startTime = Date.now();
  const args = process.argv.slice(2);
  if (args.length === 0) {
    printHelp();
    emitError("post", "INVALID_ARGS", "缺少命令参数", 2, startTime);
    return;
  }

  let parsed;
  try {
    parsed = parseArgs(args, SCHEMA);
  } catch (error) {
    utils.printError(`参数解析错误: ${error.message}`);
    printHelp();
    emitError(
      "post",
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

  let { url, sort, limit } = parsed;
  const urlRaw = url;

  utils.printBanner();
  utils.printInfo(`原始链接: ${urlRaw}`);
  try {
    url = validator.resolveProfileUrl(url);
  } catch (error) {
    utils.printError(error.message);
    emitError("post", "INVALID_URL", error.message, 1, startTime, {
      command: "post",
      url_raw: urlRaw,
    });
    return;
  }
  utils.printInfo(`规范后的链接: ${url}`);
  try {
    sort = assertChoice(sort, [0, 1], "排序 sort");
    limit = assertIntegerRange(limit, 0, 10000, "作品数量 limit");
  } catch (error) {
    utils.printError(error.message);
    emitError("post", "INVALID_ARGS", error.message, 2, startTime, {
      command: "post",
      url_raw: urlRaw,
      url,
      sort,
      limit,
    });
    return;
  }
  utils.printInfo(`排序: ${sort}, 数量: ${limit}`);

  const tokenValue = token.skillToken(process.env.GUAIKEI_API_TOKEN);
  if (tokenValue === "") {
    emitError("post", "AUTH_REQUIRED", AUTH_MESSAGE, 3, startTime, {
      command: "post",
      url_raw: urlRaw,
      url,
      sort,
      limit,
    });
    return;
  }

  const postRequest = {
    command: "post",
    url_raw: urlRaw,
    url,
    sort,
    limit,
  };
  let postTask = null;
  try {
    await post.createPostTask(tokenValue, url, sort, limit);
    utils.printSuccess("获取作品任务创建成功, 正在查询中...");
    postTask = await post.getPostTask(tokenValue, url, sort, limit);
  } catch (error) {
    utils.printError(`获取作品失败: ${error.message}`);
    emitError(
      "post",
      error.code || "UNKNOWN",
      error.message,
      error.name === "AuthError" ? 3 : 1,
      startTime,
      postRequest,
    );
    return;
  }

  if (isEmptyPost(postTask)) {
    utils.printInfo("没有找到匹配的博主或作品");
    emitEmpty("没有找到匹配的博主或作品", startTime, postRequest);
    return;
  }

  const finalOutput = buildSuccessEnvelope(
    "获取作品任务完成",
    startTime,
    postRequest,
    postTask,
  );
  const postCount = Array.isArray(postTask.post) ? postTask.post.length : 0;
  const hasUser = Boolean(postTask.user && Object.keys(postTask.user).length);
  await finishSuccess(finalOutput, {
    logFilename: `${startTime}_${validator.url2Name(url)}_post.json`,
    stderrMessage: `获取作品任务完成, 作品 ${postCount} 条${hasUser ? ", 含博主信息" : ""}`,
  });
}

main().catch((error) => {
  utils.printError(error.message || String(error));
  emitUncaught("post", error);
});
