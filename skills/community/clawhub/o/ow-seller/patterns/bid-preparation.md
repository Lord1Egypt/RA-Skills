# 投标准备流程

## 买家评标四维度应对策略

### 维度 1：价格 (权重 50%)

**策略：最优报价计算**

```python
def calculate_optimal_price(buyer_budget, my_cost, min_margin=0.15):
    """
    计算最优投标价格
    
    Args:
        buyer_budget: 买家预算上限
        my_cost: 我的成本价
        min_margin: 最低利润率
    
    Returns:
        optimal_price: 最优报价
    """
    # 最低可接受价格
    min_price = my_cost * (1 + min_margin)
    
    # 如果预算充足，定价为预算的 60-70%
    if buyer_budget > min_price * 1.5:
        target_price = buyer_budget * 0.65
    else:
        # 预算紧张，定价接近成本
        target_price = min_price
    
    return round(target_price, 2)
```

**报价策略：**
- 预算充足 → 定价 60-70% 预算
- 预算适中 → 定价 75-85% 预算
- 预算紧张 → 定价接近成本 + 最低利润

---

### 维度 2：真品证明 (权重 20%)

**必需文件清单：**

| 文件类型 | 分值 | 获取方式 |
|----------|------|----------|
| 企业营业执照 | 20分 | 工商局办理 |
| 产品代理权证明 | 20分 | 品牌方授权 |
| 原厂授权书 | 15分 | 品牌方出具 |
| 产品质检报告 | 15分 | 第三方检测机构 |
| 进口报关单 | 15分 | 海关出具 |
| 门店照片 | 10分 | 实地拍摄 |

**文件准备建议：**
```
基础资质（必须）：
- 营业执照
- 代理权证明/授权书

进阶资质（推荐）：
- 质检报告
- 报关单（进口商品）

加分项：
- 实体店照片
- 以往成交记录
- 客户好评截图
```

---

### 维度 3：到货时间 (权重 10%)

**物流方案对比：**

| 快递公司 | 平均时效 | 价格 | 适用场景 |
|----------|----------|------|----------|
| 顺丰 | 2-3天 | 高 | 紧急、贵重物品 |
| 京东 | 2-4天 | 中高 | 品质要求高 |
| 中通 | 3-5天 | 低 | 常规物品 |
| 圆通 | 4-6天 | 低 | 预算有限 |

**承诺策略：**
- 有现货 → 承诺 2-3 天
- 需调货 → 承诺 5-7 天
- 需进口 → 承诺 14-21 天

---

### 维度 4：商家信誉 (权重 20%)

**信誉提升方法：**

1. **成交记录**
   - 展示过往成交数量
   - 列出类似商品成交案例

2. **好评率**
   - 维持 95% 以上好评
   - 展示客户评价截图

3. **平台认证**
   - 申请平台认证商家
   - 获取官方标识

4. **纠纷处理**
   - 0 纠纷记录最佳
   - 如有纠纷，说明处理结果

---

## 投标文件生成

### 自动生成投标 JSON

```python
def generate_bid(request, seller_info):
    """
    自动生成投标文件
    
    Args:
        request: 买家需求信息
        seller_info: 卖家信息
    
    Returns:
        bid: 完整的投标 JSON
    """
    bid = {
        "bid_id": generate_bid_id(),
        "req_id": request["req_id"],
        "supplier": {
            "name": seller_info["name"],
            "agent_id": seller_info["agent_id"],
            "contact": seller_info["contact"]
        },
        "price": {
            "amount": calculate_optimal_price(
                request.get("budget_max"),
                seller_info.get("cost")
            ),
            "currency": "CNY",
            "includes_shipping": True
        },
        "auth_docs": prepare_auth_docs(seller_info),
        "delivery": {
            "time_days": estimate_delivery(seller_info),
            "method": "顺丰快递",
            "tracking_available": True
        },
        "reputation": {
            "total_transactions": seller_info.get("total_sales", 0),
            "success_rate": seller_info.get("good_rate", 0.95),
            "disputes": seller_info.get("disputes", 0),
            "platform_verified": seller_info.get("verified", False)
        },
        "warranty": {
            "return_policy": "7天无理由退货",
            "refund_policy": "质量问题全额退款"
        },
        "timestamp": datetime.now().isoformat()
    }
    
    return bid
```

---

## 投标优化建议

### 高胜率投标特征

1. **价格适中** - 低于预算 20-30%
2. **资质完整** - 至少 3 项证明文件
3. **到货快速** - 承诺 3 天内
4. **信誉良好** - 好评率 > 95%

### 避免的投标错误

- ❌ 报价接近预算上限（无竞争力）
- ❌ 资质文件缺失
- ❌ 到货时间过长
- ❌ 新商家无信誉记录