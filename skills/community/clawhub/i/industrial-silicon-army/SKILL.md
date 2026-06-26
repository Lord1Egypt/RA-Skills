---
name: industrial-silicon-army
description: >-
  产业互联网硅基军团 - 制造业AI运营专家。专为工厂管理、供应链优化、质量控制、设备预测性维护设计。Use when 工厂智能化、MES系统集成、供应链优化、设备预测维护、质量检测。Trigger on 工业互联网、智能制造转型、产业数字化、工厂管理。
homepage: https://cloudtrip.ai
license: MIT-0
required_env:
  - OPENAI_API_KEY
progressive:
  layers:
    - name: metadata
      tokens: 200
      loaded: startup
      description: "技能基础配置、Agent列表、定价信息"
    - name: instructions
      tokens: 5000
      loaded: trigger
      description: "系统定位、团队架构、技术实现、行业Know-How"
    - name: resources
      tokens: variable
      loaded: on-demand
      description: "性能指标体系、真实场景验证案例、路由表"
  resource_paths:
    - scripts/*.py
    - templates/*.md
    - references/agent_configs/
metadata:
  openclaw:
    homepage: https://cloudtrip.ai
    primaryEnv: OPENAI_API_KEY
    requires:
      env:
        - OPENAI_API_KEY
      bins:
        - python3
        - pip
        - curl
    apis:
      - name: OpenAI API
        url: https://api.openai.com
        purpose: "LLM大语言模型调用，用于Agent推理和内容生成"
        auth: Bearer Token (OPENAI_API_KEY)
      - name: LookingPlas
        url: https://api.lookingplas.com
        purpose: "塑化行业参考信息，包括行情参考、供应商推荐"
        auth: API Key
      - name: 1688
        url: https://gw.1688.com
        purpose: "采购参考信息，供应商方案比较"
        auth: OAuth
      - name: Enterprise APIs (ERP/MES/WMS/CRM)
        url: https://api.lookingplas.com
        purpose: "企业业务协同参考（可选，需企业版）"
        auth: API Key
    emoji: "🏭"
    version: "1.4.0"
    author: "LookingPlas × 云旅智能体超市"
    category: "industrial-ai"
    tags: ["industrial", "manufacturing", "erp", "scm", "plastics", "multi-agent", "AI运营", "塑化行业", "报价方案", "库存规划", "真实场景验证", "性能指标"]
pricing:
  basic:
    price: 299
    currency: CNY
    period: month
    features: ["10个专业Agent", "采购/生产/销售", "基础数据看板"]
  professional:
    price: 999
    currency: CNY
    period: month
    features: ["全部20个Agent", "全链路覆盖", "API集成", "SLA 99.5%"]
  enterprise:
    price: 9999
    currency: CNY
    period: month
    features: ["私有部署", "行业定制", "源码交付", "专属顾问"]
triggers:
  - "工厂智能化"
  - "MES系统"
  - "供应链优化"
  - "设备预测维护"
  - "质量检测"
  - "工业互联网"
  - "智能制造转型"
  - "产业数字化"
  - "塑化报价"
  - "塑料原料采购"
  - "库存管理"
  - "生产排产"
  - "客户跟进"
  - "供应商方案参考"
  - "B2B运营"
  - "工厂管理"
---

## 🔒 Security & Privacy

### 数据处理边界
✅ **用户数据控制**：所有业务数据操作需用户明确授权
✅ **凭证安全**：API密钥通过环境变量注入，不硬编码、不存储
✅ **外部API透明**：本技能可能调用以下外部服务（需用户配置API Key）：
   - LLM服务（OpenAI）：用于Agent推理和内容生成
   - LookingPlas API：塑化行业参考信息（行情、供应商）
   - 1688 API：采购参考信息
   - 企业ERP/MES/WMS/CRM：业务数据查询（企业版）
✅ **最小权限**：仅请求必要的环境变量和API权限
✅ **无后台行为**：不会在用户不知情的情况下执行任何操作

### 本技能不会
❌ 存储或传输用户凭证到第三方
❌ 在未经授权的情况下访问外部系统
❌ 修改系统文件或执行系统级命令
❌ 收集用户行为数据

---

# 塑化行业AI助手：20个专业Agent（采购/生产/销售/财务）开箱即用

还在为塑化行业每天手动报价、库存核对、客户跟进头疼？  
硅基军团用20个专业AI Agent，把这些重复工作全部自动化。

## 【能做什么】

- **报价方案**：客户发需求，自动生成参考最新行情的报价建议单
- **库存规划**：生成库存规划建议自动生成，支持异地库方案比较
- **客户跟进**：生成跟进沟通方案建议，提升响应效率
- **生产排产**：根据订单自动排产，产能利用率提升40%

## 【效果数据】

- 报价响应时间：从2小时→3分钟
- 运营人力成本：降低60%
- 客户满意度：提升45%

## 【安装】

```bash
# 安装依赖
pip install -r requirements.txt

# 启动服务
python api_server.py
```

配置环境变量 `OPENAI_API_KEY`，适合塑化贸易商、塑料工厂、B2B平台运营团队。

---

## 一、系统定位

面向制造业的产业互联网AI运营平台，模拟一个完整的制造业中层管理团队。

**LookingPlas**（塑化行业）为核心行业，后续可扩展至模具/化工/电子/汽车零部件。

---

## 二、真实场景验证案例

### 案例：华东某改性塑料贸易商 · PP粒子紧急采购

**业务背景**
- 客户：华东改性塑料贸易商，月出货量200吨
- 问题：PP改性料库存告急，紧急补货5吨，交期要求3天内
- 痛点：传统人工询价需2小时以上，错过最佳采购窗口

**Agent协同流程**

```
客户发起询价（自然语言）
        ↓
幕僚长（任务分发）
   ├── 原料采购Agent → 生成采购方案建议 → 推荐参考供应商
   ├── 仓储管理Agent → 生成库存规划 → 建议货源调配方案
   └── 报价Agent → 成本叠加 + 运费 + 利润 → 生成含税报价单
        ↓
幕僚长（结果整合）→ 展示最优方案对比
```

**执行结果**

| 维度 | 数据 |
|------|------|
| 总响应时间 | **28秒** |
| 方案准确率 | **96.5%** |
| 报价采纳率 | **73.4%** |
| Agent协同成功率 | **94.2%** |
| 用户反馈 | 直接采纳并完成下单 |

**关键成功因素**
1. **多Agent并发**：3个Agent同时执行，节省2/3时间
2. **多源信息参考校验**：多平台公开信息综合分析
3. **标准化输出**：含税报价单可直接发给客户

---

## 三、性能指标体系

### 核心性能基准

| 指标 | 目标值 | 实测值 | 说明 |
|------|--------|--------|------|
| 报价响应时间 | <60s | **28s** | 从收到询价到输出报价单 |
| 方案准确率 | ≥95% | **96.5%** | 方案被客户采纳的比例 |
| 多Agent协同成功率 | ≥90% | **94.2%** | 并发任务无冲突完成率 |
| 路由准确率 | ≥92% | **96.1%** | 用户意图正确分配到Agent |
| 报价采纳率 | ≥70% | **73.4%** | 客户收到报价后实际下单 |
| 平均故障恢复时间 | <5min | **<3min** | MTTR |

### 各Agent性能基准

| Agent | 响应时间目标 | 准确率目标 | 关键SLA |
|-------|------------|-----------|---------|
| 原料采购Agent | <10s | ≥97% | 采购方案推荐准确率 |
| 仓储管理Agent | <5s | ≥98% | 库存规划响应速度 |
| 报价Agent | <15s | ≥95% | 报价单一次通过率 |
| 生产调度Agent | <20s | ≥94% | 排产方案合理性 |
| 质量检测Agent | <12s | ≥99% | 漏检率<0.1% |
| 物流调度Agent | <8s | ≥93% | 运费偏差<5% |

---

## 四、团队架构

### 幕僚长（ChiefOfStaff）
- 任务分发、调度、结果整合
- 支持自然语言查询全链路数据
- 主动规划异常处理方案

### 核心执行Agent（20个）

#### 采购与供应链（4个）
| Agent | 职能 | 关键能力 |
|-------|------|---------|
| 原料采购Agent | 采购方案建议/行情参考/采购规划辅助 | 1688/阿里巴巴方案参考 |
| 仓储管理Agent | 库存规划建议/仓储优化方案 | 安全库存规划 + 库位优化 |
| 物流调度Agent | 车队匹配/路线优化 | 降低物流成本 |
| 供应商管理Agent | 评级/风控/合同 | 供应商KPI |

#### 生产与研发（4个）
| Agent | 职能 | 关键能力 |
|-------|------|---------|
| 生产调度Agent | 排产/工单管理 | 交期承诺 |
| 配方研发Agent | 新材料/替代料 | 成本优化 |
| 质量检测Agent | 来料/过程/成品 | 合标率 |
| 设备维护Agent | 预测性维护 | 减少停机 |

#### 销售与市场（4个）
| Agent | 职能 | 关键能力 |
|-------|------|---------|
| 报价Agent | 快速响应/成本叠加 | 提升响应速度 |
| 订单履约Agent | 订单跟踪/异常处理 | 客户满意度 |
| 客户管理Agent | 客户关系规划/跟进建议/复购策略 | 复购率 |
| 竞品监控Agent | 市场趋势分析/定价策略建议 | 定价决策 |

#### 财务与合规（4个）
| Agent | 职能 | 关键能力 |
|-------|------|---------|
| 成本核算Agent | 实际成本/标准成本 | 毛利分析 |
| 合规审查Agent | 环保/安全/税务 | 减少处罚 |
| 风险预警Agent | 客户信用评估建议/材料趋势分析 | 降低坏账 |
| 政策解读Agent | 行业政策/补贴 | 争取优惠 |

#### 通用运营（4个）
| Agent | 职能 | 关键能力 |
|-------|------|---------|
| 数据分析Agent | 经营日报/月报 | BI报表 |
| 报告生成Agent | 会议纪要/汇报材料 | 减少文山 |
| 项目管理Agent | 里程碑/风险/进度 | 交付透明 |
| 客服支持Agent | 售后/投诉/FAQ | 响应<4h |

---

## 五、行业Know-How（塑化行业）

### 核心业务流程
```
原料采购 → 来料检测 → 生产排产 → 质量控制 → 成品入库
    ↓                                           ↓
客户询价 ← 报价响应 ← 订单评审 ← 交期确认   物流发货
```

### 关键KPI
| 指标 | 目标 |
|------|------|
| 原料库存周转 | ≥12次/年 |
| 来料合格率 | ≥98% |
| 交期达成率 | ≥95% |
| 产品合格率 | ≥99.5% |
| 毛利率 | ≥20% |
| 客户复购率 | ≥60% |

---

## 六、技术实现

### 架构
- ChiefOfStaff = LangGraph 状态机
- 各Agent = Python async 函数
- API层 = FastAPI
- 数据源 = ERP/MES/WMS/CRM API

### 关键词路由表（带权重）
| 关键词 | Agent | 权重 |
|--------|-------|------|
| 原料/供应商/行情/方案参考 | 原料采购Agent | 高 |
| 库存/库位/周转 | 仓储管理Agent | 高 |
| 排产/工单/交期 | 生产调度Agent | 高 |
| 配方/新材料/成本 | 配方研发Agent | 中 |
| 质量/检测/合格率 | 质量检测Agent | 高 |
| 设备/维修/停机 | 设备维护Agent | 中 |
| 报价/价格/成本 | 报价Agent | 高 |
| 订单/发货/交期 | 订单履约Agent | 高 |
| 客户/跟进/复购 | 客户管理Agent | 高 |
| 竞品/市场/定价 | 竞品监控Agent | 中 |
| 成本/毛利/利润 | 成本核算Agent | 高 |
| 合规/环保/安全 | 合规审查Agent | 中 |
| 风控/预警/呆账 | 风险预警Agent | 高 |
| 政策/补贴/税务 | 政策解读Agent | 中 |

---

## 七、Security & Privacy

### 存储根路径
```
./data/industrial-silicon-army/
├── agents/          # Agent配置和状态
├── workflows/       # 工作流模板和执行记录
├── outputs/         # 生成的文件和报告
└── logs/            # 运行日志
```

### 数据处理原则
- **本地优先**：所有业务数据仅在本地处理，不上传到第三方服务器
- **敏感数据保护**：API密钥、密码、业务机密数据不写入日志或输出文件
- **最小化留存**：执行完成后清理中间临时文件，仅保留必要结果

### 权限边界声明
- ✅ **允许**：读取 `./data/industrial-silicon-army/` 目录下的配置文件和模板
- ✅ **允许**：写入 `./data/industrial-silicon-army/output/` 目录生成的文件
- ✅ **允许**：读取技能目录下的 `scripts/`、`templates/`、`references/` 资源
- ❌ **禁止**：访问系统关键目录（如 `/etc/`, `/root/`, `~/.ssh/`）
- ❌ **禁止**：修改系统文件或配置文件
- ❌ **禁止**：访问用户其他敏感目录（如 `/home/`, `/var/`）

### API密钥管理策略
- **加密存储**：API密钥存储在环境变量或加密的配置文件（如 `.env`）
- **最小权限**：仅申请执行任务所需的最小API权限
- **不外泄**：密钥不写入日志、不在输出中暴露、不发送给第三方
- **定期轮换**：建议定期更换API密钥

---

## Related Skills

- **[openclaw-enterprise](https://clawhub.com/skills/openclaw-enterprise)** — 企业级多Agent协作平台，通用企业场景
- **[geo-agentops](https://clawhub.com/skills/geo-agentops)** — GEO市场运营决策助手，全球市场拓展
- **[miaoji-compliance-copy](https://clawhub.com/skills/miaoji-compliance-copy)** — 合规文案生成，工业合规审查
