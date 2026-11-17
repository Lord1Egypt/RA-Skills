/**
 * rla_track_node.cjs — Node 侧运行时录像（Python 版 rla_track.py 的等价物）
 *
 * 怎么用（业务代码一行都不用改）：
 *   NODE_OPTIONS="--require /path/to/rla_track_node.cjs" RLA_TRACE_NODE=/tmp/run.trace.jsonl \
 *     node build_report.mjs
 *
 * 通常不用自己敲——`rla_track.py` / `rla_report.py` 会自动注入这两个环境变量。
 *
 * 它做的事：拦下 @duckdb/node-api 的 SQL 执行点，把每一条 SQL 记成一行 JSON：
 *   {"ts":..., "kind":"duckdb.node.run", "sql":"...", "file":"build_report.mjs", "line":42, "bound":true}
 * 格式与 Python 版**逐字段一致**，所以 rla_collect.py / rla_audit.py 不用改一行。
 *
 * 三条铁律（与 Python 版一脉相承）：
 *   1. **只记不碰结果**：包一层后原样透传返回值，绝不读/改业务数据（碰了会吃掉业务数据，实测踩过）。
 *   2. **参数必须内联**：Node 侧大量用 prepared + bind，录下来的 SQL 若带 `?` 就无法复算
 *      （collect 会把它当"不可复算"跳过）。所以把绑定值安全地内联成字面量。
 *   3. **审计自己出错绝不打扰业务**：所有钩子代码裹在 try/catch 里，出错静默。
 *
 * 不做什么：
 *   - 不做常驻服务内的分段录像（没有"这一次是出报告"的天然边界）。
 *   - 不碰 duckdb 之外的客户端（pg/mysql2 未验证，不写"声称支持"的代码）。
 */
'use strict';

const fs = require('fs');
const path = require('path');

const TRACE = process.env.RLA_TRACE_NODE || process.env.RLA_TRACE || '';
const SELF = __filename;

/* ─────────────────────────── 1. 栈定位：找业务代码那一帧 ─────────────────────────── */

/**
 * 栈定位：返回业务代码里最内层的那一帧，外加它的调用者。
 *
 * 为什么要 caller：真实出报告的脚本几乎都会把查询封装成一个函数（`scalar(sql)`），
 * 于是几十条 SQL 的出处全都指向同一行 —— 账本里"哪句话算出的这个数"就无从分辨。
 * 带上调用者（`build_report.mjs:26 ← 调用自 :38`）才追得回去。
 */
function locate() {
  const frames = [];
  try {
    const lines = (new Error().stack || '').split('\n').slice(1);
    for (const raw of lines) {
      const ln = raw.trim();
      if (ln.includes('rla_track_node.cjs')) continue;      // 钩子自己
      if (ln.includes('node:internal')) continue;           // Node 内部
      if (ln.includes('node_modules/@duckdb')) continue;    // 驱动内部
      const m = ln.match(/\(?((?:file:\/\/)?[^()\s]+):(\d+):(\d+)\)?$/);
      if (m) {
        let file = m[1].startsWith('file://') ? decodeURIComponent(m[1].slice(7)) : m[1];
        frames.push({ file, line: parseInt(m[2], 10) });
        if (frames.length >= 2) break;                     // 只要两层，够用且不啰嗦
      }
    }
  } catch { /* ignore */ }
  const first = frames[0] || { file: '', line: 0 };
  const caller = frames[1] ? path.basename(frames[1].file) + ':' + frames[1].line : '';
  return { file: first.file, line: first.line, caller };
}

/* ─────────────────────────── 2. 参数内联成 DuckDB 字面量 ─────────────────────────── */

/** 返回 SQL 字面量；不可安全内联时返回 null（调用方会标记 bound_unresolved）。 */
function literal(v) {
  if (v === null || v === undefined) return 'NULL';
  switch (typeof v) {
    case 'boolean': return v ? 'TRUE' : 'FALSE';
    case 'bigint': return v.toString();
    case 'number':
      if (Number.isFinite(v)) return String(v);
      return Number.isNaN(v) ? "CAST('NaN' AS DOUBLE)" : (v > 0 ? "CAST('Infinity' AS DOUBLE)" : "CAST('-Infinity' AS DOUBLE)");
    case 'string': return "'" + v.replace(/'/g, "''") + "'";
    case 'object': break;
    default: return null;
  }
  if (v instanceof Date) {
    const iso = v.toISOString().replace('T', ' ').replace('Z', '');
    return "TIMESTAMP '" + iso + "'";
  }
  if (v instanceof Uint8Array) {
    const hex = Buffer.from(v).toString('hex');
    return "from_hex('" + hex + "')";
  }
  if (Array.isArray(v)) {                       // 列表值 → DuckDB list 字面量
    const parts = v.map(literal);
    if (parts.some((p) => p === null)) return null;
    return '[' + parts.join(', ') + ']';
  }
  return null;                                   // 其他对象类型不硬凑
}

/**
 * 把位置参数（?）替换成字面量，**跳过字符串字面量里的 ?**。
 * 返回 {sql, ok, used}；ok=false 表示有参数没能安全内联。
 */
function fillPositional(sql, values) {
  let out = '';
  let i = 0;                 // values 游标
  let ok = true;
  let inSingle = false;
  let inDouble = false;

  for (let p = 0; p < sql.length; p++) {
    const ch = sql[p];
    if (inSingle) {
      out += ch;
      if (ch === "'") {
        if (sql[p + 1] === "'") { out += "'"; p++; }  // 转义的单引号 ''
        else inSingle = false;
      }
      continue;
    }
    if (inDouble) {
      out += ch;
      if (ch === '"') inDouble = false;
      continue;
    }
    if (ch === "'") { inSingle = true; out += ch; continue; }
    if (ch === '"') { inDouble = true; out += ch; continue; }
    if (ch === '?') {
      if (i >= values.length) { ok = false; out += ch; continue; }
      const l = literal(values[i++]);
      if (l === null) { ok = false; out += ch; continue; }
      out += l;
      continue;
    }
    out += ch;
  }
  if (i !== values.length) ok = false;           // 参数多了/少了都不算内联成功
  return { sql: out, ok, used: i };
}

/** 命名参数（$name）内联。 */
function fillNamed(sql, values) {
  let out = sql;
  let ok = true;
  for (const [k, v] of Object.entries(values)) {
    const l = literal(v);
    if (l === null) { ok = false; continue; }
    const re = new RegExp('\\$' + k.replace(/[.*+?^${}()|[\]\\]/g, '\\$&') + '(?![A-Za-z0-9_])', 'g');
    if (re.test(out)) out = out.replace(re, l);
  }
  return { sql: out, ok };
}

function inline(sql, values) {
  if (values === undefined || values === null) return { sql, ok: true, bound: false };
  if (Array.isArray(values)) {
    if (values.length === 0) return { sql, ok: true, bound: false };
    const r = fillPositional(sql, values);
    return { sql: r.sql, ok: r.ok, bound: true };
  }
  if (typeof values === 'object') {
    const r = fillNamed(sql, values);
    return { sql: r.sql, ok: r.ok, bound: true };
  }
  return { sql, ok: false, bound: true };
}

/* ─────────────────────────── 3. 写 trace（同内容去重） ─────────────────────────── */

let lastKey = '';
let lastTs = 0;

function emit(kind, sql, values, extra) {
  if (!TRACE) return;
  try {
    const text = String(sql == null ? '' : sql);
    if (!text.trim()) return;

    const flat = inline(text, values);
    const key = flat.sql;
    const now = Date.now();
    // connection.run(sql, values) 内部会走 prepare→bind→prepared.run，
    // 同一句 SQL 会二次触发钩子；内容相同且时间相邻 → 只留一条。
    if (key === lastKey && now - lastTs < 2000) return;
    lastKey = key;
    lastTs = now;

    const where = locate();
    const rec = {
      ts: now / 1000,
      kind,
      sql: flat.sql,
      file: where.file,
      line: where.line,
      bound: flat.bound,
    };
    if (where.caller && where.caller !== path.basename(where.file) + ':' + where.line) {
      rec.caller = where.caller;
    }
    if (flat.bound && !flat.ok) rec.bound_unresolved = true;
    if (extra) Object.assign(rec, extra);

    fs.appendFileSync(TRACE, JSON.stringify(rec) + '\n', { encoding: 'utf-8' });
  } catch { /* 审计自己出错，绝不打扰业务 */ }
}

/* ─────────────────────────── 4. 装钩子 ─────────────────────────── */

function patchPrepared(PS) {
  if (!PS || !PS.prototype) return;

  const origBind = PS.prototype.bind;
  if (typeof origBind === 'function') {
    PS.prototype.bind = function (values, types) {
      try {
        // ⚠️ 必须存**副本**：原生 bind 会把传入的对象原地改写（实测绑定后结构发生变化）。
        // 同时打标记：bind() 内部会自己调 bindValue/bindXxx，那些调用不能再覆盖这里的记录，
        // 否则命名参数 {p:'x'} 会被拆成一维数组丢掉键名（实测踩过）。
        this.__rlaBinds = Array.isArray(values)
          ? values.slice()
          : (values && typeof values === 'object' ? Object.assign({}, values) : values);
        this.__rlaBindExplicit = true;
      } catch { /* ignore */ }
      return origBind.call(this, values, types);
    };
  }

  // 逐个绑定的写法：bindVarchar(1, 'x') / bindBigInt(1, 5n) …
  // 注意排除 bindValue —— 它是 bind() 的内部实现，不是用户直接调用的 API。
  for (const name of Object.getOwnPropertyNames(PS.prototype)) {
    if (!/^bind[A-Z]/.test(name) || name === 'bindValue') continue;
    const orig = PS.prototype[name];
    if (typeof orig !== 'function') continue;
    PS.prototype[name] = function (parameterIndex, value, ...rest) {
      try {
        if (!this.__rlaBindExplicit) {           // 用户没走 bind()，才按索引记
          if (!Array.isArray(this.__rlaBinds)) this.__rlaBinds = [];
          this.__rlaBinds[parameterIndex - 1] = value;
        }
      } catch { /* ignore */ }
      return orig.call(this, parameterIndex, value, ...rest);
    };
  }

  for (const meth of ['run', 'stream']) {
    const orig = PS.prototype[meth];
    if (typeof orig !== 'function') continue;
    PS.prototype[meth] = function (...args) {
      try { emit('duckdb.node.prepared.' + meth, this.__rlaSql, this.__rlaBinds); } catch { /* ignore */ }
      return orig.apply(this, args);            // 返回值原样透传，绝不碰
    };
  }
}

function patchConnection(Conn, PS) {
  if (!Conn || !Conn.prototype) return;

  const origPrepare = Conn.prototype.prepare;
  if (typeof origPrepare === 'function') {
    Conn.prototype.prepare = async function (sql) {
      const st = await origPrepare.call(this, sql);
      try {
        if (st) st.__rlaSql = String(sql);
      } catch { /* ignore */ }
      return st;
    };
  }

  for (const meth of ['run', 'stream']) {
    const orig = Conn.prototype[meth];
    if (typeof orig !== 'function') continue;
    Conn.prototype[meth] = function (sql, values, types) {
      try { emit('duckdb.node.' + meth, sql, values); } catch { /* ignore */ }
      return orig.call(this, sql, values, types);
    };
  }

  patchPrepared(PS);
}

/**
 * 解析 @duckdb/node-api。
 *
 * 为什么不能直接 require：钩子文件住在技能目录里，那里**没有 node_modules**。
 * Node 的 require 以「钩子文件所在目录」为基准解析，直接 require 必然失败，
 * 且失败是静默的 —— 会得到一个"钩子装上了、但一条都没录到"的假象。
 * 所以按「业务代码的位置」去找：cwd → 业务脚本目录及其上溯 → 环境变量指定。
 */
function resolveDuckDB() {
  const spec = '@duckdb/node-api';
  const bases = [];
  const push = (d) => { if (d && !bases.includes(d)) bases.push(d); };

  push(process.env.RLA_NODE_MODULES);
  push(process.cwd());

  const argv1 = process.argv && process.argv[1];
  if (argv1) {
    let dir = path.dirname(argv1);
    for (let i = 0; i < 8 && dir && dir !== path.dirname(dir); i++) {
      push(dir);
      dir = path.dirname(dir);
    }
  }

  // 不写死任何本机路径：挨个基准试，都试不到就返回 null
  for (const base of bases) {
    try {
      const resolved = require.resolve(spec, { paths: [base] });
      return require(resolved);
    } catch { /* 下一个 */ }
  }
  return null;
}

function install() {
  if (!TRACE) return;
  // 主动把 trace 文件建出来（append 模式，不截断）。
  // 否则「钩子装了但业务一条 SQL 都没跑」会表现成"文件不存在"，
  // 下游只能猜是没跑还是没装上——这两种情况都该报未就绪，但原因要能说清。
  try { fs.closeSync(fs.openSync(TRACE, 'a')); } catch { /* ignore */ }

  const mod = resolveDuckDB();
  if (!mod) {
    // 业务没装 duckdb，或不在可解析的位置 → 不录像，但**不打扰业务**
    if (process.env.RLA_TRACE_VERBOSE) {
      console.error('[rla_track_node] 找不到 @duckdb/node-api，未装钩子。'
        + ' 可用 RLA_NODE_MODULES=<含 node_modules 的目录> 指定。');
    }
    return;
  }
  try {
    patchConnection(mod.DuckDBConnection, mod.DuckDBPreparedStatement);
    // 注意：这里**不能**往 trace 里写一条"钩子已装"的假记录——
    // collect 会把它当成真查询去复算，凭空多出一个数字（自己造脏数据）。
    if (process.env.RLA_TRACE_VERBOSE) {
      console.error('[rla_track_node] 钩子已装，pid=' + process.pid);
    }
  } catch { /* ignore */ }
}

install();
