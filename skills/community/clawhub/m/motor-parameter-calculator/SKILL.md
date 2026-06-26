---
name: motor-parameter-calculator
description: 电机设计参数计算助手 | 根据基本参数计算极槽配合、匝数、磁密、反电动势等核心设计数据
version: 1.2.0
tags: [motor, design, calculation, pole-slot, winding, flux, back-emf]
category: motor-engineering
---

# 电机设计参数计算助手 v1.2

根据输入的基本电机参数，快速计算极槽配合、每槽导体数、绕组系数、磁密、反电动势等关键设计数据。
**v1.2新增：完整参数计算脚本(param_calculator.py)、槽数扫描分析、性能估算。**

## 计算脚本

```bash
# 标准计算
python scripts/param_calculator.py --poles 8 --Q 36 --L 60 --Di 54 --delta 0.5 --Bg 0.75

# 指定绕组参数
python scripts/param_calculator.py --poles 8 --Q 36 --Nph 120 --Imax 15 --R 0.8

# 槽数扫描分析（方案比选）
python scripts/param_calculator.py --sweep_slots --poles 8 --L 60 --Di 54

# 交互模式
python scripts/param_calculator.py --mode interactive
```

## 适用场景

- 电机设计初期参数估算
- 极槽配合方案比选（槽数扫描）
- 匝数/线径设计计算
- 磁密验算

## 输入参数

| 参数 | 说明 | 示例值 |
|------|------|--------|
| 极数 (2p) | 极数，必须为偶数 | 8 |
| 槽数 (Q) | 定子槽数 | 36 |
| 相数 (m) | 相数，通常为3 | 3 |
| 频率 (f) | 电源频率 Hz | 50 |
| 转速 (n) | 额定转速 rpm | 1500 |
| 极距 (τ) | 极距 mm | 56.5 |
| 气隙直径 (D) | 定子内径 mm | 120 |
| 铁心长度 (L) | 铁心长度 mm | 100 |
| 气隙磁密 (Bg) | 气隙磁密 T | 0.75 |
| 每相串联匝数 Nph | 匝数 | 100 |
| 额定电流 Imax | 相电流峰值 A | 10 |
| 相电阻 R | Ω | 1.0 |

## 计算内容

| 计算项 | 公式 | 说明 |
|--------|------|------|
| 极距 τ | π×Di/2p | mm |
| 每极每相槽数 q | Q/(2p×m) | 分数槽判断 |
| 分布系数 Kd | sin(q×αe/2)/(q×sin(αe/2)) | q>1时生效 |
| 短距系数 Kp | sin(πy/2τ) | y=节距槽数 |
| 总绕组系数 Kw | Kd×Kp | 通常>0.85 |
| 每极气隙磁通 Φg | Bg×τ×L | mWb |
| 反电动势常数 Ke | 4.44×f×Nph×Kw×Φg | V（线间有效值）|
| 转矩常数 Kt | 1.5×p×Kw×Nph×Φg | Nm/A |
| 机械时间常数 Tm | J×R/(3×(Nph×Kw×Φg×p)²) | s |

## 槽数扫描分析

扫描不同槽数方案，对比 q、Kw、τ、Kt 等参数，辅助选型：

```bash
python scripts/param_calculator.py --sweep_slots --poles 8 --L 60 --Di 54
```

典型扫描结果格式：

```
Q     q      Kw      τ/mm    Bg/T    Kt
36   1.500  0.9450   21.2    0.750  0.1234
48   2.000  0.9660   16.9    0.750  0.1234
24   1.000  1.0000   42.4    0.750  0.1234
```

## 常见极槽配合参考

| 极数 | 槽数 | q | 特点 |
|------|------|---|------|
| 8 | 36 | 1.5 | 分数槽，常见伺服电机 |
| 8 | 48 | 2.0 | 整数槽，低齿槽转矩 |
| 6 | 36 | 2.0 | 整数槽，平衡性好 |
| 10 | 60 | 2.0 | 整数槽，低振动 |
| 4 | 24 | 2.0 | 整数槽，简单绕制 |

## 示例对话

```
用户：帮我计算极数8，槽数48，相数3，频率50Hz，转速1500rpm的极槽配合参数
助手：运行 param_calculator.py，自动计算 q值、每槽角度、绕组系数等

用户：对比8极36槽和8极48槽
助手：运行 --sweep_slots 模式，给出对比表格
```
