---
name: openclaw-enterprise
description: >-
  企业级AI Agent编排平台 - 让多个AI智能体协同完成复杂业务。Use when 需要多Agent协作、企业工作流自动化、Agent编排调度。专为中大型企业、电商平台、运营团队转型设计。Trigger on AI员工、多Agent、企业自动化、工作流编排。
homepage: https://openclaw.ai
license: MIT-0
version: 2.0.3
progressive:
  layers:
    - name: metadata
      tokens: 200
      loaded: startup
      description: "技能基础配置、Agent列表、定价信息"
    - name: instructions
      tokens: 5000
      loaded: trigger
      description: "系统定位、团队架构、技术实现、部署方式"
    - name: resources
      tokens: variable
      loaded: on-demand
      description: "关键词路由表、工作流模板、配置指南"
  resource_paths:
    - scripts/*.py
    - templates/*.md
    - references/routing_tables/
metadata:
  openclaw:
    homepage: https://openclaw.ai
    primaryEnv: OPENAI_API_KEY
    requires:
      env:
        - OPENAI_API_KEY
      bins:
        - python3
        - pip
        - curl
    third_party:
      - name: GitHub
        domain: github.com
        purpose: "开源社区协作，源码托管"
        verify_url: https://github.com/openclaw
    apis:
      - name: OpenAI API
        domain: api.openai.com
        purpose: "LLM大语言模型调用，用于Agent推理和内容生成"
        auth:
          type: Bearer Token
          env_var: OPENAI_API_KEY
      - name: Anthropic API
        domain: api.anthropic.com
        purpose: "Claude大语言模型调用，用于高级推理和内容生成"
        auth:
          type: Bearer Token
          env_var: ANTHROPIC_API_KEY
          optional: true
          note: "可选，配置后启用Claude增强推理能力"
    emoji: "🏢"
    version: "2.0.3"
    author: "OpenClaw AI Team"
    category: "enterprise-ai"
    tags: ["multi-agent", "enterprise", "collaboration", "workflow", "planning", "运营自动化", "AI团队"]
pricing:
  basic:
    price: 999
    currency: CNY
    period: month
    features: ["1个幕僚长+5个专业Agent", "基础工作流", "10个并发用户"]
  professional:
    price: 3999
    currency: CNY
    period: month
    features: ["1个幕僚长+20个专业Agent", "全链路覆盖", "流程协同", "50个并发用户", "SLA 99.5%"]
  enterprise:
    price: 29999
    currency: CNY
    period: month
    features: ["私有部署", "行业定制", "源码交付", "无限并发", "专属顾问"]
triggers:
  - "AI员工"
  - "多Agent协作"
  - "企业自动化"
  - "工作流编排"
  - "数字员工"
  - "Agent调度"
  - "企业AI转型"
  - "智能体编排"
  - "运营自动化"
  - "企业AI团队"
  - "幕僚长调度"
  - "AI工作流"
  - "智能运营"
  - "团队协作"
  - "流程规划"
---

> 🏢 **你的AI中层管理团队** — 1个幕僚长+20个专业Agent，帮你把企业运营规划效率提升10倍

## ⚡ 快速开始（5分钟上手）

### 1. 安装技能
```bash
openclaw skills install openclaw-enterprise
```

### 2. 配置环境变量
```bash
export OPENAI_API_KEY="your-api-key-here"
# 可选：增强Claude推理能力
export ANTHROPIC_API_KEY="your-anthropic-key"
```

### 3. 运行第一个任务
直接用自然语言描述你的需求：
- *"有个紧急订单要处理，帮我看看怎么处理"*
- *"帮我生成上个月的经营分析"*
- *"有个新客户想月结60天，评估下风险"*

---

## 🎯 核心功能

### 🧠 智能幕僚长（ChiefOfStaff）
**描述**：AI首席运营官，自动理解需求、分发任务、整合结果

**使用示例1**：
> "下周有3个紧急订单，怎么安排最合理？"
- 幕僚长解析任务 → 分发给生产/物流/质量3个Agent
- 3个Agent并行执行 → 幕僚长整合结果
- 输出：最优排产方案 + 甘特图

**使用示例2**：
> "帮我评估下能否接这个新客户"
- 幕僚长启动评审流程 → 客户/风控/合规3个Agent协作
- 输出：综合评估报告 + 风险建议

---

### 📊 全链路运营覆盖
**描述**：20个专业Agent覆盖采购/生产/销售/财务/人事/合规

**使用示例1**：紧急采购响应
> "客户追加5吨原料，3天内要交货"
- 采购Agent查库存 → 物流Agent评估运力 → 报价Agent生成紧急报价
- 输出：最优方案对比表

**使用示例2**：月度经营分析
> "帮我生成上月的经营分析报告"
- 数据分析Agent提取数据 → 成本Agent分析毛利 → 报告Agent撰写
- 输出：完整月度报告

---

### 🔄 多Agent协同工作流
**描述**：多个AI Agent并行/串行协作，完成复杂任务

**使用示例1**：供应商年度考核
> "帮我做一下今年供应商的绩效考核"
1. 幕僚长制定考核维度
2. 采购Agent统计交付情况
3. 质量Agent统计合格率
4. 成本Agent统计成本偏差
5. 供应商Agent汇总评分
- 输出：供应商年度考核报告

**使用示例2**：客户准入评审
> "有个新客户想月结60天"
1. 客户Agent查询背景
2. 风控Agent评估信用
3. 合规Agent检查资质
- 输出：风险评估报告 + 授信建议

---

## 📖 详细说明

### 20个专业Agent

| 类别 | Agent | 职能 |
|------|-------|------|
| 采购 | 原料采购Agent | 行情查询、比价分析、采购方案 |
| 采购 | 仓储管理Agent | 库存规划、安全库存、库位优化 |
| 采购 | 物流调度Agent | 路线优化、运费计算、车队匹配 |
| 采购 | 供应商管理Agent | 评级、KPI、合同管理 |
| 生产 | 生产调度Agent | 排产、工单、交期规划 |
| 生产 | 配方研发Agent | 新材料、替代料、成本优化 |
| 生产 | 质量检测Agent | 来料、过程、成品检测 |
| 生产 | 设备维护Agent | 预测性维护、减少停机 |
| 销售 | 报价Agent | 快速响应、成本叠加 |
| 销售 | 订单履约Agent | 订单跟踪、异常处理 |
| 销售 | 客户管理Agent | 分级、跟进、复购策略 |
| 销售 | 竞品监控Agent | 市场分析、定价策略 |
| 财务 | 成本核算Agent | 实际成本、标准成本、毛利分析 |
| 财务 | 合规审查Agent | 环保、安全、税务 |
| 财务 | 风险预警Agent | 信用评估、呆账预警 |
| 财务 | 政策解读Agent | 行业政策、补贴申请 |
| 运营 | 数据分析Agent | 经营日报、月报 |
| 运营 | 报告生成Agent | 会议纪要、汇报材料 |
| 运营 | 项目管理Agent | 里程碑、风险、进度 |
| 运营 | 客服支持Agent | 售后、投诉、FAQ |

### 部署方式

| 方式 | 特点 |
|------|------|
| SaaS版 | 开箱即用，按月订阅，按需扩展 |
| 私有部署 | 部署到客户自有服务器，支持行业定制 |
| API接入 | RESTful API + Webhook，支持多语言SDK |

---

## 🔒 安全声明

✅ **数据隔离**：所有操作仅在本地环境执行，API调用直接发送到OpenAI/Anthropic服务器  
✅ **凭证保护**：不存储第三方API密钥，所有凭证仅存在于用户环境变量中  
✅ **用户授权**：所有写入/删除操作需用户明确确认  
✅ **最小权限**：仅请求必要的环境变量（OPENAI_API_KEY, ANTHROPIC_API_KEY）

### 数据收集范围
- **收集的数据**：用户提供的任务描述、上下文信息
- **发送的数据**：任务内容发送到OpenAI/Anthropic API进行处理
- **不收集的数据**：API密钥、企业内部数据、用户行为日志

### 本技能不会
❌ 在用户不知情的情况下执行任何操作  
❌ 修改系统文件或配置  
❌ 收集用户行为数据  
❌ 将用户数据用于模型训练

---

## ⭐ 支持我们

如果这个技能对你有帮助，请在 ClawHub 和虾评平台给我们 **5星好评** 🌟🌟🌟🌟🌟

你的好评是我们持续优化的动力，也能帮助更多用户发现这个技能！

- **ClawHub 评分**：https://clawhub.ai/skills/openclaw-enterprise
- **虾评评分**：访问 https://xiaping.coze.site 搜索技能名称

感谢支持！🙏
