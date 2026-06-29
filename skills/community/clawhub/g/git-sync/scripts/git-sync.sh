#!/usr/bin/env bash

# R-12 审计锚点：数据目录
DEFAULT_DATA_DIR_RAW="skills/.standardization/git-sync/data/"
SKILL_DIR="$(dirname "$(dirname "${BASH_SOURCE[0]}")")"
_data_dir_abs="$SKILL_DIR/../.standardization/git-sync/data"


# git-sync v2.6.6
# 将 skill 代码规范化推送到码云/GitHub 并生成 ZIP 包
# 用法: bash git-sync.sh <skill-name> [version] [--skip-scan]
set -eo pipefail

# ── 0. 参数解析 ─────────────────────────────
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

	# 使用 pwd -W 获取 Windows 风格路径（Python 可识别）
	SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd -W)"
	
	# 从 scripts/ 往上 2 级确定 skills 目录: skills/git-sync/scripts/ → skills/
	# 使用 pwd -W 获取 Windows 风格路径（Python 可识别）
	SKILLS_DIR="$(cd "$SCRIPT_DIR/../.." && pwd -W)"
WORKSPACE_ROOT="$(cd "$SKILLS_DIR/.." && pwd -W)"
SKILL_NAME="${1:-}"
VERSION="${2:-}"
SKIP_SCAN=false
for arg in "$@"; do [ "$arg" = "--skip-scan" ] && SKIP_SCAN=true; done

if [ -z "$SKILL_NAME" ]; then
    echo "用法: bash git-sync.sh <skill-name> [version] [--skip-scan]"
    exit 1
fi

# 自动读取版本号
if [ -z "$VERSION" ]; then
    META_FILE="$SKILLS_DIR/$SKILL_NAME/_meta.json"
    if [ -f "$META_FILE" ]; then
        # 转换路径为 Windows 格式（Python 无法识别 /c/ 前缀）
        META_FILE_WIN=$(cygpath -w "$META_FILE" 2>/dev/null || echo "$META_FILE")
        VERSION=$(python -c "import json; f=open(r'$META_FILE_WIN', encoding='utf-8'); meta=json.load(f); print(meta.get('version',''))" 2>/dev/null || echo "")
    fi
    if [ -z "$VERSION" ]; then
        echo "❌ 无法读取版本号，请手动指定"; exit 1
    fi
fi

# ── 0.5 检测 rsync，不可用则切换到 Python 完整流程 ─────────────────────
if ! command -v rsync >/dev/null 2>&1; then
    echo "⚠️  rsync 不可用，切换到 Python 完整流程 (git-sync.py)..."
    if [ -f "$SCRIPT_DIR/git-sync.py" ]; then
        python "$SCRIPT_DIR/git-sync.py" "$@"
        exit $?
    else
        echo "❌ git-sync.py 不存在: $SCRIPT_DIR/git-sync.py"
        echo "   请先创建 git-sync.py，或安装 rsync"
        exit 1
    fi
fi

# 路径配置
SKILL_MD="$SKILLS_DIR/$SKILL_NAME/SKILL.md"
META_FILE="$SKILLS_DIR/$SKILL_NAME/_meta.json"
WORK_REPO="/c/Users/sm001/.workbuddy/workbuddy-skills"
REPO_NAME="workbuddy-skills"
DIST_DIR="$SKILLS_DIR/.dist"
ZIP_NAME="${SKILL_NAME}-v${VERSION}.zip"
ZIP_FILE="$DIST_DIR/$ZIP_NAME"
MANIFEST_FILE="/c/Users/sm001/.workbuddy/skills/.standardization/git-sync/data/manifest.json"
README_FILE="$WORK_REPO/README.md"

# 读取 description（用于 README.md）
SKILL_DESC=$(python "$SCRIPT_DIR/get_meta_desc.py" "$META_FILE" 2>/dev/null || echo "")

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
REPO_META="$WORK_REPO/skills/$SKILL_NAME/_meta.json"
if [ -f "$REPO_META" ]; then
    REPO_VER=$(python "$SCRIPT_DIR/get_meta_version.py" "$REPO_META" 2>/dev/null || echo "")
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

# ── 3. _meta.json 标准化校验 + 更新版本号 ──────────────────
echo ""
echo "[3/8] 校验 _meta.json 标准字段..."
python "$SCRIPT_DIR/normalize_meta.py" "$META_FILE" "$SKILL_NAME" "$VERSION" "$SKILL_DESC" 2>/dev/null || true

# ── 3.5 SKILL.md 规范化审查（同步前自动检查）───────────────
echo ""
echo "[3.5/8] SKILL.md 规范审查（跳过，由 git-sync.py 内联审计）..."
echo ""
        fi
        python "$SCRIPT_DIR/skill_audit.py" audit "$SKILLS_DIR/$SKILL_NAME" \
            --manifest-version "${MANIFEST_VER:-}" 2>/dev/null || true
    else
        echo "  ⚠️  审查执行失败，跳过"
    fi
    rm -f "$AUDIT_OUTPUT" 2>/dev/null || true
else
    echo "  ⏭️  SKILL.md 不存在，跳过审查"
fi

# ── 4. 同步文件到工作仓库 ──────────────────────────
echo ""
echo "[4/8] 同步文件到工作仓库..."
DST="$WORK_REPO/skills/$SKILL_NAME"
DST_REAL=$(realpath -m "$DST" 2>/dev/null || echo "$DST")
WORK_REPO_REAL=$(realpath -m "$WORK_REPO" 2>/dev/null || echo "$WORK_REPO")
if [[ "$DST_REAL" != "$WORK_REPO_REAL/skills/"* ]]; then
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
    --exclude="zip_out"
    --exclude="preview_server.py"
)

if [ -d "$DST" ]; then
    # 使用统一排除规则的 rsync
    rsync "${RSYNC_OPTS[@]}" "$SKILLS_DIR/$SKILL_NAME/" "$DST/" 2>/dev/null || {
        echo "  ⚠️  rsync 不可用，使用 Python 排除复制（已通过路径校验）"
        python "$SCRIPT_DIR/sync_with_exclude.py" "$(cygpath -w "$SKILLS_DIR/$SKILL_NAME")" "$(cygpath -w "$DST")"
    }
else
    mkdir -p "$DST"
    rsync "${RSYNC_OPTS[@]}" "$SKILLS_DIR/$SKILL_NAME/" "$DST/" 2>/dev/null || {
        echo "  ⚠️  rsync 不可用，使用 Python 排除复制"
        python "$SCRIPT_DIR/sync_with_exclude.py" "$(cygpath -w "$SKILLS_DIR/$SKILL_NAME")" "$(cygpath -w "$DST")"
    }
fi

# 二次保险：清理残留的 __pycache__ 和 .pyc（rsync --delete 应已处理，这是双重保障）
find "$DST" -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find "$DST" -name "*.pyc" -delete 2>/dev/null || true
echo "  已同步文件:"
find "$DST" -type f | sed "s|$WORK_REPO/skills/$SKILL_NAME/|  - |" | head -20

# ── 4.5 敏感信息扫描（同步到仓库后、提交前）──────────────────────
echo ""
echo "[4.5/8] 扫描敏感信息..."
SENSITIVE_MODE="${GIT_SYNC_SENSITIVE_MODE:-prompt}"
SCAN_OUTPUT="$SCRIPT_DIR/.sensitive_scan_${SKILL_NAME}.json"
DECISION_FILE="${SCAN_OUTPUT}.decisions.json"
if [ "$SKIP_SCAN" = true ]; then
    echo "  ⏭️  已跳过敏感信息扫描（--skip-scan）"
else
    python "$SCRIPT_DIR/sensitive_scan.py" scan "$WORK_REPO/skills/$SKILL_NAME" \
        --output "$SCAN_OUTPUT" 2>/dev/null || true
    if [ -s "$SCAN_OUTPUT" ]; then
        echo "  ⚠️  发现敏感信息："
        python -c "import json; data=json.load(open('$SCAN_OUTPUT')); [print(f'  - {e[\"file\"]}: {len(e[\"findings\"])} 处') for e in data[:5]]" 2>/dev/null || true
        rm -f "$DECISION_FILE"
        if [ "$SENSITIVE_MODE" = "always-sanitize" ]; then
            echo "  🔒  已配置为 always-sanitize，自动全部脱敏..."
            python "$SCRIPT_DIR/make_all_sanitize.py" "$SCAN_OUTPUT" > "$DECISION_FILE"
        elif [ "$SENSITIVE_MODE" = "keep-as-is" ]; then
            echo "  ⏭️  已配置为 keep-as-is，跳过脱敏"
        else
            python "$SCRIPT_DIR/sensitive_scan.py" interactive "$SCAN_OUTPUT" \
                --output "$DECISION_FILE" || {
                echo "  ⚠️  交互失败，默认全部脱敏"
                python "$SCRIPT_DIR/make_all_sanitize.py" "$SCAN_OUTPUT" > "$DECISION_FILE"
            }
        fi
        if [ -s "$DECISION_FILE" ]; then
            echo "  → 对工作仓库中的文件执行脱敏..."
            python "$SCRIPT_DIR/sensitive_scan.py" apply "$WORK_REPO/skills/$SKILL_NAME" \
                --decisions "$DECISION_FILE" \
                --scan-result "$SCAN_OUTPUT"
        fi
        rm -f "$SCAN_OUTPUT" "$DECISION_FILE" 2>/dev/null || true
    else
        echo "  ✅ 未发现敏感信息"
        rm -f "$SCAN_OUTPUT" 2>/dev/null || true
    fi
fi

# ── 5. 更新 README.md ─────────────────────────
echo ""
echo "[5/8] 更新 README.md..."
if [ -f "$README_FILE" ]; then
    echo "  🔄 全量重新生成 README.md（从仓库实际文件）..."
    python "$SCRIPT_DIR/update_readme.py" "$REPO_NAME" "$README_FILE"
else
    echo "  ⚠️  README.md 不存在，跳过"
fi

# ── 6. 提交并推送到双平台 ──────────────────────────
echo ""
echo "[6/8] 提交并推送..."
cd "$WORK_REPO"
git config user.email "workbuddy@local" 2>/dev/null || true
git config user.name "WorkBuddy" 2>/dev/null || true
git add "skills/$SKILL_NAME/"
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

# ── 7. 生成 ZIP 安装包 ──────────────────────────
echo ""
echo "[7/8] 生成 ZIP 安装包..."
mkdir -p "$DIST_DIR"
rm -f "$ZIP_FILE"

# ── 7.5 打包前敏感信息扫描 ──────────────────────
echo ""
echo "[7.5/8] 打包前敏感信息扫描..."
ZIP_SOURCE="$SKILLS_DIR/$SKILL_NAME"  # 默认用源目录
ZIP_TMP=""

if [ "$SKIP_SCAN" = true ]; then
    echo "  ⏭️  已跳过（--skip-scan）"
else
    SCAN_OUTPUT_ZIP="$SCRIPT_DIR/.sensitive_scan_${SKILL_NAME}_zip.json"
    DECISION_FILE_ZIP="${SCAN_OUTPUT_ZIP}.decisions.json"
    python "$SCRIPT_DIR/sensitive_scan.py" scan "$SKILLS_DIR/$SKILL_NAME" \
        --output "$SCAN_OUTPUT_ZIP" 2>/dev/null || true
    if [ -s "$SCAN_OUTPUT_ZIP" ]; then
        echo "  ⚠️  发现敏感信息，将在副本中脱敏..."
        rm -f "$DECISION_FILE_ZIP"
        if [ "$SENSITIVE_MODE" = "always-sanitize" ]; then
            python "$SCRIPT_DIR/make_all_sanitize.py" "$SCAN_OUTPUT_ZIP" > "$DECISION_FILE_ZIP"
        elif [ "$SENSITIVE_MODE" = "keep-as-is" ]; then
            echo "  ⏭️  已配置为 keep-as-is，跳过脱敏"
        else
            python "$SCRIPT_DIR/sensitive_scan.py" interactive "$SCAN_OUTPUT_ZIP" \
                --output "$DECISION_FILE_ZIP" || {
                python "$SCRIPT_DIR/make_all_sanitize.py" "$SCAN_OUTPUT_ZIP" > "$DECISION_FILE_ZIP"
            }
        fi
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

echo ""
echo "==============================================="
echo "  ✅ 全部完成: $SKILL_NAME v$VERSION"
echo "  📦 ZIP: $ZIP_FILE"
echo "==============================================="

# 刷新 .dist/index.html
python "$SCRIPT_DIR/build_index.py" "$DIST_DIR" 2>/dev/null || true
echo "  ✅ index.html 已刷新"

# 输出 ZIP 绝对路径（供用户取用）
echo ""
echo "ZIP 路径: $ZIP_FILE"
if command -v explorer >/dev/null 2>&1; then
    explorer "$(dirname "$(cygpath -w "$ZIP_FILE" 2>/dev/null || echo "$ZIP_FILE")")" 2>/dev/null || true
fi
