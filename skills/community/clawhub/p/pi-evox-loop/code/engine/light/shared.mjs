#!/usr/bin/env node
/**
 * shared.mjs — light CLI 共享层（0.34 从 light-cli.mjs 机械拆分）
 *
 * 只保留「多个命令域共用的 helpers 与常量」；各命令实现见 ./commands/<cmd>.mjs。
 */
/**
 * light-cli.mjs — 内置 light 后端命令行（零 npm 依赖）
 *
 * 用途：不安装 evolver 时，手工「沉淀 / 审核 / 查看」经验库的入口。
 *
 * 用法：
 *   node code/light-cli.mjs distill --signals bash,encoding-error \
 *        --strategy "用 encoding='gbk' 读取文件；不要用默认 utf-8" --summary "GBK 文件解码失败"
 *   node code/light-cli.mjs approve <gene_id>
 *   node code/light-cli.mjs quarantine <gene_id>
 *   node code/light-cli.mjs list
 *   node code/light-cli.mjs info           # 显示库路径与统计
 *
 * 说明：库路径默认 ~/.evomap/assets，可用 EVO_STORE_DIR 覆盖（与 evolver 后端共用同一格式）。
 * 去重：distill 按「归一化 strategy」判重，库中已有相同修法则跳过（不写基因也不写台账）。
 */
import fs from 'node:fs';
import path from 'node:path';
import { spawnSync } from 'node:child_process';
import os from 'node:os';
import { fileURLToPath } from 'node:url';
import * as distill from './distill.mjs';
import { STORE_DIR, readGenes, readReview, isApprovedState, isQuarantinedState } from './store.mjs';
export const SKILL_VERSION = (() => { try { return JSON.parse(fs.readFileSync(path.join(path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../../..'), 'package.json'), 'utf8')).version; } catch { return 'unknown'; } })();

export const [cmd, ...rest] = process.argv.slice(2);
export const flag = (name, def = undefined) => {
  const i = rest.indexOf(`--${name}`);
  return i >= 0 && rest[i + 1] ? rest[i + 1] : def;
};
export const positional = rest.filter((a) => !a.startsWith('--'));

// ── P0③ 引导式沉淀（2026-09-23）──────────────────────────────────────────────
// 从一段错误文本抽信号家族 + 预填 AVOID 模板 + 结构化 anti_patterns，
// 把"从一次失败直接生成 distill 草稿"的门槛降到最低（人只补 FIX）。
//
// ── 词汇对齐（anti_tags → summary / anti_patterns → 互斥 token，见 docs/advanced.md）──
// 负经验分两种表示，**不可混用**：
//   · ANTI_TAGS  ：人读 kebab 标签 → 只写进 summary（不参与匹配）
//   · ANTI_TOKENS：机器可匹配的**单 token 字面量** → 写进 anti_patterns（供 geneConflicts 用）
// 原因：`geneConflicts` 判定 = 「anti_pattern 整串 ∈ 对方 strategy token 集」，而分词器把连字符
// 视作 token 内字符 ⇒ kebab 标签（assume-default-utf8）是**单个不透明 token**，永远命中不了
// 自然语言策略。故 anti_patterns 只放"对方若主张做、即与本基因冲突"的那个**无歧义单 token**；
// **拿不准就留空**（宁缺毋滥——空 anti_patterns 只是不触发，塞 kebab 也只是不触发，但会误导人）。
export const ANTI_TAGS = {
  'encoding-error': 'assume-default-utf8',
  'permission-denied': 'write-without-restore-perm',
  'file-not-found': 'assume-path-exists',
  'invalid-json': 'strict-parse-no-fallback',
  'network-error': 'call-without-timeout-retry',
  'syntax-error': 'run-without-syntax-check',
  'type-or-value-error': 'assume-value-type',
  'assertion-failed': 'trust-unverified-output',
  unknown: 'repeat-failed-approach',
};
export const ANTI_TOKENS = {
  // 仅"能用无歧义单 token 表达被禁止主张"的家族才有值；其余刻意留空。
  // 'utf-8'：对方若主张"直接用 utf-8 读（默认编码）"，即与本基因的"按真实编码读取"冲突。
  // 注意不要放 'json.loads' 这类**双方都会出现**的 token（合规方也写它 → 误删）。
  'encoding-error': ['utf-8'],
};
// ── 统一错误输出（0.14.7，回应 skillhub errorHandling 4.3「缺统一错误码 / 中英文混杂 / 生硬退出」）──
// 退出码约定：0=成功；1=运行期失败；2=用法错误（缺参数 / 未知命令）。
// 所有错误统一前缀 [pi-evox]，需要时附「→ 修正：」一行可执行指引，避免只丢退出码让用户对着文档猜。
/**
 * 0.34 显式错误码（skillhub 0.33.0 评测 errorHandling 4.5 点名
 * 「错误码不够显式（仅退出码 0/1/2）」）。
 * 退出码 0/1/2 保留原语义以兼容既有调用方，额外附**具名错误码** [E_XXX]：
 * 脚本/宿主可据此精确区分失败类型，无需解析人类可读文案。
 */
export const ERR_CODES = {
  E_USAGE:    { exit: 2, mean: '用法错误：缺参数 / 未知命令' },
  E_ARGS:     { exit: 2, mean: '参数值不合法：取值不在允许集合内' },
  E_GUARD:    { exit: 1, mean: '质量守卫拒绝：沉淀质检未通过' },
  E_NOTFOUND: { exit: 1, mean: '目标不存在：基因 / 文件 / 编号未找到' },
  E_INTERNAL: { exit: 1, mean: '未预期的内部错误（详见原始错误）' },
};

export function fail(msg, { hint, code = 2, errCode = null } = {}) {
  const tag = errCode && ERR_CODES[errCode] ? `[${errCode}] ` : '';
  console.error(`[pi-evox] ✗ ${tag}${msg}`);
  if (hint) console.error(`         → 修正：${hint}`);
  process.exit(code);
}

/**
 * 错误提示统一为中文（0.16.0，回应 skillhub 评测 errorHandling 4.3）。
 * 问题：本 CLI 自己的消息都是中文，但 Node/系统抛出的错误是英文（ENOENT、EACCES、
 * SyntaxError 等），两者混在同一段输出里，用户看着乱、也不知道该改什么。
 * 这里把最常见的系统错误码映射成「中文原因 + 可执行修正」，其余错误也统一加中文前缀，
 * 保证**任何失败都有一句中文说明**，而不是只丢一段英文堆栈。
 */
export const SYS_ERROR_HINTS = [
  [/ENOENT/, '找不到文件或目录', '检查路径是否正确、文件是否存在；库路径可用 EVO_STORE_DIR 覆盖'],
  [/EACCES|EPERM/, '没有权限读写', '检查文件/目录权限（POSIX 用 chmod，Windows 检查只读属性）'],
  [/EISDIR/, '目标是目录而不是文件', '把 --out / 路径参数指向具体文件，不要指向目录'],
  [/EMFILE/, '同时打开的文件太多', '减少并发；或提高系统 ulimit -n'],
  [/ENOSPC/, '磁盘空间不足', '清理磁盘后重试'],
  [/EADDRINUSE/, '端口被占用', '换一个端口，或先停掉占用该端口的进程'],
  [/JSON/i, 'JSON 解析失败（文件可能损坏或有坏行）', '经验库是 JSONL（每行一个 JSON 对象）：坏行会被跳过；若整体损坏，从备份恢复'],
  [/EBUSY/, '文件被其他进程占用（Windows 常见）', '关闭正在读写该文件的程序（如编辑器/同步盘）后重试；本技能对瞬态错误会自动重试 3 次；连续失败 5 次后熔断为单次尝试（详见 IO 熔断）'],
  [/ETIMEDOUT|ESOCKETTIMEDOUT/, '网络操作超时', '检查网络/代理；或调大超时参数（见 docs/providers.md）'],
];
// 0.27 A-2：系统错误码属 POSIX 英文术语，输出时附中文对照表指针——普通用户无需查外部文档
export const TERM_GLOSSARY_HINT = '（ENOENT=文件不存在｜EACCES/EPERM=权限不足｜EBUSY=文件占用｜JSON=数据格式｜POSIX=跨平台系统接口标准；术语对照见 docs/faq.md Q17）';

export function explainErr(err) {
  const raw = String((err && (err.stack || err.message)) || err);
  const head = raw.split('\n')[0];
  console.log('  [术语对照]' + TERM_GLOSSARY_HINT);
  for (const [re, why, fix] of SYS_ERROR_HINTS) {
    if (re.test(head)) return { why, fix, head };
  }
  return { why: '运行出错', fix: '按下方原始提示定位；或运行 node code/light-cli.mjs doctor 做环境自检', head };
}

process.on('uncaughtException', (err) => {
  const e = explainErr(err);
  console.error(`[pi-evox] ✗ [E_INTERNAL] ${e.why}`);
  console.error(`         → 修正：${e.fix}`);
  console.error(`         （原始错误：${e.head}）`);
  process.exit(1);
});
process.on('unhandledRejection', (err) => {
  const e = explainErr(err);
  console.error(`[pi-evox] ✗ ${e.why}`);
  console.error(`         → 修正：${e.fix}`);
  console.error(`         （原始错误：${e.head}）`);
  process.exit(1);
});

/**
 * 操作规程文本（T1–T5）——`snippet` 输出 / `install-snippet` 写入共用的唯一来源。
 * T4 是自动沉淀的关键绑定：**修好坑后立刻沉淀**（写进项目指令文件后，agent 每个会话可见）。
 */
/** 0.22：审核取证报告（evidence 命令 + approve 前自动执行共用）。
 *  在本地四台账（工具错误/召回/注入/回填）检索基因声称失败/修法的对应事件，
 *  三级输出：强证据（直接 gene_id/工具错误）> 弱上下文（召回）> 无证据（台账外来源）。 */
export const WARNED = new Set();
export function printEvidence(g) {
  const hitsDir = process.env.EVOX_HITS_DIR || path.join(path.dirname(path.dirname(fileURLToPath(import.meta.url))), 'experiments');
  const STOP = new Set(['unknown', '失败', 'error', 'null', 'true', 'false', 'undefined', 'pending', 'approved', 'quarantined']);
  const sigFromSummary = String(g.summary || '').split(/[\s，。、（）()\[\]:：|]+/).filter((w) => w.length >= 4 && !STOP.has(w)).slice(0, 8);
  const signals = [...new Set([...(g.signals_match || []).filter((x) => !STOP.has(String(x))), ...sigFromSummary])].slice(0, 12);
  console.log(`[gene-share] 审核取证：${g.id}`);
  console.log(`  账本来源: ${hitsDir}${hitsDir.includes('publish_clean') || hitsDir.includes('_rel') ? '  ←⚠️ 这是构建/发布目录，不是生产账本！生产环境应指向已安装技能的 experiments/（可用 EVOX_HITS_DIR 指定）' : ''}`);
  console.log(`  信号词: ${signals.join(', ') || '(无)'}`);
  let found = 0;
  const files = [['工具错误', 'error_candidates.jsonl'], ['召回', 'recall_calls.jsonl'], ['注入', 'pending_injections.jsonl'], ['回填', 'hits.jsonl']];
  for (const [kind, f] of files) {
    try {
      if (!fs.existsSync(path.join(hitsDir, f)) && !WARNED.has(f)) { WARNED.add(f); console.log(`  （账本 ${f} 不存在——按空处理）`); }
      for (const l of fs.readFileSync(path.join(hitsDir, f), 'utf8').split('\n')) {
        const t = l.trim(); if (!t) continue;
        let r; try { r = JSON.parse(t); } catch { continue; }
        const text = JSON.stringify(r);
        const direct = (f === 'pending_injections.jsonl' || f === 'hits.jsonl') && text.includes(g.id);
        if (direct || signals.some((sg) => text.includes(sg))) {
          found++;
          const ts = r.ts || r.at || '?';
          const detail = String(r.snippet || r.query || r.note || r.gene_id || '').slice(0, 90);
          const tag = direct || kind === '工具错误' ? '' : '（上下文，弱证据）';
          console.log(`  [${kind}] ${ts} | ${detail}${tag}`);
        }
      }
    } catch { /* 缺文件跳过 */ }
  }
  if (!found) {
    const anyLedger = files.some(([, f]) => { try { return fs.statSync(path.join(hitsDir, f)).size > 0; } catch { return false; } });
    if (!anyLedger) console.log(`  （该目录四账本全空——**取证依据不足**：请确认 EVOX_HITS_DIR 指向生产账本（已安装技能的 experiments/）后重跑 evidence，再决定 approve）`);
    else console.log('  （无本地台账证据——可能来自共享池/其他机器/起步包：按内容与来源审核，approve 时注明来源）');
  }
  else console.log(`  → 共 ${found} 条相关事件。核对基因声称的失败/修法与上述事件一致后再批准；结论被后续事件推翻的应保持隔离并留痕。`);
}

/** 0.23 U2：install-snippet 写入管线（install / install-snippet 两命令共用） */
export function runInstallSnippet(args) {
  const fi = args.indexOf('--file');
  const target = fi >= 0 ? args[fi + 1] : null;
  if (!target) fail('用法: light-cli.mjs install-snippet --file <AGENTS.md 或 CLAUDE.md 路径> [--yes]', { errCode: 'E_USAGE' });
  const yes = args.includes('--yes');
  const out = ['── install-snippet ' + (yes ? '（写入模式）' : '（演练模式，未落盘）') + ' ──'];
  const abs = path.resolve(target);
  out.push(`  目标文件: ${abs}`);
  const exists = fs.existsSync(abs);
  out.push(`  文件存在: ${exists ? '是' : '否（--yes 时会创建）'}`);
  const cur = exists ? fs.readFileSync(abs, 'utf8') : '';
  const has = cur.includes('evox-procedure:v1');
  out.push(`  已含规程: ${has ? '是（将原位更新）' : '否（将追加到文件末尾）'}`);
  if (yes) {
    try {
      const block = procedureText();
      let next;
      if (has) {
        next = cur.replace(/<!-- evox-procedure:v1 -->[\s\S]*?<!-- \/evox-procedure -->/, '<!-- evox-procedure:v1 -->\n' + block + '\n<!-- /evox-procedure -->');
      } else {
        next = cur + (cur.endsWith('\n') || !cur ? '' : '\n') + '\n<!-- evox-procedure:v1 -->\n' + block + '\n<!-- /evox-procedure -->\n';
      }
      fs.mkdirSync(path.dirname(abs), { recursive: true });
      fs.writeFileSync(abs, next, 'utf8');
      out.push('  ✓ 已写入。该项目的 agent 每个会话都会看到此规程（T1–T5）。');
    } catch (e) { out.push('  ✗ 写入失败: ' + String(e.message || e)); }
  } else {
    out.push('  （演练未落盘；确认无误加 --yes）');
  }
  console.log(out.join('\n'));
}

export function procedureText() {
  const skillDir = path.dirname(path.dirname(fileURLToPath(import.meta.url)));
  return [
    '## 经验库操作规程（pi-evox-loop，五个触发点）',
    '',
    `技能目录: ${skillDir}`,
    '',
    '1. **任务开始**（拿到非平凡任务时，先于规划执行）：',
    `   node ${skillDir}/code/evolver-recall.mjs --query "<任务一句话>" --agent <你的名字>`,
    '2. **遇到报错**（工具返回错误、且你准备重试之前——这一刻价值最直观）：',
    `   node ${skillDir}/code/evolver-recall.mjs --error "<报错原文>"`,
    '3. **修好坑后立刻沉淀**（修了一个不显而易见的坑，趁记忆新鲜，这是 T4 自动沉淀的绑定点）：',
    `   node ${skillDir}/code/light-cli.mjs draft --error "<报错>" --context "<在做什么>" --commit`,
    '4. **任务结束回填**（用了召回给出的修法就登记，让「注入→有效」可度量）：',
    `   node ${skillDir}/code/evolver-recall.mjs --register-hit --gene <asset_id或gene_id> --note "<任务一句话>"`,
    `   node ${skillDir}/code/evolver-recall.mjs --negate --gene <asset_id或gene_id> --note "<为什么没起作用>"`,
    '',
    '原则：没命中就继续干活（零注入是对的，别为命中硬凑）；修法只在确实相关时采用；',
    '修完坑**必须立刻执行第 3 步**——这四件事做完，同一个坑才真正只踩一次。',
  ].join('\n');
}

/**
 * B：闭环健康度（0.16.0）。
 *
 * 动机：这套系统最常见的失败不是「出错」，而是**静默失效**——
 *   ① 沉淀了但没 approve ⇒ 基因入库却被隔离，永远不注入（实测某节点 39 条里 15 条如此）；
 *   ② 装了但从未召回 ⇒ 经验从不生效，而用户毫无察觉。
 * 这里把这两种沉默变成**可见的诊断与可执行动作**。
 */
/**
 * C：自己沉淀的基因是否自动通过审核（0.16.0）。**默认开启**。
 *
 * 背景：默认 quarantined 是为了质量，但实测造成大量「存了却永不注入」的静默失效
 * （某节点 39 条里 15 条待审）。而召回侧本就有修法守卫 + 叙述守卫兜底，
 * 于是「自己的库自己负责」是更合理的默认：沉淀即生效，不再需要额外一步。
 *
 * 开关（用户可随时改，优先级从高到低）：
 *   --auto-approve / --no-auto-approve  （单次）
 *   EVOX_AUTO_APPROVE=on|off            （环境）
 *   config.json: {"autoApprove": true}  （持久）
 * 注意：**仅作用于本地 distill/draft**；从共享池 `gene import` 仍按 tier 判定，不受此项影响。
 */
export function autoApproveState(args) {
  const explicit = Array.isArray(args) ? args : [];
  if (explicit.includes('--no-auto-approve') || explicit.includes('--manual-review')) return 'quarantined';
  // 0.17.0：**非交互沉淀（脚本/cron/宿主自动管道，无 TTY）默认隔离**——实测 autoApprove
  // 会把 retry-log 噪音直接放进可注入池（隔离库复现：守卫全放行）。自动管道想自动通过
  // 必须显式传 --auto-approve（有意识的决定）。交互式人工沉淀不受影响，保持 0.16.0 便利。
  if (!process.stdout.isTTY && !explicit.includes('--auto-approve')) return 'quarantined';
  if (explicit.includes('--auto-approve')) return 'approved';
  const config = readConfig();
  const def = typeof config.autoApprove === 'boolean' ? config.autoApprove : true; // 默认开
  if (process.env.EVOX_AUTO_APPROVE === 'off') return 'quarantined';
  if (process.env.EVOX_AUTO_APPROVE === 'on') return 'approved';
  return def ? 'approved' : 'quarantined';
}

/**
 * A：`install-hooks`（0.16.0）——把「宿主接入」从手工配置变成一条命令，但**由用户决定**。
 *
 * 设计原则（不擅自改用户的宿主）：
 *   1. **默认演练**：不加 --yes 只打印将要做的每件事，绝不落盘；
 *   2. 写入前**自动备份**宿主配置文件（`.bak-<时间戳>`）；
 *   3. 探测不到宿主时明确说明，不做猜测性写入。
 * 支持：OpenClaw（把 handler 写到 hooks 目录并提示注册）、Hermes（提示注册 pre_llm_call）。
 */
export async function installHooks({ args, yes }) {
  const home = os.homedir();
  const skillDir = path.dirname(path.dirname(fileURLToPath(import.meta.url))); // <技能根目录>
  const tplDir = path.join(skillDir, 'examples', 'hooks');
  const out = [];
  let wrote = false;

  const detected = [];
  const ocDir = path.join(home, '.openclaw');
  const hmDir = path.join(home, '.hermes');
  if (fs.existsSync(ocDir)) detected.push({ host: 'openclaw', dir: ocDir });
  if (fs.existsSync(hmDir)) detected.push({ host: 'hermes', dir: hmDir });
  const wantIdx = args.indexOf('--host');
  const want = wantIdx >= 0 ? String(args[wantIdx + 1] || '').toLowerCase() : null;
  const targets = want ? detected.filter((d) => d.host === want) : detected;

  // 0.30 A-2：`--auto` 只做一件事——**探测宿主并给出唯一推荐命令**（新手不必翻 FAQ Q10/Q12）。
  // 无钩子宿主但当前目录有指令文件（AGENTS.md / CLAUDE.md）→ 推荐 install-snippet。
  if (args.includes('--auto')) {
    const L = ['── install-hooks --auto（只探测并给唯一推荐命令，不写入）'];
    const cwdFiles = ['AGENTS.md', 'CLAUDE.md'].filter((f) => fs.existsSync(path.join(process.cwd(), f)));
    if (detected.length) {
      L.push(`  探测到钩子宿主: ${detected.map((d) => d.host).join(', ')}`);
      const cmd = `node code/light-cli.mjs install-hooks --host ${detected[0].host} --yes`;
      L.push(`  ▶ 推荐执行（一条就够）: ${cmd}`);
      L.push('    （不确定就不加 --host：不给 --host 会给所有探测到的宿主装）');
    } else if (cwdFiles.length) {
      L.push(`  未探测到钩子宿主，但当前目录有指令文件: ${cwdFiles.join(', ')}`);
      L.push('  ▶ 推荐执行（无钩子宿主用规程粘贴）: node code/light-cli.mjs install-snippet --file ' + cwdFiles[0] + ' --yes');
    } else {
      L.push('  未探测到钩子宿主，当前目录也没有 AGENTS.md / CLAUDE.md');
      L.push('  ▶ 任意宿主通用做法: node code/light-cli.mjs snippet > snippet.md（贴进你的指令文件）');
    }
    L.push('  说明：钩子方式 = 每次会话自动召回（更强）；规程粘贴 = 零依赖（更通用）。两者可同时用。');
    return { text: L.join('\n'), wrote: false, code: 0 };
  }

  out.push('── install-hooks ' + (yes ? '（写入模式）' : '（演练模式，未落盘）') + ' ──');
  if (!detected.length) {
    out.push('  ⚠ 未探测到已知宿主（~/.openclaw 或 ~/.hermes）。可手工按 examples/hooks/README.md 接入。');
    return { text: out.join('\n'), wrote: false, code: 1 };
  }
  out.push(`  探测到宿主: ${detected.map((d) => d.host).join(', ')}`);

  for (const t of targets) {
    const src = t.host === 'openclaw'
      ? path.join(tplDir, 'openclaw-bootstrap-recall.js')
      : path.join(tplDir, 'hermes-pre-llm-recall.py');
    if (!fs.existsSync(src)) { out.push(`  ✗ 模板缺失: ${src}`); continue; }
    const destDir = path.join(t.dir, 'hooks', 'evox-recall');
    const dest = path.join(destDir, t.host === 'openclaw' ? 'handler.js' : 'evox_recall.py');
    out.push('');
    out.push(`  [${t.host}]`);
    out.push(`    将复制: ${src}`);
    out.push(`      → ${dest}`);
    out.push(`    并将模板中的 <技能目录> 替换为: ${skillDir}`);
    if (yes) {
      try {
        fs.mkdirSync(destDir, { recursive: true });
        let body = fs.readFileSync(src, 'utf8').replace(/<技能目录>/g, skillDir);
        fs.writeFileSync(dest, body, 'utf8');
        if (t.host === 'hermes') { try { fs.chmodSync(dest, 0o755); } catch { /* 忽略 */ } }
        wrote = true;
        out.push('    ✓ 已写入');
        out.push(`    注册方式: ${t.host === 'openclaw' ? '在钩子配置里注册 agent:bootstrap → 该文件（改 handler 通常需重启网关）' : '在钩子配置里注册 pre_llm_call → 该文件（若启用 allowlist，改脚本后需刷新）'}`);
      } catch (e) {
        out.push(`    ✗ 写入失败: ${String(e.message || e)}`);
      }
    }
  }
  return { text: out.join('\n'), wrote, code: 0 };
}

export const CONFIG_FILE = path.join(path.dirname(fileURLToPath(import.meta.url)), '..', 'config.json');
export function readConfig() {
  try { return JSON.parse(fs.readFileSync(CONFIG_FILE, 'utf8')); } catch { return {}; }
}
export function writeConfig(patch) {
  const cur = readConfig();
  const next = Object.assign({}, cur, patch);
  fs.writeFileSync(CONFIG_FILE, JSON.stringify(next, null, 2), 'utf8');
  return next;
}

export function loopHealth(genes, approved) {
  // 0.17.0：默认落点改为**技能根/experiments**（脱离 cwd——此前在别的目录跑 info 会误报「从未召回」）
  const hitsDir = process.env.EVOX_HITS_DIR || path.join(path.dirname(path.dirname(fileURLToPath(import.meta.url))), 'experiments');
  const countLines = (f) => { try { return fs.readFileSync(f, 'utf8').split('\n').filter((l) => l.trim()).length; } catch { return 0; } };
  const recallCalls = countLines(path.join(hitsDir, 'recall_calls.jsonl'));
  const hits = countLines(path.join(hitsDir, 'hits.jsonl'));
  // 0.17.0 三分类（修复：此前把「已审查隔离」也误报成待审并引导 approve——对噪音基因是错误引导）
  const lww = {};
  const reviewPath = path.join(STORE_DIR, 'review.jsonl');
  try {
    for (const l of fs.readFileSync(reviewPath, 'utf8').split('\n')) {
      const t = l.trim(); if (!t) continue;
      try { const r = JSON.parse(t); lww[r.assetId] = r.state; } catch { /* 坏行跳过 */ }
    }
  } catch { /* 无台账 */ }
  const isAppr = (g) => g && g.asset_id && approved.has(g.asset_id);
  const isQuar = (g) => g && g.asset_id && isQuarantinedState(lww[g.asset_id]);
  const undecided = genes.filter((g) => !isAppr(g) && !isQuar(g));
  const quarantined = genes.filter(isQuar);

  const lines = ['── 闭环健康度 ──'];
  lines.push(`  召回次数    : ${recallCalls}${recallCalls === 0 ? '  ← 从未召回，经验不会生效' : ''}`);
  lines.push(`  命中登记    : ${hits}`);
  lines.push(`  待审(未决定): ${undecided.length}${undecided.length ? '  ← 这些不会注入！' : ''}`);
  lines.push(`  已隔离      : ${quarantined.length}${quarantined.length ? '（噪音/探针，属正常状态，无需处理）' : ''}`);
  const alive = recallCalls > 0 && undecided.length === 0;
  lines.push(`  状态        : ${alive ? '闭环运行中' : '未闭合（按下面做一步即可）'}`);
  lines.push('');

  if (recallCalls === 0) {
    lines.push('  ⚠ 还没跑过召回：经验库的价值取决于**召回是否发生**，沉淀不等于生效。');
    lines.push('    → 立刻试一次：node code/evolver-recall.mjs --query "读取中文日志报 UnicodeDecodeError"');
    lines.push('    → 想让 agent 自动召回：node code/light-cli.mjs install-hooks（先看它会做什么，加 --yes 才写入）');
  }
  if (undecided.length > 0) {
    const sample = undecided.slice(0, 3).map((g) => g.id);
    lines.push(`  ⚠ 有 ${undecided.length} 条基因待审（未做任何决定），不会注入。`);
    lines.push(`    → 逐条看内容后：有可执行修法 → approve ${sample[0]}；是日志复述/测试残留 → quarantine ${sample[0]} --reason "..."`);
    if (sample.length > 1) lines.push(`    （其余：${sample.slice(1).join(', ')}${undecided.length > 3 ? ' …' : ''}）`);
  }
  if (quarantined.length > 0) {
    lines.push(`  ℹ 已隔离 ${quarantined.length} 条（噪音/测试残留）——这是**正确状态**，不需要处理；误隔离的可 approve 恢复。`);
  }
  return lines.join('\n');
}

export const argOf = (a, name) => { const i = a.indexOf(name); return i >= 0 ? a[i + 1] : undefined; };

export function usage() {
  console.log(`light-cli — 内置经验库运维命令（零依赖）

用法（0.29 分组：先看「常用 6 条」，其余按需）：
【常用 6 条 · 日常只用这些】
  node code/light-cli.mjs doctor                        # 首次运行自检（Node/Python/目录/权限/埋点落点）
  node code/light-cli.mjs starter                       # 一键装载起步基因包（冷启动消除焦虑）
  node code/light-cli.mjs session open "<任务名>"       # 开工：自动 T1 召回 + 记账（会话围栏）
  node code/light-cli.mjs draft --error "<错误文本>" [--context "<在做什么>"] [--trigger "<动手前措辞>"] [--commit]
  node code/light-cli.mjs session close "<本轮结论>"    # 收尾：沉淀结论 + 关门（门禁会校验）
  node code/light-cli.mjs list / info / report [--days N] [--json]   # 看库 / 看健康度 / 看效果周报
  node code/light-cli.mjs gene-pull-trust                     # 池内信任分布（单源/跨源）——0.30

【沉淀与审核】
  node code/light-cli.mjs distill --signals <a,b> --strategy "<可执行修法>" [--summary "<坑>"] [--category repair] [--shareable]
  node code/light-cli.mjs distill --error "<错误文本>" [--context "<在做什么>"] [--tool <工具名>] [--shareable]   # 引导式：自动抽信号
  node code/light-cli.mjs approve <gene_id>
  node code/light-cli.mjs quarantine <gene_id> [--reason "<原因>"]
  node code/light-cli.mjs fix-signals [--apply]         # 体检/展开无效中文 signal（召回永远匹配不上的）

【共享池（跨机协作）】
  node code/light-cli.mjs gene export [--out <file>]          # 导出「已 --shareable 且过脱敏闸门」的基因
  node code/light-cli.mjs gene submit --pool <自有共享池目录>   # 过闸写入自建池（幂等）
  node code/light-cli.mjs gene import <池文件> [--tier official]  # 拉取合并；official=自建策展池自动通过，community(默认)=待审
  node code/light-cli.mjs gene pull --pool <路径|URL|命名> [--tier t] [--scene s]  # 拉取基因池（命名池/场景过滤）
  node code/light-cli.mjs gene submit --bundle <file>          # 产出单文件提交包（发给维护者/提 PR）

【接入与规程】
  node code/light-cli.mjs install-hooks --auto                      # 只探测宿主并给**唯一推荐命令**（新手用这个）——0.30
  node code/light-cli.mjs install-hooks [--host openclaw|hermes] [--yes]  # 演练；加 --yes 才写入
  node code/light-cli.mjs install <host> [--yes]              # 一键宿主接入（claude-code/cursor/codex/agents-md）
  node code/light-cli.mjs install-snippet --file <AGENTS.md> [--yes]  # 把规程写进项目指令文件（默认演练）
  node code/light-cli.mjs snippet                              # 输出可粘进 AGENTS.md 的操作规程（无钩子宿主用）
  node code/light-cli.mjs feedback "<文本>"                    # 反馈入口（本地留痕 + Discussions 引导）

【运维与诊断】
  node code/light-cli.mjs timeline [--last 50]                 # 四账本时间线（召回/注入/回填/工具错误）
  node code/light-cli.mjs harvest [--last 10]                  # error_candidates → 沉淀建议清单
  node code/light-cli.mjs harvest --done|--dismiss <N>         # 已处理/驳回某条候选（移入 .done.jsonl 留痕）
  node code/light-cli.mjs export-evidence [--out <dir>]        # 本地证据自审查包（门禁/签名/台账）
  node code/light-cli.mjs stats                                # 本地使用统计（召回/命中/回填率）
  node code/light-cli.mjs config [--auto-approve on|off]       # 自己沉淀的基因是否自动通过（默认 on）
  node code/light-cli.mjs identity                             # 本机签名身份（Ed25519 keyid/私钥路径）
  node code/light-cli.mjs verify <gene_id>                    # 验签本地库基因（exit 1 = 验签失败）
  node code/light-cli.mjs resign [--yes]                      # 把存量 v1 签名升级为 v2（v2 覆盖嵌套内容；默认演练，--yes 才落盘）——0.31
  node code/light-cli.mjs license verify <token>               # 验证 Ed25519 签名许可
  node code/light-cli.mjs demo                                 # 90 秒自演示（只读，不改状态）

共享基因库：distill/draft 加 --shareable 标记该基因「可共享」（默认不共享=不外发）。
  任何基因导出/入池前必过脱敏闸门（私有IP/绝对路径/密钥/内网服务命中即拦截，不出网）。
  import 默认 community 一律待审；仅对你自己控制的池显式 --tier official 才自动通过。
  池目录默认 ~/.evomap/pool（EVO_POOL_DIR 覆盖）。

库路径：${STORE_DIR}（可用 EVO_STORE_DIR 覆盖）`);
}

/**
 * doctor —— 首次运行自检（0.14.6 P2a，回应 skillhub usability 4.3「首次运行无引导」）。
 * 校验：Node 版本、经验库目录可写、命中登记目录可达，失败项给出**修正指引**而非只报错误。
 *
 * 用法示例：
 *   node code/light-cli.mjs doctor
 * 退出码：0=全部就绪；1=存在未通过项（日常 recall / 沉淀不受影响，仅提示先解决环境）。
 */
export function doctor() {
  const checks = [];
  const nodeMajor = Number(process.versions.node.split('.')[0]);
  checks.push({ name: 'Node 版本 ≥22', ok: nodeMajor >= 22, detail: `当前 v${process.versions.node}`, fix: '升级到 Node ≥22（traps 生成器与 pi/evolver 均要求）后重试（FAQ·Q8）' });
  let storeOk = true, storeDetail = STORE_DIR;
  try {
    fs.mkdirSync(STORE_DIR, { recursive: true });
    const probe = path.join(STORE_DIR, '.pi-evox-doctor');
    fs.writeFileSync(probe, 'ok'); fs.rmSync(probe, { force: true });
  } catch (e) { storeOk = false; storeDetail = `${STORE_DIR} 不可写：${String(e.message).slice(0, 80)}`; }
  checks.push({ name: '经验库目录可写', ok: storeOk, detail: storeDetail, fix: '检查目录权限（Linux 用 chmod，Windows 检查只读属性 / 杀软拦截）' });
  // 0.27 A-1：Python 3 前置检查（traps 生成器/流程 C 需要）——缺时给中文友好提示而非"命令找不到"
  {
    // 0.34 修复：原写法 `spawnSync('python3', …) || spawnSync('python', …)` 的 `||` **永不生效**——
    // spawnSync 总是返回对象（truthy），命令不存在时也只是 status=null / error=ENOENT，
    // 因此 `python` 兜底从不执行：只装了 python（无 python3）的机器会被误报「未检测到 Python 3」。
    let probe = spawnSync('python3', ['-c', 'import sys;print(sys.version_info[0])'], { encoding: 'utf8' });
    if (!probe || probe.status !== 0 || !String(probe.stdout || '').trim()) {
      probe = spawnSync('python', ['-c', 'import sys;print(sys.version_info[0])'], { encoding: 'utf8' });
    }
    const major = probe.status === 0 ? parseInt(String(probe.stdout || '').trim(), 10) : 0;
    checks.push({
      name: 'Python 3（仅流程 C / traps 需要）', ok: major >= 3,
      detail: major >= 3 ? `Python ${major}.x ✓` : '未检测到 Python 3',
      fix: '装 Python 3（Windows: python.org 安装包勾选 Add to PATH；macOS/Linux: python3）。**只跑流程 A/B（召回/沉淀）无需 Python**',
    });
  }
  // 0.27 B-2：timeline 落点自检——发现错位账本目录（如 0.25/0.26 的 HITS_DIR 层级缺陷）即提示
  try {
    const skillRoot = path.dirname(path.dirname(fileURLToPath(import.meta.url)));
    const suspects = [path.join(skillRoot, 'code', 'engine', 'experiments'), path.join(skillRoot, 'code', 'experiments')];
    const found = suspects.filter((d) => fs.existsSync(path.join(d, 'deposits.jsonl')));
    if (found.length) {
      checks.push({ name: 'timeline 落点漂移', ok: false, detail: `发现错位账本目录：${found.join('、')}（0.25/0.26 的 HITS_DIR 层级缺陷）`, fix: `把其中的 deposits.jsonl 合并到 ${skillRoot}/experiments/ 后删除错位目录；新版（≥0.27）已修复默认落点` });
    }
  } catch { /* 自检失败不影响 doctor 主流程 */ }
  const hitsEnv = process.env.EVOX_HITS_DIR;
  checks.push({ name: '命中登记目录可达', ok: true, detail: hitsEnv ? hitsEnv : `默认 ${path.dirname(path.dirname(fileURLToPath(import.meta.url)))}/experiments（技能根，脱离 cwd）`, fix: '如需固定落点，设 EVOX_HITS_DIR 环境变量指向可写目录' });
  // 0.18：埋点散落检测——其他目录的 experiments/ 里有 evox 埋点时提示迁移（GameRemake 会话实测散落）
  try {
    const cwdExp = path.join(process.cwd(), 'experiments');
    const skillExp = path.join(path.dirname(path.dirname(fileURLToPath(import.meta.url))), 'experiments');
    if (path.resolve(cwdExp) !== path.resolve(skillExp) && fs.existsSync(cwdExp)) {
      const strays = ['recall_calls.jsonl', 'pending_injections.jsonl', 'hits.jsonl', 'error_candidates.jsonl'].filter((f) => fs.existsSync(path.join(cwdExp, f)));
      if (strays.length) {
        checks.push({ name: '埋点散落', ok: false, detail: `发现 ${cwdExp} 含 ${strays.length} 个埋点文件（时间线/统计读的是技能根目录，散落部分不可见）`, fix: `迁移: mv ${cwdExp}/{${strays.join(',')}} ${skillExp}/ 或统一设 EVOX_HITS_DIR` });
      }
    }
  } catch { /* 探测失败不影响 doctor */ }
  const failed = checks.filter((c) => !c.ok);
  console.log('light-cli 自检（doctor）结果：');
  for (const c of checks) {
    console.log(`  [${c.ok ? '✓' : '✗'}] ${c.name} —— ${c.detail}`);
    if (!c.ok) console.log(`      → 修正：${c.fix}`);
  }
  console.log(`  IO 重试: 瞬态错误 ${parseInt(process.env.EVOX_IO_RETRY || '3', 10) || 3} 次 / 截止 ${parseInt(process.env.EVOX_IO_DEADLINE_MS || '3000', 10) || 3000}ms（EVOX_IO_RETRY / EVOX_IO_DEADLINE_MS 可调）`);
  console.log(`  IO 熔断: 连续 ${parseInt(process.env.EVOX_IO_CB_THRESHOLD || '5', 10) || 5} 次瞬态失败触发 / 冷却 ${parseInt(process.env.EVOX_IO_CB_COOLDOWN_MS || '10000', 10) || 10000}ms（EVOX_IO_CB_THRESHOLD / EVOX_IO_CB_COOLDOWN_MS 可调）`);
  // 0.25 维3：推送就绪提示（shareable+approved 且未入官方池 ≥3 条时提醒——不自动外发）
  try {
    // 池基线：EVO_POOL_DIR 显式指定，或 ~/.evomap/pool-cache/ 的已缓存池文件（用户 pull 过就有）
    let poolIds = new Set();
    const cacheDir = path.join(os.homedir(), '.evomap', 'pool-cache');
    try {
      const envDir = process.env.EVO_POOL_DIR;
      const files = envDir ? [path.join(envDir, 'genes.jsonl')] : (fs.existsSync(cacheDir) ? fs.readdirSync(cacheDir).filter((f) => f.endsWith('.jsonl')).map((f) => path.join(cacheDir, f)) : []);
      for (const pf of files) {
        for (const l of fs.readFileSync(pf, 'utf8').split('\n').filter(Boolean)) {
          try { poolIds.add(JSON.parse(l).asset_id); } catch {}
        }
      }
    } catch {}
    const genes = readGenes();
    const lww = {}; for (const r of readReview()) lww[r.assetId] = r.state;
    const ready = genes.filter((g) => g.shareable === true && isApprovedState(lww[g.asset_id]) && !poolIds.has(g.asset_id));
    if (ready.length >= 3) console.log(`  推送就绪：${ready.length} 条已审核可共享基因尚未入池 → gene submit --bundle <file> 产出提交包（人工发送，不自动外发）`);
  } catch { /* 提示失败不影响自检 */ }
  console.log(failed.length ? `\n自检未通过 ${failed.length} 项，请先修正后再用本技能（日常 recall / 沉淀不受影响）。` : `\n✓ 全部就绪，可正常使用 recall / 沉淀。`);
  process.exit(failed.length ? 1 : 0);
}
