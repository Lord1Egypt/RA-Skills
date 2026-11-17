#!/bin/bash
# KLYC-PMM 快速体验脚本 — 验证安装、演示核心功能
# 幂等设计：不修改配置文件/不写入本地索引/可反复执行
# 注意：self-test环节会通过HTTPS连接kunlunyaochi.com做网络连通性探针
# 用法: bash examples/quickstart.sh（从 skill 包根目录执行）
set -e

# 自动定位 skill 包根目录（无论从哪里调用）
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
PMM="$SKILL_ROOT/scripts/pmm_watch.sh"
SCRIPTS_DIR="$SKILL_ROOT/scripts"

PASS=0; FAIL=0

ok()  { echo "  ✅ $*"; PASS=$((PASS+1)); }
err() { echo "  ❌ $*"; FAIL=$((FAIL+1)); }

# 动态读版本号
VER=""
if [ -f "$PMM" ]; then
    VER=$(grep 'readonly VERSION' "$PMM" 2>/dev/null | head -1 | grep -oP '"([^"]+)"' | tr -d '"')
fi

echo "🏔️ KLYC-PMM v${VER:-?} 快速体验（幂等，只读不写）"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# 1. 检查依赖
echo ""
echo "📦 依赖检查..."
command -v curl >/dev/null && ok "curl" || err "curl 未安装"
command -v jq   >/dev/null && ok "jq"   || err "jq 未安装"
command -v bash >/dev/null && ok "bash" || err "bash 未安装"

# 2. 检查核心脚本
echo ""
echo "📜 脚本完整性..."
for s in pmm_watch.sh pmm_boot.sh pmm_recover.sh pmm_distill.sh pmm_backup_files.sh; do
    [ -f "$SCRIPTS_DIR/$s" ] && ok "$s" || err "$s 缺失"
done

# 3. 自检
echo ""
echo "🔍 自检..."
if [ -f "$PMM" ]; then
    bash "$PMM" self-test 2>&1 | sed 's/^/  /'
    if [ ${PIPESTATUS[0]} -eq 0 ]; then
        ok "自检通过"
    else
        err "自检未通过"
    fi
else
    err "找不到 pmm_watch.sh"
fi

# 4. 显示版本 + --help 有效性
echo ""
echo "📌 版本 & 帮助..."
if [ -f "$PMM" ]; then
    echo "  KLYC-PMM v${VER:-未知}"
    ok "版本号检测"
    
    # 验证 --help 能正常显示
    if bash "$PMM" --help 2>&1 | grep -q "退出码"; then
        ok "--help 含退出码说明"
    else
        err "--help 缺退出码说明"
    fi
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━"
echo "结果: ${PASS} 通过, ${FAIL} 失败"
if [ "$FAIL" -eq 0 ]; then
    echo "✅ 环境就绪！运行 ./scripts/pmm_watch.sh init 开始使用。"
else
    echo "⚠️ 有 ${FAIL} 项未通过，请检查。"
fi
