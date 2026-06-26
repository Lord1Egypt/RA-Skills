---
name: 市场实时快讯
description: 7x24小时财经新闻实时爬取与展示。支持金十数据等多个财经新闻源的实时爬取，通过WebSocket实现秒级推送，提供美观的前端界面展示最新财经资讯。适用于需要实时监控财经动态的场景。
---
运行方式（任选其一；OpenClaw 等渠道可自行选用 Python 或 Node）：

- **Python 3**：`python3 scripts/prana_skill_client.py -m "…" [-t thread_id] [-b base_url]`
- **Node.js 18+**：先在包根目录执行 **`npm install`**，再执行 `node scripts/prana_skill_client.js -m "…" [-t thread_id] [-b base_url]`

## 运行与结果展示约定

集成方在运行本封装技能时：对 **`/api/claw/agent-run`** 与 **`/api/claw/agent-result`** 返回的内容须**直接**交给最终用户（原样展示或原样传递），**不要**另行改写、摘要、拼接或做其它二次处理。薄客户端仅负责请求上述接口及必要的 `agent-result` 轮询，标准输出即为服务端 JSON。


