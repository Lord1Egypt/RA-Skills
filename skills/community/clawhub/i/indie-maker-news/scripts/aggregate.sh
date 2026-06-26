#!/bin/bash
# 独行者 Daily - 变现雷达（完整版）
# 9个可靠数据源，真正提供一人公司变现内容！

echo "=================================================="
echo "独行者 Daily - 变现雷达"
echo "读对一条新闻，少走一年弯路"
echo "=================================================="
echo "📍 9个数据源："
echo "  创业类：36氪、虎嗅、创业邦"
echo "  开发类：V2EX、Indie Hackers"
echo "  技术类：Hacker News、GitHub、掘金"
echo ""

python3 scripts/fetch-news-full.py

echo ""
echo "✅ 数据聚合完成！"
echo "💡 聚焦一人公司变现机会"
