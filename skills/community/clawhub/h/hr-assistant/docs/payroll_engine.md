# 薪资计算引擎文档

## 概述

薪资计算引擎是 HR 智能体的核心组件，负责计算员工薪资、个税、社保公积金。支持 2026 年最新的个税累计预扣法，以及年终奖优化计税。

## 核心特性

- ✅ **累计预扣法** — 严格按照税法计算每月个税
- ✅ **多城市社保** — 内置北上广深杭等城市社保参数
- ✅ **年终奖优化** — 自动选择最优计税方式
- ✅ **高精度计算** — 使用 Decimal 避免浮点误差
- ✅ **批量计算** — 支持多人薪资批量处理

## 架构设计

```
┌─────────────────────────────────────────────────────────────┐
│                      PayrollEngine                          │
│                    （薪资计算引擎）                          │
└─────────────────────────────────────────────────────────────┘
                              │
          ┌───────────────────┼───────────────────┐
          ▼                   ▼                   ▼
┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│  TaxCalculator  │  │InsuranceCalculator│  │  其他计算模块   │
│   （个税计算）   │  │  （社保公积金）   │  │                 │
└─────────────────┘  └─────────────────┘  └─────────────────┘
          │                   │
          ▼                   ▼
┌─────────────────┐  ┌─────────────────┐
│   2026税率表     │  │  城市社保配置库  │
│  （7级累进）     │  │ （北上广深杭等） │
└─────────────────┘  └─────────────────┘
```

## 个税计算

### 累计预扣法

2026年个税采用**累计预扣法**，计算公式：

```
本月应缴个税 = 累计应缴个税 - 累计已缴个税

其中：
累计应缴个税 = 累计应纳税所得额 × 税率 - 速算扣除数
累计应纳税所得额 = 累计收入 - 累计减除费用(5000×月数) - 累计社保公积金 - 累计专项附加扣除
```

### 2026年个税税率表

| 级数 | 累计应纳税所得额 | 税率 | 速算扣除数 |
|------|-----------------|------|-----------|
| 1 | 不超过 36,000 | 3% | 0 |
| 2 | 36,000 - 144,000 | 10% | 2,520 |
| 3 | 144,000 - 300,000 | 20% | 16,920 |
| 4 | 300,000 - 420,000 | 25% | 31,920 |
| 5 | 420,000 - 660,000 | 30% | 52,920 |
| 6 | 660,000 - 960,000 | 35% | 85,920 |
| 7 | 超过 960,000 | 45% | 181,920 |

### 计算示例

**场景**：张三 2026年1-3月工资均为 20,000 元，每月社保公积金 3,000 元

```
1月份：
累计应纳税所得额 = 20000 - 5000 - 3000 = 12000
累计应缴个税 = 12000 × 3% = 360
本月应缴个税 = 360 - 0 = 360

2月份：
累计应纳税所得额 = 40000 - 10000 - 6000 = 24000
累计应缴个税 = 24000 × 3% = 720
本月应缴个税 = 720 - 360 = 360

3月份：
累计应纳税所得额 = 60000 - 15000 - 9000 = 36000
累计应缴个税 = 36000 × 3% = 1080
本月应缴个税 = 1080 - 720 = 360
```

**4月份（税率跳档）**：
```
累计应纳税所得额 = 80000 - 20000 - 12000 = 48000
累计应缴个税 = 48000 × 10% - 2520 = 2280
本月应缴个税 = 2280 - 1080 = 1200  ← 比上月多840元
```

## 社保公积金计算

### 计算公式

```
个人缴纳 = 缴费基数 × 个人比例
单位缴纳 = 缴费基数 × 单位比例

缴费基数规则：
- 低于下限：按下限缴纳
- 高于上限：按上限缴纳
- 在范围内：按实际工资缴纳
```

### 北京 2026 社保参数示例

| 险种 | 个人比例 | 单位比例 | 基数下限 | 基数上限 |
|------|---------|---------|---------|---------|
| 养老保险 | 8% | 16% | 6,821 | 35,283 |
| 医疗保险 | 2% | 9.5% | 6,821 | 35,283 |
| 失业保险 | 0.5% | 0.5% | 6,821 | 35,283 |
| 工伤保险 | 0% | 0.4% | 6,821 | 35,283 |
| 生育保险 | 0% | 0.8% | 6,821 | 35,283 |
| 公积金 | 12% | 12% | 2,420 | 35,283 |

### 计算示例

**场景**：李四月薪 15,000 元，北京缴纳社保公积金

```
缴费基数：15,000（在 6821-35283 范围内）

养老保险：15000 × 8% = 1,200
医疗保险：15000 × 2% = 300
失业保险：15000 × 0.5% = 75
公积金：15000 × 12% = 1,800

个人缴纳合计：3,375
单位缴纳合计：约 5,775
```

## 年终奖计算

### 单独计税方式

```
年终奖个税 = 年终奖 × 适用税率 - 速算扣除数

适用税率确定：
年终奖 ÷ 12，按月度税率表确定
```

### 年终奖月度税率表

| 级数 | 月均奖金 | 税率 | 速算扣除数 |
|------|---------|------|-----------|
| 1 | 不超过 3,000 | 3% | 0 |
| 2 | 3,000 - 12,000 | 10% | 210 |
| 3 | 12,000 - 25,000 | 20% | 1,410 |
| 4 | 25,000 - 35,000 | 25% | 2,660 |
| 5 | 35,000 - 55,000 | 30% | 4,410 |
| 6 | 55,000 - 80,000 | 35% | 7,160 |
| 7 | 超过 80,000 | 45% | 15,160 |

### 年终奖陷阱

年终奖存在**税率跳档陷阱**，多发 1 元可能多缴数千元税：

```
年终奖 36,000 元：
个税 = 36000 × 3% = 1,080
税后 = 34,920

年终奖 36,001 元：
个税 = 36001 × 10% - 210 = 3,390.10
税后 = 32,610.90  ← 反而少了 2,309 元！
```

**建议**：年终奖避开以下陷阱区间
- 36,000 - 38,566
- 144,000 - 160,500
- 300,000 - 318,333
- 420,000 - 447,500
- 660,000 - 706,538
- 960,000 - 1,120,000

## API 使用

### 计算单月薪资

```python
from payroll_engine import PayrollEngine
from decimal import Decimal

engine = PayrollEngine()

result = engine.calculatePayroll(
    employeeId="E001",
    employeeName="张三",
    year=2026,
    month=3,
    baseSalary=Decimal('20000'),
    city="北京",
    positionAllowance=Decimal('3000'),
    performanceBonus=Decimal('5000'),
    cumulativeData={
        "cumulativeIncome": Decimal('40000'),  # 前2个月累计
        "cumulativeInsurance": Decimal('6000'),
        "cumulativeTax": Decimal('720')
    }
)

print(f"应发：{result.grossPay}")
print(f"社保：{result.totalInsurance}")
print(f"个税：{result.taxAmount}")
print(f"实发：{result.netPay}")
```

### 批量计算薪资

```python
employees = [
    {"employeeId": "E001", "employeeName": "张三", "baseSalary": 15000, "city": "北京"},
    {"employeeId": "E002", "employeeName": "李四", "baseSalary": 20000, "city": "上海", "performanceBonus": 5000},
]

results = engine.batchCalculatePayroll(
    employees=employees,
    year=2026,
    month=1
)
```

### 计算年终奖

```python
result = engine.calculateYearEndBonus(
    bonusAmount=Decimal('50000'),
    monthlySalary=Decimal('20000')
)

print(f"年终奖：{result.bonusAmount}")
print(f"个税：{result.taxAmount}")
print(f"税后：{result.netBonus}")
print(f"实际税率：{result.effectiveRate}%")
```

### 计算社保公积金

```python
from payroll_engine import InsuranceCalculator

result = InsuranceCalculator.calculateInsurance(
    salary=Decimal('15000'),
    city="北京",
    year=2026
)

print(f"养老保险：{result['pensionInsurance']}")
print(f"医疗保险：{result['medicalInsurance']}")
print(f"公积金：{result['housingFund']}")
print(f"合计：{result['totalInsurance']}")
```

## 数据结构

### MonthPayroll（单月薪资结果）

```python
@dataclass
class MonthPayroll:
    year: int                           # 年份
    month: int                          # 月份
    employeeId: str                     # 员工ID
    employeeName: str                   # 员工姓名
    
    # 收入项
    baseSalary: Decimal                 # 基本工资
    positionAllowance: Decimal          # 岗位津贴
    performanceBonus: Decimal           # 绩效奖金
    overtimePay: Decimal                # 加班费
    otherIncome: Decimal                # 其他收入
    grossPay: Decimal                   # 应发合计
    
    # 扣除项
    pensionInsurance: Decimal           # 养老保险
    medicalInsurance: Decimal           # 医疗保险
    unemploymentInsurance: Decimal      # 失业保险
    housingFund: Decimal                # 公积金
    totalInsurance: Decimal             # 社保公积金合计
    otherDeductions: Decimal            # 其他扣除
    
    # 个税
    taxableIncome: Decimal              # 应纳税所得额
    taxAmount: Decimal                  # 个税金额
    
    # 实发
    netPay: Decimal                     # 实发工资
    
    # 累计数据
    cumulativeIncome: Decimal           # 累计收入
    cumulativeDeduction: Decimal        # 累计减除费用
    cumulativeInsurance: Decimal        # 累计社保公积金
    cumulativeTaxableIncome: Decimal    # 累计应纳税所得额
    cumulativeTax: Decimal              # 累计已缴个税
    taxPayable: Decimal                 # 本月应缴个税
```

### YearEndBonus（年终奖结果）

```python
@dataclass
class YearEndBonus:
    bonusAmount: Decimal                # 年终奖金额
    taxableBonus: Decimal               # 应纳税所得额
    taxAmount: Decimal                  # 个税金额
    netBonus: Decimal                   # 税后年终奖
    effectiveRate: Decimal              # 实际税率
    optimalMethod: str                  # 最优计税方式
```

## 扩展城市配置

如需添加新城市，在 `InsuranceCalculator.CITY_CONFIGS` 中添加：

```python
"成都": InsuranceConfig(
    city="成都", year=2026,
    pensionEmployeeRate=Decimal('0.08'),
    pensionEmployerRate=Decimal('0.16'),
    # ... 其他参数
)
```

## 测试

运行单元测试：

```bash
cd tools
python test_payroll_engine.py
```

测试覆盖：
- 个税计算（基础、累计、跳档）
- 社保计算（多城市、上下限）
- 年终奖计算
- 边界情况（零工资、负数等）

## 注意事项

1. **精度问题**：所有金额使用 `Decimal` 类型，避免浮点误差
2. **累计数据**：每月计算需要传入前月的累计数据
3. **专项附加扣除**：需在计算时传入每月额度
4. **年终奖**：目前仅支持单独计税，并入综合所得需结合全年收入判断
5. **社保基数**：每年7月调整，需及时更新配置

## 更新日志

### v1.0.0 (2026-04-03)
- 实现累计预扣法个税计算
- 支持北上广深杭社保公积金
- 支持年终奖单独计税
- 提供完整单元测试
