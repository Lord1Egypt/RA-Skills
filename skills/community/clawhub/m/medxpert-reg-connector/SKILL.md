---
name: medxpert-reg-connector
slug: medxpert-reg-connector
title: MedXpert 全球法规连接器（MCP）
displayName: MedXpert·全球法规连接器
display_name: MedXpert·全球法规连接器
version: 1.0.0
homepage: https://zhaoxinghua09-cell.github.io/lgd-hub/
category: knowledge-management
xiaping_category: ["学术研究"]
platforms: [WorkBuddy, QClaw, ima, Claude Code, Cursor]
author: 注册老炮@MedXpert
license: MIT
description: >-
  An MCP connector for medical device regulatory retrieval, covering MDR/CE, FDA 510(k), UDI, STED, classification, and global registration pathways. Agents query the local read-only NMPA/FDA/MDR/PMDA 27-hub regulation knowledge base via MCP—no network egress, no credentials.

  医疗器械注册法规检索 MCP 连接器，覆盖 MDR/CE、FDA 510(k)、UDI、STED、分类界定、全球注册路径等场景；agent 通过 MCP 本地只读检索 NMPA/FDA/MDR/PMDA 等 27 枢纽法规知识库，无需联网外发、无需凭据。
description_en: An MCP connector for medical device regulatory retrieval, covering MDR/CE, FDA 510(k), UDI, STED, classification, and global registration pathways. Agents query the local read-only NMPA/FDA/MDR/PMDA 27-hub regulation knowledge base via MCP—no network egress, no credentials.
tags: ["医疗器械注册","MCP","reg-connector","NMPA","FDA 510(k)","MDR CE","UDI","STED","分类界定","全球注册","法规连接器","AI Agent"]
agent_created: true
---

# MedXpert 全球法规连接器（MCP）

## 1. 这是什么

reg-connector 是 MedXpert（美达信医疗）医械线的对外接口，把 MedXpert 全球法规知识库（27 份枢纽资料）封装成一个**本地只读 MCP Server**。你的 agent（WorkBuddy / Claude Code / Cursor 等任意 MCP 客户端）装上后，即可直接调用检索——零网络外发、零凭据。

它与已上架 skillhub 的知识技能 **medxpert-reg-hub** 互补：reg-hub 是"AI 读取型知识库"，给 agent 读；reg-connector 是"程序化运行时补全"，给 agent 调。两者配合，既能读又能查。

## 2. 能力清单

基于 FastMCP stdio 协议（依赖 `fastmcp`），提供 4 个工具：

- `list_hubs()` — 返回全部枢纽 JSON：`hub_key / title / sections / official_links / phase`。先调它拿到 key。
- `search_regulation(query: str, top_k: int = 5, hub_filter: str = None)` — 关键词检索（中/英/法规号，如 `UDI`、`510k`、`MDR PMS`、`委托生产`）。返回 `hub_key / title / section / snippet / score / links`。query 为空报错。
- `get_hub(hub_key: str)` — 取某枢纽完整内容（`content + official_links`）。
- `ask_classification(product: str)` — 产品分类与注册路径速查，返回 `matches + recommended_hubs + hint`。product 为空报错。

服务端标识：`SERVER_NAME = "medxpert-reg-connector"`，版本 1.0.0。

## 3. 一键安装（3 步）

① 把包解压/克隆到本地目录，确保 `references/` 与 `reg_connector_server.py` **同级**（开箱即用）。

② 安装依赖：

```bash
pip install fastmcp
```

③ 把下面片段加入宿主的 `mcp.json`（路径改成本地实际路径），重载 MCP 连接即生效。

```json
{
  "mcpServers": {
    "@nomos/medxpert/reg-connector": {
      "command": "<你的 python 解释器路径>",
      "args": ["<medxpert-reg-connector 包目录>/reg_connector_server.py"],
      "disabled": false,
      "description": "MedXpert 全球法规连接器：本地只读检索全球医疗器械法规知识库 (NMPA/FDA/MDR/PMDA 等 27 枢纽)"
    }
  }
}
```

知识库三级回退：① 包内 `references/` ② 环境变量 `REG_HUB_REFS` ③ 脚本同级 `../references`。

## 4. 调用示例

- `search_regulation("UDI")` → 命中 UDI 四体系（NMPA/FDA/EU/MDR）对照，返回枢纽、段落、片段与官方链接。
- `ask_classification("骨科金属接骨板")` → 返回分类匹配、推荐枢纽（如分类界定、技术文件/STED）与检索提示。
- `list_hubs()` → 返回 27 枢纽目录（含 hub_key、标题、章节、官方链接、阶段）。
- `get_hub("UDI全球标识枢纽")` → 取该枢纽完整正文与官方链接（key 为 references 文件名 stem，由 list_hubs 取得）。

## 5. 典型场景

- **注册路径速查**：新产品先用 `ask_classification` 找分类与路径，再 `get_hub` 看细节。
- **UDI 多国对照**：`search_regulation("UDI")` 一次拉齐中/美/欧要求。
- **临床评价·风险管理资料索引**：`search_regulation("临床评价")` / `("风险管理")`，定位知识库对应章节与官方出处。

## 6. 注意事项与边界

1. 返回为**知识库线索，非官方结论**；分类与注册路径须以官方分类库（NMPA/FDA/MDR）为准。
2. **本地只读、零外发**，适合内网/合规环境；不联网、不带凭据。
3. 知识库有更新后，需**重载 server** 才能生效。
4. 可用环境变量 `REG_HUB_REFS` 指向自定义知识库目录。

## 7. 许可与归属

MIT License，© 2026 注册老炮@MedXpert。

知识版权声明：本包所含合成知识与方法论归 MedXpert（美达信医疗）品牌所有，禁止复制、转售或用于模型训练。

## Triggers / 触发词

Trigger when the user says one of these / 用户说出下面这类话时，就该用这个技能：

- 「帮我查一下欧盟这类产品怎么分类」 / "Look up how the EU classifies this kind of product."
- 「美国对这个耗材有没有对应指南」 / "Is there a US guidance that covers this consumable?"
- 「这个产品在美国按什么路径报」 / "Which US pathway does this product go through?"
- 「器械唯一标识的规则去哪查原文」 / "Where can I read the actual UDI rule text?"
- 「日本同类产品的注册要求是什么」 / "What are Japan's registration requirements for similar products?"
- 「不联网也能查法规原文吗」 / "Can I search the regulation text without going online?"

Not for / 不适用：与本技能用途无关的通用问答，请走对应领域技能。

---

## Ecosystem / 生态入口

This skill is one door of the **LGD ecosystem** — every entry below is publicly reachable.
本技能是 **LGD 生态** 的一个入口，下列地址均对公网可达。

- **Ecosystem hub / 生态总入口**: https://zhaoxinghua09-cell.github.io/lgd-hub/
- **LGD theory (canonical) / 理论正本**: https://github.com/zhaoxinghua09-cell/LGD
- **Formal paper (DOI) / 形式化论文**: https://doi.org/10.5281/zenodo.22456647
- **Protocol & reference implementation / 协议与参考实现**: https://github.com/zhaoxinghua09-cell/uibc-core
- **Source of this skill / 本包源码**: https://github.com/zhaoxinghua09-cell/agent-skills/tree/main/skills/medxpert-reg-connector
- **All published skills / 全部已发布技能**: https://github.com/zhaoxinghua09-cell/agent-skills
- **AI-readable index / AI 说明书**: https://github.com/zhaoxinghua09-cell/agent-skills/tree/main/skills/medxpert-reg-connector/llms.txt

### Looking for something else? / 还想要别的？

Tell your AI assistant: *"Find me an LGD skill that can <your need>"* — the hub lists every published skill with a one-line purpose.
跟你的 AI 助手说一句「去 LGD 生态超市找能……的技能」，总入口按用途列全了所有已发布技能。
