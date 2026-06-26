# 价格归一化算法

## 归一化目标

将不同平台、不同优惠形式的价格统一转换为**等效到手价**，实现公平对比。

## 归一化步骤

### Step 1: 货币统一

所有价格转换为人民币（CNY）：

| 原币种 | 汇率参考 | 转换公式 |
|--------|----------|----------|
| USD | ~7.2 | USD × 7.2 |
| EUR | ~7.8 | EUR × 7.8 |
| JPY | ~0.048 | JPY × 0.048 |
| HKD | ~0.92 | HKD × 0.92 |

### Step 2: 优惠计算

根据优惠类型计算实际支付金额：

```python
def calculate_final_price(base_price, promotions):
    final = base_price
    
    # 直接折扣
    if 'discount_rate' in promotions:
        final *= promotions['discount_rate']
    
    # 满减
    if 'threshold' in promotions and final >= promotions['threshold']:
        final -= promotions['reduction']
    
    # 优惠券
    if 'coupon' in promotions:
        final -= promotions['coupon']
    
    # 赠品折价
    if 'gift_value' in promotions:
        final -= promotions['gift_value']
    
    return max(0, final)
```

### Step 3: 运费处理

| 场景 | 处理方式 |
|------|----------|
| 包邮 | 运费 = 0 |
| 固定运费 | 运费加入总价 |
| 满额包邮 | 如未达门槛，加运费 |
| 会员包邮 | 根据会员状态判断 |

### Step 4: 多件分摊

如优惠基于多件购买，需计算单件等效价：

```
单件等效价 = 总价 / 数量
```

**示例**：买 2 件减 50 元，单件 199 元
```
单件等效价 = (199 × 2 - 50) / 2 = 174 元
```

## 商品匹配算法

### 多维特征哈希

```python
def generate_product_hash(product):
    features = [
        product['brand'],           # 品牌
        product['model'],           # 型号
        product['sku_code'],        # SKU 编码
        product['main_image_hash'], # 主图哈希
        product['title_keywords'],  # 标题关键词
    ]
    return hash('|'.join(features))
```

### 匹配度计算

| 特征 | 权重 | 说明 |
|------|------|------|
| 品牌 + 型号 | 40% | 核心识别 |
| SKU 编码 | 30% | 精确匹配 |
| 主图相似度 | 20% | 视觉识别 |
| 标题关键词 | 10% | 辅助匹配 |

**判定规则**：
- 匹配度 ≥ 85% → 同一商品
- 匹配度 60-84% → 可能相同，需用户确认
- 匹配度 < 60% → 不同商品

## 历史价格对比

### 数据源
- 平台历史价格 API
- 第三方价格追踪服务
- 本地缓存记录

### 对比维度

| 指标 | 说明 |
|------|------|
| 当前价 | 实时抓取价格 |
| 历史最低 | 近 90 天最低价 |
| 历史均价 | 近 30 天平均价 |
| 价格趋势 | 涨/跌/持平 |

### 推荐逻辑

```python
def generate_recommendation(products):
    # 按等效到手价排序
    sorted_products = sorted(products, key=lambda x: x['final_price'])
    
    cheapest = sorted_products[0]
    second = sorted_products[1] if len(sorted_products) > 1 else None
    
    if second and (second['final_price'] - cheapest['final_price']) / cheapest['final_price'] < 0.05:
        # 价差小于 5%，考虑其他因素
        if cheapest['delivery_days'] > second['delivery_days'] + 2:
            return second['platform'] + "（价差小，配送更快）"
    
    return cheapest['platform'] + f"（省¥{second['final_price'] - cheapest['final_price']:.0f}）"
```

## 输出示例

```markdown
## 价格归一化结果

**原始数据**：
- 京东：¥7,999（白条减 200，运费 0）
- 天猫：¥8,199（88VIP 95 折，运费 0）
- 拼多多：¥7,599（百亿补贴，运费 10）

**归一化后**：
- 京东：¥7,799（减 200 后）
- 天猫：¥7,789（95 折后）
- 拼多多：¥7,609（含运费）

**推荐**：拼多多（最低价，省¥180）
```
