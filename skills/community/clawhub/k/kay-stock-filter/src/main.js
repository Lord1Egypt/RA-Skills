#!/usr/bin/env node
/**
 * Stock Filter Skills CLI — OpenClaw 工具调度入口
 *
 * 用法: node src/main.js <tool_name> [JSON 参数]
 *
 * 示例:
 *   node src/main.js stock_search '{"keyword":"贵州茅台"}'
 *   node src/main.js stock_filter_options
 *   node src/main.js hot_factor_list
 */

import * as tools from "./tools.js";

const REGISTRY = {
  stock_filter:         { fn: tools.stock_filter,         desc: "多条件筛选股票" },
  stock_filter_options: { fn: tools.stock_filter_options,  desc: "获取筛选选项" },
  stock_search:         { fn: tools.stock_search,          desc: "搜索股票" },
  stock_detail:         { fn: tools.stock_detail,          desc: "获取股票详情" },
  stock_detail_batch:   { fn: tools.stock_detail_batch,    desc: "批量获取股票详情" },
  stock_compare:        { fn: tools.stock_compare,         desc: "对比多只股票指标" },
  hot_factor_list:      { fn: tools.hot_factor_list,       desc: "获取热门因子预设列表" },
  hot_factor_create:    { fn: tools.hot_factor_create,     desc: "创建因子预设" },
  hot_factor_update:    { fn: tools.hot_factor_update,     desc: "更新因子预设" },
  hot_factor_delete:    { fn: tools.hot_factor_delete,     desc: "删除因子预设" },
  hot_factor_use:       { fn: tools.hot_factor_use,        desc: "使用因子预设" },
  hot_factor_sort:      { fn: tools.hot_factor_sort,       desc: "排序因子预设" },
  jiuyan_stock_analysis:{ fn: tools.jiuyan_stock_analysis, desc: "Jiuyan 股票分析" },
  jiuyan_stock_theme:   { fn: tools.jiuyan_stock_theme,    desc: "Jiuyan 股票主题" },
  jiuyan_articles:      { fn: tools.jiuyan_articles,       desc: "Jiuyan 文章查询" },
  douyin_hotspot_list:  { fn: tools.douyin_hotspot_list,   desc: "抖音热点列表" },
  douyin_hotspot_detail:{ fn: tools.douyin_hotspot_detail,  desc: "抖音热点详情" },
};

function printHelp() {
  console.log("Stock Filter Skills — 可用工具列表:\n");
  for (const [name, { desc }] of Object.entries(REGISTRY)) {
    console.log(`  ${name.padEnd(30)} ${desc}`);
  }
  console.log(`\n用法: node src/main.js <tool_name> [JSON 参数]`);
  console.log(`示例: node src/main.js stock_search '{"keyword":"贵州茅台"}'`);
}

const [,, toolName, paramsJson] = process.argv;

if (!toolName || ["--help", "-h", "help"].includes(toolName)) {
  printHelp();
  process.exit(0);
}

if (!REGISTRY[toolName]) {
  console.log(JSON.stringify({ error: `未知工具: ${toolName}，使用 --help 查看可用工具` }));
  process.exit(1);
}

try {
  const params = paramsJson ? JSON.parse(paramsJson) : undefined;
  const result = await REGISTRY[toolName].fn(params);
  console.log(result);
} catch (e) {
  console.log(JSON.stringify({ error: e.message || String(e) }));
  process.exit(1);
}
