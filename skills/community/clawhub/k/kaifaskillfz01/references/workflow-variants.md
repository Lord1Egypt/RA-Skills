# 流程变体定义

根据用户意图和场景，自动选择合适的流程变体。

---

## 变体选择逻辑

```
用户意图
├── "快速开发" / "简单" / "小功能"
│   → variant: quick
├── "严格模式" / "核心" / "关键" / "生产"
│   → variant: strict
├── "审查" / "review" / "检查代码"
│   → variant: review-only
├── "重构" / "重写"
│   → variant: refactor
└── 默认
    → variant: standard
```

---

## Variant: standard（标准，默认）

```
Assess → Plan → ⛔Approval → Implement(flash) → Review(pro) → Report
```

- 角色: PM + Developer(flash) + Reviewer(pro)
- 中等复杂度默认流程
- Plan 完整，Review 标准深度

---

## Variant: quick（快速开发）

```
Assess → Plan(精简) → ⛔Approval → Implement(flash) → Review(flash) → Report
```

- 角色: PM + Developer(flash) + Reviewer(flash)
- Plan 精简（跳过架构设计章节，只保留接口定义和边界情况）
- Review 快速（只检查逻辑正确性和 Plan 一致性，跳过安全和风格）
- 适用: 单文件功能、简单脚本、工具类小功能

### 触发
- 用户说"快速开发"/"简单开发"/"小功能"
- Assess 阶段判定复杂度为"简单"
- 用户说"不用太正式"

---

## Variant: strict（严格模式）

```
Assess → Plan → ⛔Approval → Implement(flash) → Review(pro,深度) → Report
```

- 角色: PM + Architect(pro) + Developer(flash) + Reviewer(pro)
- Plan 由 Architect 子 agent 产出（PM 提供需求后 spawn Architect）
- Review 深度检查（全部 6 个维度 + 架构一致性 + 可维护性评估）
- 适用: 核心功能、生产系统、安全敏感模块

### 触发
- 用户说"严格模式"/"核心功能"/"关键模块"
- Assess 阶段判定复杂度为"复杂"
- 涉及安全、支付、认证等敏感领域

---

## Variant: review-only（仅审查）

```
Review(pro) → Report
```

- 跳过 Assess/Plan/Implement
- 直接 spawn Reviewer 审查用户指定的代码
- 不需要 Plan 对照，只审查代码本身的质量
- 适用: 用户已有代码，只需要审查

### 触发
- 用户说"审查这段代码"/"review this"/"帮我看下这个代码"

---

## Variant: refactor（重构）

```
Assess → Plan(重构方案) → ⛔Approval → Implement(flash) → Review(pro) → Report
```

- Plan 阶段聚焦重构方案:
  - 现状分析（当前架构问题）
  - 目标架构（重构后的结构）
  - 迁移步骤（如何安全地从 A 到 B）
  - 兼容性考虑（如何不破坏现有功能）
- 适用: 重构现有代码

### 触发
- 用户说"重构"

---

## 变体参数对比

| 参数 | quick | standard | strict | review-only | refactor |
|------|-------|----------|--------|-------------|----------|
| Assess | ✅ | ✅ | ✅ | ❌ | ✅ |
| Architect | ❌ | ❌(PM兼) | ✅(子agent) | ❌ | ❌(PM兼) |
| Plan 深度 | 精简 | 标准 | 深度 | ❌ | 标准 |
| Approval | ✅ | ✅ | ✅ | ❌ | ✅ |
| Developer模型 | flash | flash | flash | ❌ | flash |
| Reviewer模型 | flash | pro | pro | pro | pro |
| Review 深度 | 快速 | 标准 | 深度 | 标准 | 标准 |
| Report | ✅ | ✅ | ✅ | ✅ | ✅ |
