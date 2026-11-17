#!/usr/bin/env bash
# setup.sh — Pi × EvoX Loop 一键安装/自检（评测建议：降低开箱即用门槛）
# 用法：
#   bash code/setup.sh          安装 + 全量自检（含依赖可用性、召回冒烟）
#   bash code/setup.sh --demo   额外跑一次「隔离演示」：用临时经验库演示召回/沉淀闭环（不触碰真实库）
# 说明：流程 A/B（召回/沉淀）零 npm 依赖即可运行（内置 light 引擎）；
#       可选集成最低：pi 1.5.1 → Node >=22.19.0；evolver 2.0.50 → ^22.13.0 || >=23.4.0。
#       `npm install` 只为可选集成（evolver）与流程 C（实验，需 pi CLI）准备。
set -u
DEMO=0
[ "${1:-}" = "--demo" ] && DEMO=1
OK=0; WARN=0
say()  { echo "[setup] $*"; }
warn() { echo "[setup] ⚠️  $*"; WARN=$((WARN+1)); }
good() { echo "[setup] ✓ $*"; OK=$((OK+1)); }
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

echo "=== Pi × EvoX Loop 安装/自检（root: $ROOT）==="

# 1) Node 版本
if ! command -v node >/dev/null 2>&1; then
  warn "未找到 node —— 请安装 Node ≥ 22（https://nodejs.org 或 nvm install 22）"
else
  NODEV=$(node -v | tr -d 'v')
  NODEMAJOR=${NODEV%%.*}
  if [ "$NODEMAJOR" -ge 22 ] 2>/dev/null; then good "node v$NODEV"; else warn "node v$NODEV < 22，pi/evolver 可能启动失败（建议 nvm install 22）"; fi
fi

# 2) Python 3（仅陷阱生成器需要）
if command -v python3 >/dev/null 2>&1 || command -v python >/dev/null 2>&1; then good "python 可用（陷阱生成器用）"; else warn "未找到 python3 —— 仅影响 traps/ 陷阱生成器，流程 A/B 不需要"; fi

# 3) npm 依赖
if [ -x node_modules/.bin/evolver ]; then
  good "可选集成就位（evolver CLI，--engine evolver 时使用）"
else
  say "npm install（可选——仅为 evolver 集成与流程 C 准备；A/B 流程零依赖）"
  if npm install --ignore-scripts --no-fund --no-audit 2>&1 | tail -1; then
    [ -x node_modules/.bin/evolver ] && good "依赖安装完成" || warn "安装完成但 evolver CLI 缺失，请检查上方输出"
  else
    warn "npm install 失败——检查网络或换镜像后重试"
  fi
fi

# 3.5) Pi CLI 可用性自检（--ignore-scripts 安装可能缺 typebox build → pi 无法启动）
if [ -x node_modules/.bin/pi ]; then
  if node_modules/.bin/pi --version >/dev/null 2>&1; then
    good "pi CLI 可运行（$(node_modules/.bin/pi --version 2>/dev/null | head -1)）"
  else
    warn "pi CLI 无法启动——常见原因：--ignore-scripts 安装后 typebox 缺 build 产物。修复：npm rebuild typebox"
  fi
else
  warn "pi CLI 未安装（仅流程 C 实验需要，A/B 不受影响）"
fi

# 3.8) 隔离演示（--demo）：用临时经验库跑通「沉淀 → 召回」，全程不触碰 ~/.evomap/assets
if [ "$DEMO" = "1" ]; then
  echo ""
  echo "=== 演示：隔离临时经验库（不触碰你的真实库）==="
  DEMOSTORE="$(mktemp -d)"
  EVO_STORE_DIR="$DEMOSTORE" node -e '
const fs = require("fs");
const store = process.env.EVO_STORE_DIR;
// 一条示例「修法型」基因（含可执行修法 + 审核台账 approved）
const gene = { id: "gene_demo_0001", asset_id: "sha256:demo0001", category: "repair",
  strategy: ["The file is GBK-encoded: open it with encoding=\"gbk\" (or read bytes and decode explicitly) instead of the default utf-8; rerun to verify the values."] };
fs.writeFileSync(store + "/genes.jsonl", JSON.stringify(gene) + "\n");
fs.writeFileSync(store + "/review.jsonl", JSON.stringify({ assetId: "sha256:demo0001", state: "approved" }) + "\n");
'
  echo "--- 流程 A：召回（应输出 1 条编号修法 + 命中登记指引）---"
  EVO_STORE_DIR="$DEMOSTORE" node code/evolver-recall.mjs || true
  echo "--- 真实使用时：用 evolver distill 沉淀、review --approve 审核（见 SKILL.md 流程 B）---"
  rm -rf "$DEMOSTORE" 2>/dev/null || true
  echo "[setup] ✓ 演示完成（临时库已清理）"
  exit 0
fi

# 4) 召回自检（空库也正常）
if [ -x node_modules/.bin/evolver ] || [ -f code/evolver-recall.mjs ]; then
  say "召回自检："
  node code/evolver-recall.mjs || true
fi

# 5) LLM 端点（可选，仅流程 C 需要）
if [ -n "${EVOLVER_REFINE_URL:-}" ]; then good "EVOLVER_REFINE_URL 已配置（--llm-refine 可用）"; else warn "EVOLVER_REFINE_URL 未配置 —— 流程 C 的 --llm-refine 将自动禁用（无默认外发，见 SKILL.md 安全声明）"; fi

echo ""
echo "=== 完成：$OK 项通过, $WARN 项提醒 ==="
echo "下一步：SKILL.md 流程 A（召回）开始使用；实验模式见流程 C。FAQ 见 SKILL.md。"
