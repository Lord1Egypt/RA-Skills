/**
 * examples/build_report.mjs — Node 出报告的最小可用示例
 *
 * 跑法：
 *   # 0. 你的项目里要先有驱动（本技能不替你装）
 *   npm install @duckdb/node-api
 *
 *   # 1. 直接跑（不审计），确认报告能出
 *   node build_report.mjs --data /path/your.parquet --out report.md
 *
 *   # 2. 带审计跑：录像 → 记账 → 审计，一条命令
 *   python3 ../../scripts/rla_report.py \
 *       --out report.md --ledger ledger.json \
 *       --mount "data=/path/your.parquet" \
 *       --report-name "我的报告" --data-as-of 2026-09-30 \
 *       -- node build_report.mjs --data /path/your.parquet --out report.md
 *
 * 要点：这个文件里**没有任何审计相关代码**。钩子从进程外挂进来，业务对它无感。
 *       所有 `conn.run(...)` 都会被录下来，参数会被内联成可复算的 SQL。
 */
import { DuckDBInstance } from '@duckdb/node-api';
import fs from 'node:fs';
import path from 'node:path';

const argOf = (name, dflt) => {
  const i = process.argv.indexOf(name);
  return i > -1 ? process.argv[i + 1] : dflt;
};

const DATA = argOf('--data', process.env.RLA_DEMO_DATA);
const OUT = argOf('--out', 'report.md');
if (!DATA) {
  console.error('用法：node build_report.mjs --data /path/your.parquet --out report.md');
  process.exit(2);
}

const inst = await DuckDBInstance.create(':memory:');
const conn = await inst.connect();
await conn.run("SET threads=2");
await conn.run(`CREATE OR REPLACE TEMP VIEW data AS SELECT * FROM read_parquet('${DATA}')`);

/** 小工具：把一条查询跑成单个数字。注意它自己也会被录像（出处会指向这一行）。 */
async function scalar(sql, values) {
  const r = await conn.runAndReadAll(sql, values);
  return Number(r.getRowObjectsJson()[0].v);
}

// ① 总数类
const rows = await scalar('SELECT COUNT(*) AS v FROM data');

// ② 去重类
const uniq = await scalar('SELECT COUNT(DISTINCT "场景ID") AS v FROM data');

// ③ 带筛选（位置参数）—— 参数会被内联，账本里留下可复算的 SQL
const yes = await scalar('SELECT COUNT(*) AS v FROM data WHERE "交易是否达成" = ?', ['是']);

// ④ 预编译 + 命名参数（Node 侧很常见）
const st = await conn.prepare('SELECT COUNT(*) AS v FROM data WHERE "省份" = $p');
st.bind({ p: '山东省' });
const sd = Number((await st.runAndReadAll()).getRowObjectsJson()[0].v);
st.destroySync();

const md = `# 数据速览

- 总行数：${rows.toLocaleString('en-US')}
- 场景数：${uniq.toLocaleString('en-US')}
- 成交行数：${yes.toLocaleString('en-US')}
- 山东省行数：${sd.toLocaleString('en-US')}
`;

fs.mkdirSync(path.dirname(path.resolve(OUT)), { recursive: true });
fs.writeFileSync(OUT, md, 'utf-8');
console.log('报告已生成：' + OUT);
