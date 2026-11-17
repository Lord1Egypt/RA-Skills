---
name: grill-with-docs
description: "Combine brainstorming deep-dive with domain modeling for precise requirement exploration"
tags: [planning, general, iterative, memory-based, file-based]
version: 1.0.0
---

# Grill with Docs �?需求探�?+ 领域建模

�?brainstorming 的发散探索与 domain-modeling 的精确建模结合，形成从模糊需求到精确领域语言的完整链路�?
## 为什么组�?
单独 brainstorming 容易停留�?想法"层面，缺乏可落地的领域定义�?单独 domain-modeling 需要前置输入，如果需求不清晰就开始建模，产出质量低�?组合后：brainstorming 输出 �?domain-modeling 输入 �?精确的领域模型�?
## 执行流程

### Phase 1: 需求探索（brainstorming�?
加载 `/brainstorming` skill，执行完整的需求探索流程：

1. 理解当前项目上下�?2. 逐个提问，挖掘真实需�?3. 挑战假设，探索替代方�?4. 输出设计文档（design doc�?
**Phase 1 完成标志**：用户确认设计方案，设计文档已生成�?
### Phase 2: 领域建模（domain-modeling�?
加载 `/domain-modeling` skill，基�?Phase 1 的设计文档进行领域建模：

1. 从设计文档提取核心业务概�?2. 构建/更新 CONTEXT.md（领域词汇表�?3. 识别限界上下文（Bounded Contexts�?4. 记录架构决策（ADR�?5. 交叉验证：设计文档中的术语是否与领域模型一�?
**Phase 2 完成标志**：CONTEXT.md 已更新，核心术语定义明确，ADR 已记录�?
### Phase 3: 交叉验证

检查两�?Phase 的输出一致性：

- [ ] 设计文档中的每个业务术语都在 CONTEXT.md 中有定义
- [ ] CONTEXT.md 中的术语与设计文档用法一�?- [ ] 没有同义词冲突（�?"订单" vs "工单" 指同一概念�?- [ ] 限界上下文边界与设计的模块划分对�?
## 适用场景

| 场景 | 说明 |
|------|------|
| **新功能设�?* | 从零开始，先探索需求再建立领域语言 |
| **系统重构** | 先理解现有系统的设计意图，再重新定义领域模型 |
| **跨团队协�?* | 需要统一团队的业务语言，消除沟通歧�?|
| **复杂业务** | 业务规则复杂，需要同时理清需求和领域边界 |

## 输出�?
1. **设计文档** �?来自 brainstorming，包含需求分析和设计方案
2. **CONTEXT.md** �?来自 domain-modeling，项目级领域词汇�?3. **ADR** �?架构决策记录
4. **一致性报�?* �?Phase 3 的交叉验证结�?
## 快速启�?
```
用户：我想设计一个新的XX功能
�?触发 /grill-with-docs
�?Phase 1: brainstorming（~15-30分钟对话�?�?Phase 2: domain-modeling（~10-20分钟建模�?�?Phase 3: 交叉验证（~5分钟检查）
�?输出完整的设�?+ 领域模型
```
