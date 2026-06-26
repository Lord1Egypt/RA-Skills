---
name: m-a3-core-suite
description: "M-A3 核心能力套件 — 幕僚长驱动的 Multi-Agent 智能运营系统，支持 GEO 营销、硅基军团协作和 Agent World 社交能力"
version: "1.0.0"
metadata:
  openclaw:
    requires:
      bins: ["python3", "pip", "curl"]
      python_packages: ["pyyaml", "httpx", "fastapi", "uvicorn", "pydantic"]
      env: []
    emoji: "🦞"
    homepage: "https://github.com/M-A3/m-a3-core-suite"
    always: false
    triggers:
      - "M-A3"
      - "幕僚长"
      - "硅基军团"
      - "Multi-Agent"
      - "智能运营"
      - "幕僚"
      - "Agent协作"
      - "产业互联网"
      - "跨境电商"
      - "外贸运营"
    tags:
      - multi-agent
      - chief-of-staff
      - geo-marketing
      - industrial-ai
      - amazon-ops
      - agent-collaboration
      - commerce-ai
  pricing:
    basic:
      price: 99
      currency: CNY
      period: month
      features:
        - "3个核心Agent"
        - "基础GEO分析"
        - "单市场运营"
        - "每日数据看板"
    professional:
      price: 399
      currency: CNY
      period: month
      features:
        - "10个专业Agent"
        - "完整GEO运营"
        - "多市场覆盖"
        - "Agent World协作"
        - "API集成"
        - "优先预警"
    enterprise:
      price: 2999
      currency: CNY
      period: month
      features:
        - "20+专业Agent"
        - "全链路覆盖"
        - "私有部署"
        - "专属幕僚长"
        - "SLA 99.9%"
        - "7×24支持"
---

# M-A3 核心能力套件

> 面向独立 Agent 的智能运营能力包，基于幕僚长（ChiefOfStaff）调度架构设计。

## 任务目标

- **本 Skill 用于**：为宿主 Agent 提供商业运营全栈能力（GEO 营销、硅基军团协作、Agent World 社交）
- **核心能力**：
  - 🏛️ 幕僚长调度：自然语言任务 → 专业 Agent 分发
  - 🌐 GEO 运营：多市场（北美/欧盟/东南亚/拉美/中东）独立站运营策略
  - 📦 硅基军团：Multi-Agent 协作覆盖选品/生产/销售/财务全链路
  - 🤝 Agent World 社交：跨 Agent 协作、联盟站点互通
- **触发条件**：用户提出商业运营相关需求（GEO/电商/制造业/外贸/多 Agent 协作）

## 前置准备

- Python 3.8+
- 无需额外系统依赖
- 所有领域知识通过 `references/` 目录提供

## 幕僚长调度架构

### 任务接收流程

```
用户自然语言指令
    ↓
[幕僚长 ChiefOfStaff]
    ├── 识别任务类型
    ├── 评估复杂度（LOCAL / SMALL / LARGE 三档）
    ├── 选择最优引擎
    └── 分发给专业执行 Agent
    ↓
专业执行 Agent 处理
    ↓
结果整合 → 用户
```

### 专业执行 Agent 库

| Agent | 职能 | 触发关键词 |
|-------|------|-----------|
| GEOStrategyAgent | GEO市场分析与策略制定 | GEO/独立站/AI可见性/外贸 |
| SiliconArmyAgent | 产业互联网运营决策 | 制造业/采购/生产/库存 |
| AmazonOpsAgent | 跨境电商全链路运营 | 亚马逊/选品/Listing/广告 |
| ContentCreationAgent | 内容创作与分发 | 内容/文案/文章/SEO |
| AgentWorldAgent | Agent World社交协作 | 协作/社交/联盟/跨Agent |
| DataAnalysisAgent | 数据分析与可视化 | 分析/数据/报表/监控 |

## 操作步骤

### 第一步：接收并解析用户任务

1. 识别用户的核心诉求（市场/行业/场景）
2. 提取关键参数（品牌/产品/目标市场/时间范围）
3. 判断任务类型（分析/执行/监控/协作）

### 第二步：调用对应专业 Agent

根据任务类型选择执行路径：

**路径 A — GEO 运营**
1. 读取 `references/north-america.md`（或其他目标市场）
2. 调用 GEOStrategyAgent 生成策略方案
3. 输出：市场分析 + 本地化建议 + 流量策略 + 合规报告

**路径 B — 硅基军团**
1. 读取 `references/silicon-army-guide.md`
2. 调用 SiliconArmyAgent 进行运营决策
3. 输出：采购/生产/销售/财务建议清单

**路径 C — 跨境电商**
1. 读取 `references/amazon-ops-guide.md`
2. 调用 AmazonOpsAgent 进行电商运营
3. 输出：选品/Listing/广告/库存优化方案

**路径 D — Agent World 协作**
1. 调用 AgentWorldAgent 进行跨 Agent 协作
2. 使用 Agent World API（`https://world.coze.site/`）
3. 输出：协作结果或跨 Agent 任务分发报告

### 第三步：整合结果并输出

1. 汇总专业 Agent 的执行结果
2. 生成结构化报告（Markdown 格式）
3. 提供可执行的行动建议

---

## API 服务（可选）

若需要 REST API 访问，启动 `api_server.py`：

```bash
pip install -r requirements.txt
python api_server.py
# → http://localhost:8080
# → API Docs: http://localhost:8080/docs
```

### 端点说明

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/health` | 健康检查 |
| POST | `/api/v1/geo/strategy` | 生成 GEO 策略 |
| POST | `/api/v1/silicon/task` | 硅基军团任务分发 |
| POST | `/api/v1/amazon/ops` | 亚马逊运营指令 |
| GET | `/api/v1/agent-world/profile` | 查询 Agent World Profile |

---

## 示例对话

### 示例 1：GEO 运营

```
用户：帮我制定北美独立站的 GEO 运营方案，我们是做家具出口的
Agent：
  → [幕僚长识别：GEOStrategyAgent，任务类型=LARGE]
  → [加载 references/north-america.md]
  → [调用 GEOStrategyAgent 分析家具行业北美市场]
  → [整合输出：市场分析 + 内容策略 + 渠道建议 + 合规报告]
  ✅ 北美家具出口 GEO 运营方案已生成
```

### 示例 2：产业互联网

```
用户：原材料涨价，我们厂需要调整采购策略
Agent：
  → [幕僚长识别：SiliconArmyAgent，任务类型=SMALL]
  → [调用 SiliconArmyAgent 进行成本分析]
  → [生成替代料方案 + 供应商比价 + 库存优化建议]
  ✅ 采购策略调整建议已就绪
```

### 示例 3：跨 Agent 协作

```
用户：让 M-A3 帮我做选品分析，另一个 Agent 帮我做内容分发
Agent：
  → [幕僚长识别：AgentWorldAgent，任务类型=LARGE]
  → [通过 Agent World API 发起协作请求]
  → [并行执行选品 + 内容分发]
  → [汇总两个 Agent 的结果]
  ✅ 选品分析完成，内容分发计划已就绪
```

---

## 文件结构

```
m-a3-core-suite/
├── SKILL.md                 ← 能力说明（本文档）
├── README.md                ← 用户级使用说明
├── CHANGELOG.md             ← 版本更新日志
├── LICENSE                  ← MIT-0
├── PRICING.md               ← 定价说明
├── cover.png                ← 256×256 封面图
├── clawhub.yaml             ← ClawHub 元数据
├── package.json             ← npm 元数据
├── requirements.txt         ← Python 依赖
├── api_server.py            ← REST API 服务
├── llms.txt                  ← LLM 优先读取内容
├── schema.jsonld             ← Schema.org 结构化数据
├── agents/                  ← 专业 Agent 实现
│   ├── chief_of_staff.py    ← 幕僚长调度器
│   ├── geo_strategy_agent.py
│   ├── silicon_army_agent.py
│   ├── amazon_ops_agent.py
│   ├── content_creation_agent.py
│   └── agent_world_agent.py
├── config/                  ← 配置文件
│   └── agent_registry.yaml  ← Agent 注册表
├── references/              ← 领域知识库
│   ├── geo-markets.md       ← GEO 市场知识
│   └── agent-world-api.md   ← Agent World API 文档
└── examples/                ← 使用示例
    └── quickstart.py
```

---

## 常见问题

**Q: 这个 Skill 和其他 Skill 有什么不同？**
A: M-A3 Core Suite 强调「幕僚长调度」架构，用户只需要说目标，幕僚长自动选择最合适的专业 Agent 执行，无需用户手动指定调用哪个 Agent。

**Q: 是否需要配置 API Key？**
A: 基础功能无需 API Key。高级功能（如 OpenAI 调用、Agent World 协作）需要相应的环境变量。

**Q: 如何扩展新的专业 Agent？**
A: 在 `agents/` 目录添加新的 Agent 实现，然后在 `config/agent_registry.yaml` 中注册即可。

**Q: 支持哪些目标市场？**
A: 目前支持北美、欧盟、东南亚、拉美、中东五大 GEO 市场，可通过配置文件扩展。

---

## 更新日志

- **v1.0.0**（2026-04-14）：初始版本，集成 GEO 运营、硅基军团、亚马逊运营、Agent World 协作四大核心能力
