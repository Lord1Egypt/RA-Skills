---
name: "JisuAPI Agent - 极速数据智能代理"
description: 用自然语言搜索并调用极速数据 500+ 接口（search → execute），含执行统计。当用户说：帮我查一下这个手机号归属地、用 Agent 调极速数据、今天 API 调用花了多少钱，或不想记具体接口路径时，使用本技能。
metadata: { "openclaw": { "emoji": "🤖", "requires": { "bins": ["python3"], "env": ["JISU_API_KEY"] }, "primaryEnv": "JISU_API_KEY" } }
---

# 极速数据 Agent（JisuAPI Agent）

> 基于 **[极速数据 Agent API](https://www.jisuapi.com/agent/docs/)** — 面向 AI Agent 的统一网关：自然语言 **搜索工具** → **执行调用** → **统计监控**。复用现有 APPKEY，按原接口规则计费。

与 `skills/jisu/jisu.py`（手动指定 `api` 路径）不同，本技能让 Agent **无需记忆接口名**：用口语描述需求，由平台自动匹配最合适的工具。

## 何时使用本技能

- 用户用 **自然语言** 描述数据需求，不确定该调哪个具体 API
- 需要 **search + execute** 完整链路（含 `search_id` 关联）
- 需要查看 **Agent 调用统计、明细、仪表盘**
- 希望覆盖 **500+ 极速数据接口**，而不逐个安装品类 skill

**技术前提：** 脚本 **`skills/jisuapi/agent.py`**，环境变量 **`JISU_API_KEY`**（Bearer 认证）。

## 工作流程

```text
用户自然语言需求
    ↓
search（语义搜索工具，返回 tool_id + 参数说明）
    ↓
execute（传入 tool_id + params，返回业务数据）
    ↓
（可选）stats / stats_detail 查看用量与费用
```

## 前置配置

1. 前往 [极速数据官网](https://www.jisuapi.com/) 注册并获取 **AppKey**
2. 在会员中心开通所需数据接口（execute 按各工具原规则计费）
3. 配置 Key：

```bash
# Linux / macOS
export JISU_API_KEY="your_appkey_here"

# Windows PowerShell
$env:JISU_API_KEY="your_appkey_here"
```

## 脚本路径

脚本文件：`skills/jisuapi/agent.py`

## 使用方式

### 1. 搜索工具（search）

根据自然语言查询匹配工具，返回 `tool_id`、参数 schema、示例、匹配度等。

文档：[search 接口](https://www.jisuapi.com/agent/docs/search)

```bash
python3 skills/jisuapi/agent.py search '{"query":"查询手机号归属地","limit":5}'

# 简写：纯文本 query
python3 skills/jisuapi/agent.py search 查询手机号归属地

# 分类筛选
python3 skills/jisuapi/agent.py search '{"query":"股票","category":"金融","limit":5}'
```

| 字段名       | 类型   | 必填 | 说明                                      |
|--------------|--------|------|-------------------------------------------|
| query        | string | 是*  | 自然语言查询（与 category 至少填一项）    |
| limit        | int    | 否   | 返回数量，默认 5，最大 20                 |
| category     | string | 否   | 分类筛选，如「生活」「金融」              |
| search_mode  | string | 否   | `auto` / `llm` / `keyword`，默认 auto     |

**计费：** search 按 Token 计费（价格低廉）；优先使用 `match_score > 0.7` 的结果。

### 2. 执行工具（execute）

调用 search 返回的 `tool_id`，传入业务参数。

文档：[execute 接口](https://www.jisuapi.com/agent/docs/execute)

```bash
python3 skills/jisuapi/agent.py execute '{"tool_id":"shouji_query","params":{"mobile":"13800138000"},"search_id":"sch_xxx"}'
```

| 字段名          | 类型   | 必填 | 说明                           |
|-----------------|--------|------|--------------------------------|
| tool_id         | string | 是   | 工具 ID（来自 search）         |
| params          | object | 是   | 工具参数                       |
| search_id       | string | 否   | 关联的搜索 ID（推荐传递）      |
| idempotency_key | string | 否   | 幂等键，防重复执行（24h 有效） |

**计费：** 按工具原规则扣费（免费工具仍免费）；参数错误导致失败通常不计费。

### 3. 一键搜索并执行（run）

便捷命令：自动 search → 选匹配度最高工具 → execute。

```bash
python3 skills/jisuapi/agent.py run '{"query":"查询手机号归属地","params":{"mobile":"13800138000"}}'

# 选第 2 个匹配工具（tool_index 从 0 起）
python3 skills/jisuapi/agent.py run '{"query":"天气预报","params":{"city":"北京"},"tool_index":1}'
```

| 字段名     | 类型   | 必填 | 说明                          |
|------------|--------|------|-------------------------------|
| query      | string | 是   | 自然语言查询                  |
| params     | object | 否   | 传给 execute 的参数           |
| limit      | int    | 否   | search 返回条数，默认 5       |
| tool_index | int    | 否   | 选用第几个工具，默认 0        |
| category   | string | 否   | 同 search                     |

### 4. 执行统计（stats）

查询调用次数、成功率、费用等。**免费接口。**

文档：[stats 接口](https://www.jisuapi.com/agent/docs/stats)

```bash
# 今日统计
python3 skills/jisuapi/agent.py stats '{}'

# 指定时间范围
python3 skills/jisuapi/agent.py stats '{"start_date":"2026-06-01","end_date":"2026-06-03","group_by":"day"}'

# 指定工具
python3 skills/jisuapi/agent.py stats '{"tool_id":"shouji_query","start_date":"2026-06-01","end_date":"2026-06-03"}'
```

| 字段名     | 类型   | 必填 | 说明                          |
|------------|--------|------|-------------------------------|
| start_date | string | 否   | 开始日期 YYYY-MM-DD           |
| end_date   | string | 否   | 结束日期 YYYY-MM-DD           |
| tool_id    | string | 否   | 筛选指定工具                  |
| group_by   | string | 否   | `day` / `hour` / `tool`       |

单次查询最多 **90 天**。

### 5. 执行明细（stats_detail）

分页查看每次 execute 的成功/失败、耗时、费用等。**免费。**

```bash
python3 skills/jisuapi/agent.py stats_detail '{"date":"2026-06-01","tool_id":"shouji_query","page":1,"page_size":20}'
```

| 字段名    | 类型   | 必填 | 说明                    |
|-----------|--------|------|-------------------------|
| date      | string | 否   | 日期，默认今天          |
| start_date| string | 否   | 范围开始                |
| end_date  | string | 否   | 范围结束                |
| tool_id   | string | 否   | 筛选工具                |
| success   | string | 否   | `1` 成功 / `0` 失败     |
| page      | int    | 否   | 页码，默认 1            |
| page_size | int    | 否   | 每页条数，默认 20，最大 100 |

### 6. 统计仪表盘（stats_dashboard）

今日汇总、昨日对比、Top5 工具、小时分布等。**免费。**

```bash
python3 skills/jisuapi/agent.py stats_dashboard '{"date":"2026-06-11"}'
```

## 返回结果示例（节选）

### search 成功

```json
{
  "status": 0,
  "msg": "ok",
  "result": {
    "search_id": "sch_20260603_120001_xxx",
    "tools": [
      {
        "tool_id": "shouji_query",
        "name": "手机号码归属地查询",
        "description": "查询手机号码的归属地、运营商等信息",
        "category": "生活",
        "parameters": {
          "mobile": {
            "type": "string",
            "required": true,
            "description": "11位手机号码"
          }
        },
        "example": { "mobile": "13800138000" },
        "match_score": 0.95
      }
    ]
  }
}
```

### execute 成功

```json
{
  "status": 0,
  "msg": "ok",
  "result": {
    "province": "北京",
    "city": "北京",
    "company": "中国移动"
  },
  "meta": {
    "tool_id": "shouji_query",
    "execution_id": "exe_20260603_120102_xxx",
    "charge": {
      "final_layer": "free",
      "cost": 0.0
    },
    "elapsed_ms": 138
  }
}
```

> 网关可能返回 `data` 字段而非 `result`；脚本会自动归一化为 `result` 便于 Agent 解析。

## 常见错误码

### search

| 代号 | 说明           |
|------|----------------|
| 203  | query 不能为空 |
| 303  | 搜索查询为空   |
| 304  | 未找到匹配工具 |

### execute

| 代号 | 说明                 |
|------|----------------------|
| 203  | tool_id 不能为空     |
| 301  | 未找到 tool          |
| 302  | 工具参数缺失或错误   |
| 103  | APPKEY 无此数据权限  |
| 104  | 请求超过次数限制     |
| 401  | 需要实名认证         |
| 402  | 需要企业认证         |
| 501  | 上游超时             |
| 502  | 上游错误             |

### 系统错误码

| 代号 | 说明                 |
|------|----------------------|
| 101  | APPKEY 为空或不存在  |
| 102  | APPKEY 已过期        |
| 105  | IP 被禁止            |

## 推荐用法

1. **标准两步流程**（推荐，可控性高）  
   - 用户：「13800138000 是哪里手机号？」  
   - `search '{"query":"查询手机号归属地","limit":3}'` → 确认 `tool_id` 与 `parameters`  
   - `execute '{"tool_id":"shouji_query","params":{"mobile":"13800138000"},"search_id":"..."}'`  
   - 从 `result` 抽取省份、运营商等回复用户

2. **快速一步流程**  
   - `run '{"query":"查询13800138000手机号归属地","params":{"mobile":"13800138000"}}'`  
   - 若 `selected_tool.match_score < 0.7`，向用户确认是否使用该工具

3. **多工具场景**  
   - search 返回多个工具时，按 `match_score` 排序展示；用户选定后再 execute  
   - 或调整 `run` 的 `tool_index`

4. **费用与监控**  
   - 定期 `stats` / `stats_dashboard` 查看用量  
   - 异常失败用 `stats_detail` 定位 `execution_id`

## 与其他技能的关系

| 技能 | 适用场景 |
|------|----------|
| **jisuapi（本技能）** | 自然语言发现 + 调用，覆盖全站 Agent 工具 |
| **jisu** | 已知确切 `api` 路径时的统一 GET 网关 |
| **gold / exchange / stock 等** | 单一品类、参数固定的专用 skill，文档更细 |

已知具体接口且参数明确时，专用 skill 或 `jisu call` 可能更直接；不确定调哪个接口时，优先用本 Agent 技能。

## 关于极速数据 Agent

**极速数据 Agent**（[文档首页](https://www.jisuapi.com/agent/docs/)）提供：

- **MCP 协议** — 支持 Cursor、Claude Desktop 等 MCP 客户端
- **HTTP 网关** — 任意语言通过 REST 接入
- **智能搜索** — 自然语言匹配 500+ 接口
- **统一计费** — 复用 APPKEY，免费接口保持免费

OpenClaw 安装：`clawhub install jisuapi`（以 ClawHub 实际包名为准）。

在官网注册后于会员中心获取 **AppKey**；各工具额度与价格见对应 API 页面及 [可用接口列表](https://www.jisuapi.com/agent/docs/tools)。
