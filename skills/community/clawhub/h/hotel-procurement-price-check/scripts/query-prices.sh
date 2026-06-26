#!/bin/bash
#===============================================
# 酒店采购比价 - 价格查询脚本 v1.0
# 用途: 查询农产品/电商商品实时价格
#===============================================

set -e

PRODUCT="$1"
CATEGORY="${2:-all}"
QUERY_TIME=$(date '+%Y-%m-%d %H:%M')

if [ -z "$PRODUCT" ]; then
  echo "{\"error\": \"请提供商品名称\", \"example\": \"bash query-prices.sh 三文鱼\"}"
  exit 1
fi

echo "=========================================="
echo "  🛒 酒店采购比价助手"
echo "=========================================="
echo ""
echo "  📦 查询商品: $PRODUCT"
echo "  ⏰ 查询时间: $QUERY_TIME"
echo ""

# Step 1: 搜索农业农村部数据
search_agri_price() {
  local product="$1"
  echo "🔍 正在查询农产品批发价..."
  
  # 搜索今日农业农村部数据
  web_search_results=$(web_search --query "${product} 农产品批发价格 今日 最新" 2>/dev/null || echo "搜索失败")
  
  echo "$web_search_results"
}

# Step 2: 搜索一亩田数据  
search_ymt_price() {
  local product="$1"
  echo "🔍 正在查询一亩田批发价..."
  
  web_search_results=$(web_search --query "${product} 一亩田 批发价格" 2>/dev/null || echo "搜索失败")
  
  echo "$web_search_results"
}

# Step 3: 搜索电商价格
search_ecommerce_price() {
  local product="$1"
  echo "🔍 正在查询电商全网价格..."
  
  web_search_results=$(web_search --query "${product} 淘宝 京东 1688 拼多多 价格" 2>/dev/null || echo "搜索失败")
  
  echo "$web_search_results"
}

# Step 4: 搜索成本拆解数据
search_cost_breakdown() {
  local product="$1"
  echo "🔍 正在分析成本结构..."
  
  web_search_results=$(web_search --query "${product} 成本构成 BOM 原材料价格 毛利率" 2>/dev/null || echo "搜索失败")
  
  echo "$web_search_results"
}

# 根据类别执行搜索
case "$CATEGORY" in
  agri)
    search_agri_price "$PRODUCT"
    search_ymt_price "$PRODUCT"
    ;;
  ecommerce)
    search_ecommerce_price "$PRODUCT"
    ;;
  cost)
    search_cost_breakdown "$PRODUCT"
    ;;
  all|*)
    search_agri_price "$PRODUCT"
    search_ymt_price "$PRODUCT"
    search_ecommerce_price "$PRODUCT"
    ;;
esac

echo ""
echo "✅ 价格查询完成"
echo ""
echo "📋 使用说明:"
echo "   单独查询农产品: bash query-prices.sh \"$PRODUCT\" agri"
echo "   单独查询电商价: bash query-prices.sh \"$PRODUCT\" ecommerce"
echo "   成本拆解分析:   bash query-prices.sh \"$PRODUCT\" cost"
