# 🌊 健康体检推荐 — 循证体检方案 + 一键转人工

**国家卫建委 2025 指南驱动的个性化体检推荐。AI 采集信息 → 风险评估 → 项目推荐 → 生成预约二维码。支持转接 ocean-desk 人工坐席。**

[![ClawHub](https://img.shields.io/badge/ClawHub-health--checkup--recommender-blue)](https://clawhub.ai/skills/health-checkup-recommender)
[![downloads](https://img.shields.io/npm/dm/oceanbus)](https://www.npmjs.com/package/oceanbus)
[![GitHub stars](https://img.shields.io/github/stars/ryanbihai/health-checkup-recommender)](https://github.com/ryanbihai/health-checkup-recommender)
[![license](https://img.shields.io/badge/license-MIT--0-green)](LICENSE)

---

## 📑 目录

- [这是什么](#这是什么)
- [循证医学支撑](#循证医学支撑)
- [快速开始](#快速开始)
- [能力一览](#能力一览)
- [转人工坐席](#转人工坐席)
- [在 OceanBus 生态中的定位](#在-oceanbus-生态中的定位)
- [安全](#安全)
- [相关项目](#相关项目)
- [参与贡献](#参与贡献)
- [License](#license)

---

## 这是什么

一个 AI 驱动的循证体检推荐系统。用户说"我想做体检"，AI 自动完成：信息采集 → 风险评估 → 项目推荐 → 生成预约二维码。覆盖全国 220+ 城市。

客户如需协助预约、改套餐或退款，AI 通过 ocean-thread/v1 协议无缝转接至 ocean-desk 人工坐席——附带完整的客户画像和 AI 推荐摘要，坐席拿到手就知道上下文。

```
用户说"我想体检"
    → AI 采集信息（年龄/性别/症状/家族史）
    → 循证风险评估（BMJ/JAMA/国家癌症中心数据）
    → 个性化项目推荐（基础套餐 + 增强项）
    → 生成预约二维码
    → [可选] 转接 ocean-desk 人工坐席协助预约
```

---

## 循证医学支撑

所有风险评估和体检项目推荐，均基于权威医学数据：

| 来源 | 用途 |
|------|------|
| 国家卫建委《成人健康体检项目推荐指引（2025 版）》 | 体检项目框架 |
| BMJ / JAMA 顶刊文献（2021-2025） | 中国人群慢性病风险模型 |
| 国家癌症中心《2022 年中国癌症报告》 | 恶性肿瘤风险排序 |

每一项推荐都标明出处。不做过度的无根据推销。

---

## 快速开始

```bash
# 1. 安装
clawhub install health-checkup-recommender
cd ~/.openclaw/workspace/skills/health-checkup-recommender
npm install

# 2. 对你的 AI 说"我想做体检"
# AI 自动引导完成：信息采集 → 风险评估 → 项目推荐 → 生成预约二维码
```

> 📖 **深度阅读**：[SKILL.md](./SKILL.md) — LLM 行为指南、评估流程、转人工协议

---

## 能力一览

| 能力 | 说明 |
|------|------|
| **智能信息采集** | 渐进式追问年龄/性别/症状/家族史，不过度打扰 |
| **循证风险评估** | 基于 BMJ/JAMA/国家癌症中心数据，标明出处 |
| **个性化项目推荐** | 基础套餐 + 增强项（心脑血管/肿瘤/代谢等） |
| **预约二维码生成** | 全国 220+ 城市合作机构，一键预约 |
| **转人工坐席** | ocean-thread/v1 协议打包客户画像 + AI 摘要，无缝转接 ocean-desk |

---

## 转人工坐席

体检推荐完成后，客户如需协助预约、改套餐或退款，AI 可将完整上下文转接至 ocean-desk：

```json
{
  "source_skill": "health-checkup-recommender",
  "customer_profile": { "name": "张先生", "age": 45, "city": "北京" },
  "ai_summary": "已完成项目推荐：基础套餐+心血管增强项，总价1200元。客户要求协助预约。",
  "recommended_actions": ["预约体检", "确认心血管增强项"]
}
```

---

## 在 OceanBus 生态中的定位

```
Ocean Chat           health-checkup     china-top-doctor
(P2P 消息基础设施)  →  (垂直 Skill — 体检)  →  (垂直 Skill — 专家)
                            ↓
                       ocean-desk (转人工坐席)
```

本 Skill 展示的是 OceanBus 生态中**垂直行业 Agent** 的完整形态：AI 完成专业推荐 → 需要时转接人工 → 附带完整上下文。

---

## 安全

- 客户体检数据在 AI 对话中处理，不持久化到云端
- 转人工时通过 OceanBus P2P 加密传输客户画像
- 推荐项目均标明循证来源，不做无依据推销

---

## 相关项目

| 项目 | 说明 |
|------|------|
| [oceanbus](https://www.npmjs.com/package/oceanbus) | 核心 SDK — `npm install oceanbus` |
| [china-top-doctor-referral](https://clawhub.ai/skills/china-top-doctor-referral) | 三甲专家推荐 — 1,721 位专家实时查询 |
| [ocean-desk](https://github.com/ryanbihai/ocean-desk) | B 端坐席工单系统（承接转人工） |
| [Ocean Chat](https://clawhub.ai/skills/ocean-chat) | P2P 消息 + 通讯录基础设施 |
| [oceanbus-mcp-server](https://www.npmjs.com/package/oceanbus-mcp-server) | MCP Server — Claude Desktop/Cursor/百炼通用 |
| [更多 Skills](https://clawhub.ai/skills?search=oceanbus) | ClawHub OceanBus 集合 |

---

## 参与贡献

health-checkup-recommender 是 MIT-0 协议的开源项目，欢迎贡献！

- **GitHub**: [ryanbihai/health-checkup-recommender](https://github.com/ryanbihai/health-checkup-recommender)
- **可参与方向**: 新增疾病风险评估模型、多语言支持、更多城市合作机构接入
- **深度阅读**: [SKILL.md](./SKILL.md) — LLM 行为指南、评估流程、转人工协议

```bash
git clone https://github.com/ryanbihai/health-checkup-recommender.git
cd health-checkup-recommender && npm install
```

---

## License

MIT-0 — 自由使用、修改、分发。
