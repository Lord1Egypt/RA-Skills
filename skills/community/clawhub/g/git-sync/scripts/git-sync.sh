#!/usr/bin/env bash

# R-12 审计锚点：数据目录
DEFAULT_DATA_DIR_RAW="skills/.standardization/git-sync/data/"
SKILL_DIR="$(dirname "$(dirname "${BASH_SOURCE[0]}")")"
_data_dir_abs="$SKILL_DIR/../.standardization/git-sync/data"


# git-sync v2.32.0
# 将 skill/agent 代码规范化推送到码云/GitHub，支持 ClawHub/SkillHub/PyPI/Release
# 用法: bash git-sync.sh <name> [version] [--skip-market] [--market-only] [--pypi] [--release]
set -eo pipefail

# ── 0. 参数解析 ─────────────────────────────
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd -W)"
SKILLS_DIR="$(cd "$SCRIPT_DIR/../.." && pwd -W)"
WORKSPACE_ROOT="$(cd "$SKILLS_DIR/.." && pwd -W)"
# 从 _paths.py 读取统一管理的仓库路径（v2.37.0 多仓库：按类型解析）
WORK_REPO="$(python -c "import sys; sys.path.insert(0,'$SCRIPT_DIR'); from _paths import get_work_repo; print(get_work_repo('skill').as_posix())" 2>/dev/null || echo "$HOME/WorkBuddy/maby_skills")"
NAME="${1:-}"
VERSION="${2:-}"
SKIP_MARKET=false
MARKET_ONLY=false
DO_PYPI=false
DO_RELEASE=false
for arg in "$@"; do
    [ "$arg" = "--skip-market" ] && SKIP_MARKET=true
    [ "$arg" = "--market-only" ] && MARKET_ONLY=true
    [ "$arg" = "--pypi" ] && DO_PYPI=true
    [ "$arg" = "--release" ] && DO_RELEASE=true
done

# ── 0.5 类型检测：skill 还是 agent ──────────────────────
detect_type() {
    local name="$1"
    if [ -f "$SKILLS_DIR/$name/_meta.json" ]; then
        echo "skill"
    elif [ -d "$HOME/WorkBuddy/maby_agent/$name" ] || [ -d "$WORK_REPO/../maby_agent/$name" ]; then
        echo "agent"
    else
        echo "unknown"
    fi
}

# 按类型解析目标仓库（v2.37.0 多仓库）
resolve_repo() {
    local ptype="$1"
    python -c "import sys; sys.path.insert(0,'$SCRIPT_DIR'); from _paths import get_repo_config; import json; print(json.dumps(get_repo_config('$ptype'), ensure_ascii=False))"
}

# 处理 all 模式：遍历所有项目
if [ "$NAME" = "all" ]; then
    echo "==============================================="
    echo "  git-sync: 全部项目同步"
    echo "==============================================="
    for skill in "$SKILLS_DIR"/*/; do
        s=$(basename "$skill")
        [ "$s" = ".standardization" ] || [ "$s" = ".dist" ] && continue
        echo ""
        echo ">>> 技能: $s"
        bash "$0" "$s" "$@" --skip-market 2>&1 || true
    done
    for agent in "$HOME/WorkBuddy/maby_agent"/*/; do
        [ ! -d "$agent" ] && continue
        a=$(basename "$agent")
        echo ""
        echo ">>> 智能体: $a"
        bash "$0" "$a" "$@" --skip-market 2>&1 || true
    done
    echo ""
    echo "==============================================="
    echo "  ✅ 全部项目同步完成"
    echo "==============================================="
    exit 0
fi

if [ -z "$NAME" ]; then
    echo "用法: bash git-sync.sh <name> [version] [--skip-market] [--market-only] [--pypi] [--release]"
    exit 1
fi

TYPE=$(detect_type "$NAME")
if [ "$TYPE" = "unknown" ]; then
    echo "❌ 未找到项目: $NAME（不在 skills/ 也 不在 agent/）"
    exit 1
fi
echo "  类型: $TYPE"

# 按类型设置源路径（v2.37.0 多仓库）
if [ "$TYPE" = "skill" ]; then
    SRC_DIR="$SKILLS_DIR/$NAME"
    REPO_CFG=$(resolve_repo "skill")
    WORK_REPO_DIR="$NAME"   # maby_skills 仓库根下直接是技能目录
    META_FILE="$SRC_DIR/_meta.json"
elif [ "$TYPE" = "agent" ]; then
    SRC_DIR="$HOME/WorkBuddy/maby_agent/$NAME"
    REPO_CFG=$(resolve_repo "agent")
    WORK_REPO_DIR="$NAME"   # maby_agent 仓库根下直接是智能体目录
    # 兼容：如果 maby_agent 不存在，从老仓库直接读取
    if [ ! -d "$SRC_DIR" ]; then
        SRC_DIR="$WORK_REPO/../maby_agent/$NAME"
    fi
    # 自动检测 __init__.py（不硬编码 rag_assistant/）
    META_FILE=$(python -c "import sys; sys.path.insert(0,'$SCRIPT_DIR'); from pathlib import Path; d=Path('$SRC_DIR'); fs=sorted(d.rglob('__init__.py')); [print(str(f)) for f in fs if f.parent!=d and '__version__' in f.read_text(errors='ignore')]" 2>/dev/null | head -1)
fi
# 从仓库配置解析目标仓库路径与名称
REPO_NAME=$(echo "$REPO_CFG" | python -c "import sys,json; print(json.load(sys.stdin).get('name','maby_skills'))" 2>/dev/null || echo "maby_skills")
WORK_REPO=$(echo "$REPO_CFG" | python -c "import sys,json; print(json.load(sys.stdin).get('path',''))" 2>/dev/null || echo "$HOME/WorkBuddy/maby_skills")

SKILL_NAME="$NAME"

# 自动读取版本号
if [ -z "$VERSION" ]; then
    if [ "$TYPE" = "skill" ]; then
        META_FILE_WIN=$(cygpath -w "$META_FILE" 2>/dev/null || echo "$META_FILE")
        VERSION=$(python -c "import json; f=open(r'$META_FILE_WIN', encoding='utf-8'); meta=json.load(f); print(meta.get('version',''))" 2>/dev/null || echo "")
    elif [ "$TYPE" = "agent" ]; then
        VERSION=$(python -c "
import re, sys; sys.path.insert(0,'$SCRIPT_DIR')
from pathlib import Path
d=Path('$SRC_DIR')
for f in sorted(d.rglob('__init__.py')):
    if f.parent==d: continue
    try:
        t=f.read_text(encoding='utf-8')
        m=re.search(r'__version__\s*=\s*\"([^\"]+)\"',t)
        if m: print(m.group(1)); break
    except: pass
" 2>/dev/null || echo "")
    fi
    if [ -z "$VERSION" ]; then
        echo "❌ 无法读取版本号，请手动指定"; exit 1
    fi
fi

# market-only 模式：跳过前面的步骤，直接发市场/PyPI
if [ "$MARKET_ONLY" = true ]; then
    echo ""
    echo "==============================================="
    echo "  市场只发模式: $SKILL_NAME v$VERSION"
    echo "==============================================="
    if [ "$TYPE" = "skill" ]; then
        echo ""
        echo "  → 发布到 ClawHub..."
        python "$SCRIPT_DIR/clawhub_publish.py" "$SKILL_NAME" "$VERSION" 2>/dev/null || echo "  ❌ ClawHub 发布失败"
        echo "  → 发布到 SkillHub..."
        python "$SCRIPT_DIR/skillhub_publish.py" "$SKILL_NAME" "$VERSION" 2>/dev/null || echo "  ❌ SkillHub 发布失败"
    elif [ "$TYPE" = "agent" ]; then
        echo "  → 发布到 PyPI..."
        python "$SCRIPT_DIR/pypi_publish.py" "$SRC_DIR" "$NAME" "$VERSION" 2>/dev/null || echo "  ❌ PyPI 发布失败"
    fi
    exit 0
fi

# ── 0.5 检测 rsync，不可用则切换到 Python 完整流程 ─────────────────────
if ! command -v rsync >/dev/null 2>&1; then
    echo "⚠️  rsync 不可用，切换到 Python 完整流程 (git-sync.py)..."
    if [ -f "$SCRIPT_DIR/git-sync.py" ]; then
        # 过滤掉新版特有参数，git-sync.py 只认旧参数
        PY_ARGS=()
        for a in "$@"; do
            case "$a" in
                --skip-market|--market-only|--pypi|--release) ;;
                *) PY_ARGS+=("$a") ;;
            esac
        done
        python "$SCRIPT_DIR/git-sync.py" "${PY_ARGS[@]}"
        exit $?
    else
        echo "❌ git-sync.py 不存在: $SCRIPT_DIR/git-sync.py"
        echo "   请先创建 git-sync.py，或安装 rsync"
        exit 1
    fi
fi

# 路径配置
SKILL_MD="$SRC_DIR/SKILL.md"
META_FILE_JSON="$SRC_DIR/_meta.json"
DIST_DIR="$SKILLS_DIR/.dist"
ZIP_NAME="${SKILL_NAME}-v${VERSION}.zip"
ZIP_FILE="$DIST_DIR/$ZIP_NAME"
MANIFEST_FILE="$HOME/.workbuddy/skills/.standardization/git-sync/data/manifest.json"
README_FILE="$WORK_REPO/README.md"

# 统一临时文件目录（与 _paths.py TEMP_DIR 一致）
TEMP_DIR="$SCRIPT_DIR/../../.standardization/git-sync/temp"
mkdir -p "$TEMP_DIR" 2>/dev/null || true

# 读取 description（仅 skill 有 meta.json）
if [ "$TYPE" = "skill" ] && [ -f "$META_FILE" ]; then
    SKILL_DESC=$(python "$SCRIPT_DIR/get_meta_desc.py" "$META_FILE" 2>/dev/null || echo "")
else
    SKILL_DESC="$SKILL_NAME - $TYPE"
fi

echo "==============================================="
echo "  git-sync: $SKILL_NAME v$VERSION"
echo "==============================================="

# ── 1. 检查维护清单 ─────────────────────────────
echo ""
echo "[1/8] 检查维护清单..."
MANIFEST_CHECK=$(python "$SCRIPT_DIR/manifest.py" check "$REPO_NAME" "$SKILL_NAME" 2>/dev/null || echo "NOT_FOUND")
if [ "$MANIFEST_CHECK" = "NOT_FOUND" ]; then
    echo "  ➕  不在清单中，自动添加..."
    python "$SCRIPT_DIR/manifest.py" add "$REPO_NAME" "$SKILL_NAME" "$VERSION" 2>/dev/null || true
elif [ "$MANIFEST_CHECK" = "FOUND:not-uploaded" ]; then
    echo "  ✅ 在清单中，未上传（正常）"
else
    echo "  ✅ 在清单中，已上传"
fi

# ── 2. 版本号对比（仓库 vs 本地源文件）───────────────────
echo ""
echo "[2/8] 版本号对比（仓库 vs 本地源文件）..."
REPO_VER=""
LOCAL_VER="$VERSION"
REPO_META_FILE="$WORK_REPO/$WORK_REPO_DIR/_meta.json"
if [ -f "$REPO_META_FILE" ]; then
    REPO_VER=$(python "$SCRIPT_DIR/get_meta_version.py" "$REPO_META_FILE" 2>/dev/null || echo "")
else
    REPO_VER=$(python -c "
import re; from pathlib import Path
d=Path('$WORK_REPO/$WORK_REPO_DIR')
for f in sorted(d.rglob('__init__.py')):
    if f.parent==d: continue
    try:
        t=f.read_text(encoding='utf-8')
        m=re.search(r'__version__\s*=\s*\"([^\"]+)\"',t)
        if m: print(m.group(1)); break
    except: pass
" 2>/dev/null || echo "")
fi
echo "  仓库版本: ${REPO_VER:-（无）}"
echo "  本地源文件版本: $LOCAL_VER"

ver_lt() { [ "$(printf '%s\n' "$1" "$2" | sort -V | head -1)" = "$1" ] && [ "$1" != "$2" ]; }

VER_ACTION="normal"
if [ -z "$REPO_VER" ]; then
    echo "  → 仓库无版本记录，正常同步"
elif [ "$REPO_VER" = "$LOCAL_VER" ]; then
    echo "  ⏭️  仓库版本 = 本地版本（$REPO_VER），跳过同步"
    # 交互环境询问是否强制；非交互环境直接跳过
    if [ -t 0 ]; then
        read -p "  是否强制更新？（y=强制 / n=跳过）[Y/n]: " FORCE_CHOICE
        case "$FORCE_CHOICE" in y|Y) VER_ACTION="normal" ;; *) echo "  ⏭️  已跳过（版本相同 $LOCAL_VER）"; exit 0 ;; esac
    else
        echo "  ⏭️  非交互环境，已跳过（版本相同 $LOCAL_VER）"
        exit 0
    fi
elif ver_lt "$REPO_VER" "$LOCAL_VER"; then
    echo "  ✅ 仓库版本 < 本地版本，正常升级"
else
    echo "  ❌ 版本异常：仓库版本($REPO_VER) > 本地版本($LOCAL_VER)"
    echo "  请选择处理策略："
    echo "    1) 强制用本地版本覆盖  2) 用仓库版本覆盖本地  3) 中止"
    read -p "  请输入选项 [1-3]: " CONFLICT_CHOICE
    case "$CONFLICT_CHOICE" in
        1) echo "  ⚠️  强制覆盖模式"; VER_ACTION="force" ;;
        2) LOCAL_VER="$REPO_VER"; VER_ACTION="normal" ;;
        3|*) echo "  ❌ 已中止"; exit 1 ;;
    esac
fi

# ── 3. skill 独有步骤：_meta.json 标准化校验 ──────────────
if [ "$TYPE" = "skill" ]; then
    echo ""
    echo "[3/8] 校验 _meta.json 标准字段..."
    python "$SCRIPT_DIR/normalize_meta.py" "$META_FILE" "$SKILL_NAME" "$VERSION" "$SKILL_DESC" 2>/dev/null || true

    # ── 3.5 SKILL.md 规范化审查（仅 skill）────────────────
    echo ""
    if [ -f "$SKILL_MD" ]; then
        echo "[3.5/8] SKILL.md 规范审查..."
        python "$SCRIPT_DIR/skill_audit.py" audit "$SRC_DIR" \
            --manifest-version "$VERSION" 2>/dev/null || true
    else
        echo "[3.5/8] ⏭️  SKILL.md 不存在，跳过审查"
    fi
fi

# ── 4. 同步文件到工作仓库 ──────────────────────────
echo ""
echo "[4/8] 同步文件到工作仓库..."
DST="$WORK_REPO/$WORK_REPO_DIR"
DST_REAL=$(realpath -m "$DST" 2>/dev/null || echo "$DST")
WORK_REPO_REAL=$(realpath -m "$WORK_REPO" 2>/dev/null || echo "$WORK_REPO")
if [[ "$DST_REAL" != "$WORK_REPO_REAL/${WORK_REPO_DIR%%/*}"* ]]; then
    echo "❌ 安全错误：目标路径越界: $DST_REAL"; exit 1
fi

# 统一排除规则（与 pack_zip.py 和 .git-sync-exclude.txt 保持一致）
# 注意：白名单文件（settings.html 等）需在排除前用 --include 声明
RSYNC_OPTS=(
    -a --delete
    --include="settings.html"
    --include="preview.html"
    --exclude="__pycache__/"
    --exclude=".git/"
    --exclude=".eggs/"
    --exclude="eggs/"
    --exclude="dist/"
    --exclude="build/"
    --exclude=".eggs-info/"
    --exclude=".pytest_cache/"
    --exclude=".mypy_cache/"
    --exclude="node_modules/"
    --exclude=".gitignore"
    --exclude=".ds_store"
    --exclude="thumbs.db"
    --exclude="config.json"
    --exclude="manifest.json"
    --exclude="pack_zip.py"
    --exclude="*.pyc"
    --exclude="*.pyo"
    --exclude="*.log"
    --exclude="*.zip"
    --exclude="*.bak"
    --exclude="*.tmp"
    --exclude="._*"
    --exclude=".decisions.json"
    --exclude=".sensitive_scan_*.json"
    --exclude=".standardization/git-sync/temp/*"
    --exclude="zip_out"
    --exclude="preview_server.py"
)

if [ -d "$DST" ]; then
    # 使用统一排除规则的 rsync
    rsync "${RSYNC_OPTS[@]}" "$SRC_DIR/" "$DST/" 2>/dev/null || {
        echo "  ⚠️  rsync 不可用，使用 Python 排除复制（已通过路径校验）"
        python "$SCRIPT_DIR/sync_with_exclude.py" "$(cygpath -w "$SRC_DIR")" "$(cygpath -w "$DST")"
    }
else
    mkdir -p "$DST"
    rsync "${RSYNC_OPTS[@]}" "$SRC_DIR/" "$DST/" 2>/dev/null || {
        echo "  ⚠️  rsync 不可用，使用 Python 排除复制"
        python "$SCRIPT_DIR/sync_with_exclude.py" "$(cygpath -w "$SRC_DIR")" "$(cygpath -w "$DST")"
    }
fi

# 二次保险：清理残留的 __pycache__ 和 .pyc（rsync --delete 应已处理，这是双重保障）
find "$DST" -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find "$DST" -name "*.pyc" -delete 2>/dev/null || true
echo "  已同步文件:"
find "$DST" -type f | sed "s|$DST/|  - |" | head -20

# ── 4.5 敏感信息扫描（同步到仓库后、提交前）──────────────────────
echo ""
echo "[4.5/8] 扫描敏感信息（强制，不可跳过）..."
SCAN_OUTPUT="$TEMP_DIR/sensitive_scan_${SKILL_NAME}.json"
DECISION_FILE="$TEMP_DIR/sensitive_scan_${SKILL_NAME}.decisions.json"
python "$SCRIPT_DIR/sensitive_scan.py" scan "$DST" \
    --output "$SCAN_OUTPUT" 2>/dev/null || true
if [ -s "$SCAN_OUTPUT" ]; then
    echo "  ⚠️  发现敏感信息："
    python -c "import json; data=json.load(open('$SCAN_OUTPUT')); [print(f'  - {e[\"file\"]}: {len(e[\"findings\"])} 处') for e in data[:5]]" 2>/dev/null || true
    rm -f "$DECISION_FILE"
    echo "  🔒  自动全部脱敏..."
    python "$SCRIPT_DIR/make_all_sanitize.py" "$SCAN_OUTPUT" > "$DECISION_FILE"
    if [ -s "$DECISION_FILE" ]; then
        echo "  → 对工作仓库中的文件执行脱敏..."
        python "$SCRIPT_DIR/sensitive_scan.py" apply "$DST" \
            --decisions "$DECISION_FILE" \
            --scan-result "$SCAN_OUTPUT"
    fi
    rm -f "$SCAN_OUTPUT" "$DECISION_FILE" 2>/dev/null || true
else
    echo "  ✅ 未发现敏感信息"
    rm -f "$SCAN_OUTPUT" 2>/dev/null || true
fi

# ── 5. 更新 README.md（仅 skill）─────────────────────
echo ""
if [ "$TYPE" = "skill" ]; then
    echo "[5/8] 更新 README.md..."
    if [ -f "$README_FILE" ]; then
        echo "  🔄 全量重新生成 README.md（从仓库实际文件）..."
        python "$SCRIPT_DIR/update_readme.py" "$REPO_NAME" "$README_FILE"
    else
        echo "  ⚠️  README.md 不存在，跳过"
    fi
else
    echo "[5/8] ⏭️  智能体不涉及 README.md，跳过"
fi

# ── 6. 提交并推送到双平台 ──────────────────────────
echo ""
echo "[6/8] 提交并推送..."
cd "$WORK_REPO"
git config user.email "workbuddy@local" 2>/dev/null || true
git config user.name "WorkBuddy" 2>/dev/null || true
git add "$WORK_REPO_DIR/"
git add "README.md" 2>/dev/null || true
HAS_CHANGES=false
if git diff --cached --quiet; then
    echo "  ℹ️  没有变更需要提交"
else
    COMMIT_MSG="feat: sync $SKILL_NAME v$VERSION"
    git commit -m "$COMMIT_MSG"
    echo "  ✅ 已提交: $COMMIT_MSG"
    HAS_CHANGES=true
fi

# ── 6.5 推送到双平台（追踪结果）──────────────────
GITEE_OK=false
GITHUB_OK=false

echo "  → 推送到码云..."
git pull gitee main --rebase 2>/dev/null || echo "  ⚠️  码云pull失败，继续..."
if git push gitee main 2>&1; then
    echo "  ✅ 码云推送成功"
    GITEE_OK=true
else
    echo "  ❌ 码云推送失败"
fi

echo "  → 推送到 GitHub..."
git pull origin main --rebase 2>/dev/null || echo "  ⚠️  GitHub pull失败，继续..."
if git push origin main 2>&1; then
    echo "  ✅ GitHub推送成功"
    GITHUB_OK=true
else
    echo "  ❌ GitHub推送失败"
fi

# ── 6.7 根据推送结果分别更新清单 ──────────────────
if [ "$GITEE_OK" = true ]; then
    python "$SCRIPT_DIR/manifest.py" version "$REPO_NAME" "$SKILL_NAME" "$VERSION" --platform gitee 2>/dev/null && \
        echo "  ✅ 清单版本号已更新 [码云]: $SKILL_NAME → $VERSION" || true
    python "$SCRIPT_DIR/manifest.py" set-uploaded "$REPO_NAME" "$SKILL_NAME" --platform gitee 2>/dev/null || true
    echo "  ✅ 已标记 码云 uploaded"
fi

if [ "$GITHUB_OK" = true ]; then
    python "$SCRIPT_DIR/manifest.py" version "$REPO_NAME" "$SKILL_NAME" "$VERSION" --platform github 2>/dev/null && \
        echo "  ✅ 清单版本号已更新 [GitHub]: $SKILL_NAME → $VERSION" || true
    python "$SCRIPT_DIR/manifest.py" set-uploaded "$REPO_NAME" "$SKILL_NAME" --platform github 2>/dev/null || true
    echo "  ✅ 已标记 GitHub uploaded"
fi

if [ "$GITEE_OK" = false ]; then
    echo "  ⚠️  码云推送失败，保持 not-uploaded (gitee)"
fi
if [ "$GITHUB_OK" = false ]; then
    echo "  ⚠️  GitHub推送失败，保持 not-uploaded (github)"
fi

if [ "$GITEE_OK" = true ] && [ "$GITHUB_OK" = true ]; then
    echo "  ✅ 双平台均推送成功，uploaded=true"
else
    echo "  ⚠️  未全部推送成功，uploaded=false（至少一个平台失败）"
fi

if [ "$TYPE" = "skill" ]; then
    # ── 7. 生成 ZIP 安装包 ──────────────────────────
    echo ""
    echo "[7/8] 生成 ZIP 安装包..."
    mkdir -p "$DIST_DIR"
    rm -f "$ZIP_FILE"

# ── 7.5 打包前敏感信息扫描 ──────────────────────
echo ""
echo "[7.5/8] 打包前敏感信息扫描..."
ZIP_SOURCE="$SRC_DIR"  # 默认用源目录
ZIP_TMP=""

SCAN_OUTPUT_ZIP="$TEMP_DIR/sensitive_scan_${SKILL_NAME}_zip.json"
DECISION_FILE_ZIP="$TEMP_DIR/sensitive_scan_${SKILL_NAME}_zip.decisions.json"
python "$SCRIPT_DIR/sensitive_scan.py" scan "$SKILLS_DIR/$SKILL_NAME" \
    --output "$SCAN_OUTPUT_ZIP" 2>/dev/null || true
if [ -s "$SCAN_OUTPUT_ZIP" ]; then
    echo "  ⚠️  发现敏感信息，将在副本中脱敏..."
    rm -f "$DECISION_FILE_ZIP"
    python "$SCRIPT_DIR/make_all_sanitize.py" "$SCAN_OUTPUT_ZIP" > "$DECISION_FILE_ZIP"
    if [ -s "$DECISION_FILE_ZIP" ]; then
        ZIP_TMP_BASE=$(python -c "import tempfile, os; print(os.path.normpath(tempfile.gettempdir()))" 2>/dev/null || echo "/tmp")
        ZIP_TMP="$ZIP_TMP_BASE/.tmp_zip_$$"
        rm -rf "$ZIP_TMP" 2>/dev/null || true
        mkdir -p "$ZIP_TMP"
        cp -r "$SKILLS_DIR/$SKILL_NAME" "$ZIP_TMP/" 2>/dev/null || true
        echo "  打包: $ZIP_TMP/$SKILL_NAME"
        python "$SCRIPT_DIR/sensitive_scan.py" apply "$ZIP_TMP/$SKILL_NAME" \
            --decisions "$DECISION_FILE_ZIP" \
            --scan-result "$SCAN_OUTPUT_ZIP"
        ZIP_SOURCE="$ZIP_TMP/$SKILL_NAME"
    fi
    rm -f "$SCAN_OUTPUT_ZIP" "$DECISION_FILE_ZIP" 2>/dev/null || true
else
    echo "  ✅ 未发现敏感信息"
    rm -f "$SCAN_OUTPUT_ZIP" 2>/dev/null || true
fi

# 清理 ZIP 源目录中的临时文件
python "$SCRIPT_DIR/clean_zip_source.py" "$ZIP_SOURCE" 2>/dev/null || true

# 调用 pack_zip.py 打包（已内置排除规则）
python "$SCRIPT_DIR/pack_zip.py" "$ZIP_SOURCE" "$ZIP_FILE"
echo "  ✅ ZIP 已生成: $ZIP_FILE"

# 清理临时目录
if [ -n "$ZIP_TMP" ] && [ -d "$ZIP_TMP" ]; then
    rm -rf "$ZIP_TMP"
fi

echo "  📦 ZIP: $ZIP_FILE"

# 刷新 .dist/index.html
python "$SCRIPT_DIR/build_index.py" "$DIST_DIR" 2>/dev/null || true
echo "  ✅ index.html 已刷新"

# 输出 ZIP 绝对路径（供用户取用）
echo "ZIP 路径: $ZIP_FILE"
if command -v explorer >/dev/null 2>&1; then
    explorer "$(dirname "$(cygpath -w "$ZIP_FILE" 2>/dev/null || echo "$ZIP_FILE")")" 2>/dev/null || true
fi
else
    echo "[7/8] ⏭️  智能体跳过 ZIP 打包"
fi

# ── 8. 发布到市场/PyPI ──────────────────────────
echo ""
echo "[8/8] 发布到平台..."
if [ "$SKIP_MARKET" = false ]; then
    if [ "$TYPE" = "skill" ]; then
        # 发布到 ClawHub
        echo "  → 发布到 ClawHub..."
        python "$SCRIPT_DIR/clawhub_publish.py" "$SKILL_NAME" "$VERSION" 2>/dev/null || echo "  ❌ ClawHub 发布失败"

        # 发布到 SkillHub
        echo "  → 发布到 SkillHub..."
        python "$SCRIPT_DIR/skillhub_publish.py" "$SKILL_NAME" "$VERSION" 2>/dev/null || echo "  ❌ SkillHub 发布失败"
    fi

    # PyPI（仅 agent，且在 --pypi 标志下）
    if [ "$TYPE" = "agent" ] && [ "$DO_PYPI" = true ]; then
        echo "  → 发布到 PyPI..."
        python "$SCRIPT_DIR/pypi_publish.py" "$SRC_DIR" "$NAME" "$VERSION" 2>/dev/null || echo "  ❌ PyPI 发布失败"
    fi
else
    echo "  ⏭️  跳过市场发布（--skip-market）"
fi

# ── 9. 创建 Release ──────────────────────────
if [ "$DO_RELEASE" = true ]; then
    echo ""
    echo "[9/8] 创建 Release..."
    python "$SCRIPT_DIR/release_creator.py" "$NAME" "$TYPE" "$VERSION" 2>/dev/null || echo "  ❌ Release 创建失败"
fi

echo ""
echo "==============================================="
echo "  ✅ 全部完成: $SKILL_NAME v$VERSION"
echo "==============================================="
