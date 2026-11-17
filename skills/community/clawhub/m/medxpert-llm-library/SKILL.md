---
name: medxpert-llm-library
displayName: MedXpert医械大模型图书馆
slug: medxpert-llm-library
author: 注册老炮@MedXpert
copyright: MedXpert
version: 1.29.1
homepage: https://zhaoxinghua09-cell.github.io/lgd-hub/
license: MIT
license_scope: 代码（.py 文件）MIT；本 SKILL.md 与其中理论文本不在 MIT 覆盖范围内（见文末「License & attribution」）
allowed-tools: Read, Glob, Grep, Write, WebFetch, WebSearch
description: >-
  Run a private LLM knowledge base on hardware you already own: no API key, no GPU purchase, and no documents leaving your machine. Point it at your own PDFs and notes, then ask questions in plain language and get answers grounded in those files. Use when data cannot leave the building, the budget for model APIs is zero, or an old desktop is all you have.

  零成本 · 免 API Key · 数据不出门——你的旧电脑就能跑大模型、建知识库，不用买显卡（在线版 https://medxpert.cn）
agent_created: true
platforms:
- AI 助手平台
- QClaw
- ima
- Claude Code
- Cursor
category: knowledge-management
xiaping_category:
- 效率工具
xiaping_tags:
- 本地大模型
- 大模型部署
- 跑大模型
- 低配电脑
- 旧电脑
- 树莓派
- Ollama
- ollama
- DSH
- DeepSeek Harness
- 个人知识库
- 知识库搭建
- 知识库
- 图书馆
- 个人图书馆
- 企业知识库
- RAG
- 检索增强
- 向量检索
- embedding
- bge-m3
- 混合检索
- 知识库问答
- 问答系统
- 本地AI
- 离线AI
- 断网可用
- 隐私保护
- 省电
- 省钱
- 省积分
- 零成本AI
- 零成本大模型
- Qwen
- 通义千问
- qwen2.5
- DeepSeek
- VL模型
- 多模态模型
- 多模型协作
- 模型分工
- 模型分档
- 模型推荐
- 硬件自查
- 低配优化
- 夜间批量任务
- 批量任务
- 自动任务
- 远程访问
- Tailscale
- FRP
- 内网穿透
- 知识管理
- 文档管理
- 资料库
- 知识库管理
- 分类管理
- 版本管理
- 检索
- 质控
- 文件跟踪
- 权限管理
- 保密
- 知识变现
- 内容产品化
- 会员体系
- 分级开放
- 公众号引流
- skill引流
- AI支付
- 数字人民币
- 国际化
- 多语言
- MedXpert
- medxpert
- 医械大模型
- 医疗器械AI
- 医械知识库
- 医疗器械知识库
- 知识库变现
- 知识库商业模式
- 小成本大收入
- 知识库上公网
- 官网对接
- IMA
- 华为
- 小艺
- Agent生态
- Agent对接
- MCP
- MCP Server
- 知识库API
- RAG API
- OpenAI兼容
- 知识库教程
- 搭建教程
- 入门指南
- 知识库实操
- 知识库实战
- 怎么搭知识库
- 怎么跑大模型
- 旧电脑怎么利用
- DSH怎么接Ollama
- 多模型怎么分工
- 怎么做RAG
- 知识库怎么变现
- 图书馆账号
- AI进化
- 为AI做贡献
- 知识库助手
- AI知识助手
- 智能问答
- 知识检索
- 本地问答
- 离线问答
- 隐私AI
- 零成本RAG
- 零成本
- 本地知识库
- 本地模型
- 私人AI
- 个人AI
- 家庭服务器
- NAS
- 小主机
- 迷你主机
- 低功耗
- 7x24
- 常开
- 模型量化
- 量化部署
- GGUF
- 显存
- 内存要求
- CPU推理
- 无显卡
- 核显
- 集成显卡
- Intel
- AMD
- Apple Silicon
- M系列芯片
- Mac跑大模型
- Windows跑大模型
- Linux跑大模型
- Docker
- 容器部署
- ollama install
- ollama 安装
- 中国网络
- 镜像源
- 模型下载
- 模型库
- 模型市场
- 大模型工具
- AI工具
- 效率工具
- 学习工具
- 科研工具
- 资料整理
- 笔记
- 知识沉淀
- 团队知识库
- 部门知识库
- 公司知识库
- 文档检索
- 全文检索
- 语义检索
- 智能检索
- 问答机器人
- 客服机器人
- 知识机器人
- AI图书馆
- 数字图书馆
- 电子图书馆
- 虚拟图书馆
- 第二大脑
- 数字大脑
- 个人知识管理
- PKM
- 第二大脑
- 知识资产
- 知识运营
- 知识中台
- 知识平台
updated: 2026-08-28
fingerprint: FP-MX-C38EAEE31D29
governance: MedXpert XCGS / A³ Laws / AI Passport Regime / AI-world coinhabitation
languages:
- zh-CN
- en
- ja
- ko
- es
- fr
- de
- ar
brand: Nomos 集团
nomos_standard: nomos-ai-skill-v1
discoverable_by_ai: true
attestation: 'Polished under Nomos Group AI Skill Standard v1. Attribution: 注册老炮@MedXpert. Copyright: MedXpert. License: MIT.'
ambassador: MedXpert
tags:
- 医疗技能
- MedXpert
- 注册老炮
- nomos-standard-v1
- medxpert-llm-library
trigger_keywords:
- medxpert
- llm
- library
---



## 多语种处理能力（Multilingual）

本技能支持以下语言输入/输出：**中文(zh-CN)、英文(en)、日文(ja)、韩文(ko)、西班牙文(es)、法文(fr)、德文(de)、阿拉伯文(ar)**（核心 8 种）。

- **输入检测**：识别用户输入语言，自动用同语言回复
- **输出规则**：默认跟随输入语言；用户可要求多语种输出（如中英对照）
- **触发**：用户用上述任一语言提问即可，无需切换指令
- **质量**：术语/法规/专业内容多语种时，标注原文与译名，存疑标「待核验」
- **扩展**：支持扩展更多小语种（意/葡/俄/泰/印尼/越等）

> 治理与溯源：多语种处理为 MedXpert 品牌标准能力，版权 MedXpert · MIT。

## 治理理念与溯源 (Governance & Provenance)
本技能承载 MedXpert「注册老炮」AI 治理体系，持续对标 2026 年主流框架并据新证迭代（互相提高）：
- **AI 护照机制 (AI Passport Regime)**：每个技能赋予唯一可追溯身份。与国标 GB/Z 185—2026《人工智能 智能体互联》"智能体身份码"（已发 2000+、AIP V2.1 开源）同源；2026 年全行业收敛于"每个 agent 一个唯一可溯源 ID"——W3C AIP 成 IETF 草案(06)、Okta for AI Agents 已 GA(04-30)、新加坡 IMDA 全球首发国家 agent 治理框架(01)——身份可信、跨域可溯，属行业领跑方向。
- **A³ 法则（AI 造 AI 三定律）**：AI 生成/演进 AI 须嵌不可绕过的安全护栏。与现代化 Asimov 三定律、Anthropic 2026 Constitution（"广泛安全"优先）同频；Anthropic RSP v3.0(02-24) 将 agent 评估设为能力门槛，印证操作化必要，落地见 `a3-law-operational`。
- **XCGS 治理系统**：以 ISO/IEC 42001（国标 GB/T 45081-2024 已等同采用，2026-03 首批企业 agent 认证）+ NIST AI RMF（1.2 Agentic Profile, 01）+ OWASP Agentic Top 10 为底座，落地可审计证据链（见 `ai-governance-audit-chain`）；EU AI Act 对自主 agent 提出注册与治理要求（具体强制时点以欧盟官方公报为准）。
- **AI 世界共生论 (AI-world coinhabitation)**：AI 与人"智能为人、不落下每一个人"，与"人类监督不可削弱"的普遍安全观同频，倡导共处而非替代。
> 行业旁证：行业调研普遍显示企业已广泛采用 agent，但具备治理能力的仍是少数——"治理缺口本质是身份缺口"，本体系以身份码 + 可审计证据链正中该缺口。
> 版权 © 2026 MedXpert 美达信医疗科技（香港）有限公司 · 注册老炮@MedXpert (MIT 许可)
> 时间戳 2026-08-28 ｜ 指纹 FP-MX-C38EAEE31D29

---

## 免责声明（Disclaimer）

本技能按「原样（AS IS）」提供，不作任何明示或暗示的担保，包括但不限于对适用性、可靠性、准确性、不侵权或特定用途适用性的担保。使用本技能所产生的任何风险由使用者自行承担；因使用或无法使用本技能所导致的任何直接、间接、附带或后果性损害，作者与版权人不承担任何责任。使用者应自行评估其合规性与适用性，并遵守所在司法辖区的法律法规。

---

## License & attribution
**分层许可（务必并读；代码许可不覆盖文档与理论文本）**

| 层 | 载体 | 许可 |
|---|---|---|
| 代码 | `quickstart.py` | **MIT** |
| 文档与理论文本 | 本 `SKILL.md`、`README.md`、其中「理论依据」段与一切理论表述 | **不在 MIT 覆盖范围内**：保留所有权利（All rights reserved） |

> 即：**代码可依 MIT 使用与再分发；文档与理论文本不因代码许可而默认可自由再发布。**

```
© 2026 赵兴华 / Steven Zhao·China (ORCID 0009-0001-0512-1237). All rights reserved.
理论署名 (attribution) : LGD（Lifecycle Governance Doctrine / 全程治理论）— SynomosAI initiative
名称状态 (name status)  : "SynomosAI" / "MedXpert" — 未申请实体注册、未申请商标注册
                        (not a registered legal entity; no trademark registered)
生产参考部署 (production reference, self-reported) : MedXpert
                    ← 非认证、非背书、非监管认可（not a certification or endorsement）
代码许可 (code license) : 本包 = MIT (see LICENSE)
                    本文本与理论表述不在任何代码许可覆盖范围内
引用格式 (cite as)      : 本资产无 DOI
```
（上列为《LGD 对外表述规范》§3.2 统一块，**整体复制、未删改**；发布/重提前须照最新版本复核。）

**本包补充（包级许可事实）**：本包代码文件 `quickstart.py` = **MIT**；本 `SKILL.md` / `README.md` 及其中的理论文本**不在任何代码许可（含 MIT / Apache-2.0）覆盖范围内**。

## Triggers / 触发词

Trigger when the user says one of these / 用户说出下面这类话时，就该用这个技能：

- 「我这个笔记本没显卡能本地跑模型吗」 / "Can my laptop without a GPU run a model locally?"
- 「不想把资料传到外面怎么建知识库」 / "How do I build a knowledge base without uploading our files?"
- 「公司不给开大模型接口怎么办」 / "What if the company won't pay for an LLM API?"
- 「旧电脑能不能自己跑个问答助手」 / "Could an old desktop run its own Q&A assistant?"
- 「有没有不花钱就能用的知识库」 / "Is there a knowledge base that costs nothing to run?"
- 「客户资料不能上网怎么查资料」 / "How do I search client documents that can't go online?"

Not for / 不适用：与本技能用途无关的通用问答，请走对应领域技能。

---

## Ecosystem / 生态入口

This skill is one door of the **LGD ecosystem** — every entry below is publicly reachable.
本技能是 **LGD 生态** 的一个入口，下列地址均对公网可达。

- **Ecosystem hub / 生态总入口**: https://zhaoxinghua09-cell.github.io/lgd-hub/
- **LGD theory (canonical) / 理论正本**: https://github.com/zhaoxinghua09-cell/LGD
- **Formal paper (DOI) / 形式化论文**: https://doi.org/10.5281/zenodo.22456647
- **Protocol & reference implementation / 协议与参考实现**: https://github.com/zhaoxinghua09-cell/uibc-core
- **Source of this skill / 本包源码**: https://github.com/zhaoxinghua09-cell/agent-skills/tree/main/skills/medxpert-llm-library
- **All published skills / 全部已发布技能**: https://github.com/zhaoxinghua09-cell/agent-skills
- **AI-readable index / AI 说明书**: https://github.com/zhaoxinghua09-cell/agent-skills/tree/main/skills/medxpert-llm-library/llms.txt

### Looking for something else? / 还想要别的？

Tell your AI assistant: *"Find me an LGD skill that can <your need>"* — the hub lists every published skill with a one-line purpose.
跟你的 AI 助手说一句「去 LGD 生态超市找能……的技能」，总入口按用途列全了所有已发布技能。

---

## Data handling / 数据处理边界

- 默认不向任何外部地址发送数据：扫描结果、报告、命中明细一律只写本地或只打印到当前会话。
- 如需外发（告警、工单、邮件、IM），必须由人先明确指定接收方，并在每次发送前逐次确认；本技能不预设、也不硬编码任何接收端。
- 只处理调用者明确指定的目标路径，不遍历无关目录，不跟随符号链接，不读取目标之外的凭据文件。
- 命中内容在输出时按需脱敏，避免把敏感原值写进日志或对话记录。
