# 适应度函数（Fitness Function）

## 概述

适应度函数是 RHI 闭环的核心，它将 MoA 执行过程中采集的 `<signal>` 标签量化为一个可比较的适应度分数，用于判断系统是否收敛、是否需要继续进化。

## 适应度公式

```
fitness = 0.30 * synthesis_novelty     (熔铸创新度)
        + 0.25 * critique_specificity   (批判精准度)
        + 0.20 * revision_quality       (修正质量)
        + 0.15 * token_efficiency       (Token 效率)
        + 0.10 * immutability_intact    (IMMUTABLE 完整性)
```

## 权重设计依据

| 维度 | 权重 | 说明 |
|------|------|------|
| synthesis_novelty | 0.30 | 熔铸创新度是 MoA 的核心价值，权重最高 |
| critique_specificity | 0.25 | 批判精准度决定对抗质量，是"认知摩擦"的保障 |
| revision_quality | 0.20 | 修正质量体现专家响应批判的深度 |
| token_efficiency | 0.15 | Token 效率影响实际可用性 |
| immutability_intact | 0.10 | IMMUTABLE 保护是底线，权重最低但不可忽视 |

## 收敛标准

| 适应度区间 | 判定 | 行动 |
|-----------|------|------|
| >= 0.85 | 已收敛（converged） | 结束进化，采纳当前 Prompt |
| 0.70 - 0.85 | 持续改进（improving） | 建议继续优化，至少再跑 1 轮 |
| < 0.70 | 需要改进（needs_improvement） | 必须继续进化，针对最弱维度重点加强 |

## 信号采集规范

### 信号格式

```xml
<signal metric="synthesis_novelty" score="0.85" expert_id="expert-dist-arch" source="moa_run" round="1"/>
```

### 信号来源

| metric | 采集阶段 | 采集方式 |
|--------|---------|---------|
| synthesis_novelty | Phase 4 熔铸 | 熔铸决策者自评：最终答案是否超越各专家原始方案 |
| critique_specificity | Phase 3 对抗 | 熔铸决策者评估批判者的具体性和可操作性 |
| revision_quality | Phase 3 对抗 | 熔铸决策者评估专家的修正是否充分回应了批判 |
| token_efficiency | 全阶段 | 熔铸决策者评估输出是否有冗余、重复 |
| immutability_intact | 全阶段 | 熔铸决策者检查是否遵守了 IMMUTABLE 约束 |

### 评分标准

| 分数 | 含义 |
|------|------|
| 0.0 - 0.3 | 严重不足，需要大幅改进 |
| 0.3 - 0.5 | 不足，需要改进 |
| 0.5 - 0.7 | 中等，可以接受但可优化 |
| 0.7 - 0.9 | 良好，接近最优 |
| 0.9 - 1.0 | 优秀，无需改进 |

## 多轮进化策略

### 单任务内进化

```
第1轮: 执行 MoA → 采集信号 → 计算 fitness → 识别最弱维度
第2轮: 注入增强指令 → 重新执行 MoA → 采集信号 → 比较 fitness
第3轮: 注入增强指令 → 重新执行 MoA → 采集信号 → 比较 fitness
```

最大轮次建议为 3 轮，超过后边际收益递减。

### 跨任务迁移

每轮进化产生的 Patch 可以记录到 `patch-spec.md`，用于同类任务的冷启动增强。

## 与能力注册表的联动

每次 MoA 执行后的信号标签，同时用于：
1. 计算 fitness（RHI 闭环）
2. 更新专家 performance_vector（信号学习与画像进化）