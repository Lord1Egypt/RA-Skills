# 各国监管体系速查表 v1.0

> **用途**：SKILL.md Step 2（监管体系解码）的预载底图。使用本表可跳过基础搜索，直接聚焦增量更新确认。
>
> **维护规则**：法规变更后更新"最后验证日期"字段。监管机构和资质分类体系变化慢（年级别），官方名录 URL 和认证商数量变化快，每次执行 Skill 时须 `web_fetch` 验证名录现状。
>
> **关键提醒**：代理提交合法性（`multiTenantProxyLegal`）是每个市场的 P0 前置条件，未确认前不可上生产。

---

## 🇻🇳 越南

| 字段 | 内容 |
|------|------|
| **监管机构** | 越南税务总局 GDT（Tổng cục Thuế / General Department of Taxation） |
| **主管部委** | 越南财政部（Bộ Tài chính） |
| **合规模式** | CTC（Continuous Transaction Controls）—— 发票提交须经 GDT 实时清算 |
| **通道类型** | T-VAN（Tax Value-Added Network）：纳税人与 GDT 之间的中间商网络 |
| **我方目标资质** | T-VAN 认证服务商（GDT 官方认证，约 10 家） |
| **官方名录 URL** | https://www.tct.gov.vn（税务总局官网，内含 T-VAN 认证商名单） |
| **已知 T-VAN 认证商** | MISA, VNPT, Viettel, BKAV, FPT, Bizzi 等（约 10 家） |
| **发票格式** | XML（GDT 定义的 Schema，含电子签名） |
| **数字签名 CA** | VNPT-CA, Viettel-CA, MISA-CA, BkavCA, FPT-CA（均须信通部认证） |
| **核心法规** | Decree 123/2020, Circular 78/2021, Decree 70/2025, Circular 32/2025/TT-BTC |
| **代理提交合法性** | ⚠️ **未最终确认**——我方以多租户代理身份持有 PKI 证书是否合法，须越南本地税务律师书面确认（最高优先级风险项） |
| **数据本地化要求** | 电子发票 XML 存储于中国境内服务器是否合规，须越南信息安全律师确认（高风险） |
| **接入架构建议** | Phase 1：通过 T-VAN 中间商（MISA 或 VNPT），8-10 周接入；Phase 2：月均>5000 张时评估 GDT 直连 H2H |
| **高峰期风险** | GDT 系统在月末/季末有历史超时记录，降级队列是 P0 功能，自动重试策略：超时 10s → 入队 → 每 5min 重试 → 最多 12 次 |
| **已确认合作方** | T-VAN 已成功接入（Phase 1 live），合作方名称见内部合同文件 |
| **紧迫风险** | 法规变更通知目前为非正式默契，需补签合同条款（5 工作日书面通知义务） |
| **最后验证日期** | 2026-03 |

### 越南特有注意事项

- 税率现状：标准税率 10%，部分行业减税 8%（Decree 44/2025 或当期有效减税令，需 T-VAN 书面确认当前有效期）
- `vnSectorTag` 黑名单：METAL_PRODUCTS, CHEMICAL, PETROLEUM, TELECOM, FINANCE, REAL_ESTATE, AUTOMOTIVE, PETROLEUM_OP 等适用 10% 标准税率；其余适用减税 8%
- 发票纠错机制：第 70 号法令取消"注销"，改为"调整（Điều chỉnh）"和"替换（Thay thế）"
- 越南语强制：商品/服务名称必须含越南语描述
- 2025.6.1 起新增：年收入≥10亿越盾个体户须 POS 联网；付款方式字段全类型必填

---

## 🇲🇾 马来西亚

| 字段 | 内容 |
|------|------|
| **监管机构** | 马来西亚内陆税收局 LHDN（Lembaga Hasil Dalam Negeri / Inland Revenue Board of Malaysia） |
| **平台名称** | MyInvois（LHDN 官方电子发票平台，由 MDEC 提供技术支持） |
| **合规模式** | CTC（Continuous Transaction Controls）—— 实时提交，LHDN 在线验证 |
| **通道类型** | 两条路径并行：① 直连 MyInvois Portal/API；② 通过 MDEC 认证的 Peppol SP（Access Point） |
| **我方目标资质** | MDEC 认证的 Peppol SP（Service Provider / Access Point）—— 持有底层传输通道 |
| **官方名录 URL** | https://www.myinvois.hasil.gov.my（MyInvois 官网）；Peppol SP 名录：https://peppol.org/peppolauthority/singapore-and-malaysia/ |
| **发票格式** | JSON 或 XML；Schema 默认 v1.1；数字签名：XAdES |
| **API 限流** | Submit 接口 100 RPM（月结日峰值期削峰必选项，非优化项）；Get Submission 为主通道；Get Recent 仅用于离线对账 |
| **核心法规** | MyInvois Technical Specs v1.1, LHDN e-Invoice Specific Guideline |
| **代理提交合法性** | ✅ **已确认**——LHDN FAQ 明确允许服务商证书委托，多租户 PKI 代理合法 |
| **cancellable_until** | 72 小时撤销窗口，时间戳必须持久化存储，是核心业务约束 |
| **Token Pool 设计** | Redis 双层缓存 + 提前 5 分钟续期 + 分布式锁 + 指数退避 |
| **SLA 责任边界** | = 发票进队列时效，非 LHDN 验证通过时效 |
| **轮询接口分工** | Get Submission：主通道；Get Doc Details：仅 Invalid 诊断用；Get Recent：仅离线对账用 |
| **BPO 内涵（马来西亚）** | 低成熟度市场——线下跑 LHDN 窗口、税局关系疏通、代办证件，需本地实体团队 |
| **最后验证日期** | 2026-03 |

### 马来西亚特有注意事项

- Classification Code（分类码）：每张发票必须包含 LHDN 官方 45 个分类码之一，`myClassificationCode` 字段必填
- MyInvois 强制截止日期：按年营业额分阶段强制，已进入全面强制阶段（2025年起）
- 架构关键设计：Get Doc Details 接口仅用于 Invalid 状态诊断，不得作为主轮询通道（高频调用触发限流）

---

## 🇸🇬 新加坡

| 字段 | 内容 |
|------|------|
| **监管机构** | 新加坡税务局 IRAS（Inland Revenue Authority of Singapore）+ IMDA（Infocomm Media Development Authority） |
| **平台名称** | InvoiceNow（基于 Peppol 网络的全国电子发票体系） |
| **合规模式** | Post-Audit（事后审计）—— 无实时 CTC 要求，发票不经税局实时验证 |
| **通道类型** | Peppol Access Point（AP）—— 需持 IMDA 认证的 InvoiceNow AP 资质 |
| **我方目标资质** | IMDA 认证 InvoiceNow AP（当前约 35 家，2026-04 数据） |
| **官方名录 URL** | https://www.imda.gov.sg/how-we-can-help/nationwide-e-invoicing-framework（IMDA 官网）；AP 完整名录：irsplistforwebsite.pdf（已在项目知识库） |
| **接入路径** | 通过 Storecove 接入 Peppol InvoiceNow（Phase 2 路径，P0 blocker：Storecove C5 API 就绪确认） |
| **已知目标合作方** | **SESAMi**（第一梯队：InvoiceNow 奖历年第一，Best Performance AP）；**DataPost**（第一梯队：Direct Connection 奖，成本效率高）；**Storecove**（接入层，非 AP，提供 C5 API） |
| **发票格式** | UBL 2.1（Peppol BIS Billing 3.0） |
| **代理提交合法性** | ✅ **Peppol 架构天然支持多租户代理**，无额外法律风险 |
| **数据本地化要求** | 新加坡无强制数据本地化要求（对比越南和印尼，风险最低） |
| **BPO 内涵（新加坡）** | 中成熟度市场——数据映射异常处理、错误报文人工修正；新加坡 IRAS 文档质量高（英文），部分问题可直接查阅官方文档解决 |
| **商业模式验证** | 新加坡是 CaaS 商业模式验证对象（MNC 区域总部客户），目标验证"多国控制塔年订阅溢价"假设 |
| **最后验证日期** | 2026-04 |

### 新加坡特有注意事项

- IMDA AP 名录（2026-04）：35 家认证 AP，含本地（Local）和外资（Foreign）分类，SESAMi 连续多年获 Best Performance（Transaction）第一
- GST 税率：2024年起 9%，无强制实时 CTC，税率计算相对简单
- Peppol 网络：新加坡与澳大利亚、欧盟等 Peppol 成员国互通，对有跨境需求的 MNC 客户是卖点
- InvoiceNow 采纳仍在推广阶段，非全面强制（截止 2026 年）

---

## 🇮🇩 印度尼西亚

| 字段 | 内容 |
|------|------|
| **监管机构** | 印尼税务总局 DJP（Direktorat Jenderal Pajak / Directorate General of Taxes） |
| **平台名称** | Coretax（2025年推出的新一代税务核心系统，替代 e-Faktur） |
| **合规模式** | CTC（Continuous Transaction Controls）—— 强制通过 DJP 认证中介（PJAP）接入 |
| **通道类型** | PJAP（Penyedia Jasa Aplikasi Perpajakan）：强制中介模式，不可直连 DJP |
| **我方目标资质** | 与 PJAP 认证服务商合作（我方自身无需 PJAP 资质，需接入 PJAP 通道） |
| **官方名录 URL** | https://www.pajak.go.id（DJP 官网，PJAP 名录需实时查询） |
| **核心法规** | PMK-81/2024（强制 PJAP 中介要求），Coretax 技术规范 |
| **代理提交合法性** | ⚠️ **强制 PJAP 中介**，多租户代理合法性须通过 PJAP 合作关系解决，不可直连 |
| **进入条件** | 🔵 条件进入——Coretax 系统稳定性是首要前置条件；2025 年 Coretax 上线初期存在系统稳定性问题 |
| **进入时间窗口** | 需等待 Coretax 稳定后（建议 2026Q4 或之后评估） |
| **BPO 内涵（印尼）** | 强中介市场——PJAP 合作伙伴须具备本地 DJP 关系网络，异常处理复杂度高 |
| **最后验证日期** | 2026-03 |

### 印尼特有注意事项

- Coretax 是 DJP 的单一出口，不像越南有多家 T-VAN 可选，通道风险更集中
- PMK-81/2024 强制 PJAP 中介，意味着我方必须通过认证 PJAP 接入，不能绕过
- 印尼是东南亚中资企业第二大目的地，战略价值高，但系统稳定性是客观约束

---

## 🇮🇹 意大利

| 字段 | 内容 |
|------|------|
| **监管机构** | 意大利税务局 AdE（Agenzia delle Entrate） |
| **平台名称** | SDI（Sistema di Interscambio）—— 所有 B2B 发票交换平台 |
| **合规模式** | CTC（Continuous Transaction Controls）—— 全球最早强制 CTC 的国家之一（2019 年 B2B 强制） |
| **通道类型** | 通过 SDI 认证的中间商接入（Intermediari SDI） |
| **我方目标资质** | 通过 Seeburger 接入 SDI（Seeburger 为 Phase 1 路径，为我方的白标底层通道） |
| **接入路径** | Seeburger 统一接入（同时覆盖德国、波兰、意大利），先签框架协议 |
| **发票格式** | FatturaPA XML（意大利特有格式，含 Codice Fiscale 和 Partita IVA） |
| **关键时间节点** | scarto（税局拒绝）通知在 5 天内，须在窗口内处理，Webhook SLA 至关重要 |
| **代理提交合法性** | ✅ Seeburger 作为认证中间商负责合规，我方通过 Seeburger 接入无额外法律风险 |
| **战略定位** | 🔴 旗帜市场——接入展示和资本故事用途，不投入大规模运营（至少到 2027 年） |
| **产品深度投入时间** | 2027 年之后 |
| **BPO 内涵（意大利）** | 高成熟度市场——SLA 保障、API 健康监控；Seeburger 承担格式合规，我方专注业务逻辑 |
| **最后验证日期** | 2026-03 |

### 意大利特有注意事项

- Natura Code（N-Code）：免税/不征税发票须填写 Natura 免税代码（如 N2.1, N3.2），`itNaturaCode` 字段必填
- scarto 窗口：SDI 拒绝通知须在 5 天内处理，超期发票状态进入不可逆状态
- Seeburger 合同谈判重点：格式更新 SLA（强制变更 15 工作日）、Webhook 延迟≤30 分钟、数据留欧盟境内

---

## 🇩🇪 德国（跟随市场，参考）

| 字段 | 内容 |
|------|------|
| **监管机构** | 德国联邦财政部（BMF）+ 各州税务局 |
| **合规模式** | 2025年起推进强制电子发票（B2B），过渡期至 2027-2028 年 |
| **通道类型** | 多种格式并存：ZUGFeRD 2.x, XRechnung, EN16931 |
| **我方接入路径** | Seeburger 统一接入 |
| **进入时间窗口** | 框架协议先行，产品深度投入等到 2027 年 |
| **最后验证日期** | 2026-03 |

---

## 📊 跨市场监管体系对比速查

| 国家 | 合规模式 | 通道类型 | 我方接入路径 | 代理合法性 | 数据本地化 | 市场层级 |
|------|---------|---------|------------|----------|----------|---------|
| 🇻🇳 越南 | CTC | T-VAN | 合作伙伴 T-VAN | ⚠️ 待确认 | ⚠️ 待确认 | 核心 |
| 🇲🇾 马来西亚 | CTC | Peppol SP/直连 | Peppol SP + 直连 | ✅ 已确认 | 较宽松 | 核心 |
| 🇸🇬 新加坡 | Post-Audit | Peppol AP | Storecove | ✅ Peppol天然支持 | 无强制要求 | 核心 |
| 🇮🇩 印尼 | CTC | PJAP（强制） | PJAP 合作方 | ⚠️ PJAP绑定 | 严格 | 跟随 |
| 🇮🇹 意大利 | CTC | SDI 中间商 | Seeburger | ✅ Seeburger兜底 | 欧盟GDPR | 旗帜 |

---

*本文档与 SKILL.md Step 2 配套使用，为漏斗分析提供预载基础，减少重复搜索。每次执行 Skill 时仍须 `web_fetch` 官方名录页面确认当前认证商数量和名单，本表不可替代实时验证。*
