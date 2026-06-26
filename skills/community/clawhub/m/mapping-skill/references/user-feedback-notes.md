# 用户反馈与迭代记录

本文件用于沉淀 Mapping-Skill 在真实使用中的反馈、踩坑与改进点。

## 使用方式

每次收到新的实践反馈后，建议按以下格式补充：

- 日期
- 场景
- 用户反馈
- 暴露的问题
- 采取的改进
- 影响的文件

---

## 当前已知迭代方向

### 1. SKILL.md 需要明确写出具备的功能

- **反馈**：不仅要有执行流程，还要明确列出 skill 具备哪些功能
- **改进方向**：在 `SKILL.md` 顶部显式列出能力清单与触发条件
- **影响文件**：`SKILL.md`

### 2. 需要写明项目链接

- **反馈**：要在 skill 中加入 GitHub 与 ClawHub 项目链接
- **改进方向**：在 `README.md` 与 `SKILL.md` 中统一加入链接
- **影响文件**：`README.md`、`SKILL.md`

### 3. 要兼容 Claude Code 与 OpenClaw

- **反馈**：该 skill 不止给 Claude Code 使用，也给 OpenClaw 使用，因此两边都需要说明
- **改进方向**：README 中增加双平台使用说明，SKILL 中增加 OpenClaw / 飞书工作流能力说明
- **影响文件**：`README.md`、`SKILL.md`

### 4. 要把真实实践中的最佳提示词持续加入 skill

- **反馈**：后续会继续提供 Mapping-Skill 实践文档，需要把其中高价值提示词加入 skill，并明确 skill 已支持这些功能
- **改进方向**：维护 `references/prompt-best-practices.md`，并在 `SKILL.md` 中保留“最佳实践提示词”入口
- **影响文件**：`SKILL.md`、`references/prompt-best-practices.md`

### 5. OpenClaw + 飞书工作流要有更清晰说明

- **反馈**：已有 OpenReview、CVF、飞书写邮件、给定 URL 导表等实际工作流，需要在说明文档中更完整呈现
- **改进方向**：README 中增加 OpenClaw 与飞书配置说明、工作流示例与输出说明
- **影响文件**：`README.md`、`SKILL.md`
