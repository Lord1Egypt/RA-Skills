// tools/gen-ladder.js — 为 theme.css 与 16 套 preset 生成"色板梯级"变量(第九轮 P1)
//
// 为什么需要:此前色板只有 primary/primary-dark、dark/dark-soft、off-white/card-bg,
// **没有任何浅化梯级**。于是"浅底卡片/分层底/热力中档格/徽章底"无变量可用,只能手写 hex ——
// 实测夹具 41 个色板外色中 60% 的用法可精确表达为"某色板色 × 白混合"(见 .claude/plans)。
// 补齐梯级是"页面只用变量"这条纪律能被执行的前提。
//
// 取值口径沿用 theme-presets.md 第三章既有的"逐通道加权平均"(不新造算法):
//   mix(base, k) = round(base × k + 255 × (1-k))
// 每个文件都按**该文件自己的**基色计算 → 换预设时梯级自动随之改变(无需再手工推导)。
//
// 用法: node tools/gen-ladder.js [--check]
//   缺省    = 写入(幂等:已存在则按当前基色重算并覆盖该块)
//   --check = 只报告将写入什么,不落盘(CI/复核用)
const fs = require("fs");
const path = require("path");

const ROOT = path.resolve(__dirname, "..", "..");
const FILES = [
  path.join(ROOT, "assets", "theme.css"),
  ...fs
    .readdirSync(path.join(ROOT, "assets", "presets"))
    .filter((f) => f.endsWith(".css"))
    .map((f) => path.join(ROOT, "assets", "presets", f)),
];

// 梯级定义:[新变量名, 基色变量名, 混合比(色占比), 用途注释]
// 比例来自实测反推(见 .claude/plans/palette-and-determinism.md 1.1 节):
//   17% 命中样张 #FAD9DB(d=1.0)、22% 命中 #C9D2DC(d=1.4)、8% 命中 #E8ECF1/#E8EEF5 这对近似重打。
const LADDER = [
  ["--brand-primary-soft", "--brand-primary", 0.17, "主色浅底:徽章/高亮格/热力中档"],
  ["--brand-primary-pale", "--brand-primary", 0.08, "主色最浅底:提示条/斑马纹"],
  ["--brand-dark-pale", "--brand-dark", 0.08, "深底浅化:卡片浅底/浅色分区"],
  ["--brand-dark-tint", "--brand-dark", 0.22, "深底中浅:表头底纹/分层底"],
  ["--brand-dark-mid", "--brand-dark", 0.55, "深底中间层:金字塔/漏斗中段"],
  ["--ink-soft", "--text-primary", 0.7, "中性深灰:次级文字/较重分隔线"],
  ["--ink-faint", "--text-primary", 0.5, "中性中灰:弱化文字/网格线"],
  ["--surface-sunken", "--text-primary", 0.04, "下沉面:浅灰面板底(区别于画布底)"],
  ["--signal-green-soft", "--signal-green", 0.16, "语义浅底:达成/正向格"],
  ["--signal-yellow-soft", "--signal-yellow", 0.16, "语义浅底:预警/中档格"],
  ["--signal-red-soft", "--signal-red", 0.16, "语义浅底:风险/未达格"],
  ["--signal-blue-soft", "--signal-blue", 0.16, "语义浅底:信息/参照格"],
];

const BEGIN = "  /* ── 色板梯级(第九轮 P1 自动生成:tools/gen-ladder.js;勿手改值)────── */";
const END = "  /* ── 色板梯级结束 ── */";

const hx = (s) => [1, 3, 5].map((i) => parseInt(s.slice(i, i + 2), 16));
const toHex = (a) => "#" + a.map((v) => v.toString(16).padStart(2, "0").toUpperCase()).join("");
const mix = (base, k) => toHex(hx(base).map((v) => Math.round(v * k + 255 * (1 - k))));

// 取某变量在文件中持有的具体色值;别名(var(--x))递归解析。
function resolve(src, name, seen = new Set()) {
  if (seen.has(name)) throw new Error(`变量别名成环: ${name}`);
  seen.add(name);
  const m = new RegExp(`^\\s*${name}:\\s*([^;]+);`, "m").exec(src);
  if (!m) throw new Error(`找不到变量 ${name}`);
  const v = m[1].trim();
  if (/^#[0-9A-Fa-f]{6}$/.test(v)) return v.toUpperCase();
  const alias = /^var\(\s*(--[a-z0-9-]+)\s*\)$/i.exec(v);
  if (alias) return resolve(src, alias[1], seen);
  throw new Error(`变量 ${name} 的值不是 hex 也不是别名: ${v}`);
}

function generate({ check }) {
  let changed = 0;
  for (const file of FILES) {
    const src = fs.readFileSync(file, "utf-8");
    const rel = path.relative(ROOT, file);

    const lines = [BEGIN];
    for (const [name, base, k, note] of LADDER) {
      const value = mix(resolve(src, base), k);
      lines.push(`  ${name}: ${value};`.padEnd(38) + `/* ${base} @${Math.round(k * 100)}% · ${note} */`);
    }
    lines.push(END);
    const block = lines.join("\n");

    let out;
    if (src.includes(BEGIN)) {
      // 幂等重算:替换既有块
      const re = new RegExp(`${BEGIN.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")}[\\s\\S]*?${END.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")}`);
      out = src.replace(re, block);
    } else {
      // 首次插入:放在字体组之前(色板段末尾)
      const anchor = /^\s*\/\* 字体 \*\/$/m;
      if (!anchor.test(src)) throw new Error(`${rel} 找不到插入锚点 "/* 字体 */"`);
      out = src.replace(anchor, (m) => `${block}\n\n${m}`);
    }

    if (out === src) {
      console.log(`  ─ ${rel}(无变化)`);
      continue;
    }
    changed++;
    if (check) console.log(`  ~ ${rel}(将更新 ${LADDER.length} 个梯级变量)`);
    else {
      fs.writeFileSync(file, out);
      console.log(`  ✔ ${rel}`);
    }
  }
  return changed;
}

// 只在作为 CLI 直接运行时才写盘。
// 为什么必须有这道闸:generation-checks.js 的 A5 需要 require 本文件取 LADDER 定义,
// 若 require 就顺带重建了梯级块,A5 检查的正是被自己修好的文件 —— 守卫永远不会失败。
// (2026-08-17 实测踩过:删掉 --ink-faint 后 A5 仍然全绿。)
if (require.main === module) {
  const check = process.argv.includes("--check");
  const changed = generate({ check });
  console.log(
    `\n${check ? "预演" : "已写入"}:${FILES.length} 个主题文件,${changed} 个${check ? "待" : "已"}更新,每个 ${LADDER.length} 个梯级变量`
  );
}

module.exports = { LADDER, BEGIN, END, generate };
