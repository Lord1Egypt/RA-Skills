# 报告助手

> 状态：草稿 — 等待 charity-pm 完成需求规格后开发

帮助中小型草根 NGO 快速生成项目报告、年度工作报告等文档。

## 使用方式

<!-- TODO: 由 charity-skill-dev 在实现完成后填充 -->

## 目录结构

```
report-assistant/
  SKILL.md          ← AI agent 指令文件（由 charity-skill-dev 按 spec 编写）
  index.js          ← Skill 入口（待开发）
  templates/        ← 报告模板文件（待 charity-template-curator 收集）
  README.md         ← 本文件
```

## 依赖

| 包 | 用途 |
|----|------|
| `@charity-skills/pii-filter` | 确保输入文本不含 PII 再送模型 |
| `@charity-skills/disclaimer-injector` | 输出文档强制注入 AI 声明和免责提示 |

## 合规说明

本 Skill 的所有输出均经过合规处理：
1. 输入经 PII 过滤，确保个人信息不入模型
2. 输出文档自动包含「AI 辅助生成」声明
3. 输出文档自动包含「AI 生成，仅供参考，请核实数据」免责提示

上线前须经 `charity-legal-advisor` 合规审查和 `security-engineer` 安全审查。
