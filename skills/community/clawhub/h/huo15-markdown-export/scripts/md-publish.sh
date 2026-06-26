#!/usr/bin/env bash
# md-publish.sh — 渲染多端产物 + 本地 KB 归档 + 输出二阶段 share-ready JSON
#
# 设计目标:把"发出去给人看"和"给自己留档"做成同一个动作。
# 与 md-share.sh 的差别:
#   - md-share:轻量,单/多产物 + share JSON,不归档
#   - md-publish:多产物默认 + 自动 KB 归档(~/knowledge/huo15/) + 二阶段 QR PDF 提示
#
# 设计原则(同 md-share):capability detection,零硬依赖
#   - 不 import / 不 spawn enhance / 不 spawn wecom
#   - JSON 输出告诉 AI 接下来怎么 chain(优先 enhance,无则降级)
#   - 装本 skill 没装 enhance 也能跑:KB 归档照写,share URL 留 placeholder
#
# 用法:
#   ./md-publish.sh <input.md> [--mode all|pdf|image|html|wechat]
#                              [--slug my-q1-summary]    # KB 归档文件名,不传 = basename
#                              [--label "Q1 复盘"]
#                              [--with-qr]               # 启用二阶段 QR PDF(需要 enhance)
#                              [--no-archive]            # 跳过 KB 归档
#                              [--kb-dir ~/knowledge/huo15]
#                              [--expire-hours 24]
#
# 默认 mode=all:同一份 md 一次性渲染 PDF / PNG长图 / HTML / 公众号 inline
# AI 拿到 4 个 share URL 后组装"多版本菜单"消息发回当前会话,人在回路决定转发
#
# JSON 输出额外字段(相比 md-share):
#   - kb_archive: { path, slug, frontmatter_keys: [...] }
#   - post_share_actions:
#       1. 把每个 file 的 enhance URL 回写到 KB 归档 frontmatter 的 share_urls
#       2. 若 --with-qr:用第一个 PDF 的 URL 重新调 md2pdf-puppet --qr-url 生成带二维码的打印版
#       3. (可选) 把 KB 归档文件本身也 enhance_share 一次,作为"原始 markdown"备份链接

set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(dirname "$SCRIPT_DIR")"

INPUT="${1:-}"
[[ -z "$INPUT" ]] && {
  cat >&2 <<'EOF'
用法: md-publish.sh <input.md> [--mode all|pdf|image|html|wechat] [--slug NAME] [--label TEXT]
                                [--with-qr] [--no-archive] [--kb-dir DIR] [--expire-hours N]

默认 mode=all,自动 KB 归档到 ~/knowledge/huo15/YYYY-MM-DD-<slug>.md。
EOF
  exit 1
}
shift
[[ -f "$INPUT" ]] || { echo "× 找不到输入: $INPUT" >&2; exit 1; }
ABS_INPUT="$(cd "$(dirname "$INPUT")" && pwd)/$(basename "$INPUT")"

MODE="all"
SLUG=""
LABEL=""
WITH_QR=0
NO_ARCHIVE=0
KB_DIR="$HOME/knowledge/huo15"
EXPIRE_HOURS="24"
OUTPUT_DIR=""
PREFER="file"   # v0.4.3 默认发文件(harness 思维)

while [[ $# -gt 0 ]]; do
  case "$1" in
    --mode) MODE="$2"; shift 2 ;;
    --slug) SLUG="$2"; shift 2 ;;
    --label) LABEL="$2"; shift 2 ;;
    --with-qr) WITH_QR=1; shift ;;
    --no-archive) NO_ARCHIVE=1; shift ;;
    --kb-dir) KB_DIR="$2"; shift 2 ;;
    --expire-hours) EXPIRE_HOURS="$2"; shift 2 ;;
    --output-dir) OUTPUT_DIR="$2"; shift 2 ;;
    --prefer) PREFER="$2"; shift 2 ;;
    --*) echo "未知选项: $1" >&2; exit 1 ;;
    *) echo "未知参数: $1" >&2; exit 1 ;;
  esac
done

# 标准化 PREFER
case "$PREFER" in
  file|link) ;;
  *) echo "--prefer 只能是 file 或 link,得到: $PREFER" >&2; exit 1 ;;
esac

BASENAME="$(basename "$ABS_INPUT" .md)"
SLUG="${SLUG:-$BASENAME}"
LABEL="${LABEL:-$SLUG}"
TODAY="$(date +%F)"
TS="$(date +%Y%m%d-%H%M%S)"

# 校验 slug 安全(只允许 [a-zA-Z0-9_一-龥-])
if [[ ! "$SLUG" =~ ^[A-Za-z0-9_-]+$ ]] && ! python3 -c "import re,sys; re.fullmatch(r'[\w-]+',sys.argv[1]) or sys.exit(1)" "$SLUG" 2>/dev/null; then
  echo "× slug 仅允许字母/数字/下划线/中划线/中文: $SLUG" >&2
  exit 1
fi

# 渲染输出目录
[[ -z "$OUTPUT_DIR" ]] && OUTPUT_DIR="$(mktemp -d -t huo15-md-publish.XXXXXX)"
mkdir -p "$OUTPUT_DIR"

# 调用 md-share 完成基础渲染 + 拿基础 JSON
echo "→ 渲染产物 (mode=$MODE)..." >&2
SHARE_JSON="$(bash "$SCRIPT_DIR/md-share.sh" "$ABS_INPUT" --mode "$MODE" --label "$LABEL" --output-dir "$OUTPUT_DIR" --expire-hours "$EXPIRE_HOURS" --prefer "$PREFER")"

# KB 归档
KB_ARCHIVE_PATH=""
if [[ $NO_ARCHIVE -eq 0 ]]; then
  mkdir -p "$KB_DIR"
  KB_ARCHIVE_PATH="$KB_DIR/${TODAY}-${SLUG}.md"

  # 抽取首段作为 KB summary
  SUMMARY=$(awk '
    /^---$/{toggle=!toggle; next}
    toggle{next}
    /^#/{next}
    /^[[:space:]]*$/{if(found)exit; next}
    {gsub(/[*_`~#>]/,""); print; found=1; if(NR>30)exit}
  ' "$ABS_INPUT" | head -3 | tr '\n' ' ' | sed 's/  */ /g' | cut -c1-200)

  # 写归档 frontmatter + 原文
  {
    echo "---"
    echo "title: ${LABEL}"
    echo "slug: ${SLUG}"
    echo "published_at: ${TODAY}"
    echo "source: ${ABS_INPUT}"
    echo "summary: \"${SUMMARY}\""
    echo "render_outputs:"
    # 从 SHARE_JSON 抽 file paths
    echo "$SHARE_JSON" | python3 -c '
import json, sys
j = json.load(sys.stdin)
for f in j.get("files", []):
    print(f"  - kind: {f[\"kind\"]}")
    print(f"    path: {f[\"path\"]}")
    print(f"    size_kb: {f[\"size_kb\"]}")
    print(f"    theme: {f.get(\"theme\",\"\")}")
'
    echo "share_urls: []   # AI 调 enhance_share_file 后回写"
    echo "tags: [复盘, 火一五]"
    echo "---"
    echo
    cat "$ABS_INPUT"
  } > "$KB_ARCHIVE_PATH"

  echo "→ KB 归档:$KB_ARCHIVE_PATH" >&2
fi

# 拼最终 JSON:在 share JSON 基础上加 kb_archive + post_share_actions
# 用 python 做 JSON 合并保证合法
python3 - "$SHARE_JSON" "$KB_ARCHIVE_PATH" "$WITH_QR" "$EXPIRE_HOURS" "$LABEL" "$SLUG" "$ABS_INPUT" "$SCRIPT_DIR" "$PREFER" <<'PYEOF'
import json, sys, os
share_json_str, kb_path, with_qr, expire_h, label, slug, abs_input, script_dir, prefer = sys.argv[1:10]
j = json.loads(share_json_str)

j["skill"] = "huo15-markdown-export"
j["mode"] = "publish"
j["label"] = label
j["slug"] = slug

if kb_path:
    j["kb_archive"] = {
        "path": kb_path,
        "slug": slug,
        "frontmatter_keys": ["title","slug","published_at","source","summary","render_outputs","share_urls","tags"],
    }
else:
    j["kb_archive"] = None

# post_share_actions:v0.4.3 harness 思维 — 默认发文件(--prefer file),链接 fallback
# step 1 顺序由 PREFER 决定:file → send_file 在前;link → share_link 在前
j["prefer"] = prefer
j["skill_version"] = "0.4.3"

send_file_action = {
    "for_each_file": True,
    "kind": "send_file_to_channel",
    "tools_pattern": ["wecom_send_file", "wechat_send_file", "dingtalk_send_file", "channel_send_file", "huo15_wecom_send_file", "*_send_file", "*_upload_file"],
    "args_per_file": {"filePath": "<file.path>", "fileName": "<file.basename>", "label": "<file.label>"},
    "when": "当前会话有任意一个 send_file / upload_file 类工具可见(企微 / 钉钉 / 微信 / Slack 等)",
    "rationale": "**默认最稳路径**:用户在对话框直接拿到文件。不依赖公网 URL,不暴露 token,不被截图泄漏。≤25MB 企微限额内首选",
    "fallback_to_next_when": "send_file 工具都不可见 / 文件超大 / 用户明确要 URL",
}

share_link_action = {
    "for_each_file": True,
    "kind": "share_via_public_url",
    "tool": "enhance_share_file",
    "args_per_file": {"filePath": "<file.path>", "label": "<file.label>", "expireHours": int(expire_h)},
    "result_field": "structuredContent.url",
    "when": "用户明确说'给我链接'/'分享链接' OR 文件 > 25MB OR send_file 工具都不可见",
    "rationale": "公网 URL 适合跨渠道转发,但**要求 enhance/OpenClaw gateway 配了公网 bot_base_url**;否则 URL host 是 localhost/192.168.x/10.x/172.16-31.x/169.254.x 等内网地址,企微/钉钉外网用户看就是 404",
    "warning": "严禁手写/拼接 URL,必须 structuredContent.url 取;**收到 URL 后跑 unsafe_host_check,内网地址不发,降级**",
    "unsafe_host_check": {
        "block_if_host_in": ["localhost", "127.0.0.1", "0.0.0.0", "::1"],
        "block_if_host_starts_with": [
            "192.168.", "10.", "169.254.",
            "172.16.", "172.17.", "172.18.", "172.19.", "172.20.", "172.21.",
            "172.22.", "172.23.", "172.24.", "172.25.", "172.26.", "172.27.",
            "172.28.", "172.29.", "172.30.", "172.31."
        ],
        "action_when_blocked": "不发链接,降级 priority=lower(本地路径 / 发文件)",
        "user_message": "enhance/gateway 未配公网 bot_base_url,本次走文件路径(或本地路径)"
    },
}

# 组装 step,按 prefer 决定顺序
if prefer == "link":
    post_actions = [
        {**share_link_action, "step": 1},
        {**send_file_action, "step": 2},
    ]
else:
    post_actions = [
        {**send_file_action, "step": 1},
        {**share_link_action, "step": 2},
    ]

if kb_path:
    post_actions.append({
        "step": len(post_actions) + 1,
        "tool": "Edit (内置文件编辑)",
        "target_file": kb_path,
        "instruction": (
            "若用了 share_via_public_url(step 中 enhance_share_file),把拿到的每个 URL 回写到 KB 归档 frontmatter 的 share_urls 列表,"
            "格式:`- {kind: pdf, url: 'https://...'}`。仅发文件场景跳过(没 URL 可回写)。"
        ),
        "skip_when": "本次只走 send_file_to_channel(无 URL 可写)",
    })

if with_qr == "1":
    pdf_files = [f for f in j["files"] if f["kind"] == "pdf"]
    if pdf_files:
        post_actions.append({
            "step": len(post_actions) + 1,
            "for_pdf_only": True,
            "tool": f"node {script_dir}/md2pdf-puppet.js",
            "args": {
                "input": abs_input,
                "output": pdf_files[0]["path"].replace(".pdf", ".qr.pdf"),
                "--theme": pdf_files[0].get("theme", "apple-tech"),
                "--qr-url": "<前面拿到的 PDF 文件对应的 enhance url>",
                "--qr-label": "扫码看在线版",
            },
            "instruction": (
                "二阶段:用 share_link 拿到的 PDF URL 重新跑 md2pdf-puppet,生成带二维码的打印版 PDF。"
                "**需要先有 enhance URL,所以这一步要求本次至少跑过一次 share_via_public_url**。"
            ),
            "skip_when": "本次未生成 enhance URL(仅走 send_file 路径)",
        })

j["post_share_actions"] = post_actions

# ai_instruction:解释 prefer 顺序 + 各步关系
prefer_note = (
    "**默认 prefer=file**(harness 思维):用户在对话框直接拿文件,避开 localhost URL 404。"
    if prefer == "file"
    else "用户显式 prefer=link:优先公网 URL,适合跨渠道转发场景。"
)
j["ai_instruction"] = (
    prefer_note + " 流程:"
    + ("1) 优先 send_file 工具发文件;2) 不行降级 enhance_share_file 拿 URL(**跑 unsafe_host_check:host 是 localhost/127.0.0.1/192.168.x/10.x/172.16-31.x/169.254.x 不发,降级**);" if prefer == "file"
       else "1) 优先 enhance_share_file 拿 URL(**跑 unsafe_host_check 同上**);2) 不行降级 send_file 工具直发文件;")
    + (f" 3) 若用了 share_link 且 URL 通过 unsafe_host_check,Edit 回写 URLs 到 kb_archive.path 的 frontmatter share_urls;" if kb_path else "")
    + (f" 4) (--with-qr)用 PDF URL 跑 md2pdf-puppet --qr-url 生成带二维码版;" if with_qr == "1" else "")
    + " 最后:把结果组装消息回当前会话用户,让用户自己决定转发到哪个群"
    + "(严禁主动广播、严禁 @all、严禁假设用户的目标群)。"
    + " **跨 skill 适用**:任何从第三方工具(enhance_preview / gateway static / agent 自写 HTML 等)拿到的 URL,也按 unsafe_host_check 把关 — 不只本 skill 的 enhance_share_file。"
)

print(json.dumps(j, ensure_ascii=False, indent=2))
PYEOF
