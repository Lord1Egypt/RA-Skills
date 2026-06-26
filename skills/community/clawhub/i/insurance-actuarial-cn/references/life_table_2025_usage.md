# 第四套生命表(2025)使用说明与精算定价公式

> 本文件为 `insurance-actuarial-cn` Skill 配套参考

## 一、第四套生命表概述

**发布机构**：中国精算师协会
**发布日期**：2025年10月29日
**实施日期**：2026年1月1日（金融监管总局同步发文）
**取代**：第三套生命表（2010版，基线数据2005-2008年）

### 三张核心表

| 表名 | 表编号 | 适用业务 |
|------|-------|---------|
| 非养老类业务一表 | CL1 | 定期寿险、终身寿险（保障型） |
| 非养老类业务二表 | CL2 | 两全保险、年金保险（储蓄型） |
| 养老类业务表 | CL3 | 专属养老保险、养老年金 |

### 与第三套生命表主要差异

| 维度 | 第三套(2010) | 第四套(2025) | 差异影响 |
|------|-------------|-------------|---------|
| 基线数据 | 2005-2008年 | 2018-2023年 | 反映寿命延长趋势 |
| 男性预期寿命(60岁) | +20.7岁 | +22.5岁 | 年金险赔付期延长约2年 |
| 女性预期寿命(60岁) | +24.2岁 | +26.1岁 | 女性养老险成本上升 |
| 养老类业务 | 无专项表 | **新增CL3专项表** | 养老险定价更精准 |
| 编制机构 | 中国人寿保险业经验生命表编制办公室 | 中国精算师协会 | 权威性提升 |

## 二、生命表基础符号与计算

### 符号说明

| 符号 | 定义 | 说明 |
|------|------|------|
| l_x | x岁初始生存人数 | 基准：l_0 = 100,000（假设基数） |
| d_x | x岁至x+1岁的死亡人数 | d_x = l_x - l_{x+1} |
| q_x | x岁的死亡率 | q_x = d_x / l_x |
| p_x | x岁的生存率 | p_x = 1 - q_x |
| e_x | x岁的人均余命 | e_x = Σ(l_{x+t} / l_x)，t=0到极限年龄 |
| _nP_x | x岁在未来n年内的生存概率 | _nP_x = l_{x+n} / l_x |

### 定价基本公式

```
定期寿险趸缴纯保费：
  A_{x:n}^1 = Σ v^{k+1} × d_{x+k} / l_x    (k = 0, 1, ..., n-1)
  其中 v = 1/(1+i)，i = 预定利率

生存年金（期首付）：
  äx:n = Σ v^k × _kP_x    (k = 0, 1, ..., n-1)

期缴纯保费：
  P = A_{x:n}^1 / äx:n   （定期寿险）
  P = A_x / äx           （终身寿险）

  其中 A_x = Σ v^{k+1} × d_{x+k} / l_x （终身寿险趸缴纯保费）
```

## 三、精算定价代码示例

```python
# 第四套生命表定价示例
import numpy as np

# 第四套生命表(2025) CL1 示例数据（简化版，实际使用完整表）
# 数据来源：中国精算师协会《中国人身保险业经验生命表（2025）》

# 定期寿险定价（30岁男性，保额100万，保障20年，预定利率3.0%）
def term_life_premium(age, sum_assured, term, interest_rate, table='CL1'):
    """
    定期寿险期缴纯保费计算
    """
    # 加载第四套生命表数据（实际应用中从官方文件读取）
    l_x = load_life_table(table)  # 生存人数表
    d_x = load_decrement_table(table)  # 死亡人数表
    
    v = 1 / (1 + interest_rate)  # 折现因子
    i = interest_rate
    
    # 死亡给附现值（A公式）
    death_pv = 0
    for k in range(term):
        # 第k年的死亡率
        q = d_x[age + k] / l_x[age + k]
        # 折现因子
        v_k1 = v ** (k + 1)
        death_pv += v_k1 * q
    
    # 生存年金现值（ä公式，期首付）
    annuity_pv = 0
    for k in range(term):
        # 第k年的生存率
        p = 1 - d_x[age + k] / l_x[age + k]
        v_k = v ** k
        annuity_pv += v_k * np.prod([1 - d_x[age + j] / l_x[age + j] for j in range(k)])
    
    # 期缴纯保费
    pure_premium = sum_assured * death_pv / annuity_pv
    
    return {
        'pure_premium': pure_premium,
        'death_pv': death_pv,
        'annuity_pv': annuity_pv,
        'v': v
    }

# 终身寿险定价
def whole_life_premium(age, sum_assured, interest_rate, table='CL1'):
    """
    终身寿险期缴纯保费（生命表到105岁）
    """
    l_x = load_life_table(table)
    d_x = load_decrement_table(table)
    v = 1 / (1 + interest_rate)
    
    death_pv = 0
    for k in range(105 - age):  # 生命表极限年龄约105岁
        q = d_x[age + k] / l_x[age + k]
        death_pv += v ** (k + 1) * q
    
    # 终身生存年金（简化）
    annuity_pv = sum(1 / (1 + interest_rate) ** k * l_x[age + k] / l_x[age] for k in range(105 - age))
    
    return sum_assured * death_pv / annuity_pv
```

## 四、准备金计算公式

```python
def calculate_reserve(age, sum_assured, policy_year, premium, 
                     interest_rate, table='CL1'):
    """
    过去法计算寿险责任准备金
    准备金 = 已缴纯保费累积值 - 已给付保险金现值
    
    第t年末准备金（过去法）：
    _tV = P × ä'_x:t - A^1_{x:t}
    
    其中：
    - P：期缴纯保费
    - ä'_x:t：已缴保费累积值（考虑利息）
    - A^1_{x:t}：已给付保险金现值
    """
    v = 1 / (1 + interest_rate)
    
    # 已缴保费累积值（过去法）
    premium_accumulated = premium * ((1 + interest_rate) ** policy_year - 1) / interest_rate
    
    # 未来给付现值（未来法，简化）
    future_payment_pv = sum_assured * 0.02 * v ** policy_year  # 简化估算
    
    reserve = premium_accumulated - future_payment_pv
    
    return max(0, reserve)  # 准备金不能为负
```

## 五、预定利率上限与产品设计协同

| 时间段 | 预定利率上限 | 适用险种 |
|-------|-----------|---------|
| 2013-2019年 | 4.025% | 普通型寿险 |
| 2019-2023年 | 3.5% | 普通型寿险 |
| 2023年起 | 3.0% | 普通型寿险 |
| 2024年起 | 分红险上限2.0% | 分红险 |
| 现行 | 3.0%（普通型） | 终身寿险/年金险 |

**产品策略建议**：
- 预定利率3.0%环境下：增额终身寿险竞争力下降，年金险价值凸显
- 分红险+万能账户组合：对抗利率下行风险
- 健康险（定价不受利率上限约束）：重点发展方向
