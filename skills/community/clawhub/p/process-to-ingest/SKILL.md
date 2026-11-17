---
name: process-to-ingest
description: "端到端运行手册：先用 workflow-structurer 把一份数字内容梳理成结构化流程文档，再按 demo-asset-ingest 规范打包并通过 clawhub publish 入库到 ClawHub 资源中心。适用：把可用数字内容沉淀为可检索、可安装资源，且需要可复现步骤。"
metadata:
  clawdbot:
    emoji: "📦"
    requires: ["clawhub"]
---

# Process → Ingest（处理到入库运行手册）

本技能演示两个协作工具的串联：

| 阶段 | 工具 | 职责 |
|------|------|------|
| 上游：业务流程处理 | `workflow-structurer` | 渐进式澄清，把模糊需求拆成含输入/输出/职责/风险/校验/规则的结构化步骤 |
| 下游：数字资源入库 | `demo-asset-ingest` | 按 ClawHub-skill 规范打包，用 `clawhub publish` 发布到资源中心 |

## 最小可用形状

```
process-to-ingest/
├── SKILL.md              # 本文件（frontmatter + 操作说明）
└── references/
    └── DESCRIPTION.md    # 上游流程梳理产物（结构化 handoff）
```

## 基本步骤（可复现）

1. **确认目标与内容**：`clawhub whoami` 确认身份；`clawhub search <slug>` 查重，确保 slug kebab-case 且全局唯一；确认内容可公开、已脱敏。
2. **结构化流程**：用 workflow-structurer 的五阶段（澄清目标→步骤骨架→逐步钻取→汇总确认→handoff）产出 `DESCRIPTION.md`，每步补全 Input/Output/Responsibilities/Risks/Validation/Rules。
3. **打包**：创建 `<slug>/SKILL.md` 与 `<slug>/references/DESCRIPTION.md`；`ls -R <slug>` 验证。
4. **预检**：`clawhub publish <slug> --slug <slug> --name "..." --tags "..." --topics "..." --dry-run`，退出码 0。
5. **入库**：去掉 `--dry-run` 正式发布。
6. **验证**：`clawhub search <slug>` 命中（新条目可能有审核延迟）。

## 关键注意事项

- 不跳步：先结构化后打包；先有 Risks 再写 Rules。
- slug 全局唯一，发布前必查重。
- 发布前脱敏，禁止凭证/客户数据。
- 先 dry-run 再正式 publish。
- Validation 与 Rules 不混写；一次只处理一个步骤。

上游结构化产物见 `references/DESCRIPTION.md`。
