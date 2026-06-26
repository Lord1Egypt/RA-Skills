#!/bin/bash
# iFinD MCP 便捷调用脚本

# 配置路径：优先使用 ~/.openclaw/，兼容旧路径 ~/.config/
MCPorter_CONFIG="${HOME}/.openclaw/mcporter.json"
if [ ! -f "$MCPorter_CONFIG" ]; then
    MCPorter_CONFIG="${HOME}/.config/mcporter.json"
fi

if [ ! -f "$MCPorter_CONFIG" ]; then
    echo "Error: mcporter config not found."
    echo "请先配置 ~/.openclaw/mcporter.json"
    echo "详见 SKILL.md 首次使用指引"
    exit 1
fi

if [ $# -lt 2 ]; then
    echo "Usage: $0 <stock|fund|edb|news> <query>"
    echo "Examples:"
    echo "  $0 stock '贵州茅台'"
    echo "  $0 fund '易方达科技ETF'"
    echo "  $0 edb '中国GDP'"
    echo "  $0 news '华为公告'"
    exit 1
fi

SERVER="$1"
QUERY="$2"

case "$SERVER" in
    stock)
        SERVER_NAME="hexin-ifind-stock"
        ;;
    fund)
        SERVER_NAME="hexin-ifind-fund"
        ;;
    edb)
        SERVER_NAME="hexin-ifind-edb"
        ;;
    news)
        SERVER_NAME="hexin-ifind-news"
        ;;
    *)
        echo "Error: Unknown server '$SERVER'"
        echo "Valid options: stock, fund, edb, news"
        exit 1
        ;;
esac

~/.npm-global/bin/mcporter --config "$MCPorter_CONFIG" call "$SERVER_NAME.get_stock_summary" query="$QUERY" 2>/dev/null || \
~/.npm-global/bin/mcporter --config "$MCPorter_CONFIG" call "$SERVER_NAME.search_funds" query="$QUERY" 2>/dev/null || \
~/.npm-global/bin/mcporter --config "$MCPorter_CONFIG" call "$SERVER_NAME.get_macro_data" query="$QUERY" 2>/dev/null || \
~/.npm-global/bin/mcporter --config "$MCPorter_CONFIG" call "$SERVER_NAME.get_company_news" query="$QUERY"
