#!/bin/bash

# NAS电影下载脚本 (v4.0 - 支持自动归档到机械硬盘)
# 用途：下载电影到SSD，完成后自动移动字幕到机械硬盘并删除种子

set -e

# 配置
JACKETT_URL="${JACKETT_URL:-http://192.168.1.246:9117}"
JACKETT_API_KEY="${JACKETT_API_KEY:-o5gp976vq8cm084cqkcv30av9v3e5jpy}"
QB_URL="${QB_URL:-http://192.168.1.246:8888}"
QB_USERNAME="${QB_USERNAME:-admin}"
QB_PASSWORD="${QB_PASSWORD:-adminadmin}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# SMB配置 - SSD硬盘（下载临时存放）
SMB_USERNAME="${SMB_USERNAME:-13917908083}"
SMB_PASSWORD="${SMB_PASSWORD:-Roger0808}"
SMB_SERVER="${SMB_SERVER:-192.168.1.246}"
SMB_SHARE_SSD="super8083"           # SSD硬盘
SMB_PATH_DOWNLOAD="qb/downloads"    # 下载路径

# SMB配置 - 机械硬盘（最终归档）
SMB_SHARE_HDD="sata11-139XXXX8083"  # 机械硬盘
SMB_PATH_MOVIE="movie"              # 电影归档路径

# 字幕配置
SUBTITLE_LANGUAGES="${SUBTITLE_LANGUAGES:-zh,en}"
WITH_SUBTITLE="false"
ARCHIVE_AFTER_DOWNLOAD="false"

# 帮助信息
usage() {
    echo "用法: $0 -q <电影名称> [选项]"
    echo ""
    echo "参数："
    echo "  -q, --query          电影名称（必需）"
    echo "  -s, --subtitle       下载字幕"
    echo "  -a, --archive        下载完成后归档到机械硬盘并删除种子"
    echo "  -w, --wait           等待下载完成后执行后续操作"
    echo "  -l, --lang           字幕语言（默认：$SUBTITLE_LANGUAGES）"
    echo "  -h, --help           显示帮助"
    echo ""
    echo "示例："
    echo "  $0 -q \"电影名\" -s -a -w    # 下载+字幕+归档+等待完成"
    exit 1
}

# 解析参数
MOVIE_NAME=""
WAIT_COMPLETION="false"

while [[ $# -gt 0 ]]; do
    case $1 in
        -q|--query) MOVIE_NAME="$2"; shift 2 ;;
        -s|--subtitle) WITH_SUBTITLE="true"; shift ;;
        -a|--archive) ARCHIVE_AFTER_DOWNLOAD="true"; shift ;;
        -w|--wait) WAIT_COMPLETION="true"; shift ;;
        -l|--lang) SUBTITLE_LANGUAGES="$2"; shift 2 ;;
        -h|--help) usage ;;
        *) echo "未知参数: $1"; usage ;;
    esac
done

[[ -z "$MOVIE_NAME" ]] && { echo "错误：缺少电影名称"; usage; }

echo "========================================"
echo "🎥 NAS电影下载助手 v4.0"
echo "========================================"
echo "电影: $MOVIE_NAME"
echo "字幕: $WITH_SUBTITLE | 归档: $ARCHIVE_AFTER_DOWNLOAD"
echo "SSD: $SMB_SHARE_SSD | HDD: $SMB_SHARE_HDD"
echo ""

# 使用原脚本下载
export SMB_SHARE="$SMB_SHARE_SSD"
export SMB_PATH="$SMB_PATH_DOWNLOAD"
"$SCRIPT_DIR/download-movie.sh" -q "$MOVIE_NAME" ${WITH_SUBTITLE:+-s} ${WAIT_COMPLETION:+-w}

# 如果启用了归档且等待完成
if [[ "$ARCHIVE_AFTER_DOWNLOAD" == "true" && "$WAIT_COMPLETION" == "true" ]]; then
    echo ""
    echo "📦 开始归档流程..."
    
    # 调用归档脚本
    python3 "$SCRIPT_DIR/archive-movie.py" \
        --movie-name "$MOVIE_NAME" \
        --ssd-share "$SMB_SHARE_SSD" \
        --ssd-path "$SMB_PATH_DOWNLOAD" \
        --hdd-share "$SMB_SHARE_HDD" \
        --hdd-path "$SMB_PATH_MOVIE" \
        --qb-url "$QB_URL" \
        --qb-user "$QB_USERNAME" \
        --qb-pass "$QB_PASSWORD"
fi

echo ""
echo "========================================"
echo "✅ 任务完成"
echo "========================================"
