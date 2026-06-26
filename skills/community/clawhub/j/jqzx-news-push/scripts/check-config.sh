#!/bin/bash

# 检查每日新闻推送所需的环境变量配置

echo "🔍 检查每日新闻推送配置..."
echo ""

# 检查各环境变量
check_var() {
    local name=$1
    local value=$2
    if [ -z "$value" ]; then
        echo "❌ $name: 未配置"
        return 1
    else
        echo "✅ $name: 已配置"
        return 0
    fi
}

all_ok=true

check_var "JI_ZHIXIN_TOKEN (机器之心Token)" "$JI_ZHIXIN_TOKEN" || all_ok=false
check_var "GETNOTE_API_KEY (Get笔记API Key)" "$GETNOTE_API_KEY" || all_ok=false
check_var "GETNOTE_CLIENT_ID (Get笔记Client ID)" "$GETNOTE_CLIENT_ID" || all_ok=false
check_var "FEISHU_TARGET (飞书用户ID)" "$FEISHU_TARGET" || all_ok=false

echo ""

if [ "$all_ok" = true ]; then
    echo "✅ 所有配置完成！"
    echo ""
    echo "使用方法："
    echo "  • 说「推送今天的新闻」立即获取并发送"
    echo "  • 说「设置每日新闻」配置定时任务"
else
    echo "❌ 配置未完成，请先配置环境变量"
    echo ""
    echo "配置方法："
    echo "  将以下内容添加到 ~/.bashrc："
    echo ""
    echo "  export JI_ZHIXIN_TOKEN=\"你的机器之心Token\""
    echo "  export GETNOTE_API_KEY=\"你的Get笔记API Key\""
    echo "  export GETNOTE_CLIENT_ID=\"你的Get笔记Client ID\""
    echo "  export FEISHU_TARGET=\"你的飞书用户ID\""
    echo ""
    echo "  然后运行: source ~/.bashrc"
fi
