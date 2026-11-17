#!/usr/bin/env bash
# skillhub_cn_publish.sh — Step 10 (optional): 腾讯 skillhub.cn 发布
# Usage: SKILLHUB_CN_TOKEN=skh_xxx ./skillhub_cn_publish.sh <fork-abs-path>
#
# 协议（2026-07-13 实测）：
#   POST https://api.skillhub.cn/api/v1/community/skills/publish
#   Content-Type: multipart/form-data ; Authorization: Bearer skh_xxx
#   field "payload" (JSON): slug / name / displayName(必填) / summary / description / version
#   field "files" (repeated): 每个源码文件（白名单外的文件会被平台拒收）
set -euo pipefail

FORK="${1:-}"

if [[ -z "$FORK" ]]; then
  cat <<EOF >&2
Usage: SKILLHUB_CN_TOKEN=skh_xxx $0 <fork-abs-path>

  example: SKILLHUB_CN_TOKEN=skh_xxx $0 /abs/path/opensourceskills/my-skill

⚠️  必须用绝对路径。
⚠️  SKILLHUB_CN_TOKEN 前缀 skh_，与 GitHub/clawhub token 完全独立。
⚠️  Publish 成功后请立刻去 skillhub.cn 撤销该 token。
EOF
  exit 1
fi

case "$FORK" in /*) ;; *) echo "❌ 必须用绝对路径" >&2; exit 2 ;; esac
[[ -d "$FORK" ]] || { echo "❌ 不是目录: $FORK" >&2; exit 3; }
[[ -f "$FORK/SKILL.md" ]] || { echo "❌ SKILL.md not found in $FORK" >&2; exit 4; }

# 发布前清理派生缓存（__pycache__/*.pyc 等；部分 hub 会拒收 .pyc）
. "$(dirname "$0")/_lib_exclude.sh"
osg_clean_fork "$FORK"

if [[ -z "${SKILLHUB_CN_TOKEN:-}" ]]; then
  echo "❌ SKILLHUB_CN_TOKEN 环境变量未设置" >&2
  exit 5
fi
command -v curl >/dev/null 2>&1 || { echo "❌ 需要 curl" >&2; exit 6; }
command -v python3 >/dev/null 2>&1 || { echo "❌ 需要 python3（生成 payload/解析响应）" >&2; exit 6; }

API="https://api.skillhub.cn"
AUTH="Authorization: Bearer $SKILLHUB_CN_TOKEN"

# ---- 从 SKILL.md frontmatter 提取字段 ----
SLUG="$(basename "$FORK")"
NAME="$(grep -m1 -o '^name:[[:space:]]*.*' "$FORK/SKILL.md" 2>/dev/null | sed 's/^name:[[:space:]]*//' || echo "$SLUG")"
NAME="${NAME:-$SLUG}"
# Version：优先 frontmatter `version:` 字段，回退正文 `**Version**: x.y.z`，最后兜底 1.0.0
# 注意：grep 无匹配返回 1，set -euo pipefail 下须 || true 防脚本中断
VERSION="$(grep -m1 -o '^version:[[:space:]]*[0-9]*\.[0-9]*\.[0-9]*' "$FORK/SKILL.md" 2>/dev/null | grep -o '[0-9]*\.[0-9]*\.[0-9]*' || true)"
if [[ -z "$VERSION" ]]; then
  VERSION="$(grep -m1 -o '\*\*Version\*\*:[[:space:]]*[0-9]*\.[0-9]*\.[0-9]*' "$FORK/SKILL.md" 2>/dev/null | grep -o '[0-9]*\.[0-9]*\.[0-9]*' || true)"
fi
VERSION="${VERSION:-1.0.0}"
# displayName：优先 # 一级标题，回退 name
DISPLAY="$(grep -m1 -o '^#[[:space:]]*.*' "$FORK/SKILL.md" 2>/dev/null | sed 's/^#[[:space:]]*//' || echo "$NAME")"
DISPLAY="${DISPLAY:-$NAME}"
# description/summary：取 frontmatter description 首句（折叠多行）
DESC="$(awk '/^description:/{f=1;sub(/^description:[ >|]*/,"");if($0!="")print;next} f&&/^[a-zA-Z_]+:/{exit} f{gsub(/^[ \t]+/,"");print}' "$FORK/SKILL.md" 2>/dev/null | tr '\n' ' ' | sed 's/  */ /g;s/ *$//')"
[[ -z "$DESC" ]] && DESC="$DISPLAY"
SUMMARY="$(echo "$DESC" | cut -c1-40)"

# changelog：不放进 payload 的话，平台会填默认值 "Initial release"（2026-09-05 实测）。
# 优先独立 CHANGELOG.md 的首条版本记录（本 skill 的惯例，见 scaffold.sh），
# 回退 SKILL.md 内嵌变更日志首条（形如 "- **v1.3.4（2026-09-05）**：..."），
# 两者都没有则留空（平台回退默认文案）。
CHANGELOG=""
if [[ -f "$FORK/CHANGELOG.md" ]]; then
  # 兼容常见写法：## [1.0.0] - date / ### v1.0.17 (2026-08-03) / ## 1.0.3
  CHANGELOG="$(grep -m1 -oE '^#{2,4}[[:space:]]*v?\[?[0-9]+\.[0-9]+\.[0-9]+\]?.*' "$FORK/CHANGELOG.md" 2>/dev/null | sed -e 's/^#*[[:space:]]*//' || true)"
fi
if [[ -z "$CHANGELOG" ]]; then
  CHANGELOG="$(grep -m1 -oE '^-[[:space:]]*\*\*v[0-9]+\.[0-9]+\.[0-9]+[^]]*\*\*[:：].*' "$FORK/SKILL.md" 2>/dev/null || true)"
  # 去掉行首列表符与加粗标记；标题行常以「：」结尾而正文在子列表里，故一并去掉结尾孤立冒号
  CHANGELOG="$(printf '%s' "$CHANGELOG" | sed -e 's/^-[[:space:]]*//' -e 's/\*\*//g' -e 's/[:：][[:space:]]*$//')"
fi
CHANGELOG="$(printf '%s' "$CHANGELOG" | cut -c1-300)"

echo "ℹ️  slug=$SLUG  version=$VERSION"
echo "ℹ️  displayName=$DISPLAY"
if [[ -n "$CHANGELOG" ]]; then
  echo "ℹ️  changelog=$CHANGELOG"
else
  echo "⚠️  未提取到 changelog（无 CHANGELOG.md 且 SKILL.md 无内嵌版本记录）→ 平台将填默认值"
fi

# ---- 校验 token + slug 可用性 ----
echo "🔎 校验 token 与 slug..."
me_code="$(curl -s -o /dev/null -w '%{http_code}' --max-time 20 -H "$AUTH" "$API/api/v1/auth/me" 2>/dev/null || echo 000)"
if [[ "$me_code" == "401" ]]; then echo "❌ token 无效（401）" >&2; exit 7; fi

# ---- 组装 payload JSON（python 安全转义，写临时文件避免 curl -F 内联字符串被空格/特殊字符截断）----
PAYLOAD_FILE="$(mktemp "${TMPDIR:-/tmp}/skh_payload.XXXXXX.json")"
trap 'rm -f "$PAYLOAD_FILE"' EXIT
python3 - "$SLUG" "$NAME" "$DISPLAY" "$SUMMARY" "$DESC" "$VERSION" "$CHANGELOG" > "$PAYLOAD_FILE" <<'PY'
import json,sys
slug,name,display,summary,desc,version,changelog=sys.argv[1:8]
payload={
  "slug":slug,"name":name,"displayName":display,
  "summary":summary,"description":desc,"version":version,
  "claimSlug":True,"joinContest":False
}
# 仅在提取到时带 changelog，避免用空串覆盖平台默认文案
if changelog:
    payload["changelog"]=changelog
print(json.dumps(payload,ensure_ascii=False))
PY

# ---- 收集要发的文件（白名单：只发源码；剔除无后缀文件/dotfile/archive/签名/依赖）----
cd "$FORK"
FILES=()
while IFS= read -r f; do
  f="${f#./}"
  case "$f" in
    .git/*|node_modules/*|output/*|tmp/*|tests/*|assets/*.png|assets/*.jpg|assets/*.jpeg|assets/*.webp) continue ;;   # 目录/大二进制/测试产物/预览图
    LICENSE|NOTICE|COPYING|.gitignore|.gitattributes|sign.key|.osg-exclude) continue ;;  # 平台白名单拒收/本地配置
    *.tar.gz|*.tgz|*.zip|*.bin|*.dat|*.DS_Store|*.pyc|*.pyo|*/__pycache__/*) continue ;;
    *) FILES+=("$f") ;;
  esac
done < <(find . -type f 2>/dev/null | sort)

if [[ ${#FILES[@]} -eq 0 ]]; then echo "❌ 无可发布文件" >&2; exit 8; fi
echo "ℹ️  待发 ${#FILES[@]} 个文件: ${FILES[*]}"

# ---- multipart publish ----
CURL_ARGS=(-s --max-time 180 -X POST "$API/api/v1/community/skills/publish"
           -H "$AUTH" -F "payload=<$PAYLOAD_FILE;type=application/json")
for f in "${FILES[@]}"; do CURL_ARGS+=(-F "files=@$f;type=application/octet-stream"); done

echo "🚀 Publishing to skillhub.cn ..."
RESP="$(curl "${CURL_ARGS[@]}" 2>&1)"
echo "$RESP"

# ---- 解析结果 ----
if echo "$RESP" | grep -q '"ok":true'; then
  echo ""
  echo "✅ Published to skillhub.cn ($VERSION)"
  # 验真：detail 接口回查
  echo "🔎 验真..."
  D="$(curl -s --max-time 20 -H "$AUTH" "$API/api/v1/skills/$SLUG" 2>/dev/null)"
  echo "$D" | grep -q "\"slug\":\"$SLUG\"" && echo "✅ detail 验真通过" || echo "⚠️  detail 未查到，稍后手动确认"
else
  echo "" >&2
  echo "❌ Publish 失败，原始响应见上。常见原因：" >&2
  echo "   - displayName 不能为空（本脚本已自动提取，若仍报请检查 SKILL.md 一级标题）" >&2
  echo "   - slug 格式（须 ^[a-z0-9][a-z0-9-]*[a-z0-9]$）" >&2
  echo "   - token 失效 / 实名认证未完成" >&2
  exit 9
fi

echo ""
echo "🔐 立刻去 skillhub.cn 撤销刚才用的 token"
