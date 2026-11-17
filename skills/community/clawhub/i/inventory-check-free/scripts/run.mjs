#!/usr/bin/env node
/**
 * run.mjs —— 库存账实核对（免费）
 *
 * 全部检查都在**本机**完成：调用同目录下的 engine/inventory-check.js（纯 Node 标准库实现）。
 * 检查全部在**本机**完成（纯 Node 标准库），不读环境变量、不外发材料、不需要注册与 API Key。
 *
 * 刻意不做的事：
 *   · 不实现本版本范围之外的检查项（它们只能是未执行，绝不会被伪造出来）；
 *   · 材料不足时**不给结论**：打印缺什么并以退出码 3 结束。
 *
 * 用法：
 *   node scripts/run.mjs --sample
 *   node scripts/run.mjs --input my-match.json
 *   node scripts/run.mjs --input my-match.json --json
 *
 * 退出码：
 *   0  已执行检查（结果里有问题项或没有问题项都算执行成功）
 *   1  没给入参
 *   3  材料不足（空 / 只有空白 / 只有一个字符 / 类型不对 / 没有可核对要素）—— 此时不给"未发现问题"的结论
 *   4  入参文件读不到或内容无法解析
 *   9  未预期错误
 */

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { createRequire } from 'node:module';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const require = createRequire(import.meta.url);
const ENGINE = require(path.join(HERE, 'engine', 'inventory-check.js'));

const CAPABILITY = '库存账实核对（免费）';

const NOTE = '本版本只执行上面列出的检查项，核对全部在本机完成；'
  + '未执行的检查项已如实列出，不会用默认值编造结论。';

const SAMPLE = { text: ENGINE.SAMPLE_TEXT };   // 样例本身就是一张带表头的库存盘点表

const USAGE = `库存账实核对（免费） —— 本机执行的AI核对

  检查项：${ENGINE.CHECKS_GIVEN.join('、')}
  本版本不包含：${ENGINE.CHECKS_WITHHELD.join('、')}

用法：
  node scripts/run.mjs --sample
  node scripts/run.mjs --input my-match.json

入参写法：
  · {"text":"（把你那张表的**表头**和若干行一起复制进来，Tab 分隔最稳）"}
  · 直接把库存盘点表（**含表头**）从 Excel 复制成文本粘进来即可，Tab 分隔最稳

参数：
  -i, --input    入参 JSON 文件路径（也接受直接粘贴的库存盘点表纯文本，需含表头）
      --sample   使用内置样例
      --json     以 JSON 输出（默认给人看）
  -h, --help     显示本帮助

退出码：0 已执行检查 / 1 缺少入参 / 3 材料不足 / 4 入参文件读不到或无法解析 / 9 未预期错误
`;

function parseArgs(argv) {
  const out = { input: '', sample: false, json: false, help: false };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === '--input' || a === '-i') out.input = argv[++i] || '';
    else if (a === '--sample') out.sample = true;
    else if (a === '--json') out.json = true;
    else if (a === '--help' || a === '-h') out.help = true;
  }
  return out;
}

/** 读入参：合法 JSON 就按其结构走；不是 JSON 就当作纯文本材料（例如直接粘贴的合同全文） */
function loadInput(file) {
  let raw;
  try {
    raw = fs.readFileSync(file, 'utf8');
  } catch (e) {
    return { error: `读不到入参文件：${file}（${e.code || e.message}）` };
  }
  const stripped = raw.replace(/^\uFEFF/, '');
  const trimmed = stripped.trim();
  if (!trimmed) return { payload: { text: '' }, note: '入参文件内容为空' };
  if (trimmed.length > 4 * 1024 * 1024) {
    return { error: `入参文件过大（${trimmed.length} 字符）：超过 4M 上限，无法解析。` };
  }
  try {
    return { payload: JSON.parse(trimmed) };
  } catch (e) {
    if (e instanceof RangeError) {
      return { error: `入参 JSON 嵌套过深，无法解析（${e.message}）。` };
    }
    return { payload: { text: stripped }, note: '入参文件不是合法 JSON，已按纯文本单证材料处理' };
  }
}

/** 材料不足：说清楚缺什么，并且明确不给结论 */
function reportInsufficient(args, outcome, loaded) {
  const missing = (outcome && outcome.missing) || ['入参无法解析成可核对的单证材料'];
  const advice = (outcome && outcome.advice)
    || '请把库存盘点表（含表头）贴进来：可用 {"text": "…"}，或先用 --sample 看看需要什么格式。';

  const view = {
    ok: false,
    tier: 'free',
    capability: CAPABILITY,
    checks_given: ENGINE.CHECKS_GIVEN,
    checks_withheld: ENGINE.CHECKS_WITHHELD,
    omitted_findings: 0,
    note: '材料不足，本次没有执行任何检查，因此不出结论：既不做"一致"的认定，也不做"不一致"的认定，'
      + '更不会输出"未发现问题"。',
    result: {
      status: 'insufficient_input',
      missing: missing,
      advice: advice,
      executed_checks: 0,
      executed_locally: true,
      network_used: false,
    },
  };

  if (args.json) {
    console.log(JSON.stringify(view, null, 2));
    return 3;
  }

  console.log('材料不足，本次没有执行任何检查，因此不出结论。');
  console.log('（检查项依赖你提供的库存盘点表：材料不足或认不出表头时不做任何认定，也不套用默认值。）');
  if (loaded && loaded.note) console.log(`（${loaded.note}）`);
  console.log('');
  console.log('缺少的内容：');
  for (const m of missing) console.log(`  - ${m}`);
  console.log('');
  console.log(`怎么补：${advice}`);
  return 3;
}

function main() {
  const args = parseArgs(process.argv.slice(2));
  if (args.help) { console.log(USAGE); return 0; }

  let payload = null;
  let loaded = null;
  if (args.input) {
    loaded = loadInput(args.input);
    if (loaded.error) { console.error(loaded.error); return 4; }
    payload = loaded.payload;
  } else if (args.sample) {
    payload = SAMPLE;
  } else {
    console.error('缺少入参。用 --input 指定库存盘点表文件，或用 --sample 自检。');
    console.error('');
    console.error(USAGE);
    return 1;
  }

  let outcome;
  try {
    outcome = ENGINE.run(payload);
  } catch (e) {
    console.error(`引擎执行出错：${e && e.message ? e.message : e}`);
    return 9;
  }

  if (!outcome || outcome.status !== 'success') {
    return reportInsufficient(args, outcome, loaded);
  }

  const view = {
    ok: true,
    tier: 'free',
    capability: CAPABILITY,
    checks_given: ENGINE.CHECKS_GIVEN,
    checks_withheld: ENGINE.CHECKS_WITHHELD,
    omitted_findings: (outcome.result.summary && outcome.result.summary.omitted) || 0,
    note: NOTE,
    result: outcome.result,
  };

  if (args.json) {
    console.log(JSON.stringify(view, null, 2));
    return 0;
  }

  console.log('免费AI核对完成');
  console.log(`本次执行的检查项：${view.checks_given.join('、') || '(无)'}`);
  if (view.checks_withheld.length) {
    console.log(`本版本不包含：${view.checks_withheld.join('、')}`);
  }
  console.log('执行方式：核对在本机用 Node 标准库完成，不发送你的材料、没有次数上限');
  if (loaded && loaded.note) console.log(`（${loaded.note}）`);
  console.log('');
  console.log(JSON.stringify(view.result, null, 2));
  console.log('');
}

try {
  process.exit(main());
} catch (e) {
  console.error(`未预期的错误：${e && e.message ? e.message : e}`);
  process.exit(9);
}
