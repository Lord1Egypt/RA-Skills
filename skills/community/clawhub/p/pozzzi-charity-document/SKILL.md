---
name: document-assistant
description: 噗滋（pozzzi）慈善 - 帮助中小型 NGO 生成日常行政文书，支持合同协议、会议纪要、公函、感谢信和工作计划五类文书，内置固定法律条款直通机制避免模型改写关键条款。
---

# 文书助手

> ℹ️ **公益开源工具（v0.1.0）**
>
> 本 Skill 为噗滋（pozzzi）慈善开源工具集成员，由社区贡献者维护，遵循 MIT License。
>
> **使用约束**（用户自负责任）：
> - 🚫 禁止处理 14 岁以下未成年人个体级数据（《未成年人保护法》第 72-74 条）
> - 🚫 禁止用于编造法规条文、文件编号、资质证书编号等
> - 🚫 不适用于公开募捐相关内容生成（建议使用专业工具）
> - ⚠️ AI 生成内容**必须经人工审核后方可使用**，开发者不对使用结果承担责任
> - ⚠️ 本工具不构成专业的法律/财务/管理建议
> - ✅ 用户自带模型 API（混元/DeepSeek/豆包，均已各自备案）
> - ✅ 噗滋（pozzzi）作为工具提供者，不接触/不存储用户数据
>
> 详细法律声明：[LICENSE](https://github.com/kirinspark/pozzzi-charity/blob/main/LICENSE) | [免责声明](https://github.com/kirinspark/pozzzi-charity/blob/main/docs/legal/disclaimer.md)

文书助手是噗滋慈善（pozzzi-charity） Skill 集群的第三核心 Skill，覆盖 NGO 日常行政文书需求。

## 支持的文书类型

- **合同/协议** — 志愿者协议、合作协议、租赁协议、服务协议
- **会议纪要** — 理事会、监事会、团队会议
- **公函** — 致政府部门、资助方、合作伙伴
- **感谢信** — 致捐赠人、志愿者、合作方
- **工作计划/总结** — 年度、季度、月度

## 核心特性

- **固定条款直通**（fixed-clause-handler）：合同中的保密、不可抗力、争议解决等法律条款不经模型，直接从模板复制，防止 AI 改写
- **差异化语气**：合同 temperature=0.2（严谨）→ 感谢信 temperature=0.6（温暖）
- **合同法律免责**：合同类文书额外提示"建议法律专业人士审核"

## 技术依赖

- `model-gateway` — 多模型路由、域名白名单、内置 PII 前置过滤
- `disclaimer-injector` — AI 声明和免责提示注入
- `storage-adapter` — 本地数据存储（日志、历史）
