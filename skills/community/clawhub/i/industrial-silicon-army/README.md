# 产业互联网硅基军团 🏭

> 面向制造业的Multi-Agent AI运营平台 — 1个幕僚长 + 20个专业Agent，覆盖采购/生产/研发/销售/财务/合规全链路

[![Version](https://img.shields.io/badge/version-1.3.7-green.svg)](package.json)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Agents](https://img.shields.io/badge/Agents-20-orange.svg)](#)
[![Manufacturing](https://img.shields.io/badge/Manufacturing-Full%20Chain-blue.svg)](#)

> LookingPlas × 云旅智能体超市 联合出品

---

## 💡 一句话价值主张

**把整个制造运营团队装进口袋。** 1个AI幕僚长统一调度20个专业Agent，从原料采购到财务合规全链路辅助决策，重复工作减少80%，让工厂管理者随时随地用自然语言掌控全局。

---

## ⚡ 行业效果数据

| 指标 | 传统模式 | 硅基军团模式 |
|------|---------|------------|
| 报价响应速度 | 天级 | **分钟级** |
| 库存周转 | 月均1.2次 | **周均3.5次** |
| 设备非计划停机 | 高发 | **减少60%** |
| 合规审查效率 | 人工3-5天 | **当天完成** |
| 运营人力成本 | 全职团队 | **减少70%** |

---

## 🎯 行业版本

| 版本 | 行业 | 状态 | 核心Agent定制 |
|------|------|------|--------------|
| **v1.0 LookingPlas** | 塑化行业 | ✅ 已上线 | 原料行情、牌号匹配、物性表 |
| **v1.1 模具行业** | 注塑/冲压模具 | 🚧 开发中 | 模具寿命、BOM管理 |
| **v1.2 化工行业** | 精细化工 | 📋 规划中 | 配方合规、安全管理 |
| **v1.3 汽车零部件** | Tier1/Tier2 | 📋 规划中 | IATF 16949、追溯体系 |

---

## 👥 20个专业Agent一览

### 采购与供应链（4个）
| Agent | 职能 | 关键能力 |
|-------|------|---------|
| 🔍 原料采购Agent | 采购方案建议/行情参考/采购规划辅助 | 行情参考 + 方案比较 |
| 📦 仓储管理Agent | 库存规划建议/仓储优化方案 | 安全库存规划 + 周转分析 |
| 🚚 物流调度Agent | 车队匹配建议/路线优化 | 降低物流成本 |
| 🤝 供应商管理Agent | 评级/风控/合同 | 供应商KPI + 风控建议 |

### 生产与研发（4个）
| Agent | 职能 | 关键能力 |
|-------|------|---------|
| ⚙️ 生产调度Agent | 排产/工单管理 | 交期规划 + 产能评估 |
| 🧪 配方研发Agent | 新材料/替代料 | 成本优化 + 性能匹配 |
| ✅ 质量检测Agent | 来料/过程/成品 | 合标率 + 追溯管理 |
| 🔧 设备维护Agent | 预测性维护 | 减少非计划停机 |

### 销售与市场（4个）
| Agent | 职能 | 关键能力 |
|-------|------|---------|
| 💰 报价Agent | 快速响应/成本叠加 | 分钟级报价，提升赢率 |
| 📋 订单履约Agent | 订单处理/异常协助 | 客户满意度 |
| 👤 客户管理Agent | 客户分级/跟进建议 | 复购率提升 |
| 📊 竞品监控Agent | 市场趋势分析/定价策略建议 | 动态定价参考 |

### 财务与合规（4个）
| Agent | 职能 | 关键能力 |
|-------|------|---------|
| 🧮 成本核算Agent | 实际成本/标准成本 | 毛利分析 |
| ⚖️ 合规审查Agent | 环保/安全/税务 | 减少处罚 |
| 🚨 风险预警Agent | 客户信用评估建议/材料趋势分析 | 降低坏账 |
| 📜 政策解读Agent | 行业政策/补贴 | 争取优惠 |

### 通用运营（4个）
| Agent | 职能 | 关键能力 |
|-------|------|---------|
| 📈 数据分析Agent | 经营日报/月报生成 | BI报表 |
| 📝 报告生成Agent | 会议纪要/汇报材料 | 减少文山会海 |
| 📌 项目管理Agent | 里程碑/风险/进度 | 交付透明 |
| 🎧 客服支持Agent | 售后/投诉/FAQ | 响应<4小时 |

---

## 🏗️ 技术架构

```
用户（自然语言）
      ↓
┌─────────────────────────────────────┐
│     幕僚长 (ChiefOfStaff)            │
│     LangGraph 状态机 + RAG知识库      │
└──────────────┬──────────────────────┘
               ↓ 自动路由
     20个专业Agent（并行执行）
               ↓
   ERP / MES / WMS / CRM API
```

- **幕僚长引擎**: LangGraph 状态机 + 关键词路由
- **Agent运行时**: Python asyncio，Docker容器化
- **API层**: FastAPI，RESTful + Webhook
- **数据集成**: ERP / MES / WMS / CRM 标准接口
- **行业适配**: LookingPlas塑化行业数据模型

---

## 🚀 快速开始

```bash
cd industrial-silicon-army
pip install -r requirements.txt
python api_server.py
# → http://localhost:8080
```

### 接口一览

| 方法 | 路径 | 说明 |
|------|------|------|
| `GET` | `/health` | 服务健康检查 |
| `POST` | `/api/v1/execute` | 执行任务（幕僚长自动路由） |
| `GET` | `/api/v1/agents` | 获取Agent列表 |
| `GET` | `/api/v1/agents/{id}` | 获取单个Agent详情与调用统计 |
| `GET` | `/api/v1/stats` | 系统调用统计（不含任务内容） |
| `POST` | `/api/v1/batch` | 批量并发执行多个任务 |

### API文档（在线）
`http://localhost:8080/docs`

### 接口示例

```bash
# 调用幕僚长，自动路由任务
curl -X POST http://localhost:8080/api/v1/execute \
  -H "Content-Type: application/json" \
  -d '{"task": "本周原料库存不足，帮我分析行情并生成采购方案建议"}'

# 批量执行任务
curl -X POST http://localhost:8080/api/v1/batch \
  -H "Content-Type: application/json" \
  -d '{
    "tasks": [
      {"task": "分析本月生产成本", "task_id": "cost-001"},
      {"task": "有客户投诉产品质量问题", "task_id": "cs-002"},
      {"task": "生成库存分析报告", "task_id": "inv-003"}
    ]
  }'
```

### Python SDK
```python
from industrial_silicon_army import ChiefOfStaff

client = ChiefOfStaff(base_url="http://localhost:8080")
result = client.execute(
    task="原材料价格波动，请分析对毛利影响并生成应对方案建议"
)
print(result)
```

---

## 🆚 竞品对比

| 能力 | 产业互联网硅基军团 | SAP/用友U8 | 定制开发 |
|------|-----------------|-----------|---------|
| Agent数 | **20个专业Agent** | 单系统 | 按需 |
| 自然语言交互 | ✅ 全程自然语言 | ❌ 需培训 | ❌ 无 |
| 部署周期 | **1-2周** | 3-12个月 | 数月 |
| 实施成本 | **¥3,588/年**起 | ¥50万+ | ¥20万+ |
| 行业适配 | 塑化/模具/化工/汽车 | 通用，需定制 | 完全定制 |
| 运维成本 | 低（SaaS托管） | 高（自维） | 高（持续维保） |
| 扩展性 | API全开放 | 有限 | 按需 |

---

## 📞 联系方式

- 🌐 Website: [https://cloudtrip.ai](https://cloudtrip.ai)
- 📧 Email: [support@cloudtrip.ai](mailto:support@cloudtrip.ai)
- 🐙 GitHub: [github.com/cloudtrip-ai](https://github.com/cloudtrip-ai)

---

*© 2024 LookingPlas × 云旅智能体超市. Apache 2.0 Licensed.*
