# 挑战协议规范

## 概述

本协议定义了挑战代码质量发现的系统方法。目标是在采取行动前确保发现准确，减少误报和浪费的努力。

## 挑战方法论

### 步骤 1：主张分解

把发现拆成原子的、可验证的主张：

1. **存在性主张**: "X 在文件 Y 中存在/不存在"
2. **行为主张**: "函数 X 在 Z 时执行 Y"
3. **结构主张**: "类型 X 有 N 个成员"
4. **符合性主张**: "实现因 X 偏离设计"
5. **数值主张**: "缺少 N 项（期望 M，找到 K）"

每个主张必须可独立验证。

### 步骤 2：证据收集

对每个主张，收集：

1. **主要证据**: 直接读取源代码
2. **次要证据**: 相关文件、导入、类型定义
3. **设计证据**: 引用的设计文档
4. **用法证据**: 代码实际如何被使用

证据层级：
- 源代码 > 设计文档 > 注释 > 假设

### 步骤 3：对抗性分析

应用以下挑战策略：

#### 策略 A：直接验证
读取引用的确切文件和行。主张与现实相符吗？

```
Claim: "Line 58: type X is missing"
Action: Read line 58 of the file
Result: Line 58 shows type X IS present → claim overturned
```

#### 策略 B：上下文扩展
主张可能技术上正确但因脱离上下文而误导。

```
Claim: "Function X has no error handling"
Action: Read the full function and its callers
Result: Error handling is done by callers → claim weakened
```

#### 策略 C：范围纠正
主张可能混淆了不同的范围或命名空间。

```
Claim: "28 edge types required, only 21 found"
Action: Check what "28" refers to in design docs
Result: 28 = language types, not edge types → claim overturned
```

#### 策略 D：时间检查
主张可能引用了过时的代码。

```
Claim: "File X uses deprecated API Y"
Action: Check git history and current code
Result: API was updated last week → claim overturned
```

#### 策略 E：完整性检查
主张可能部分正确但不完整。

```
Claim: "Type X is missing from union"
Action: Check all union members
Result: X is present but Y is actually missing → claim weakened
```

### 步骤 4：结论判定

使用此决策树：

```
Is the primary claim factually incorrect?
  ├─ Yes → verdict = "overturned"
  └─ No → Is the severity/scope overstated?
       ├─ Yes → verdict = "weakened"
       └─ No → Is the claim accurate?
            ├─ Yes → verdict = "confirmed"
            └─ Uncertain → verdict = "weakened" (lower confidence)
```

### 步骤 5：置信度评分

| 置信度 | 含义 |
|--------|------|
| 90-100% | 清晰、无歧义的证据 |
| 70-89% | 证据充分，有轻微不确定性 |
| 50-69% | 证据混合；需要判断 |
| 低于 50% | 证据不足；建议进一步调查 |

影响置信度的因素：
- 源代码清晰度
- 设计文档可用性
- 主张具体性
- 证据完整性

## 反模式

### 1. 确认偏差
**错误**: 只寻找支持发现的证据
**正确**: 先主动寻找反证

### 2. 制造怀疑
**错误**: 没有真实反证却挑战发现
**正确**: 只在证据真正矛盾时挑战

### 3. 吹毛求疵
**错误**: 挑战琐碎细节而忽视核心问题
**正确**: 聚焦影响发现有效性的主张

### 4. 范围蔓延
**错误**: 把挑战扩展到发现主张之外
**正确**: 只处理发现所断言的内容

## 输出质量标准

一份好的挑战报告：

1. **具体**: 引用确切的文件路径和行号
2. **可验证**: 反证可被独立核对
3. **公正**: 存在支持证据时予以承认
4. **可执行**: 提供清晰建议
5. **相称**: 置信度与证据强度匹配

## 集成点

### 与质量流水线
- 高严重度发现可自动触发挑战
- 结果反馈到发现置信度评分
- 被推翻的发现标记用于改进模板

### 与知识系统
- 已确认的发现可捕获为 knowhow
- 挑战模式可编码为评审规范
- 常见误报模式成为学习材料

### 与团队技能
- 挑战可委派给专门智能体
- 结果为团队评分和收敛提供信息
- 对抗模式与 team-adversarial-swarm 对齐
