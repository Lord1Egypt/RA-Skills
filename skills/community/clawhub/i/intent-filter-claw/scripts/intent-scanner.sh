#!/usr/bin/env bash
# intent-scanner.sh — 意向识别采集与分析命令参考
# 注意：实际平台采集需要对应平台的 API 权限和 Cookie
# 本脚本提供命令结构参考，实际执行需配置平台凭证

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"

usage() {
  cat <<EOF
用法: intent-scanner.sh <命令> [选项]

命令:
  scan      扫描平台评论（需要平台 API 权限）
  analyze   分析本地评论文件，输出意向线索
  dispatch  将线索推送到飞书

scan 选项:
  --platform    平台名称 (xiaohongshu|douyin|weibo|zhihu|bilibili)
  --keyword     监控关键词
  --days        采集最近 N 天（默认 7）
  --output      输出文件路径（默认 ./data/comments.csv）

analyze 选项:
  --input           输入评论文件（CSV，需含 username,content 列）
  --score-threshold 意向评分阈值（默认 70）
  --output          输出线索文件路径（默认 ./leads/high-intent.csv）

dispatch 选项:
  --leads    线索文件路径
  --channel  推送渠道 (feishu)
  --chat-id  飞书群 chat_id 或用户 open_id

示例:
  # 扫描小红书护肤品相关评论（最近 7 天）
  ./scripts/intent-scanner.sh scan \\
    --platform xiaohongshu \\
    --keyword "护肤品推荐" \\
    --days 7 \\
    --output ./data/xiaohongshu-comments.csv

  # 分析评论文件，筛选评分 ≥70 的高意向用户
  ./scripts/intent-scanner.sh analyze \\
    --input ./data/comments.csv \\
    --score-threshold 70 \\
    --output ./leads/high-intent.csv

  # 将线索推送到飞书群
  ./scripts/intent-scanner.sh dispatch \\
    --leads ./leads/high-intent.csv \\
    --channel feishu \\
    --chat-id oc_xxxxxxxx
EOF
}

cmd="${1:-}"
shift || true

case "$cmd" in
  scan)
    platform=""
    keyword=""
    days=7
    output="./data/comments.csv"
    while [[ $# -gt 0 ]]; do
      case "$1" in
        --platform) platform="$2"; shift 2 ;;
        --keyword)  keyword="$2";  shift 2 ;;
        --days)     days="$2";     shift 2 ;;
        --output)   output="$2";   shift 2 ;;
        *) echo "未知参数: $1"; exit 1 ;;
      esac
    done
    echo "[scan] 平台: $platform | 关键词: $keyword | 最近 ${days} 天"
    echo "[scan] 输出: $output"
    echo "[提示] 实际采集需要配置平台 API 凭证，请参考各平台开放平台文档"
    ;;

  analyze)
    input=""
    threshold=70
    output="./leads/high-intent.csv"
    while [[ $# -gt 0 ]]; do
      case "$1" in
        --input)           input="$2";     shift 2 ;;
        --score-threshold) threshold="$2"; shift 2 ;;
        --output)          output="$2";    shift 2 ;;
        *) echo "未知参数: $1"; exit 1 ;;
      esac
    done
    if [[ -z "$input" ]]; then
      echo "[错误] 请指定 --input 文件路径"
      exit 1
    fi
    echo "[analyze] 输入: $input | 阈值: $threshold | 输出: $output"
    echo "[提示] 实际分析由 AI Agent 执行，本脚本提供命令结构参考"
    ;;

  dispatch)
    leads=""
    channel="feishu"
    chat_id=""
    while [[ $# -gt 0 ]]; do
      case "$1" in
        --leads)    leads="$2";   shift 2 ;;
        --channel)  channel="$2"; shift 2 ;;
        --chat-id)  chat_id="$2"; shift 2 ;;
        *) echo "未知参数: $1"; exit 1 ;;
      esac
    done
    echo "[dispatch] 线索文件: $leads | 渠道: $channel | 目标: $chat_id"
    echo "[提示] 实际推送通过 OpenClaw message 工具执行"
    ;;

  help|--help|-h)
    usage
    ;;

  *)
    echo "未知命令: $cmd"
    usage
    exit 1
    ;;
esac
