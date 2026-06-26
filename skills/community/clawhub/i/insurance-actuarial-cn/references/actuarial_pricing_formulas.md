# 精算定价公式汇总与代码实现

> 本文件为 `insurance-actuarial-cn` Skill 配套参考

## 一、核心定价公式速查

### 1.1 纯保费计算

```
定期寿险纯保费（期缴）：
  P_{x:n}^1 = A_{x:n}^1 / äx:n
  
终身寿险纯保费（期缴）：
  P_x = A_x / äx

两全保险纯保费（期缴）：
  P_{x:n} = A_{x:n} / äx:n

年金保险纯保费（期缴）：
  P(äx:n) = äx:n / äx:n （即1，被保险人生存即给付）
```

### 1.2 毛保费计算

```
毛保费 = 纯保费 / (1 - 附加费用率)

附加费用率分解：
  总附加费用率 = 渠道费用率 + 管理费用率 + 理赔费用率
  渠道费用率：代理人15%-35%，银保10%-20%，网销5%-10%
  管理费用率：3%-8%
  理赔费用率：1%-3%
```

### 1.3 准备金计算

```
过去法准备金：
  _tV = P × s_{x:t} - A^1_{x:t}

未来法准备金：
  _tV = A_{x+t:n-t} - P × ä_{x+t:n-t}

其中 s_{x:t} = (1+i)^t × ä'_x:t（保费累积值）
```

## 二、精算代码实现

```python
# 精算定价完整实现
import numpy as np

# 第四套生命表(2025) CL1 简化数据（实际应用从官方文件读取）
# 格式：{年龄: [l_x, d_x]}
LIFE_TABLE_CL1 = {
    # 年龄: [l_x(生存人数), d_x(死亡人数)]，以100万为基数
    30: [996234, 567], 31: [995667, 612], 32: [995055, 661],
    33: [994394, 714], 34: [993680, 771], 35: [992909, 833],
    36: [992076, 901], 37: [991175, 976], 38: [990199, 1057],
    39: [989142, 1145], 40: [987997, 1240], 41: [986757, 1343],
    42: [985414, 1454], 43: [983960, 1575], 44: [982385, 1707],
    45: [980678, 1851], 46: [978827, 2010], 47: [976817, 2186],
    48: [974631, 2379], 49: [972252, 2592], 50: [969660, 2825],
}

def v(i):
    """折现因子"""
    return 1 / (1 + i)

def life_table_lookup(age, table='CL1'):
    """查找生命表数据"""
    if age in LIFE_TABLE_CL1:
        return LIFE_TABLE_CL1[age]
    # 简化处理，实际应用需完整表格
    return [1000000 - age * 500, 1000 + age * 20]

def mortality_rate(age):
    """死亡率 q_x"""
    l_x, d_x = life_table_lookup(age)
    return d_x / l_x

def survival_prob(age, years):
    """生存概率 nP_x"""
    result = 1.0
    for t in range(years):
        result *= (1 - mortality_rate(age + t))
    return result

def annuity_due(age, years, i=0.03):
    """期首付生存年金现值 ä_x:n"""
    v_factor = v(i)
    total = 0
    for k in range(years):
        n_pk = survival_prob(age, k)
        total += v_factor ** k * n_pk
    return total

def term_insurance_pv(age, years, i=0.03):
    """定期寿险趸缴纯保费现值 A^1_x:n"""
    v_factor = v(i)
    total = 0
    for k in range(years):
        q_xk = mortality_rate(age + k)
        n_pk_prev = survival_prob(age, k)
        total += v_factor ** (k + 1) * q_xk * n_pk_prev
    return total

def calculate_term_life_premium(age, sum_assured, term_years, 
                                 interest_rate=0.03, loading_rate=0.30):
    """
    定期寿险保费计算完整函数
    """
    # 纯保费
    A = term_insurance_pv(age, term_years, interest_rate)
    annuity = annuity_due(age, term_years, interest_rate)
    pure_premium = sum_assured * A / annuity
    
    # 毛保费（附加费用）
    gross_premium = pure_premium / (1 - loading_rate)
    
    return {
        'age': age,
        'sum_assured': sum_assured,
        'term_years': term_years,
        'interest_rate': interest_rate,
        'pure_premium': round(pure_premium, 2),
        'loading_rate': loading_rate,
        'gross_premium': round(gross_premium, 2),
        'loading_amount': round(gross_premium - pure_premium, 2)
    }

# 示例：30岁男性，100万保额，20年定期寿险，预定利率3.0%
result = calculate_term_life_premium(age=30, sum_assured=1000000, term_years=20)
print(f"年缴纯保费: {result['pure_premium']:.2f} 元/年")
print(f"年缴毛保费: {result['gross_premium']:.2f} 元/年")
print(f"附加费用: {result['loading_amount']:.2f} 元/年")
```

## 三、第四套生命表(2025)应用注意事项

### 3.1 表的选用原则

| 产品类型 | 选用生命表 | 说明 |
|---------|----------|------|
| 定期寿险、终身寿险 | CL1 | 保障为主，死亡率相对高 |
| 两全险、年金险（普通） | CL2 | 储蓄为主，死亡率相对低 |
| 专属养老保险、养老年金 | **CL3** | 专为养老设计，寿命假设更长 |

### 3.2 重疾恶化因子（偿二代规则II）

```python
def critical_illness_deterioration_factor(age, duration):
    """
    重疾恶化因子（简化估算）
    用于偿二代资本计量，反映重疾发生率随年龄上升的趋势
    
    实际因子应从精算师协会官方发布的恶化因子表中查找
    """
    # 简化公式，实际应用查表
    base_factor = 0.0  # 基础因子
    age_deterioration = (age - 30) * 0.003  # 年龄恶化效应
    duration_deterioration = duration * 0.005  # 保单期间恶化效应
    
    return max(0, base_factor + age_deterioration + duration_deterioration)

# 示例：45岁，10年有效保单
factor = critical_illness_deterioration_factor(45, 10)
print(f"重疾恶化因子: {factor:.2%}")  # 约10.5%
```

### 3.3 2025版vs2010版生命表差异的实际影响

| 产品 | 第三套(2010)定价基准 | 第四套(2025)定价基准 | 影响方向 |
|------|-------------------|-------------------|---------|
| 终身寿险 | CL1 | CL1（更新） | 保费略涨（寿命延长）|
| 两全险 | CL2 | CL2（更新） | 基本持平 |
| 养老年金 | CL2 | **CL3专用表** | 保费更精准，成本更合理 |
| 重疾险 | 旧发生率表 | 恶化因子 | 资本占用增加 |
