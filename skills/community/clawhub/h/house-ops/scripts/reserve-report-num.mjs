#!/usr/bin/env node
// reserve-report-num.mjs — 原子分配下一个 3 位报告编号
// 用法: node scripts/reserve-report-num.mjs [PROJECT_ROOT]
// 行为: 扫描 reports/ 现有 `NNN-*` 文件取最大编号 +1，然后以 O_EXCL 独占创建
//       reports/.num-NNN.lock 占位文件——并发调用（headless batch）不会拿到同一个号。
// 输出: 仅打印 3 位编号（如 "007"），供调用方拼接文件名。
// 说明: 占位文件被 .gitignore 忽略（data/reports 通配 + .gitkeep 白名单规则覆盖）。
//       清理策略: 报告落盘后保留占位文件无害；如需清理可删除 .num-*.lock。

import { readdir, open } from 'node:fs/promises';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = process.argv[2] ?? join(dirname(fileURLToPath(import.meta.url)), '..');
const reportsDir = join(root, 'reports');

const files = await readdir(reportsDir).catch(() => []);
let max = 0;
for (const f of files) {
  const m = /^(?:\.num-)?(\d{3})(?:-.*)?\.lock$/.exec(f) ?? /^(\d{3})-/.exec(f);
  if (m) max = Math.max(max, Number(m[1]));
}

for (let n = max + 1; n <= 999; n++) {
  const num = String(n).padStart(3, '0');
  const lockPath = join(reportsDir, `.num-${num}.lock`);
  let fh;
  try {
    fh = await open(lockPath, 'wx'); // O_EXCL：已存在则抛错，尝试下一个号
  } catch {
    continue;
  }
  await fh.close();
  console.log(num);
  process.exit(0);
}
console.error('报告编号已用尽（>999）');
process.exit(1);
