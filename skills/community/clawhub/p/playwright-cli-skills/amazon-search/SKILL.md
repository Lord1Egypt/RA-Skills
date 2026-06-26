# Amazon Product Search Skill

## 概述
使用 Playwright CLI 自动搜索亚马逊商品，提取 Top 10 商品数据并生成 CSV 文件。

## 前置要求
- Playwright CLI 已安装
- 亚马逊登录状态已保存（`~/amazon-auth.json`）

## 使用方法

### 1. 加载登录状态
```bash
playwright-cli state-load ~/amazon-auth.json
```

### 2. 搜索商品（替换 YOUR_KEYWORD 为你的关键词）
```bash
playwright-cli goto "https://www.amazon.com/s?k=YOUR_KEYWORD&s=best-selling"
```

### 3. 等待页面加载完成后，提取数据
```bash
playwright-cli eval "Array.from(document.querySelectorAll('[data-component-type=\"s-search-result\"]')).slice(0,10).map((el, i) => { const asin = el.getAttribute('data-asin'); const title = el.querySelector('h2')?.textContent?.trim() || ''; const linkEl = el.querySelector('h2 a'); const link = linkEl ? 'https://www.amazon.com' + linkEl.getAttribute('href') : ''; const priceEl = el.querySelector('.a-price .a-offscreen'); let price = priceEl ? priceEl.textContent.trim() : ''; const ratingEl = el.querySelector('[aria-label*=\"out of 5 stars\"]'); const rating = ratingEl ? ratingEl.getAttribute('aria-label').match(/[\\d.]+/)?.[0] : ''; const reviewsEl = el.querySelector('a[href*=\"customerReviews\"] span'); const reviews = reviewsEl ? reviewsEl.textContent.replace(/[()]/g, '') : ''; const img = el.querySelector('img')?.src || ''; const salesInfo = el.querySelector('[aria-label*=\"bought in past month\"]')?.textContent || ''; return {rank: i+1, asin, title, price, rating, reviews, salesInfo, img, link: link.substring(0,150)}; })"
```

### 4. 生成 CSV 文件
使用提取的数据生成 CSV，格式如下：
```csv
排名,商品名称,评分,评价数,价格,销量信息,图片URL,商品链接,ASIN
1,商品名称,4.8,105,$5.98,-,图片URL,https://www.amazon.com/dp/ASIN,ASIN
```

## 关键注意事项

### ⚠️ 重要：ASIN 必须是真实的
- **不要**编造 ASIN 号码
- 从页面元素 `[data-asin]` 属性中提取
- 亚马逊链接格式：`https://www.amazon.com/dp/[ASIN]`

### ⚠️ 图片 URL
- 从 `img` 标签的 `src` 属性提取
- 通常是 `https://m.media-amazon.com/images/...` 格式

### ⚠️ 价格和评分
- 价格：`.a-price .a-offscreen` selector
- 评分：`[aria-label*="out of 5 stars"]` 的 aria-label 属性
- 评价数：`a[href*="customerReviews"] span`

## 完整脚本示例

```javascript
// 提取 Top 10 商品数据
const products = Array.from(document.querySelectorAll('[data-component-type="s-search-result"]')).slice(0,10).map((el, i) => {
  const asin = el.getAttribute('data-asin');
  const title = el.querySelector('h2')?.textContent?.trim() || '';
  const priceEl = el.querySelector('.a-price .a-offscreen');
  const price = priceEl ? priceEl.textContent.trim() : '';
  const ratingEl = el.querySelector('[aria-label*="out of 5 stars"]');
  const rating = ratingEl ? ratingEl.getAttribute('aria-label').match(/[\d.]+/)?.[0] : '';
  const reviewsEl = el.querySelector('a[href*="customerReviews"] span');
  const reviews = reviewsEl ? reviewsEl.textContent.replace(/[()]/g, '') : '';
  const img = el.querySelector('img')?.src || '';
  const salesInfo = el.querySelector('[aria-label*="bought in past month"]')?.textContent || '';
  
  return {
    rank: i+1,
    asin,
    title: title.substring(0,80),
    price,
    rating,
    reviews,
    salesInfo,
    img,
    link: `https://www.amazon.com/dp/${asin}`
  };
});

console.log(JSON.stringify(products, null, 2));
```

## 常见错误

### 错误1：编造 ASIN
❌ 错误：`B0C5Y8VZ9X`（随机生成）  
✅ 正确：从页面 `data-asin` 属性提取

### 错误2：错误的链接格式
❌ 错误：`https://www.amazon.com/product/B0xxx`  
✅ 正确：`https://www.amazon.com/dp/B0xxx`

### 错误3：未加载登录状态
搜索前必须先执行 `state-load ~/amazon-auth.json`

## 输出文件命名规范
```
amazon-{keyword}-top10-{date}.csv
```

例如：`amazon-graduation-favor-bags-top10-2025-01-15.csv`
