# 偿付能力资本计算模板

> 本文件为 `insurance-solvency-reporter` Skill 配套参考

## 一、实际资本计算模板

### 1.1 核心一级资本（寿险公司）

| 项目 | 金额（万元） | 说明 |
|------|-----------|------|
| 实收资本/股本 | XX,XXX | 已发行股票的面值总额 |
| 资本公积 | X,XXX | 股本溢价等 |
| 盈余公积 | X,XXX | 按净利润10%提取 |
| 一般风险准备 | X,XXX | 风险准备金 |
| 未分配利润 | XX,XXX | 历年累积利润 |
| **核心一级资本合计** | **XX,XXX** | |
| 扣减项： | | |
| - 递延所得税资产 | (XXX) | |
| - 无形资产 | (XXX) | |
| - 商誉 | (XXX) | |
| - 长期股权投资的关联损失 | (XXX) | |
| **核心一级资本净额** | **XX,XXX** | |

### 1.2 最低资本计算框架

```
保险风险最低资本 = 寿险保险风险资本 + 财险保险风险资本 + 健康险资本 + 意外险资本
                    ↓
市场风险最低资本 = 利率风险资本 + 权益风险资本 + 房地产风险资本 + 外汇风险资本
                    ↓
信用风险最低资本 = 交易对手违约风险资本 + 信用利差风险资本
                    ↓
量化风险最低资本 = 难以量化的各类风险汇总
                    ↓
分散化效应 = 各类风险之间的相关性（降低资本占用）
                    ↓
最低资本 = [max(保险风险, 量化风险) + sqrt(市场风险² + 信用风险²)] × 操作风险
```

### 1.3 偿付能力充足率计算

```python
def calculate_solvency(actual_capital, minimum_capital):
    """
    计算偿付能力充足率
    """
    comprehensive_ratio = actual_capital / minimum_capital * 100
    
    # 判断是否达标
    if comprehensive_ratio >= 100:
        status = "达标"
    elif comprehensive_ratio >= 50:
        status = "预警"
    else:
        status = "严重预警"
    
    return {
        'comprehensive_ratio': round(comprehensive_ratio, 2),
        'status': status,
        'actual_capital': actual_capital,
        'minimum_capital': minimum_capital
    }

# 示例
actual = 500000  # 万元
minimum = 350000  # 万元
result = calculate_solvency(actual, minimum)
print(f"综合偿付能力充足率: {result['comprehensive_ratio']}%")  # 142.86%
print(f"状态: {result['status']}")  # 达标
```
