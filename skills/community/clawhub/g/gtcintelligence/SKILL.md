# GTC 2026 Information Collection Plan (ICP) v2

> 版本：v2 | 更新：2026-03-01 17:30 UTC
> 变化：整合用户情报（10条预发布信号）+ 媒体报道（The Register, CES 2026, GTC 2025）
> 基于：PIR_v1.md (10条PIR) + session_universe.md v1 + 新增情报层
> 团队：3人现场（A/B/C） + 5人远程监控

---

## ⚡ 情报更新摘要（v2 新增，2026-03-01）

以下为 GTC 前已掌握的非公开 / 半公开信号，需现场**验证或否证**：

| # | 信号内容 | 可信度 | 对应PIR | 验证优先级 |
|---|---------|--------|---------|-----------|
| S1 | LPU：16x/32x per compute tray，256x per rack；端侧chat或云侧长上下文推理待定；目标2028量产 | 中高 | PIR-01/04 | ★★★ |
| S2 | Feynman独占TSMC 1.6nm；25% IO die + EMIB packaging给Intel做 | 高（GTC25已公布代号，细节待确认）| PIR-01 | ★★★ |
| S3 | VR200 NVL72平台带HBM4（与CES规格一致，已半公开）| 已确认 | PIR-01/02 | ★ 验证细节 |
| S4 | 2027年scale-up CPO；2026年先走scale-out给Spectrum-X和InfiniBand | 高（GTC25已宣布CPO路线图）| PIR-08 | ★★ |
| S5 | NVL576带448G SerDes；中板使用PTFE base和Q-glass M9材料 | 中（未见公开报道）| PIR-03/08 | ★★★ |
| S6 | Vera：唯一支持LPDDR5x数据中心CPU，用于post-train，解决Amdahl's Law | 已确认（CES规格） | PIR-01 | ★ 追问post-train用例 |
| S7 | GPU+Stacked Memory方案；多节点设计对接Storage Disaggregation，缓解KV Cache | 中高 | PIR-05/07 | ★★★ |
| S8 | 正交背板展出（更真实版本）；量产时间线：CCL 12月→PCB 1月(2个月)→测试3个月→2026年中 | 中 | PIR-03 | ★★ |
| S9 | BF5、NVL8、QC等新产品发布 | 中 | PIR-09/05 | ★★ |
| S10 | 软件/应用/生态：Physical AI, Robotics, Digital Twin, 垂直领域合作 | 高概率 | PIR-07/10 | ★ 跟进 |

---

## 采集原则

1. **每条 PIR 至少两条独立采集路径**（避免单点信息依赖）
2. **三层分类**：Layer A 必采 / Layer B 高ROI / Layer C 机会型
3. **证据等级**：一手演讲 > 官方文档 > 展台/1:1 > 二手报道
4. **禁止单一数据点做结论**：任何关键结论需 2+ 独立来源
5. **v2新增**：已知信号优先「验证/否证」，而非重新发现

---

## PIR-01：Vera Rubin 平台全貌与 Feynman 路线（满分22 · 最高优先）

### 已知基础（不用采集，用于构建问题）
- **VR200 NVL72**（已确认，CES 2026）：72 Rubin GPU / 36 Vera CPU / 20.7TB HBM4 / 1,580 TB/s带宽 / NVLink6 260TB/s
- **Vera CPU**（已确认）：88 Olympus Arm核 / 1.5TB LPDDR5x / 1.8TB/s NVLink-C2C
- **Rubin Ultra NVL576**（GTC 2025宣布）：576 GPU dies / 4 dies per package / 1TB HBM4e / 600kW / late 2027
- **Feynman**（GTC 2025宣布代号）：2028年 GPU 架构
- **Samsung/Micron HBM4**（2026-02确认）：开始出货，Samsung 11.7-13Gbps / 3.3TB/s每stack

### 新增采集目标（v2）

| 路径 | 来源 | Session | 层级 | 负责 | 目标证据 |
|------|------|---------|------|------|---------|
| P01-A | Jensen Keynote | INF-001 | A-必采 | 现场A | Feynman规格公告：TSMC 1.6nm独占？Intel EMIB 25%分成？ |
| P01-B | Rubin架构深度 | INF-002 | A-必采 | 现场A | NVL72 vs NVL144 CPX 实际部署建议 |
| P01-C | LPU深度session | INF-LPU | A-必采 | 现场A | LPU tray配置（16x/32x/256x）+ 端侧vs云侧定位 |
| P01-D | Vera post-train session | INF-Vera | B-高ROI | 现场B | LPDDR5x post-train延迟优势量化 / Amdahl's Law单线程证据 |
| P01-E | 供应链合作伙伴 | 展台/INF-006 | B-高ROI | 远程 | Intel EMIB合作细节 |

### 关键问题（现场提问清单）

**关于Feynman：**
1. TSMC 1.6nm独占协议是排他性的吗？期限多久？AMD是否同样受影响？
2. Intel EMIB 25% IO die合作——这是NVIDIA第一次用Intel Foundry做生产部件吗？
3. Feynman的架构演进：是否将Groq LPU数据流设计整合进主GPU架构？
4. Feynman 2028量产——是否意味着Rubin Ultra（2027）和Feynman之间没有其他代际？

**关于LPU集成（S1/S2）：**
5. LPU在当前Rubin体系里是独立tray还是集成到GPU die旁边（"GPU/LPU + 3D SRAM + HBM"形态）？
6. LPU解决的是prefill（5% compute-bound）还是decode（95% memory-bound）？端侧和云侧有不同答案吗？
7. CUDA软件层如何调度LPU？是作为prefill加速（类似CPX替代）还是speculative decoding？
8. 热设计：LPU靠近GPU的3D堆叠方案对GPU主频的影响已量化了吗？

**关于Vera CPU：**
9. Vera作为"唯一支持LPDDR5x的数据中心CPU"——post-training场景下相比x86节省了多少成本/功耗？
10. 在单线程性能（Amdahl's Law瓶颈）上，Vera的Olympus核心相比Grace有多大提升？

### 误判防范
- ⚠️ 区分「Feynman路线图公告」vs「Feynman量产时间表」
- ⚠️ LPU：区分「软件层集成（CUDA调度）」vs「硬件层集成（3D堆叠）」，后者是S1所指
- ⚠️ 「TSMC 1.6nm独占」的granularity：是整张wafer exclusive还是产能优先权？
- ⚠️ LPDDR5x的1.5TB——注意是NUMA架构，实际访问延迟需确认

---

## PIR-02：Blackwell Ultra 产能与真实性能（满分19）

### 已知基础
- GB300 NVL72已出货，576GB HBM3e per superchip
- Rubin VR200预计2026 H2，HBM4已从Samsung/Micron开始出货

### 采集路径

| 路径 | 来源 | Session | 层级 | 负责 | 目标证据 |
|------|------|---------|------|------|---------|
| P02-A | Blackwell Ultra session | INF-003 | A-必采 | 现场A | 当前交货等待时间 + 产能是否爬坡完成 |
| P02-B | 超大规模客户案例 | INF-CLD | A-必采 | 现场B/C | 实际交付时间线 vs 承诺 |
| P02-C | OEM展台 | Dell/HPE/ODM | B-高ROI | 现场B | GB300配额状态 |
| P02-D | Connect With Experts | NVDA Product | B-高ROI | 现场A | GB300→VR200过渡策略 |

### 关键问题
1. GB300 NVL72现在的交货等待时间还有多长？是否已正常化？
2. Rubin NVL72 H2量产——是Q2、Q3还是Q4，哪些客户会最先拿到？
3. 训练和推理工作负载下，GB300 vs H200的实际性能差距（非NVIDIA自测）？
4. NVL72里实际NVLink带宽稳定性——有生产环境数据吗？
5. Rubin CPX（GDDR7 prefill加速）——什么时候进生产，哪些workload优先？

---

## PIR-03：AI Factory 规模经济、TCO 与硬件基础设施（满分17）

### 已知基础（v2新增）
- **正交背板（S8）**：CCL 12月下单(1个月) → PCB制造(2个月) → 综合测试(3个月) → **预计2026年中量产**
- **NVL576 SerDes（S5）**：448G SerDes；中板材料：PTFE base + Q-glass M9
- **CPO时间线**：scale-out（Spectrum-X / InfiniBand）2026年；scale-up CPO 2027年
- 功耗：NVL72不会"双倍于"Blackwell Ultra，但具体数字未公布

### 采集路径

| 路径 | 来源 | Session | 层级 | 负责 | 目标证据 |
|------|------|---------|------|------|---------|
| P03-A | AI Factory参考架构 | INF-004 | A-必采 | 现场B | 官方参考架构含正交背板设计 |
| P03-B | NVL576电力/冷却 | INF-005 | A-必采 | 远程 | VR200 NVL72功耗数字 / 600kW NVL576路线图 |
| P03-C | 正交背板展台 | 展台 | B-高ROI | 现场C | **验证S8**：是否已有可交付样品？量产时间是否2026年中？ |
| P03-D | 材料/PCB session | 合作伙伴 | B-高ROI | 现场C | **验证S5**：PTFE+Q-glass M9是否在NVL576中板量产 |

### 关键问题
1. NVL576 SerDes：448G是否已进入量产设计，还是仍在验证阶段？
2. Q-glass M9中板材料——使用这种材料的具体原因（信号完整性？热管理？）
3. 正交背板展品——这是工程样品还是接近量产状态？CCL/PCB/测试时间线与S8一致吗？
4. NVL72满载功耗是多少kW？液冷是否强制要求？
5. 5年TCO：1000 GPU AI工厂中，液冷 vs 风冷的成本差是多少？

---

## PIR-04：NVIDIA Dynamo + LPU 集成生产成熟度（满分20 · v2上调）

### 已知基础（v2大幅扩充）
- **Groq $20B收购**（2025-12）：NVIDIA获Groq LPU IP许可 + 核心团队（Ross/Madra加入NVDA）
- **Groq核心价值**：Data Flow架构（汇编线/流水线式推理），消除Von Neumann架构的load-store瓶颈
- **LPU定位**：每颗230MB SRAM，574颗运行Llama 70B；Groq保留独立运营
- **Rubin CPX**（2025-09宣布）：GDDR7 prefill加速，30 PFLOPS NVFP4，128GB GDDR7；解决disaggregated inference prefill phase
- **LPU架构演进（S1/S2）**：Feynman可能整合LPU理念到GPU，以解决"5% vs 95%负载优化"的矛盾

### 采集路径

| 路径 | 来源 | Session | 层级 | 负责 | 目标证据 |
|------|------|---------|------|------|---------|
| P04-A | Dynamo生产session | AGT-001 | A-必采 | 现场B | 生产客户名单 + 稳定性数据 |
| P04-B | LPU集成专题 | AGT-LPU | A-必采 | 现场B | **验证S1**：LPU tray形态 / CUDA调度 / 端侧vs云侧 |
| P04-C | Groq团队session | 若有独立session | A-必采 | 现场A/B | Groq Data Flow如何融入CUDA生态 |
| P04-D | Dynamo vs vLLM | AGT-005 | B-高ROI | 远程 | benchmark方法论 + 数字 |
| P04-E | KV Cache分层架构 | AGT-007 | B-高ROI | 远程 | CXL/Storage层KV Cache卸载架构 |

### 关键问题
1. LPU在GTC 2026是正式产品发布，还是「demo + 路线图」？
2. LPU的SRAM（230MB/颗）在新架构里是否扩容？还是通过3D堆叠接入HBM？
3. Data Flow架构（Groq核心IP）集成到CUDA层的技术路径——是新的CUDA kernel API，还是硬件透明？
4. Rubin CPX（GDDR7 prefill）和LPU的关系：LPU会替代CPX的角色吗？
5. KV Cache GPU+Stacked Memory方案（S7）——这是NVIDIA原生支持还是第三方（Enfabrica/Pliops）？
6. LPU散热：在GPU旁边3D堆叠后，GPU主频是否受限？热设计方案？
7. Dynamo在multi-node场景（>1000 GPU）的实际可靠性数据？

### 误判防范
- ⚠️ 「LPU集成」有两个层次：①软件层（CUDA调度LPU farm）②硬件层（GPU die旁3D堆叠）— S1指后者，但Feynman之前可能都只是前者
- ⚠️ Groq的SRAM优势不是SRAM本身，是Data Flow架构——区分两者

---

## PIR-05：ICMS / BlueField-4/5 实际部署验证（满分17）

### 已知基础（v2新增BF5）
- BF4已发布，DOCA生态，ICMS（Intelligent Cloud Management Service）声称5× TPS提升
- **BF5（S9）**：GTC 2026预计发布，规格未知

### 采集路径

| 路径 | 来源 | Session | 层级 | 负责 | 目标证据 |
|------|------|---------|------|------|---------|
| P05-A | ICMS生产session | AGT-002 | A-必采 | 现场C | 独立验证的生产数据（5×TPS的条件） |
| P05-B | **BF5发布session** | INF-BF5 | A-必采 | 现场C | **验证S9**：BF5规格、定价、与BF4差异 |
| P05-C | 存储合作伙伴 | 存储session | B-高ROI | 远程 | G3.5层：WEKA/Pure/NetApp/DDN集成状态 |
| P05-D | KV Cache存储分层 | AGT-007 | B-高ROI | 远程 | GPU+Stacked Memory接到Storage Disaggregation |

### 关键问题
1. BF5发布规格：带宽、功耗、与BF4相比核心提升在哪里？
2. ICMS的5× TPS——测试条件：什么模型，什么批量大小，什么负载模式？
3. GPU + Stacked Memory（S7）：这个"Stacked Memory"是指GPU die上的3D SRAM，还是外挂的CXL内存池？
4. Storage Disaggregation方案里，BF5/ICMS是否提供NVMe-over-Fabrics的原生加速？
5. BF4 → BF5：ICMS已有部署的客户，是否需要硬件替换还是固件升级？

---

## PIR-06：NIM 企业采用实况（满分16）

### 采集路径

| 路径 | 来源 | Session | 层级 | 负责 | 目标证据 |
|------|------|---------|------|------|---------|
| P06-A | NIM企业案例 | AGT-003 | A-必采 | 现场C | 部署规模 + 定价结构 |
| P06-B | NIM微服务目录 | AGT-008 | A-必采 | 远程 | GA/Beta清单 + 新增模型 |
| P06-C | ISV集成 | ISV session/展台 | B-高ROI | 现场C | SAP/ServiceNow/Salesforce深度 |
| P06-D | 私有化NIM部署 | 技术session | B-高ROI | 远程 | on-prem最小硬件要求 |

### 关键问题
1. NIM私有化部署最小硬件要求（GPU型号/数量）？
2. NIM按调用量计费选项是否已GA？
3. 哪些ISV已内嵌NIM API到生产产品（不是beta集成）？
4. 企业pilot → 生产平均时间？主要卡点是什么？

---

## PIR-07：Agentic 工作负载基础设施需求（满分17 · v2上调）

### 已知基础（v2扩充）
- Physical AI / Robotics / Digital Twin是GTC 2026三大主题（官方确认）
- Rubin CPX专为长上下文prefill设计（code assistant 100万+ tokens场景）
- KV Cache分层（S7）：GPU SRAM → System DRAM → CXL → Storage

### 采集路径

| 路径 | 来源 | Session | 层级 | 负责 | 目标证据 |
|------|------|---------|------|------|---------|
| P07-A | Physical AI / Robotics | AGT-ROBOT | A-必采 | 现场B | 机器人训练基础设施规格 + 客户案例 |
| P07-B | Agentic推理基础设施 | AGT-004 | A-必采 | 现场B | 100万token场景需要多少CPX vs Rubin GPU |
| P07-C | KV Cache多层架构 | AGT-007 | B-高ROI | 远程 | 验证S7：Storage Disaggregation产品成熟度 |
| P07-D | Digital Twin基础设施 | AGT-DT | C-机会 | 远程 | Omniverse + Isaac compute需求 |

### 关键问题
1. 生产agentic负载（10步+ tool-call链）vs 批量推理：GPU利用率差异有量化数据吗？
2. Rubin CPX是否能覆盖S1中"端侧长上下文推理"用例，还是需要独立的LPU方案？
3. KV Cache tiered storage（S7）：GPU Stacked Memory指哪层？性能/成本如何？
4. Physical AI/Robotics：训练用什么规模的GPU集群？有客户案例能公开吗？
5. Digital Twin：Omniverse对Rubin有哪些新的特定优化？

---

## PIR-08：互联网络 — Spectrum-X / InfiniBand / CPO 路线（满分19 · v2扩充）

### 已知基础（v2新增）
- **CPO路线图（GTC 2025宣布）**：
  - Quantum-X Photonics InfiniBand：144×800G，200G SerDes，液冷，2025年底可用
  - **Spectrum-X Photonics Ethernet（scale-out）：2026年**（128×800G 或 512×200G = 100Tbps）
  - scale-up CPO：2027年
- **NVLink Fusion生态**：Intel、ARM、Fujitsu、Qualcomm、SiFive已加入
- **UALink困境**：AMD被迫通过Ethernet隧道，Broadcom推SUE，NVSwitch竞争者SkyHammer（Upscale AI）
- **S4验证**：2026=scale-out CPO，2027=scale-up CPO

### 采集路径

| 路径 | 来源 | Session | 层级 | 负责 | 目标证据 |
|------|------|---------|------|------|---------|
| P08-A | Spectrum-X CPO session | NET-CPO | A-必采 | 现场A | **验证S4**：Spectrum-X Photonics是否2026年Q2/Q3出货？ |
| P08-B | NVLink Fusion生态 | NET-NVLF | A-必采 | 现场A | 新伙伴公告 + Intel EMIB合作进展 |
| P08-C | scale-up CPO时间线 | INF-CPO27 | B-高ROI | 远程 | 2027 scale-up CPO规格 / 带宽目标 |
| P08-D | 448G SerDes验证 | NET-SER | B-高ROI | 远程 | **验证S5**：NVL576中的448G SerDes现状 |
| P08-E | Connect With Experts | 网络团队 | B-高ROI | 现场A | NVLink vs UALink长期格局 |

### 关键问题
1. Spectrum-X Photonics 2026——具体出货时间是Q2/Q3/Q4？首批客户是谁？
2. NVL576的448G SerDes（S5）——这是GTC新宣布还是已有工程文档支持？
3. PTFE + Q-glass M9中板材料（S5）——在NVL576中是否已验证过串扰和热管理达标？
4. Intel加入NVLink Fusion（$5B投资确认）——数据中心产品具体是哪代CPU+GPU chiplet？
5. scale-up CPO 2027——用于NVSwitch还是直连GPU die之间？带宽目标是多少TB/s？
6. UALink现状：AMD Helios已用Ethernet隧道，NVLink Fusion是否已实质性赢得这场战争？

---

## PIR-09：BlueField DPU 经济性 + BF5 新品（满分17 · v2上调）

### 采集路径

| 路径 | 来源 | Session | 层级 | 负责 | 目标证据 |
|------|------|---------|------|------|---------|
| P09-A | BF5发布 | NET-BF5 | A-必采 | 现场C | **验证S9**：BF5规格 + 定价 |
| P09-B | ICMS+BF4/BF5 ROI | AGT-002 | A-必采 | 现场C | 升级路径 + ROI量化 |
| P09-C | DOCA生态 | NET-005 | B-高ROI | 远程 | BF5 GA合作伙伴数量 |
| P09-D | 存储卸载 | NET-C02 | C-机会 | 远程 | Storage Disaggregation benchmark |

### 关键问题
1. BF5：带宽、功耗、DOCA版本、与BF4的主要性能跳跃是什么？
2. BF4已部署客户的升级路径：BF5是直接替换还是firmware升级够用？
3. 在GPU+Stacked Memory + Storage Disaggregation方案里（S7），BF5的角色是什么？
4. BF4 vs BF5的MSRP差异？部署比（BF:GPU）是否改变？

---

## PIR-10：NVIDIA MLOps 全栈完整度（满分15）

（内容不变，见v1）

---

## PIR-NEW：Groq / LPU 生态系统与 Data Flow 推理战略（满分18 · v2新增）

> 这是 GTC 2026 最大潜在惊喜之一。单独列出以确保足够采集资源。

### 背景
- NVIDIA $20B获Groq LPU技术许可（2025-12）
- Groq核心价值：**Assembly Line / Data Flow架构**，数据流过芯片而非fetch-decode-execute
- LPU在Llama 70B需要574颗；单颗230MB SRAM / ~RTX 3090级FLOPS
- 在Rubin架构里的位置：可能作为speculative decoding加速器，或prefill（竞争CPX）
- S1暗示：LPU将更紧密集成到GPU旁边（GPU/LPU + 3D SRAM + HBM +HBF?）
- S2暗示：Feynman可能在架构层面整合Groq的Data Flow理念

### 采集路径

| 路径 | 来源 | Session | 层级 | 负责 | 目标证据 |
|------|------|---------|------|------|---------|
| PN-A | Groq/LPU专题session | AGT-LPU | A-必采 | 现场A | 产品定义：是新的product line还是内嵌到Rubin/Feynman |
| PN-B | Jensen Keynote | INF-001 | A-必采 | 现场A | LPU公告在keynote中的占比和定位 |
| PN-C | Connect With Experts | Groq团队成员 | A-必采 | 现场A/B | 技术路径一手问答 |
| PN-D | 竞争对比 | 若有推理专题 | B-高ROI | 远程 | LPU vs CPX vs 纯软件speculative decoding的成本/性能 |

### 关键问题
1. GTC 2026上LPU是demo、EA、还是正式产品发布（GA）？
2. 16x/32x per compute tray（S1）——这是服务器机箱内几块GPU配几块LPU？比例是什么？
3. 256x per rack（S1）——对应NVL144 CPX还是全新rack配置？
4. "端侧chat vs 云侧长上下文推理"未定位（S1）——是market research还是技术原因？
5. Feynman中，Data Flow架构是否会被软化集成到Rubin GPU的tensor core旁？
6. LPU + 3D SRAM + HBM（S1/S2）——这种堆叠方案涉及哪家封装代工？CoWoS还是Intel EMIB？
7. 散热问题：LPU在GPU旁3D堆叠是否已有热测试数据？对GPU Boost频率的影响？
8. HBF（S1提及"HBF?"）——这是什么？是高带宽Flash的缩写吗？

---

## 采集资源分配（更新版）

| 人员 | 主责 PIR | 重点新增 | 备注 |
|------|---------|---------|------|
| 现场A | PIR-01/PIR-NEW/PIR-08 | **Feynman + LPU是最高优先** | Groq团队Connect预约要最早 |
| 现场B | PIR-04/07/01(Vera) | LPU架构深度 + agentic | Dynamo+LPU session必到 |
| 现场C | PIR-05/06/09 | **BF5发布session** | ICMS + BF5两个session必排 |
| 远程1-5 | 全部Layer B/C | S4/S5验证（CPO/SerDes） | 异步监控CPO/Spectrum-X session |

---

## 高价值非 session 采集渠道

| 渠道 | 目标信息 | PIR | 操作 |
|------|---------|-----|------|
| Connect With Experts | **Groq/LPU团队**（最高优先，S1/S2核心）| PIR-NEW | 第一天keynote后立即预约 |
| Connect With Experts | 网络/CPO团队（S4/S5验证）| PIR-08 | 提前发邮件预约 |
| NVIDIA展台 | 正交背板实物（S8） | PIR-03 | 现场C拍照+技术问答 |
| 展台合作伙伴 | BF5 DOCA生态合作伙伴 | PIR-09 | 询问GA集成状态 |
| Startup展区 | Groq集成商、Disaggregated Inference | PIR-04/07 | 找用了Dynamo+LPU的startup |
| 媒体发布会 | 官方公告（Feynman/LPU/BF5）| PIR-01/NEW/09 | 监控NVIDIA Newsroom RSS |
| 非正式交流 | 供应链：CoWoS/EMIB产能 | PIR-01/S2 | 晚宴/走廊 |

---

## 关键假设与风险

| 假设 | 若错误的影响 |
|------|------------|
| LPU在GTC 2026有具体产品公告 | 若只是roadmap demo，PIR-NEW大幅降级 |
| Feynman有TSMC 1.6nm+Intel EMIB独家披露 | 若只重申2025路线图，S2价值降低 |
| BF5在GTC 2026发布 | 若推迟，PIR-09收缩 |
| Spectrum-X CPO在2026量产 | 若推迟到2027，S4调整 |
| 正交背板展出（更真实版本） | 若仍是概念展示，S8价值降低 |
