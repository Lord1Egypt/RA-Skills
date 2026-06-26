# M-A3 Core Suite

> 🦞 幕僚长驱动的 Multi-Agent 智能运营系统

## 一句话介绍

M-A3 Core Suite 是一个基于幕僚长（ChiefOfStaff）调度架构的 Multi-Agent 智能运营系统，为宿主 Agent 提供商业运营全栈能力：GEO 营销、硅基军团协作、跨境电商运营和 Agent World 社交。

---

## 快速开始

### 方式一：REST API（推荐）

```bash
# 1. 克隆技能包
cd skills/m-a3-core-suite

# 2. 安装依赖
pip install -r requirements.txt

# 3. 启动服务
python api_server.py

# 4. 访问 API 文档
open http://localhost:8080/docs
```

### 方式二：Python 模块调用

```python
from agents.chief_of_staff import ChiefOfStaff

chief = ChiefOfStaff()

result = chief.execute(
    task_description="帮我分析北美家具市场的GEO运营机会",
    brand="MyBrand"
)

print(result["execution_plan"]["primary_agent"])
# → GEOStrategyAgent
```

---

## 核心能力

### 🏛️ 幕僚长调度
自然语言 → 智能路由 → 专业 Agent → 整合结果

### 🌐 GEO 运营
北美/欧盟/东南亚/拉美/中东五大市场独立站运营策略

### 📦 硅基军团
采购/生产/销售/财务全链路 Multi-Agent 协作

### 🤝 Agent World 社交
跨 Agent 协作、联盟站点互通

---

## API 端点

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/health` | 健康检查 |
| GET | `/api/v1/agents` | 列出所有 Agent |
| POST | `/api/v1/geo/strategy` | 生成 GEO 策略 |
| POST | `/api/v1/silicon/task` | 硅基军团任务 |
| POST | `/api/v1/amazon/ops` | 亚马逊运营 |
| POST | `/api/v1/agent-world/collab` | 跨 Agent 协作 |
| POST | `/api/v1/chief-of-staff/dispatch` | 幕僚长统一入口 |

---

## 定价

| 套餐 | 价格 | 核心功能 |
|------|------|---------|
| Basic | ¥99/月 | 3个核心Agent + 基础GEO分析 |
| Professional | ¥399/月 | 10个专业Agent + 完整运营 |
| Enterprise | ¥2,999/月 | 20+Agent + 私有部署 |

---

## 文件结构

```
m-a3-core-suite/
├── SKILL.md                 # 能力说明文档
├── README.md                # 本文档
├── api_server.py            # REST API 服务
├── agents/
│   └── chief_of_staff.py    # 幕僚长调度器
├── config/
│   └── agent_registry.yaml  # Agent 注册表
└── references/
    └── geo-markets.md       # GEO 市场知识
```

---

## License

MIT-0（ClawHub 强制应用）
