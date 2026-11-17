# lava-mcp · 熔岩消息面热度监测

[熔岩（Lava）](https://lava.ai-dolphin.com/subscribe) 提供 **A 股股票和概念板块的消息面热度监测** 结构化只读数据——**量化交易必备**的消息面热度信号，供系统与智能体通过远程 MCP / REST 调用。

> 只读 · 结构化要点 + 匿名机构/大V ID · **不含多空方向与原文** · 不构成投资建议

## 新手 3 步

① 开通并复制 API Key（登录熔岩 → 左侧「AI数据服务」→ API Key → 新建）

② 装 Skill，或在豆包办公/WorkBuddy/千问办公填 MCP 地址 https://lava.ai-dolphin.com/subscribe/v1/mcp

③ 用中文问「某某股票最近消息面热不热」

## 远程 MCP（推荐）

| 项 | 值 |
| --- | --- |
| 传输 | Streamable HTTP |
| Endpoint | `https://lava.ai-dolphin.com/subscribe/v1/mcp` |
| 鉴权 | 请求头 `Authorization: Bearer <API Key>`（或 `X-API-Key`） |
| 客户端 | 豆包办公、WorkBuddy（BUDDY）、千问办公（QwenWork）等支持自定义 HTTP MCP 的客户端 |

开通与计费见 [落地页](https://lava.ai-dolphin.com/subscribe)：开通赠 100 元代金券；1000 次 = 5 元。

## Skill 模板

仓库内 [`SKILL.md`](./SKILL.md) 与官方模板一致，也可直接读取：

https://lava.ai-dolphin.com/subscribe/v1/skill

适用于固化「查个股/概念消息面热度」流程。

## 文档与机器可读规范

- 产品落地页：https://lava.ai-dolphin.com/subscribe
- API 文档（canonical）：https://lava.ai-dolphin.com/subscribe/docs
- OpenAPI 3.0：https://lava.ai-dolphin.com/subscribe/v1/openapi.json
- llms.txt：https://lava.ai-dolphin.com/llms.txt
- MCP Registry：[`server.json`](./server.json)
- Glama：[`glama.json`](./glama.json)

## 主要工具（MCP）

| Tool | 用途 |
| --- | --- |
| `get_stock_news_heat` | 个股消息面热度与结构化观点列表 |
| `search_news_flow` | 关键词检索消息面结构化记录 |
| `get_concept_stock_heat` | 概念 → 个股提及排行 |
| `get_stock_concept_heat` | 个股 → 概念提及排行 |
| `get_agency_ranking` / `get_agency_pit` / `get_agency_history` / `list_agency_pit_dates` | 匿名机构/大V评分（当前 / PIT / 时序） |
| `get_account` | 余额与用量（不计费） |

## 合规边界

- 勿将输出写成荐股、多空或收益承诺
- 机构/大V仅使用匿名 `agency_id`，勿猜测真实机构/大V名
- 勿外推控制台路径（`/subscribe/v1/console` 为 noindex）

## License

文档与 Skill 模板以站点公开内容为准；本仓库仅作接入说明与分发入口。
