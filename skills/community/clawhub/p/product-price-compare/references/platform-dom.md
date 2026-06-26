# 电商平台 DOM 结构参考

## 京东 (JD.com)

### 商品列表页
```css
/* 商品卡片 */
.gl-item .p-price .i-price  /* 价格 */
.gl-item .p-name a  /* 商品标题 */
.gl-item .p-icons  /* 促销标签 */
```

### 商品详情页
```css
/* 价格 */
#summary .p-price .price  /* 当前价 */
#summary .p-price .total  /* 到手价 */

/* 促销信息 */
#summary .p-promo  /* 促销活动 */
#summary .p-promo .promo-text  /* 促销文本 */

/* 配送信息 */
#summary .p-delivery  /* 配送方式 */
```

## 天猫/淘宝 (Tmall/Taobao)

### 商品列表页
```css
/* 商品卡片 */
.item .price  /* 价格 */
.item .title  /* 商品标题 */
.item .promo  /* 促销信息 */
```

### 商品详情页
```css
/* 价格 */
.tb-rmb-num  /* 当前价 */
.tm-price  /* 活动价 */

/* 促销 */
.tb-detail-promotion  /* 促销活动 */
.tb-sku-price  /* SKU 价格 */

/* 配送 */
.tb-delivery  /* 配送信息 */
```

## 拼多多 (Pinduoduo)

### 商品列表页
```css
/* 商品卡片 */
.goods-card .price  /* 价格 */
.goods-card .name  /* 商品名称 */
.goods-card .tag  /* 标签（百亿补贴等）*/
```

### 商品详情页
```css
/* 价格 */
.price-box .current-price  /* 当前价 */
.price-box .original-price  /* 原价 */

/* 促销 */
.promo-box  /* 促销活动 */
.subsidy-tag  /* 百亿补贴标签 */

/* 配送 */
.delivery-info  /* 配送信息 */
```

## 元素提取注意事项

1. **价格格式**：可能包含"¥"、"元"等符号，需统一解析
2. **动态加载**：部分价格通过 JS 异步加载，需等待渲染
3. **多 SKU**：商品有多个规格时，需提取最低价或默认 SKU 价格
4. **会员价**：注意区分普通价与会员价（如 88VIP、Plus 会员）
