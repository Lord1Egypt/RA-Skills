# Review Rules

## 维度 1：目标一致性（Goal Alignment）

检查计划是否覆盖 business_goal 所需的关键步骤。

**评分规则**：
- 完全覆盖所有关键步骤 → 100%
- 覆盖主要步骤，遗漏次要步骤 → 70%
- 遗漏关键步骤 → 30%
- 完全偏离目标 → 0%

## 维度 2：拓扑合理性（Topology Soundness）

检查依赖关系是否正确。

**检查项**：
- 无循环依赖
- 无不可达节点
- 无孤立节点
- 入口/出口节点正确
- 条件边的 condition_expression 合理

## 维度 3：技能绑定合理性（Skill Binding Quality）

检查 target_skill 是否与节点 purpose 匹配。

**检查项**：
- target_skill 存在于白名单
- skill description 与 node purpose 语义匹配
- 无过度绑定（大技能做小事）
- 无欠绑定（小技能做大事）

## 维度 4：作用域安全性（Scope Safety）

**检查项**：
- scoped_state_keys 非空
- 无冗余键（声明了但未使用）
- 无敏感字段（薪资、身份证等明文）
- input_mapping 引用存在

## 维度 5：可执行性（Executability）

**检查项**：
- 节点 timeout_seconds 合理
- 条件表达式语法正确
- 无死锁风险
- 引擎可消费（符合 schema）

## 维度 6：效率与复杂度

**检查项**：
- 可并行节点已并行
- 无冗余/重复节点
- DAG 深度 ≤ max_depth
- 节点数 ≤ max_nodes

## 维度 7：风险与治理

**检查项**：
- 高风险技能有 human_review_required
- 敏感数据已脱敏
- 失败路径已定义
- 审计可追踪
