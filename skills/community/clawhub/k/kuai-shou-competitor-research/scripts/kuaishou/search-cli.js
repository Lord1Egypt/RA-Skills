#!/usr/bin/env node

const constants = require("../config/constants");
const log = require("../utils/log");
const search = require("../api/search");
const token = require("../utils/token");
const utils = require("../utils/utils");
const validator = require("../validate/keyword");
const { parseArgs, buildHelp } = require("../utils/args");

const SCHEMA = {
  flags: {
    "--keyword": {
      alias: "-K",
      key: "keyword",
      type: "string",
      required: true,
      desc: "搜索关键词",
    },
    "--sort": {
      alias: "-S",
      key: "sort",
      type: "number",
      default: 0,
      transform: (v) => Number(v),
      desc: "排序, 0: 综合排序(默认), 1: 最新发布, 2: 最多点赞",
    },
    "--time": {
      alias: "-T",
      key: "time",
      type: "number",
      default: 0,
      transform: (v) => Number(v),
      desc: "发布时间, 0: 不限(默认), 1: 近1日, 7: 近7日, 30: 近1月",
    },
    "--duration": {
      alias: "-D",
      key: "duration",
      type: "number",
      default: 0,
      transform: (v) => Number(v),
      desc: "作品时长, 0: 不限(默认), 1: 1分钟内, 2: 1-5分钟, 3: 超5分钟",
    },
    "--limit": {
      alias: "-L",
      key: "limit",
      type: "number",
      default: 10,
      transform: (v) => Number(v),
      desc: "搜索数量, 1-10000",
    },
  },
  positionalKey: "keyword",
};

function printHelp() {
  console.error(
    buildHelp(SCHEMA, "node scripts/kuaishou/search-cli.js <关键词> [选项]", [
      "node scripts/kuaishou/search-cli.js -K AI",
      'node scripts/kuaishou/search-cli.js -K "AI 模型"',
      "node scripts/kuaishou/search-cli.js --keyword AI --sort 1 --limit 10",
      'node scripts/kuaishou/search-cli.js --keyword "AI 模型" --sort 2 --time 7 --limit 20',
    ]) +
      "\n\n注意:\n" +
      "  - 关键词建议 2-50 个汉字，避免特殊符号\n" +
      "  - 请确保环境变量 GUAIKEI_API_TOKEN 已配置\n" +
      "  - 所有参数都会自动清洗和验证\n",
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

  let { keyword, sort, time, duration, limit } = parsed;

  utils.printBanner();
  utils.printInfo(`原始关键词: ${keyword}`);
  keyword = validator.cleanKeyword(keyword);
  const isRight = validator.isKeywordValid(keyword);
  if (!isRight) {
    process.exit(1);
  }
  utils.printInfo(`清洗后关键词: ${keyword}`);

  [sort, time, duration, limit] = validator.optionFormat(
    sort,
    time,
    duration,
    limit,
  );
  utils.printInfo(
    `排序: ${sort}, 发布时间: ${time}, 作品时长: ${duration}, 数量: ${limit}`,
  );

  const tokens = token.skillToken(process.env.GUAIKEI_API_TOKEN);
  if (tokens === "") process.exit(3);

  let searchTask = null;
  try {
    await search.createSearchTask(tokens, keyword, sort, time, duration, limit);
    utils.printSuccess(`搜索任务创建成功, 正在搜索中...`);

    searchTask = await search.getSearchTask(
      tokens,
      keyword,
      sort,
      time,
      duration,
      limit,
    );
  } catch (error) {
    const errorOutput = {
      status: "error",
      error_code: error.code || "UNKNOWN",
      message: error.message,
      timestamp: new Date().toLocaleString(),
      request: {
        command: "search",
        keyword: keyword,
        sort: sort,
        time: time,
        duration: duration,
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
  if (!searchTask || !Array.isArray(searchTask) || searchTask.length === 0) {
    utils.printError(`搜索任务没有返回结果, 请稍后重试或联系开发者`);
    const emptyOutput = {
      status: "empty",
      error_code: "NO_MATCH",
      message: "没有找到匹配的视频内容",
      timestamp: new Date().toLocaleString(),
      request: {
        command: "search",
        keyword: keyword,
        sort: sort,
        time: time,
        duration: duration,
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
    message: "搜索任务完成",
    timestamp: new Date().toLocaleString(),
    request: {
      command: "search",
      keyword: keyword,
      sort: sort,
      time: time,
      duration: duration,
      limit: limit,
    },
    skill_metadata: {
      skill_version: constants.VERSION,
      runtime_version: process.versions.node,
      execution_time: Date.now() - startTime,
    },
    results: searchTask,
  };
  console.log(JSON.stringify(finalOutput, null, 2));
  utils.printSuccess(
    `搜索任务完成, 共返回 ${finalOutput.results.length} 条结果`,
  );

  await log.taskWrite(
    `${startTime}_${keyword}_${sort}_${time}_${duration}_${limit}_search.json`,
    JSON.stringify(finalOutput, null, 2),
  );
}

main().catch((error) => {
  utils.printError(error.message);
  process.exit(1);
});
