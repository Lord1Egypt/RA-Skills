#!/bin/bash

# Amazon Product Search Automation Script
# Usage: ./amazon-search.sh "your search keyword"

KEYWORD="$1"

if [ -z "$KEYWORD" ]; then
    echo "❌ 错误：请提供搜索关键词"
    echo "用法: ./amazon-search.sh \"graduation party favor bags\""
    exit 1
fi

# 转换关键词用于文件名（替换空格为-）
FILENAME_KEYWORD=$(echo "$KEYWORD" | tr ' ' '-' | tr -d '"')
DATE=$(date +%Y-%m-%d)
OUTPUT_FILE="$HOME/amazon-${FILENAME_KEYWORD}-top10-${DATE}.csv"

echo "🔍 开始搜索亚马逊商品: $KEYWORD"
echo "📁 输出文件: $OUTPUT_FILE"

# Step 1: 加载登录状态
echo "📋 Step 1: 加载登录状态..."
playwright-cli state-load ~/amazon-auth.json

# Step 2: 搜索商品（URL编码关键词）
echo "🔎 Step 2: 搜索商品..."
ENCODED_KEYWORD=$(echo "$KEYWORD" | sed 's/ /+/g')
playwright-cli goto "https://www.amazon.com/s?k=${ENCODED_KEYWORD}&s=best-selling"

# Step 3: 等待页面加载
echo "⏳ Step 3: 等待页面加载..."
sleep 3

# Step 4: 提取数据并生成 CSV
echo "📊 Step 4: 提取商品数据..."

# 创建 CSV 头部
echo "排名,商品名称,评分,评价数,价格,销量信息,图片URL,商品链接,ASIN" > "$OUTPUT_FILE"

# 使用 Playwright 提取数据并追加到 CSV
playwright-cli eval "
const products = Array.from(document.querySelectorAll('[data-component-type=\"s-search-result\"]')).slice(0,10).map((el, i) => {
  const asin = el.getAttribute('data-asin');
  const title = el.querySelector('h2')?.textContent?.trim() || '';
  const priceEl = el.querySelector('.a-price .a-offscreen');
  const price = priceEl ? priceEl.textContent.trim() : '';
  const ratingEl = el.querySelector('[aria-label*=\"out of 5 stars\"]');
  const rating = ratingEl ? ratingEl.getAttribute('aria-label').match(/[\\d.]+/)?.[0] : '';
  const reviewsEl = el.querySelector('a[href*=\"customerReviews\"] span');
  const reviews = reviewsEl ? reviewsEl.textContent.replace(/[()]/g, '') : '';
  const img = el.querySelector('img')?.src || '';
  const salesInfo = el.querySelector('[aria-label*=\"bought in past month\"]')?.textContent || '';
  
  return {
    rank: i+1,
    asin,
    title: title.replace(/,/g, ';').substring(0,100),
    price,
    rating,
    reviews,
    salesInfo,
    img,
    link: asin ? 'https://www.amazon.com/dp/' + asin : ''
  };
});

// 生成 CSV 行
const csvRows = products.map(p => \
  p.rank + ',' + 
  '\"' + p.title + '\",' + 
  p.rating + ',' + 
  p.reviews + ',' + 
  '\"' + p.price + '\",' + 
  '\"' + p.salesInfo + '\",' + 
  '\"' + p.img + '\",' + 
  '\"' + p.link + '\",' + 
  p.asin
).join('\\n');

// 输出到控制台，让 bash 捕获
console.log('CSV_DATA_START');
console.log(csvRows);
console.log('CSV_DATA_END');
" --raw 2>/dev/null | tee /tmp/amazon_output.txt

# 提取 CSV 数据并追加到文件
sed -n '/CSV_DATA_START/,/CSV_DATA_END/p' /tmp/amazon_output.txt | grep -v "CSV_DATA" >> "$OUTPUT_FILE"

echo ""
echo "✅ 完成！CSV 文件已生成: $OUTPUT_FILE"
echo ""
echo "📊 数据预览："
head -6 "$OUTPUT_FILE" | column -t -s,
