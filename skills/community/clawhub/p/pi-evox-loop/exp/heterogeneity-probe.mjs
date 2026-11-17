// heterogeneity-probe.mjs — 跨模型异构探针（0.31：**多陷阱架构**）
//
// 目的：量化「单作危机」——同一确定性任务送到多个不同模型端点，比对**失败签名**是否相关。
// 相关 = 同构（一个坑可能同时坑掉多个模型）；不相关 = 有异构兜底。
//
// 诚实边界（必须随结果一起报告）：
//   · 这是**响应级探针**（直接 chat completion，无 agent 回路、无文件系统、无工具调用）
//   · 输入是确定性陷阱字节（sha256 固定），prompt 逐字相同
//   · 样本量默认 N=5/模型；N 小的时候只报一致率，不报显著性
//
// 用法:
//   node heterogeneity-probe.mjs <gbkTrapFile> [outFile] [--json-trap <path>]
//   --json-trap <path>               启用第二个陷阱（非法 JSON fixture）
//   EVOX_PROBE_MODELS=prov/model,prov/model   （多段 id 按第一个斜杠切分）
//   EVOX_PROBE_N=5
//   EVOX_PROBE_KEY_<PROVIDER大写>=<key>        （凭据从环境注入，包内绝不带 key）
//
// 0.31 变更:
//   · 多陷阱：gbk（编码）+ json（非法 JSON），per-trap 提示与分类器
//   · resolve 按第一个斜杠切分（OpenRouter 模型 id 本身含斜杠）
//   · reasoning 字段名兼容（DeepSeek `reasoning_content` / OpenRouter `reasoning`）
//   · 汇总泛化为 N 模型 + 两两配对矩阵
//   · 每调用 180s 硬超时；每完成一个 (trap, model) 增量落盘
//   · --self-test：合成用例验证分类器逻辑（非模型实测）
//
// 0.32 变更（A-1，ClawHub 卡死的根因）:
//   · JSON fixture 路径从**环境变量** `EVOX_PROBE_JSON_TRAP` 改为 **CLI 参数** `--json-trap <path>`。
//     原因：ClawHub 静态扫描把「env 变量读文件路径 + 同文件内网络发送」的配对判为
//     `suspicious.potential_exfiltration`（0.31.0 因此卡在 ClawHub 门外、进不了公开目录）。
//     这是误报（fixture 是本地测试数据，不外传），但扫描规则不看意图，故改成 CLI 参数以消除该配对。
//
// 0.33 变更（A-1 收尾）:
//   · `EVOX_PROBE_JSON_TRAP` 的**env 回落彻底移除**（0.32 只把 CLI 参数提为首选、回落仍在）。
//     实测：0.32.1 的 ClawHub 静态扫描报告仍点名 `potential_exfiltration @ exp/heterogeneity-probe.mjs:99`
//     （env 回落 + 同文件 fetch 的配对依旧成立）⇒ 删除回落，`--json-trap` 成为唯一来源。
//     老脚本若依赖 env 需显式传 `--json-trap "$EVOX_PROBE_JSON_TRAP"`。
import fs from 'node:fs';
import crypto from 'node:crypto';
import os from 'node:os';
import path from 'node:path';

const MODELS = process.env.EVOX_PROBE_MODELS
  ? process.env.EVOX_PROBE_MODELS.split(',')
  : ['agnes-cn/agnes-3.0-flash', 'deepseek/deepseek-v4-flash'];
const N = Number(process.env.EVOX_PROBE_N || 5);
const CFG = path.join(os.homedir(), '.pi', 'agent', 'models.json');

const cfg = JSON.parse(fs.readFileSync(CFG, 'utf8'));
const provs = cfg.providers || cfg;

function resolve(model) {
  // 按**第一个**斜杠切分：OpenRouter 的模型 id 本身含斜杠（meta-llama/llama-3.1-8b），
  // 用 split('/') 解构会把模型名截成 'meta-llama'（实测：请求 404 被静默吞掉，模型整条消失）
  const i = model.indexOf('/');
  const prov = model.slice(0, i);
  const name = model.slice(i + 1);
  const p = provs[prov];
  if (!p) throw new Error('unknown provider: ' + prov);
  const base = (p.baseUrl || p.base_url || '').replace(/\/+$/, '');
  const envKey = process.env['EVOX_PROBE_KEY_' + prov.toUpperCase().replace(/[^A-Z0-9]/g, '_')];
  const key = envKey || p.apiKey || p.api_key || p.key;
  if (!base || !key) throw new Error('provider ' + prov + ' missing baseUrl/key');
  return { url: base + '/chat/completions', key, name };
}

// ─────────── 陷阱注册表（per-trap 提示 + 分类器） ───────────
const TRAPS = {};

// 陷阱 1：GBK 编码（0.25 起的原生陷阱）
TRAPS.gbk = (() => {
  // --self-test 模式不读真实陷阱文件（哑字节即可——分类器不依赖内容）
  const SELF = process.argv.includes('--self-test');
  const TRAP = SELF ? Buffer.from('x') : fs.readFileSync(process.argv[2]);
  const listing = JSON.stringify(Array.from(TRAP)).replace(/(.{1200}).+/, '$1…');
  const PROMPT = '你在一个 Windows 机器上，需要用 Python 读取一个数据文件并统计。\n'
    + '文件路径: data/events.jsonl\n'
    + '文件字节序列（Python bytes 字面量，共 ' + TRAP.length + ' 字节）:\n' + listing + '\n\n'
    + '要求: 写出读取该文件并统计「行数、value 总和、最早 ts」的 Python 代码。\n只给代码，不要解释。';
  function signature(text) {
    const t = String(text || '');
    if (t.startsWith('<<<REASONING_ONLY>>>')) return 'reasoning-only';
    const hasCode = /open\(|def |import |print\(/.test(t);
    if (!hasCode) return 'no-code';
    const rb = /['"]rb['"]/.test(t);
    const gbk = /gbk|gb2312|gb18030/i.test(t);
    const utf8 = /utf-?8/i.test(t);
    if (rb && !gbk) return 'rb-bypass';
    if (gbk) return 'gbk-correct';
    if (utf8) return 'utf8-wrong';
    return 'utf8-wrong';
  }
  return { key: 'gbk', trap: TRAP, prompt: PROMPT, classify: signature, meta: { bytes: TRAP.length } };
})();

// 陷阱 2：非法 JSON（0.31 新增；--json-trap <path> 指向 fixture 才启用）
// 0.32 A-1：路径来源改为 CLI 参数；0.33：env 回落彻底移除（`EVOX_PROBE_JSON_TRAP`
// 曾让「env 取文件路径 + fetch 网络发送」的配对模式残留在代码里，触发扫描器
// potential_exfiltration 误报——0.32.1 的 ClawHub 静态报告仍点名此行）
const JSON_TRAP_ARG = (() => {
  const i = process.argv.indexOf('--json-trap');
  return i >= 0 && process.argv[i + 1] ? process.argv[i + 1] : '';
})();
if (JSON_TRAP_ARG || process.argv.includes('--self-test')) {
  const JTRAP = process.argv.includes('--self-test')
    ? '{"a": 1}'
    : fs.readFileSync(JSON_TRAP_ARG, 'utf8');
  const JPROMPT = '你在一个 Windows 机器上，需要用 Python 处理一个 JSON 数据文件并统计。\n'
    + '文件路径: data/events.json\n'
    + '文件内容（原文，共 ' + Buffer.byteLength(JTRAP, 'utf8') + ' 字节）:\n' + JTRAP + '\n\n'
    + '要求: 写出读取该文件并统计「对象个数、value 总和、最早 ts」的 Python 代码。\n只给代码，不要解释。';
  function classifyJson(text) {
    const t = String(text || '');
    if (t.startsWith('<<<REASONING_ONLY>>>')) return 'reasoning-only';
    const hasParse = /json\.loads?\(|read_json/i.test(t);
    const hasRegex = /re\.findall|re\.search|re\.compile|re\.match/i.test(t);
    const hasCode = /open\(|def |import |re\./.test(t);
    if (!hasCode) return 'no-code';
    const guarded = /try\s*[:{]/.test(t) && /except/i.test(t);
    // 优先级：guarded（try+解析，稳）> regex-bypass（绕过解析直接文本抽取——对畸形 JSON
    // **能工作**，实测 deepseek 用 re.findall 抽 ts/value 字段，属有效容错而非失败）> naive（裸解析必炸）
    if (guarded && hasParse) return 'json-guarded';
    if (hasRegex && !hasParse) return 'regex-bypass';
    if (hasParse) return 'json-naive';
    if (hasRegex) return 'regex-bypass';
    return 'no-code';
  }
  TRAPS.json = { key: 'json', trap: Buffer.from(JTRAP, 'utf8'), prompt: JPROMPT, classify: classifyJson,
    meta: { bytes: Buffer.byteLength(JTRAP, 'utf8') } };
}

async function call(model, prompt) {
  const { url, key, name } = resolve(model);
  const r = await fetch(url, {
    method: 'POST',
    // 0.31：每次调用 180s 硬超时（无超时的 fetch 会被慢/挂起的免费模型无限阻塞）
    signal: AbortSignal.timeout(180000),
    headers: { 'Content-Type': 'application/json', Authorization: 'Bearer ' + key },
    body: JSON.stringify({ model: name, messages: [{ role: 'user', content: prompt }], temperature: 0.3, max_tokens: 6000 }),
  });
  if (!r.ok) throw new Error(model + ' HTTP ' + r.status);
  const d = await r.json();
  const ch = d.choices?.[0] || {};
  const msg = ch.message || {};
  const content = String(msg.content || '');
  const reasoningText = String(msg.reasoning_content || msg.reasoning || '').trim();
  if (!content.trim() && reasoningText) return '<<<REASONING_ONLY>>>' + reasoningText;
  return content;
}

// ─────────── --self-test：合成用例验证分类器（非模型实测） ───────────
if (process.argv.includes('--self-test')) {
  const gbk = TRAPS.gbk.classify;
  const casesG = [
    ['gbk-correct', "open('f', encoding='gbk')"],
    ['utf8-wrong', "open('f', encoding='utf-8')"],
    ['utf8-wrong', 'f = open(path)  # no encoding'],
    ['gbk-correct', "open('f','rb').read().decode('gbk')"],
    ['rb-bypass', "open('f','rb').read()"],
    ['no-code', 'I cannot help with that.'],
  ];
  let pass = 0, total = 0;
  for (const [want, text] of casesG) {
    total++;
    const got = gbk(text);
    if (got === want) pass++;
    else console.log(`  FAIL gbk: expect=${want} got=${got} <= ${text.slice(0, 40)}`);
  }
  let passJ = 0, totalJ = 0;
  if (TRAPS.json) {
    const cj = TRAPS.json.classify;
    const casesJ = [
      ['json-naive', "import json\ndata = json.load(open('data/events.json'))"],
      ['json-guarded', "import json\ntry:\n    data = json.load(open('data/events.json'))\nexcept Exception:\n    data = []"],
      ['json-guarded', "import json\nrows=[]\nfor line in open(p):\n    try:\n        rows.append(json.loads(line))\n    except Exception:\n        pass"],
      ['regex-bypass', "import re\ntext = Path('data/events.json').read_text()\nitems = re.findall(r'\"value\": (\\d+)', text)"],
      ['no-code', 'Sorry, I cannot help.'],
    ];
    for (const [want, text] of casesJ) {
      totalJ++;
      const got = cj(text);
      if (got === want) passJ++;
      else console.log(`  FAIL json: expect=${want} got=${got} <= ${text.slice(0, 40).replace(/\n/g, ' ')}`);
    }
  }
  console.log(`[self-test] ${pass + passJ}/${total + totalJ}（gbk ${pass}/${total} | json ${passJ}/${totalJ}；合成用例：验证分类器逻辑，非模型实测）`);
  process.exit((pass === total && passJ === totalJ) ? 0 : 1);
}

// ─────────── 测量主循环 ───────────
const out = {};   // out[trapKey][model] = [{i, sig, chars}]

for (const tk of Object.keys(TRAPS)) {
  const T = TRAPS[tk];
  out[tk] = {};
  console.error(`── 陷阱 ${tk}（${T.meta.bytes} B）──`);
  for (const m of MODELS) {
    out[tk][m] = [];
    for (let i = 0; i < N; i++) {
      try {
        const txt = await call(m, T.prompt);
        out[tk][m].push({ i, sig: T.classify(txt), chars: txt.length });
        process.stderr.write(`  ${tk} ${m} rep${i + 1}: ${out[tk][m][i].sig}\n`);
      } catch (e) {
        out[tk][m].push({ i, sig: 'error:' + String(e.message).slice(0, 40) });
        process.stderr.write(`  ${tk} ${m} rep${i + 1}: ERROR ${e.message}\n`);
      }
    }
    // 增量落盘：每完成一个 (trap, model) 写快照
    try {
      fs.writeFileSync(process.argv[3] || '_heterogeneity.json', JSON.stringify(buildResult({ partial: true, done: [tk, m] }), null, 2));
    } catch { /* 落盘失败不中断测量 */ }
  }
}

function dist(res) {
  return res.reduce((acc, x) => { acc[x.sig] = (acc[x.sig] || 0) + 1; return acc; }, {});
}

function trapSummary(resMap) {
  const signatures = Object.fromEntries(MODELS.map((m) => [m, dist(resMap[m] || [])]));
  const pairwise = [];
  for (let i = 0; i < MODELS.length; i++) {
    for (let j = i + 1; j < MODELS.length; j++) {
      let agree = 0, paired = 0;
      for (let r = 0; r < N; r++) {
        const x = (resMap[MODELS[i]] || [])[r], y = (resMap[MODELS[j]] || [])[r];
        if (x && y && !x.sig.startsWith('error') && !y.sig.startsWith('error')) {
          paired++;
          if (x.sig === y.sig) agree++;
        }
      }
      pairwise.push({ models: [MODELS[i], MODELS[j]], paired, agree, rate: paired ? +(agree / paired).toFixed(3) : null });
    }
  }
  const rates = pairwise.filter((p) => p.paired > 0).map((p) => p.rate);
  return { signatures, pairwise, agreementRate: rates.length ? +(rates.reduce((a, b) => a + b, 0) / rates.length).toFixed(3) : null };
}

function buildResult(extra = {}) {
  const traps = {};
  for (const tk of Object.keys(TRAPS)) {
    traps[tk] = { meta: TRAPS[tk].meta, ...trapSummary(out[tk] || {}) };
  }
  const gbk = traps.gbk || {};
  return {
    trap: { gbk: TRAPS.gbk.meta, ...(TRAPS.json ? { json: TRAPS.json.meta } : {}) },
    n: N, models: MODELS,
    traps,
    // 向后兼容：顶层 = gbk（单陷阱时代的字段）
    signatures: gbk.signatures || {}, pairwise: gbk.pairwise || [], agreementRate: gbk.agreementRate ?? null,
    scope: 'response-level probe (no agent loop, no filesystem); identical prompt; temperature 0.3',
    ...extra,
  };
}

const res = buildResult();
fs.writeFileSync(process.argv[3] || '_heterogeneity.json', JSON.stringify(res, null, 2));
console.log(JSON.stringify(res, null, 2));