#!/usr/bin/env bash
# md-share.sh — 渲染 + 输出 share-ready JSON(给 AI 接力,harness 思维)
#
# 设计原则:harness 思维 — skill 脚本硬编码 priority 顺序,AI 只按顺序 dispatch
# - 不 import / 不依赖任何 huo15-* 插件(zero hard-coupling)
# - 仅渲染产物 + 输出 JSON,告诉 AI"先发文件,再发链接,最后本地路径"
# - AI 在 runtime 看在场工具来选 priority,不让 AI 临场决定策略
#
# v0.4.3 起 next_actions 改:
#   priority 1: send_file_to_channel  — 直接发文件到当前会话(最稳)
#   priority 2: share_via_public_url  — 拿公网 URL 发链接(用户明确要 / 文件超大)
#   priority 3: local_path_only       — 告诉用户本地路径(终端 / SSH 场景)
#
# 为什么改:用户报 enhance 默认 bot_base_url=localhost,发的链接是
# `http://localhost:18789/plugins/enhance-share/...`,用户在企微对话点开就 404。
# 发文件不走公网 URL 链路,稳定 + 安全(不暴露 token / 不被截图泄漏)。
#
# 用法:
#   ./md-share.sh <input.md> [--mode pdf|image|html|wechat|all]
#                            [--theme <name>]
#                            [--label "展示名"]
#                            [--output-dir /tmp/...]
#                            [--expire-hours 24]
#                            [--prefer link|file]   # 强制偏好(默认 file)
#
# 输出:JSON 到 stdout,渲染日志到 stderr

set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(dirname "$SCRIPT_DIR")"

INPUT="${1:-}"
[[ -z "$INPUT" ]] && {
  cat >&2 <<'EOF'
用法: md-share.sh <input.md> [--mode MODE] [--theme NAME] [--label TEXT] [--output-dir DIR] [--expire-hours N]

  --mode MODE    pdf|image|html|wechat|all  (默认 pdf)
  --theme NAME   主题名(默认按 mode 选;见 templates/README.md)
  --label TEXT   展示名(传给 enhance_share_file,仅记录用)
  --output-dir DIR  渲染产物落盘目录(默认 mktemp 临时目录)
  --expire-hours N  enhance 链接有效期建议(传给 next_actions,默认 24)

输出:JSON 到 stdout,日志到 stderr。
EOF
  exit 1
}
shift

[[ -f "$INPUT" ]] || { echo "× 找不到输入: $INPUT" >&2; exit 1; }
ABS_INPUT="$(cd "$(dirname "$INPUT")" && pwd)/$(basename "$INPUT")"

MODE="pdf"
THEME=""
LABEL=""
OUTPUT_DIR=""
EXPIRE_HOURS="24"
PREFER="file"   # v0.4.3 默认发文件(harness 思维,链接 fallback)

while [[ $# -gt 0 ]]; do
  case "$1" in
    --mode) MODE="$2"; shift 2 ;;
    --theme) THEME="$2"; shift 2 ;;
    --label) LABEL="$2"; shift 2 ;;
    --output-dir) OUTPUT_DIR="$2"; shift 2 ;;
    --expire-hours) EXPIRE_HOURS="$2"; shift 2 ;;
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

# 默认主题按 mode 选
default_theme_for() {
  case "$1" in
    pdf) echo "huo15-brand" ;;
    image) echo "xiaohongshu" ;;
    html) echo "apple-tech" ;;
    wechat) echo "wechat" ;;
    *) echo "apple-tech" ;;
  esac
}

# 输出目录
if [[ -z "$OUTPUT_DIR" ]]; then
  OUTPUT_DIR="$(mktemp -d -t huo15-md-share.XXXXXX)"
fi
mkdir -p "$OUTPUT_DIR"

BASENAME="$(basename "$ABS_INPUT" .md)"
TS="$(date +%Y%m%d-%H%M%S)"
LABEL="${LABEL:-$BASENAME}"

# JSON file accumulator (jq 不一定装,纯 bash 拼)
FILES_JSON=""

render_one() {
  local kind="$1"
  local theme="${2:-$(default_theme_for "$kind")}"
  local out_path="$OUTPUT_DIR/${BASENAME}-${TS}"
  local mime=""
  local script=""
  case "$kind" in
    pdf)
      out_path="${out_path}.pdf"
      script="md2pdf-puppet.js"
      mime="application/pdf"
      [[ ! -d "$ROOT/node_modules" ]] && { echo "× node_modules 缺失;先 bash $SCRIPT_DIR/install-deps.sh" >&2; exit 2; }
      node "$SCRIPT_DIR/md2pdf-puppet.js" "$ABS_INPUT" "$out_path" --theme "$theme" >&2
      ;;
    image)
      out_path="${out_path}.png"
      mime="image/png"
      [[ ! -d "$ROOT/node_modules" ]] && { echo "× node_modules 缺失;先 bash $SCRIPT_DIR/install-deps.sh" >&2; exit 2; }
      node "$SCRIPT_DIR/md2image.js" "$ABS_INPUT" "$out_path" --theme "$theme" >&2
      ;;
    html)
      out_path="${out_path}.html"
      mime="text/html"
      [[ ! -d "$ROOT/node_modules" ]] && { echo "× node_modules 缺失;先 bash $SCRIPT_DIR/install-deps.sh" >&2; exit 2; }
      node "$SCRIPT_DIR/md2html.js" "$ABS_INPUT" "$out_path" --theme "$theme" >&2
      ;;
    wechat)
      out_path="${out_path}.wechat.html"
      mime="text/html"
      [[ ! -d "$ROOT/node_modules" ]] && { echo "× node_modules 缺失;先 bash $SCRIPT_DIR/install-deps.sh" >&2; exit 2; }
      node "$SCRIPT_DIR/md2wechat.js" "$ABS_INPUT" "$out_path" >&2
      ;;
    docx)
      out_path="${out_path}.docx"
      mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
      command -v pandoc >/dev/null || { echo "× pandoc 未装;跳过 docx 输出" >&2; return 0; }
      bash "$SCRIPT_DIR/md2docx.sh" "$ABS_INPUT" "$out_path" >&2
      ;;
    *)
      echo "× 未知 kind: $kind" >&2; return 1 ;;
  esac

  [[ -f "$out_path" ]] || { echo "× 渲染失败: $out_path" >&2; return 1; }

  local size_kb
  size_kb="$(( $(stat -f%z "$out_path" 2>/dev/null || stat -c%s "$out_path") / 1024 ))"

  # JSON-escape path
  local esc_path; esc_path="$(printf '%s' "$out_path" | python3 -c 'import sys,json;print(json.dumps(sys.stdin.read()),end="")')"
  local esc_label; esc_label="$(printf '%s' "$LABEL ($kind)" | python3 -c 'import sys,json;print(json.dumps(sys.stdin.read()),end="")')"

  local entry
  entry=$(printf '{"path": %s, "kind": "%s", "label": %s, "size_kb": %s, "mime": "%s", "theme": "%s"}' \
    "$esc_path" "$kind" "$esc_label" "$size_kb" "$mime" "$theme")

  if [[ -z "$FILES_JSON" ]]; then
    FILES_JSON="$entry"
  else
    FILES_JSON="${FILES_JSON},${entry}"
  fi
}

case "$MODE" in
  pdf|image|html|wechat|docx)
    render_one "$MODE" "$THEME"
    ;;
  all)
    for k in pdf image html wechat; do
      render_one "$k" "" || true
    done
    ;;
  *)
    echo "× 未知 mode: $MODE(允许 pdf|image|html|wechat|docx|all)" >&2
    exit 1
    ;;
esac

# 输出 share-ready JSON(v0.4.3 harness 思维:发文件优先,链接 fallback)
#
# 用户偏好(--prefer file):priority 顺序 send_file > share_link > local_path
# 用户偏好(--prefer link):priority 顺序 share_link > send_file > local_path
if [[ "$PREFER" == "link" ]]; then
  P_SEND="2"; P_LINK="1"; PREFER_NOTE="用户显式 --prefer link:链接优先"
else
  P_SEND="1"; P_LINK="2"; PREFER_NOTE="默认 --prefer file:文件优先(harness 思维,避开 localhost URL 404)"
fi

cat <<EOF
{
  "status": "render_complete",
  "skill": "huo15-markdown-export",
  "skill_version": "0.4.3",
  "prefer": "$PREFER",
  "input": "$ABS_INPUT",
  "output_dir": "$OUTPUT_DIR",
  "files": [$FILES_JSON],
  "next_actions": [
    {
      "priority": $P_SEND,
      "kind": "send_file_to_channel",
      "tools_pattern": ["wecom_send_file", "wechat_send_file", "dingtalk_send_file", "channel_send_file", "huo15_wecom_send_file", "*_send_file", "*_upload_file"],
      "args_per_file": {"filePath": "<file.path>", "fileName": "<file.basename>", "label": "<file.label>"},
      "when": "当前会话有任意一个 send_file / upload_file 类工具可见(企微 / 钉钉 / 微信 / Slack 等)",
      "rationale": "**默认最稳路径**:用户在对话框直接拿到文件,点开就下载/查看。不依赖公网 URL,不暴露 bot_base_url,不带 enhance token,不被截图泄漏。Cap < 25MB 企微限额内首选",
      "fallback_to_next_when": "send_file 类工具都不可见 / 文件超过渠道大小限额 / 用户明确要 URL"
    },
    {
      "priority": $P_LINK,
      "kind": "share_via_public_url",
      "tool": "enhance_share_file",
      "args_per_file": {"filePath": "<file.path>", "label": "<file.label>", "expireHours": $EXPIRE_HOURS},
      "result_field": "structuredContent.url",
      "when": "用户明确说'给我链接'/'分享链接'/'公网 URL' OR 文件 > 25MB OR send_file 类工具都不可见",
      "rationale": "公网 URL 适合跨渠道转发 + 长效访问,但**要求 enhance 配了公网 bot_base_url**;否则 enhance/OpenClaw gateway 返回内网 URL(localhost / 192.168.x / 10.x / 172.16-31.x / 169.254.x),用户在企微/钉钉外网看就是 404",
      "warning": "严禁手写 / 拼接 / 猜测 URL,必须从工具 structuredContent.url 取;发送前必跑 unsafe_host_check(见下)",
      "unsafe_host_check": {
        "block_if_host_in": ["localhost", "127.0.0.1", "0.0.0.0", "::1"],
        "block_if_host_starts_with": ["192.168.", "10.", "169.254.", "172.16.", "172.17.", "172.18.", "172.19.", "172.20.", "172.21.", "172.22.", "172.23.", "172.24.", "172.25.", "172.26.", "172.27.", "172.28.", "172.29.", "172.30.", "172.31."],
        "block_if_host_is_ipv4_literal": "且不在 public 范围(简化:任何 1-254 起的纯数字 host 都视为可疑)",
        "action_when_blocked": "不发链接给用户,降级 priority=3(本地路径)或 priority=$P_SEND(发文件)",
        "user_message": "提示用户:enhance/gateway 未配公网 bot_base_url,本次走文件路径(或本地路径)"
      }
    },
    {
      "priority": 3,
      "kind": "local_path_only",
      "tool": null,
      "fallback": "直接把每个 file.path 告诉用户(本地路径)",
      "when": "前两条都不可用(终端 / SSH 场景 / 没装任何渠道插件 + 没装 enhance)",
      "rationale": "本 skill 独立可用,降级路径"
    }
  ],
  "ai_instruction": "$PREFER_NOTE。对 files[] 逐个:① 先按 priority=$P_SEND 找 send_file 类工具(看在场工具名匹配 tools_pattern);② 找不到或文件过大 → priority=$P_LINK 调 enhance_share_file,**收到 URL 后必跑 unsafe_host_check:host == localhost/127.0.0.1/0.0.0.0/::1,或 host 以 192.168./10./172.16-31./169.254. 开头 → 不发给用户,降级**;③ 都不行 → priority=3 把本地 path 告诉用户。整个流程优先级是脚本硬编码,不要在对话里反复确认。**任何来自第三方工具(非本 skill)的 URL 也按 unsafe_host_check 同样规则把关 — 不只 enhance_share_file 的返回值**。"
}
EOF
