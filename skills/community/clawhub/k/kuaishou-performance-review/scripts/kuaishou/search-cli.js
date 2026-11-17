#!/usr/bin/env node

const log = require("../utils/log");
const search = require("../api/search");
const token = require("../utils/token");
const utils = require("../utils/utils");
const validator = require("../validate/keyword");
const { parseArgs, buildHelp } = require("../utils/args");
const {
  emitError,
  emitEmpty,
  printSuccessEnvelope,
  emitUncaught,
} = require("../utils/output");

const SCHEMA = {
  flags: {
    "--keyword": {
      alias: "-k",
      key: "keyword",
      type: "string",
      required: true,
      desc: "搜索关键词",
    },
    "--sort": {
      alias: "-s",
      key: "sort",
      type: "number",
      default: 0,
      transform: (v) => Number(v),
      desc: "排序, 0: 综合(默认), 1: 最新发布, 2: 最多点赞",
    },
    "--time": {
      alias: "-t",
      key: "time",
      type: "number",
      default: 0,
      transform: (v) => Number(v),
      desc: "发布时间, 0: 不限(默认), 1: 近1日, 7: 近7日, 30: 近1月",
    },
    "--duration": {
      alias: "-d",
      key: "duration",
      type: "number",
      default: 0,
      transform: (v) => Number(v),
      desc: "作品时长, 0: 不限(默认), 1: 1分钟内, 2: 1-5分钟, 3: 超5分钟",
    },
    "--limit": {
      alias: "-l",
      key: "limit",
      type: "number",
      default: 10,
      transform: (v) => Number(v),
      desc: "搜索数量, 1-10000；包月 Token 实际最多 30",
    },
  },
  positionalKey: "keyword",
};

const AUTH_MESSAGE =
  "GUAIKEI_API_TOKEN 未配置或格式无效。须为 16-256 位字母、数字、下划线或连字符";

const KEYWORD_MESSAGE =
  '关键词不合法: 需 1-50 个字符, 不能是链接, 不含 < > " \'';

function printHelp() {
  process.stderr.write(
    buildHelp(SCHEMA, "node scripts/kuaishou/search-cli.js <关键词> [选项]", [
      "node scripts/kuaishou/search-cli.js -k AI",
      'node scripts/kuaishou/search-cli.js --keyword "AI 模型" --sort 2 --time 7 --limit 20',
    ]) +
      "\n\n注意:\n" +
      '  - 关键词 1-50 个字符，不能是链接，不含 < > " \'\n' +
      "  - --time 只能是 0、1、7、30，不是天数以外的序号\n" +
      "  - 排序、时间、时长和数量若不在允许范围内，命令会直接失败，不会改成默认值后继续搜索\n" +
      "  - 数量 1-10000；包月 Token 实际最多 30，超限返回 PLAN_LIMIT\n" +
      "  - 短参数大小写都可以，例如 -k 和 -K\n" +
      "  - 关键词以 - 开头时写成 --keyword=-AI，或在 -- 后面写位置参数\n",
  );
}

async function main() {
  const startTime = Date.now();
  const args = process.argv.slice(2);
  if (args.length === 0) {
    printHelp();
    emitError("search", "INVALID_ARGS", "缺少命令参数", 2, startTime);
    return;
  }

  let parsed;
  try {
    parsed = parseArgs(args, SCHEMA);
  } catch (error) {
    utils.printError(`参数解析错误: ${error.message}`);
    printHelp();
    emitError(
      "search",
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

  let { keyword, sort, time, duration, limit } = parsed;
  const keywordRaw = keyword;

  utils.printBanner();
  utils.printInfo(`原始关键词: ${keywordRaw}`);
  keyword = validator.normalizeKeyword(keyword);
  if (!validator.isKeywordValid(keyword)) {
    utils.printError(KEYWORD_MESSAGE);
    emitError("search", "INVALID_KEYWORD", KEYWORD_MESSAGE, 2, startTime, {
      command: "search",
      keyword_raw: keywordRaw,
      keyword,
      sort,
      time,
      duration,
      limit,
    });
    return;
  }
  utils.printInfo(`清洗后关键词: ${keyword}`);
  try {
    [sort, time, duration, limit] = validator.assertSearchOptions(
      sort,
      time,
      duration,
      limit,
    );
  } catch (error) {
    utils.printError(error.message);
    emitError("search", "INVALID_ARGS", error.message, 2, startTime, {
      command: "search",
      keyword_raw: keywordRaw,
      keyword,
      sort,
      time,
      duration,
      limit,
    });
    return;
  }
  utils.printInfo(
    `排序: ${sort}, 发布时间: ${time}, 作品时长: ${duration}, 数量: ${limit}`,
  );

  const tokenValue = token.skillToken(process.env.GUAIKEI_API_TOKEN);
  if (tokenValue === "") {
    emitError("search", "AUTH_REQUIRED", AUTH_MESSAGE, 3, startTime, {
      command: "search",
      keyword_raw: keywordRaw,
      keyword,
      sort,
      time,
      duration,
      limit,
    });
    return;
  }

  const searchRequest = {
    command: "search",
    keyword_raw: keywordRaw,
    keyword,
    sort,
    time,
    duration,
    limit,
  };
  let searchTask = null;
  try {
    await search.createSearchTask(
      tokenValue,
      keyword,
      sort,
      time,
      duration,
      limit,
    );
    utils.printSuccess("搜索任务创建成功, 正在搜索中...");
    searchTask = await search.getSearchTask(
      tokenValue,
      keyword,
      sort,
      time,
      duration,
      limit,
    );
  } catch (error) {
    utils.printError(`搜索失败: ${error.message}`);
    emitError(
      "search",
      error.code || "UNKNOWN",
      error.message,
      error.name === "AuthError" ? 3 : 1,
      startTime,
      searchRequest,
    );
    return;
  }

  if (!Array.isArray(searchTask) || searchTask.length === 0) {
    utils.printInfo("没有找到匹配的视频");
    emitEmpty("没有找到匹配的视频", startTime, searchRequest);
    return;
  }

  const { payload: finalOutput, text } = printSuccessEnvelope(
    "搜索任务完成",
    startTime,
    searchRequest,
    searchTask,
  );
  utils.printSuccess(
    `搜索任务完成, 共返回 ${finalOutput.results.length} 条结果`,
  );

  await log.taskWrite(
    `${startTime}_${keyword}_${sort}_${time}_${duration}_${limit}_search.json`,
    text,
  );
}

main().catch((error) => {
  utils.printError(error.message || String(error));
  emitUncaught("search", error);
});
