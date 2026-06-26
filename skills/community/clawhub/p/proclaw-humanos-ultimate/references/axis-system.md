# 核心轴系统

## 目录
- [概览](#概览)
- [5个核心轴](#5个核心轴)
- [轴位置测量](#轴位置测量)
- [轴间交互](#轴间交互)
- [轴原型](#轴原型)

## 概览

核心轴系统是HumanOS Ultimate版的性格维度框架，定义了5个核心轴，每个轴代表一对互补的极性。

### 系统目标
- 精确描述性格维度
- 识别性格优势
- 发现内在矛盾
- 指导整合实践

### 系统原则
- 连续性: 轴是连续谱，不是二元对立
- 平衡性: 两极都有价值，追求平衡
- 适应性: 轴位置可随情境调整
- 整合性: 多轴相互影响

## 5个核心轴

### 轴1: 结构轴 (Axis of Structure)

**两极**:
- 稳定性 (Stability): 重视秩序、可预测性、传统
- 变革性 (Transformation): 重视变化、创新、突破

**描述**: 描述个人对稳定和变化的基本态度

**稳定性特征**:
- 喜欢可预测的环境
- 重视传统和经验
- 倾向于维持现状
- 谨慎决策

**变革性特征**:
- 喜欢新鲜和变化
- 重视创新和突破
- 倾向于挑战现状
- 冒险决策

### 轴2: 行动轴 (Axis of Action)

**两极**:
- 内向 (Introversion): 能量来自内在
- 外向 (Extraversion): 能量来自外在

**描述**: 描述个人能量来源和行动倾向

**内向特征**:
- 从独处中获得能量
- 深度思考
- 内省倾向
- 少量但深层关系

**外向特征**:
- 从社交中获得能量
- 快速行动
- 外向表达
- 广泛但表层关系

### 轴3: 感知轴 (Axis of Perception)

**两极**:
- 具体 (Concrete): 关注事实、细节、现实
- 抽象 (Abstract): 关注概念、模式、可能性

**描述**: 描述个人感知和理解世界的方式

**具体特征**:
- 关注事实和细节
- 实用导向
- 现实主义
- 逐步推理

**抽象特征**:
- 关注概念和模式
- 创意导向
- 理想主义
- 直觉推理

### 轴4: 决策轴 (Axis of Decision)

**两极**:
- 逻辑 (Logic): 基于客观分析和逻辑推理
- 价值 (Value): 基于个人价值观和情感

**描述**: 描述个人决策的基本方式

**逻辑特征**:
- 客观分析
- 逻辑推理
- 公平公正
- 规则导向

**价值特征**:
- 主观感受
- 价值观考量
- 人际和谐
- 情感导向

### 轴5: 表达轴 (Axis of Expression)

**两极**:
- 收敛 (Convergent): 集中、精确、聚焦
- 发散 (Divergent): 扩展、创造、多样

**描述**: 描述个人表达和创造的倾向

**收敛特征**:
- 集中注意力
- 精确表达
- 深度聚焦
- 专注单一目标

**发散特征**:
- 扩展可能性
- 创造性表达
- 广泛探索
- 多目标并行

## 轴位置测量

### 测量方法

轴位置用-1到1之间的连续值表示:
- -1: 完全倾向于负面极
- 0: 完全平衡
- 1: 完全倾向于正面极

### 测量流程

```python
def measure_axis_position(axis_name, responses):
    # 基于响应计算轴位置
    positive_responses = count_positive_responses(axis_name, responses)
    negative_responses = count_negative_responses(axis_name, responses)
    total = positive_responses + negative_responses

    if total == 0:
        return 0.0

    # 计算位置 (-1 到 1)
    position = (positive_responses - negative_responses) / total

    return position
```

### 轴强度

除位置外，每个轴还有强度指标(0到1):
- 高强度(>0.7): 轴位置稳定，不易改变
- 中强度(0.5-0.7): 轴位置较稳定
- 低强度(<0.5): 轴位置灵活，易受情境影响

```python
def calculate_axis_strength(axis_name, responses):
    # 基于响应一致性计算强度
    consistency = measure_response_consistency(axis_name, responses)
    return consistency
```

### 轴平衡度

平衡度描述两极的平衡程度(0到1):
- 高平衡(>0.7): 两极发展均衡
- 中平衡(0.4-0.7): 一极稍强
- 低平衡(<0.4): 一极明显强于另一极

```python
def calculate_axis_balance(axis_position):
    balance = 1 - abs(axis_position)
    return balance
```

## 轴间交互

### 交互类型

1. **协同交互 (Synergistic Interaction)**: 两轴同向增强
2. **张力交互 (Tension Interaction)**: 两轴反向对立
3. **互补交互 (Complementary Interaction)**: 两轴互补

### 主要交互对

**结构轴 × 行动轴**:
- 稳定性 + 内向: 沉稳谨慎型
- 稳定性 + 外向: 外向稳定型
- 变革性 + 内向: 内向创新型
- 变革性 + 外向: 外向冒险型

**感知轴 × 决策轴**:
- 具体 + 逻辑: 分析务实型
- 具体 + 价值: 实践关怀型
- 抽象 + 逻辑: 理论分析型
- 抽象 + 价值: 理想关怀型

**表达轴 × 其他轴**:
- 收敛 + 具体: 精确务实型
- 收敛 + 抽象: 深度理论型
- 发散 + 具体: 广泛实践型
- 发散 + 抽象: 创造理论型

### 交互强度

基于两个轴的位置计算交互强度:
- 强交互(>0.6): 交互影响大
- 中交互(0.3-0.6): 交互影响中等
- 弱交互(<0.3): 交互影响小

```python
def calculate_interaction_strength(position1, position2):
    strength = abs(position1 * position2)
    return strength
```

## 轴原型

### 原型定义

基于主导轴位置组合形成轴原型，描述典型的性格模式。

### 常见原型

**稳定性-内向-具体-逻辑-收敛型**:
- 特征: 稳重、谨慎、分析、专注
- 优势: 深度分析、稳定可靠
- 盲区: 缺乏灵活性、表达受限

**变革性-外向-抽象-价值-发散型**:
- 特征: 创新、冒险、理想、创意
- 优势: 创造力强、影响力大
- 盲区: 不稳定、缺乏执行力

**稳定性-外向-具体-价值-收敛型**:
- 特征: 稳重、外向、务实、关怀
- 优势: 领导力强、人际和谐
- 盲区: 创新不足、过于谨慎

**变革性-内向-抽象-逻辑-发散型**:
- 特征: 创新、内向、理论、分析
- 优势: 深度思考、理论创新
- 盲区: 社交困难、实践不足

### 原型识别

```python
def identify_axis_prototype(axis_positions):
    # 识别主导极性
    dominant_poles = []
    for axis_name, position in axis_positions.items():
        pole = get_dominant_pole(axis_name, position)
        dominant_poles.append(pole)

    # 生成原型名称
    archetype_name = "-".join(dominant_poles[:3])

    return {
        'name': archetype_name,
        'dominant_poles': dominant_poles,
        'balance_assessment': assess_axis_balance(axis_positions)
    }
```

### 原型演化

轴原型不是固定的，可随时间和经验演化:

- 自然演化: 生活经历自然改变轴位置
- 有意调整: 通过练习和训练调整轴位置
- 情境适应: 在不同情境中调整轴表达
- 整合成长: 将对立极性整合

## 使用建议
- 测量所有5个轴
- 识别主导轴和平衡度
- 分析轴间交互
- 识别轴原型
- 设计整合实践
