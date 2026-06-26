> **Copyright (c) 2026 IDC. All Rights Reserved. Licensed under CC-BY-SA-4.0.** See `IDCcopyright.md` for details.

# Supplier Direction Mapping — MarketGlance Reference

Complete mapping from COMPASS dimensions to IDC MarketGlance supplier types. Use this reference during Step 6.

---

## MarketGlance Three Supplier Types

### 1. Industry Scenario Vendors (行业场景厂商)

**Coverage:** 11 vertical sectors — Government, Finance, Industrial Manufacturing, Transportation, Internet, Retail, Smart Devices, Energy, Healthcare, Automotive, Embodied AI.

**Core advantage:** Deep accumulation of industry-specific data formats, business processes, regulatory requirements, and industry semantics.

**Best for:** Scenarios where industry Know-How density is high and domain expertise is non-negotiable.

### 2. Enterprise Scenario Vendors (企业场景厂商)

**Coverage:** 14 functional areas — Operations, Software Development, Procurement, Finance, Marketing & Sales, HR, Customer Service/Conversational AI, Supply Chain, Legal, Data Analytics, Code Generation, APA (Agentic Process Automation), Digital Humans, Security.

**Core advantage:** Deep understanding of horizontal functional processes, closer to actual enterprise operational chains.

**Best for:** Function-focused scenarios where process standardization across industries is possible.

### 3. Agent Development Platform Vendors (智能体开发平台厂商)

**Coverage:** Full lifecycle — Build, Orchestrate, Test, Deploy, Operate, Govern.

**Core advantage:** Provides the platform foundation for Agent construction, enabling enterprises to connect existing systems, build governance infrastructure, and address long-tail scenarios.

**Best for:** Cross-system orchestration, custom Agent building, governance backbone, and scaling beyond initial pilots.

---

## COMPASS Dimension → Supplier Mapping

### Perception

| Scenario type | Recommended supplier | Rationale |
|--------------|---------------------|-----------|
| Industry-specific data (medical imaging, financial instruments, industrial inspection) | **Industry Scenario Vendors** | Requires deep domain data understanding |
| General document parsing, multi-language email processing | **Enterprise Scenario Vendors** (Data Analytics / Operations) or **Platform Vendors** with multimodal capabilities | Cross-industry applicability |
| Multi-format input normalization at scale | **Platform Vendors** + **Enterprise Scenario Vendors** (APA) | Platform for flexibility, APA for process integration |

### Analysis

| Scenario type | Recommended supplier | Rationale |
|--------------|---------------------|-----------|
| Industry Know-How intensive (financial risk control, supply chain scheduling) | **Industry Scenario Vendors** | Domain rules are critical |
| Function-focused (financial analysis, marketing attribution, HR forecasting) | **Enterprise Scenario Vendors** (corresponding functional area) | Process standardization exists |
| Flexible self-built analysis workflows | **Platform Vendors** | Customization requirements high |

### Orchestration

| Scenario type | Recommended supplier | Rationale |
|--------------|---------------------|-----------|
| Cross-system dynamic routing | **Platform Vendors** (primary) | Core platform capability |
| Single clear business chain (order → production → logistics → settlement) | **Industry/Enterprise Scenario Vendors** with mature chain solutions | Proven templates available |
| Upgrading existing process automation | **Enterprise Scenario Vendors** (APA/BPM category) | Natural evolution from RPA/BPM |

### Monitoring

| Scenario type | Recommended supplier | Rationale |
|--------------|---------------------|-----------|
| Regulated industries (financial trading, industrial equipment, energy dispatch) | **Industry Scenario Vendors** | Compliance requirements are industry-specific |
| General security and IT operations | **Enterprise Scenario Vendors** (Security) | Standardized patterns |
| Custom monitoring Agent connecting multiple alert sources | **Platform Vendors** | Integration flexibility needed |

### Collaboration

| Scenario type | Recommended supplier | Rationale |
|--------------|---------------------|-----------|
| Internal OA, IM, project coordination | **Enterprise Scenario Vendors** (Operations) | Standard enterprise patterns |
| Cross-organization, cross-industry collaboration | **Platform Vendors** (custom build) | Unique requirements |
| External customer communication and after-sales | **Enterprise Scenario Vendors** (Customer Service / Conversational AI) | Specialized capability |

### Sedimentation

| Scenario type | Recommended supplier | Rationale |
|--------------|---------------------|-----------|
| Decision trace, knowledge base infrastructure | **Platform Vendors** | Technical foundation |
| Industry Know-How encoding and preservation | **Industry Scenario Vendors** (essential complement) | Domain expertise required |

### Scalability

| Scenario type | Recommended supplier | Rationale |
|--------------|---------------------|-----------|
| Core elastic scaling capability | **Platform Vendors** (especially cloud-native) | Infrastructure foundation |
| Specific peak scenarios (e.g., e-commerce customer service surge) | **Enterprise Scenario Vendors** (mature solutions) | Proven at scale |

---

## Combination Patterns

Most enterprises will ultimately form a **multi-type supplier portfolio**. Default to combination recommendations rather than single-vendor solutions.

### Pattern A: Platform + Industry Depth

```
Platform Vendor (orchestration backbone, governance, scaling)
    + Industry Scenario Vendor (domain semantics, regulatory compliance)
    + Enterprise Scenario Vendor (functional depth for specific processes)
```

**Best for:** Regulated industries (finance, healthcare, energy) with high domain specificity.

### Pattern B: Platform + Functional Depth

```
Platform Vendor (cross-system orchestration, custom Agents)
    + Enterprise Scenario Vendors (APA, Customer Service, Operations)
```

**Best for:** Cross-functional enterprises needing horizontal process automation.

### Pattern C: Scenario-First, Platform-Later

```
Phase 1: Enterprise Scenario Vendor (proven solution for pilot)
Phase 2: Platform Vendor (governance backbone for scaling)
Phase 3: Industry Scenario Vendor (domain depth for competitive advantage)
```

**Best for:** Enterprises early in their Agent journey, prioritizing quick wins.

---

## Product Form Combinations

Supplier matching is not a single choice. The final portfolio typically includes:

| Product form | Role | Typical supplier type |
|-------------|------|----------------------|
| In-app embedded Agents | Enhance existing systems | Enterprise Scenario Vendors |
| Low-code platform-built Agents | Custom scenarios | Platform Vendors |
| Standalone Agent products | Specialized functions | Enterprise/Industry Scenario Vendors |
| Custom-built Agents | Unique requirements | Platform Vendors + internal development |

**Phase guidance:**
- **Validation phase:** Lean toward scenario vendors' proven solutions
- **Scaling phase:** Shift toward platform vendors for orchestration and governance
- **Cross-scenario coordination:** Requires platform capability as foundation
- **Industry Know-How intensive:** Industry scenario vendors remain essential throughout

---

## MarketGlance Sub-Category Quick Reference

### Industry Agents (11 verticals)

| 子段 | 典型场景 |
|------|---------|
| 政府 | 政务办事、公共数据治理、城市运行监控 |
| 金融 | 风控、反欺诈、财富管理、理赔核保 |
| 工业制造 | 质检、排产、设备预测性维护、BOM协同 |
| 交通 | 出行调度、路网监控、车路协同 |
| 互联网 | 内容审核、推荐、搜索、运营分析 |
| 零售 | 门店运营、供应链协同、客户旅程运营 |
| 智能终端 | 端侧对话、端云协同、设备个性化 |
| 能源 | 电网调度、设备预警、能耗优化 |
| 医疗 | 临床辅助、病历结构化、医学影像 |
| 汽车 | 座舱交互、智能驾驶辅助、售后服务 |
| 具身智能 | 机器人感知与操作、场景任务规划 |

### Enterprise Agents (14 functional areas)

| 子段 | 典型场景 |
|------|---------|
| 运营 | OA、IM、协同办公流程 |
| 软件开发 | 需求拆解、代码生成、测试 |
| 采购 | 供应商管理、比价、对账 |
| 财务 | 核算、报销、风险检查 |
| 营销与销售 | 线索运营、归因、内容生产 |
| HR | 招聘、培训、薪酬、员工服务 |
| 客户服务/对话式AI | 售前售后、客服扩容 |
| 供应链 | 计划、协同、履约 |
| 法务 | 合同审查、合规、电子签 |
| 数据分析 | 取数、BI、报表、洞察 |
| 代码生成 | 面向开发者的辅助编码 |
| APA | 跨系统流程自动化，从RPA升级到Agentic |
| 数字人 | 品牌营销、直播、员工服务形象 |
| 安全智能体 | SOC、威胁检测、安全运营 |

### Agent Development Platforms

覆盖开发编排、测试评估、运行托管、运维治理、闭环迭代五大能力模块，在方案里承担跨系统连接、治理底座、长尾场景托底的角色。

---

## Quick Reference Table: COMPASS → Supplier → MarketGlance Sub-Category

| COMPASS维度 | 所属约束层级 | 典型业务场景 | 优先关注的供应商方向 | 对应 MarketGlance 子段 |
|-------------|-------------|-------------|---------------------|----------------------|
| **P** Perception | 第一层（信息输入） | 票据识别、合同提取、多渠道订单归集 | 行业场景厂商（行业特有数据）；企业场景厂商-APA/数据分析 | 行业：金融、医疗、工业制造、能源；企业：APA、数据分析、运营 |
| **A** Analysis | 第二层（信息处理） | 多供应商比价、库存优化、信用评估 | 行业场景厂商（行业规则密集）；企业场景厂商（对应职能方向）；智能体开发平台厂商 | 行业：金融、工业制造；企业：数据分析、财务、营销与销售、HR；开发平台 |
| **O** Orchestration | 第二层（信息处理） | 订单全流程、采购协同、合同审批流转 | 智能体开发平台厂商；APA厂商；行业/企业场景厂商（成熟链路） | 企业：APA、运营、采购、供应链；开发平台 |
| **M** Monitoring | 第二层（信息处理） | 交易异常监控、设备预警、合规偏差检测 | 行业场景厂商（政务、金融等监管密集行业）；企业场景厂商-安全方向 | 行业：金融、工业制造、能源、政府；企业：安全智能体 |
| **C** Collaboration | 第二层（信息处理） | 跨部门项目协同、客户沟通、售后协调 | 企业场景厂商-运营/客服方向；智能体开发平台厂商 | 企业：运营、客户服务/对话式AI、数字人；开发平台 |
| **S** Sedimentation | 第三层（信息资产化） | 经验固化、知识库建设、最佳实践沉淀 | 开发平台厂商（技术底座）；行业场景厂商（行业Know-How编码） | 开发平台；对应行业子段 |
| **S** Scalability | 第三层（信息资产化） | 高峰期弹性扩容、业务规模化复制 | 智能体开发平台厂商 | 开发平台；企业：客户服务/对话式AI、运营 |

> 厂商介绍与产品能力以厂商官网为准，厂商产品与案例评估参考IDC MarketGlance分类及相关厂商产品评估报告。具体厂商清单参考IDC Agent MarketGlance最新季度发布：
> - 中国AI Agent行业应用与开发平台市场概览：[CHC54462426](https://my.idc.com/getdoc.jsp?containerId=CHC54462426&pageType=PRINTFRIENDLY)
> - 中国企业级AI Agent应用市场概览：[CHC54371726](https://my.idc.com/getdoc.jsp?containerId=CHC54371726&pageType=PRINTFRIENDLY)

---

## Vendor Directories (load on demand)

When the user asks for specific vendor names after diagnosis, load the corresponding vendor directory file:

| Directory file | Coverage | When to load |
|---------------|----------|-------------|
| `references/vendor-industry.md` | 11 industry vertical sub-categories with complete vendor lists | User asks for industry-specific vendors |
| `references/vendor-enterprise.md` | 14 enterprise functional sub-categories with complete vendor lists | User asks for function-specific vendors |
| `references/vendor-platform.md` | Agent development platform vendors with complete list | User asks for platform vendors |

**Loading rules:**
1. Only load vendor directories AFTER the diagnosis is complete (Step 6+)
2. Provide the full candidate list for the relevant sub-category; do NOT filter or rank
3. If the user's scenario spans multiple sub-categories, load each relevant file and list separately
4. Remind the user that vendor evaluation should reference IDC MarketGlance vendor product evaluation reports

**Data source:** Based on IDC MarketGlance "中国AI Agent行业应用与开发平台市场概览" and "中国企业级AI Agent应用市场概览". Updated quarterly.
