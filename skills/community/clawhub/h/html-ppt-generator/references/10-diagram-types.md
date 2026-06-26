# 10 · 业务图谱库（Architecture / Flow / Data / Hierarchy / Decision）

> ⚠️ **强制约束（来自 06-workflow.md）**
>
> **每份报告（5 页以上）必须满足：**
> - □ **至少 2 页使用业务图谱**（diagram-types/ 下的架构图/流程图/层级图/决策图等）
> - □ 规划表"业务图谱"列必须明确填写文件名（如 `hierarchy/pyramid.md`）
> - □ 生成 HTML 前必须验证：业务图谱使用页数 ≥ 2
>
> **违反以上任一约束 = 规划不通过，必须重新规划。**

> 覆盖汇报场景五大图谱族。所有模板已迁移至 `diagram-types/` 子目录，按图族分文件夹存放。
> 基础 SVG 数据图表（折线/柱/条/雷达等）→ 见 `05-content.md`（svg-extended/ 索引）。
> 若用户要求的图谱不在本库 → 执行末尾的【网络查询流程】。

---

## ⚡ 按需加载规则

> 每次生成页面时，**只读当前页面实际使用的 1–2 个图谱文件**。
> 不得预加载整个 diagram-types/ 目录。

### 📁 diagram-types/ 图谱索引

#### 一、架构图族 `diagram-types/architecture/`

| 文件 | 图谱类型 | 触发关键词 | 高度 |
|------|---------|-----------|------|
| `layered.md` | 分层架构图 | 系统分层、技术栈层次、前中后台分层、平台层级结构 | 220px |
| `c4-context.md` | C4 上下文图 | 系统边界、外部依赖、上下文视图、用户-系统关系 | 220px |
| `microservice.md` | 微服务拓扑图 | 微服务、网关、服务网格、API路由、容器编排、调用链 | 240px |
| `network-topology.md` | 网络拓扑图 | 网络拓扑、路由器交换机、防火墙、VPN、DMZ区域、物理网络、内外网隔离 | 240px |
| `data-architecture.md` | 数据架构图 | 数据架构、数据湖、数据仓库、ETL管道、数据流向、存储分层、数据平台 | 230px |
| `product-architecture.md` | 产品架构图 | 产品架构、功能模块、产品层级、业务域划分、用户端产品、产品全景 | 240px |
| `application-architecture.md` | 应用架构图 | 应用架构、前后端关系、中间件、外部服务集成、系统集成、应用全景图 | 240px |
| `deployment-architecture.md` | 部署架构图 | 部署架构、云环境、K8s集群、容器化部署、高可用方案、多机房、灾备 | 240px |
| `event-driven.md` | 事件驱动架构图 | 事件驱动、消息队列、Kafka、发布订阅、事件流、异步通信、MQ架构 | 230px |
| `security-architecture.md` | 安全架构图 | 安全架构、零信任、权限边界、安全域、身份认证、访问控制、纵深防御 | 240px |
| `domain-driven.md` | 领域模型图 (DDD) | DDD、限界上下文、聚合根、领域事件、领域服务、核心域支撑域 | 240px |
| `cloud-architecture.md` | 云架构图 | 云架构、AWS/Azure/GCP、云原生、多云、混合云、云服务组合、弹性扩展 | 240px |
| `tech-stack.md` | 技术栈全景图 | 技术栈、技术选型、框架组合、工具链、前后端技术、依赖关系、技术雷达 | 220px |

#### 二、流程图族 `diagram-types/flow/`

| 文件 | 图谱类型 | 触发关键词 | 高度 |
|------|---------|-----------|------|
| `swimlane.md` | 泳道图 | 跨部门流程、审批流转、角色协作、服务交互 | 200px |
| `funnel.md` | 漏斗图 | 转化率、用户路径、销售漏斗、流失分析 | 160–200px |
| `user-journey.md` | 用户旅程图 | 用户体验、触点、情绪曲线、痛点高光、服务蓝图 | 220px |
| `cycle.md` | 循环图/飞轮模型 | 飞轮效应、PDCA、闭环增长、正反馈循环、业务循环 | 240px |
| `value-chain.md` | 价值链分析 | 波特价值链、主要活动、支持活动、成本结构、竞争优势 | 220px |

#### 三、进阶数据图族 `diagram-types/data/`

| 文件 | 图谱类型 | 触发关键词 | 高度 |
|------|---------|-----------|------|
| `sankey.md` | Sankey 桑基图 | 流量流向、预算分配、来源去向、能源流 | 200px |
| `bullet.md` | Bullet 子弹图 | KPI 目标对比、实际 vs 计划、多指标达成 | 26px/条 |
| `treemap.md` | Treemap 树图 | 市场份额、资产组合、分类占比、面积=价值 | 180px |
| `comparison-table.md` | 特性对比表 | 方案对比、产品比较、竞品分析、选型评分、勾叉表 | 自适应 |
| `chord.md` | 弦图/关系矩阵 | 多方关系强度、交叉流量、部门协作频率、双向依赖 | 260px |

#### 四、层级分析图族 `diagram-types/hierarchy/`

| 文件 | 图谱类型 | 触发关键词 | 高度 |
|------|---------|-----------|------|
| `pyramid.md` | 金字塔图 | 组织层级、需求层次、战略优先级、依赖结构 | 200px |
| `matrix-2x2.md` | 2×2 矩阵 | 优先级矩阵、竞争定位、四象限分析 | 280px |
| `onion.md` | 同心圆/洋葱图 | 价值圈层、核心-外围、品牌感知、技术依赖圈 | 220px |
| `fishbone.md` | 鱼骨图/石川图 | 原因分析、根因排查、6M框架、问题溯源、因果分析 | 220px |
| `venn.md` | 韦恩图 | 集合关系、交集差集、共同点、业务重叠、需求对比 | 200–220px |
| `iceberg.md` | 冰山模型 | 显性隐性、表象根因、水面上下、冰山效应、深层分析 | 240px |

#### 五、决策图族 `diagram-types/decision/`

| 文件 | 图谱类型 | 触发关键词 | 高度 |
|------|---------|-----------|------|
| `risk-matrix.md` | 风险矩阵 | 风险评估、安全威胁、5×5热力格、项目风险 | 240px |
| `raci.md` | RACI 矩阵 | 任务分配、职责边界、角色矩阵、R/A/C/I | 自适应 |
| `swot.md` | SWOT 分析 | SWOT、优势劣势机会威胁、内外部因素、战略分析 | 280px |
| `pest.md` | PEST/PESTLE 分析 | PEST、PESTLE、宏观环境、政治经济社会技术、外部扫描 | 260px |

---

## 快速选型表

| 用户说了什么 | 图谱族 | 首选文件 |
|------------|--------|---------|
| 系统分层、技术栈层次、前中后台分层 | 架构图 | `architecture/layered.md` |
| 微服务、网关、服务调用链、容器编排 | 架构图 | `architecture/microservice.md` |
| 系统边界、外部依赖、上下文视图 | 架构图 | `architecture/c4-context.md` |
| 网络拓扑、路由交换机、防火墙、内外网隔离 | 架构图 | `architecture/network-topology.md` |
| 数据架构、数据湖仓、ETL、数据流向、数据平台 | 架构图 | `architecture/data-architecture.md` |
| 产品架构、功能模块全景、业务域划分 | 架构图 | `architecture/product-architecture.md` |
| 应用架构、前后端集成、中间件、应用全景图 | 架构图 | `architecture/application-architecture.md` |
| 部署架构、云环境、K8s集群、高可用、灾备 | 架构图 | `architecture/deployment-architecture.md` |
| 消息队列、事件驱动、Kafka、发布订阅、MQ | 架构图 | `architecture/event-driven.md` |
| 安全架构、零信任、权限边界、纵深防御 | 架构图 | `architecture/security-architecture.md` |
| DDD、限界上下文、聚合根、领域模型、核心域 | 架构图 | `architecture/domain-driven.md` |
| 云架构、AWS/Azure/GCP、多云、混合云、云原生 | 架构图 | `architecture/cloud-architecture.md` |
| 技术栈、技术选型、框架组合、工具链、技术雷达 | 架构图 | `architecture/tech-stack.md` |
| 跨部门流程、审批、角色交接 | 流程图 | `flow/swimlane.md` |
| 转化率、用户路径、漏斗 | 流程图 | `flow/funnel.md` |
| 用户旅程、体验触点、情绪曲线 | 流程图 | `flow/user-journey.md` |
| 飞轮效应、PDCA、业务闭环循环 | 流程图 | `flow/cycle.md` |
| 波特价值链、活动分解、成本结构 | 流程图 | `flow/value-chain.md` |
| 流量/预算流向、来源去向 | 进阶数据图 | `data/sankey.md` |
| KPI 目标对比、达成率 | 进阶数据图 | `data/bullet.md` |
| 市场占比、资产组合、面积图 | 进阶数据图 | `data/treemap.md` |
| 方案/产品/竞品对比、选型评分 | 进阶数据图 | `data/comparison-table.md` |
| 部门协作关系、双向依赖强度 | 进阶数据图 | `data/chord.md` |
| 组织层级、战略优先级 | 层级分析 | `hierarchy/pyramid.md` |
| 优先级矩阵、竞争定位四象限 | 层级分析 | `hierarchy/matrix-2x2.md` |
| 价值层次、核心-外围圈层 | 层级分析 | `hierarchy/onion.md` |
| 鱼骨图、原因分析、根因排查 | 层级分析 | `hierarchy/fishbone.md` |
| 集合关系、交集、业务重叠 | 层级分析 | `hierarchy/venn.md` |
| 冰山模型、显性隐性、深层根因 | 层级分析 | `hierarchy/iceberg.md` |
| 风险评估、安全威胁优先级 | 决策图 | `decision/risk-matrix.md` |
| 任务分配、职责边界 | 决策图 | `decision/raci.md` |
| SWOT、优势劣势机会威胁 | 决策图 | `decision/swot.md` |
| PEST/PESTLE、宏观环境扫描 | 决策图 | `decision/pest.md` |

---

## 🌐 网络查询流程（当图谱不在以上库中时）

### 触发条件

用户描述的图谱类型**不在上述库中**，或描述模糊需要确认最佳视觉形式：

```
触发词举例：
  "画个 XXX 图"（从未见过的图名）
  "类似 McKinsey 那种矩阵"（需要查具体结构）
  "商业模式画布"（需查标准画法）
  "VRIN 框架"（需查字段和布局）
```

### 查询步骤

```
Step 1 · 识别图谱名称
  从用户描述中提取图谱关键词
  示例："安索夫矩阵" → 查询词 = "Ansoff matrix SVG structure"

Step 2 · WebSearch
  查询模板："{图谱名} diagram visual structure SVG"
  或中文："{图谱名} 画法 结构"
  目标：找到该图谱的标准组成元素和布局规则

Step 3 · 提取 SVG 构建规则
  从搜索结果中识别：
  - 有哪些基本形状（方框/圆/菱形/梯形/箭头）
  - 布局方向（左→右 / 上→下 / 环形 / 放射形）
  - 必填的标注（轴标签/象限名/流向说明）

Step 4 · 用本库的 SVG 公式套入
  套用最相近的已知图谱 SVG 结构作为基础
  修改形状/颜色/标签 → 生成目标图谱
```

### 常见需查询图谱参考词

| 用户描述 | 建议搜索词 / 状态 |
|---------|-----------|
| 商业模式画布 | business model canvas layout |
| 安索夫矩阵 | Ansoff matrix growth strategy diagram |
| VRIN/VRIO 框架 | VRIN framework table structure |
| 波士顿矩阵 (BCG) | → 可用 `hierarchy/matrix-2x2.md` 改造 |
| 飞轮模型 | → 已在 `flow/cycle.md` |
| 冰山模型 | → 已在 `hierarchy/iceberg.md` |
| 价值链 | → 已在 `flow/value-chain.md` |
| PESTLE/PEST | → 已在 `decision/pest.md` |
| 鱼骨图/石川图 | → 已在 `hierarchy/fishbone.md` |
| SWOT 分析 | → 已在 `decision/swot.md` |
| 韦恩图 | → 已在 `hierarchy/venn.md` |
| 雷达/蜘蛛网 | → 已在 `svg-extended/radar.md` |
| 甘特图 | → 已在 `svg-extended/gantt.md` |
