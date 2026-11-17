# 架构模式库与设计决策树

> 从 mu-dev-workflow SKILL.md §阶段2 拆出。选架构模式时读取此文件。

## 六大架构模式

| 模式 | 名称 | 特征 | 适用场景 | 代表Skill |
|------|------|------|----------|-----------|
| **A** | 路由分发 | 入口按意图分发到不同处理路径 | 多场景覆盖 | work-summary, meeting-shrimp, tuan-analysis, critical-thinking |
| **B** | 线性流水线 | 固定步骤顺序执行，每步有门控 | 有明确产出文档 | lrp, operating-plan, case-shrimp, jd-shrimp, interview-shrimp, prfaq |
| **C** | 双模式交互 | 快速模式(已有信息) + 完整模式(引导收集) | 需大量上下文但用户可能有部分信息 | lrp, op, team-goal, prfaq, pyramid-principle |
| **D** | 能力模块 | 多独立能力 + 场景路由组合调用 | 多功能复合型 | review-feedback, meeting-shrimp, highly-effective |
| **E** | 规则引擎 | 检测→匹配→逐条修正 | 质量检查/安全扫描/格式修正 | humanizer-MineSweeping, lobster-guard, skill-creator |
| **F** | 三级分层 | 按优先级分层(P0/P1/P2) | 区分必须做vs可以做 | self-tuning, dev-workflow, room-booking |

## 设计决策树

```
Q1: 是否有多个独立的"使用场景"？
  → 是 → 【模式A路由分发】或【模式D能力模块】
  → 否 → Q2

Q2: 用户是否可能已有部分信息（不需要从头收集）？
  → 是 → 必须加【模式C双模式交互】
  → 否 → Q3

Q3: 核心流程是否是固定的步骤序列？
  → 是 → 【模式B线性流水线】
  → 否 → Q4

Q4: 是否基于规则进行扫描/检测/修正？
  → 是 → 【模式E规则引擎】
  → 否 → 【模式F三级分层】或组合模式
```

## 高频共通组件（建议每个Skill都配备）

1. **定位与触发说明**（100%）：description + Quick Trigger + 不适用场景
2. **Anti-Pattern清单**（80%）：常见错误和反模式
3. **Pre-Delivery Checklist**（70%）：输出前自检
4. **references/ 拆分**（85%）：L2≤250行，超出拆到references/
5. **联动说明**（60%）：与其他Skill的关系和替代方案
6. **质检/验证步骤**（75%）：输出前的质量门控
7. **IRON LAW**（30%）：不可违反的核心硬规则
