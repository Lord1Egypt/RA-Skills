# 马德里技能：法律依据来源、成员数据与官方工具

> **用途**：承接 SKILL.md 原 §3.1（信息来源）、§3.2（成员数据三口径）、§3.5（背景工具与标准）。
> **权威范围**：本文件是**法律依据来源清单、成员数据口径、官方工具入口**的唯一权威源。
> **时效**：成员数、声明、规费均为易变数据，须按 SKILL.md §3.0 时效清单联网核验；查不到的数据直接答复「无」，严禁编造。

## 一、信息来源（原 §3.1）

本技能以以下官方文件为法律基础（来源块见各 reference 文件头部）：

· 马德里协定（1979-09-28 修改，WIPO Lex text 384735）—— @references/madrid-agreement.md（**中文逐字全文**，2026-09-25 抓取，Article 1–18 含 9 个分条；文末附技能整理的要点与勘误）；英文全文 @references/madrid-agreement-en.md（英文 text/283530，2026-08-08 抓取，Article 1–18）
· 马德里议定书（2007-11-12 修正，WIPO Lex TRT/MADRIDP-GP/001）—— @references/madrid-protocol.md（**中文逐字全文**，2026-09-25 抓取，Article 1–16 + 10 分条 + 官方脚注；文末附技能整理的要点与勘误）；英文全文 @references/madrid-protocol-en.md（英文 text/283484，2026-08-08 抓取，Article 1–16 + 10 分条）
· 马德里实施细则（页面标注 2025-11-01 生效；Rule 40(1) 载 2020-02-01 生效，WIPO Lex TRT/MADRIDP-GP/040）—— @references/madrid-regulations.md（**中文逐字全文**，2026-09-25 抓取，Rule 1–41 + 官方脚注 1–9；文末附要点、英文条款标题对照表与勘误）；英文全文 @references/madrid-regulations-en.md（英文 text/596531，Rule 1–41 正文，不含费用表）
· 马德里行政规程（2023-02-01 生效，WIPO Lex TRT/MADRIDP-GP/036）—— @references/madrid-admin-instructions.md（**中文逐字全文**，2026-09-25 抓取，7 部分 19 条 + 第 11 条之二；文末附要点与勘误）；英文全文 @references/madrid-admin-instructions-en.md（英文 text/586472，2026-08-08 抓取，7 部分 Section 1–19）
· WIPO 马德里成员声明页面（更新于 2026-03-15）—— @references/madrid-declarations.md
· **WIPO 规费表（2023-02-01 版）与单独规费页（2026-08-23 更新，2026-09-23 抓取）—— @references/madrid-fees.md（本技能规费数值的唯一权威源）**
· 常见问题与实务反例汇编（依上述条约与费用表整理）—— @references/madrid-faq.md
· Madrid e-Filing 申请人操作指南（WIPO 官方 43 页 PDF）——**该原件已于 v3.7.0 依维护决定自本技能移除**（控制技能体积）；提炼要点见 @references/madrid-faq.md §三，如需原件请自 WIPO 马德里 e-Filing 页取得。
· 马德里体系商品和服务分类审查指南（第五版，2026 年）——**官方 PDF 原件已于 v3.7.0 移除**；提炼版见 @references/madrid-goods-services-classification.md，如需原件请自 WIPO 取得。
· 马德里商标国际注册申请快速审查办理指南（CNIPA）—— @references/madrid-fast-track-examination-cnipa.md
· （美国侧费用已移交）美国作为原属局/指定局的 USPTO 马德里费用（37 CFR §7.6 认证/转递费、§7.7 国际费代收，USD，含费码）：**如本环境已安装 `us-tm-madrid` 技能**，见该技能 references 目录下的 madrid-uspto-fees.md（2026-08-09 抓取）；**未安装时**直接查 USPTO Fee Schedule（https://www.uspto.gov/learning-and-resources/fees-and-payment/uspto-fee-schedule ），本技能仅保留 WIPO 侧规费（CHF），不复制美国侧数据。

> **转换委托（可选）**：上列 WIPO/CNIPA 官方 PDF 文档（如 e-Filing 操作指南、分类审查指南）如需整本转换为结构化 Markdown 更新本库，**若已安装 `legal-doc-converter` 技能**可委托其执行（共享转换层，脚本单一维护，本技能不复制脚本）；**未安装时**直接按官方 PDF 原文查阅，或由本技能的 `references/madrid-faq.md §三` 取已提炼的要点，无需先转换。

## 二、马德里联盟成员数据三口径（原 §3.2）

| 口径 | 数值 | 含义与说明 |
| --- | --- | --- |
| 缔约方（成员）数 | 117 个 | 加入马德里体系的政治实体，含 3 个政府间组织：欧盟 EU、比荷卢 BX、非洲知识产权组织 OAPI。数据基准 WIPO 成员页（**2026-10-11 核验**，页头显示 117 members / 133 countries；官方成员 PDF 载明「Saudi Arabia – October 8, 2026」）。最新成员：格林纳达（2025-12-15 交存，2026-03-15 生效）、沙特阿拉伯（2026-07-23 公布，**2026-10-08 生效**）。**自 2026-10-08 起 117 / 133 即为实际口径**（生效前为 116 / 132）。 |
| 可指定缔约方数 | 约 119 个 | WIPO 规费计算器等工具中可勾选的「指定项」总数 = 117 个成员 + 可被单独指定的属地（如荷兰王国下属的库拉索 CW、圣马丁 SX 等，泽西岛、根西岛已单列），随属地指定状态浮动。 |
| 覆盖国家/地区数 | 133 个 | 在 117 个成员项下可实际获得商标保护的国家/地区（EU 成员 27 国、OAPI 成员 17 国等合并计入）。 |

关键说明：

· **全部成员均为《马德里议定书》缔约方**——WIPO 成员页 Key Facts 原文：「All Madrid System members are party to the Madrid Protocol – the governing treaty of the Madrid System.」（2026-09-23 核验）。实务上不存在「纯协定成员」，故一般凭基础申请即可提起；§4.7、§4.8 中保留的纯协定分支属历史/个别情形的兜底，仍需逐案核验。
· 中国（CN）指定不延伸至香港、澳门——港澳不是马德里可指定缔约方，须通过单一国家/地区途径申请。
· 保全条款提醒：成员普遍性不等于声明普遍适用。依议定书第 9 条之六(1)(b) 与费用表第 2.4/5.3/6.4 项，被指定缔约方与原属缔约方**均为协定 + 议定书双参加国**时，该国依第 8 条(7)、第 5 条(2)(b)/(c) 所作声明在双方关系中不生效力（详见 @references/madrid-faq.md Q11）。

## 三、背景工具与标准（原 §3.5）

· 尼斯分类：须按尼斯分类第 13 版（NCL13-2026，2026-01-01 生效）分类；NCL 版本每年 1 月 1 日可能更新，实务以 MGS 数据库显示当前版本为准。
· MGS（Madrid Goods & Services Manager）：WIPO 官方商品/服务标准化术语库，https://webaccess.wipo.int/mgs/ ，用于核实术语是否为 WIPO 接受的标准化表述；支持 BROWSE（按类浏览）与 SEARCH（关键词搜索）。
· Madrid Monitor：WIPO 官方国际注册状态实时查询，https://www3.wipo.int/madrid/monitor/en/ ，支持 By number / By trademark / By holder 查询。
· eMadrid：WIPO 电子化综合平台，https://www.wipo.int/madrid/en/emadrid/ ，含 e-Filing（新申请）、Pay Fee（在线缴费）、Manage（后续管理）、Madrid Monitor（状态查询）。
· ROMARIN：WIPO 官方马德里商标查询库（实施细则第 33 条），https://www.wipo.int/romarin ，与 Madrid Monitor 互补（Monitor 偏单件状态跟踪，ROMARIN 偏批量检索与数据分析）。
· MM 标准表格：MM2 国际注册申请书（新申请）、MM3 后期指定申请书、MM4 续展申请书、MM5 变更登记申请书（名称/地址变更、转让、删减、放弃）、MM6 许可备案申请书。
· WIPO Fee Calculator：官方在线规费计算器，https://madrid.wipo.int/feecalcapp/ ，支持 New application / Subsequent designation / Second Part fee / Renewal。

---

## 四、法律层级关系（原 §一）

· 马德里协定（1891 签订 / 1967 斯德哥尔摩 / 1979 修改）：体系基础条约，18 条。
· 马德里议定书（1989 通过 / 2007 修正）：现代补充，16 条；双参加国（既参加协定又参加议定书）相互关系中议定书优先。
· 实施细则（2025-11-01 生效）：操作规则，9 章 41 条 + 费用表。
· 行政规程（2023-02-01 生效）：日常操作指南，7 部分 19 条（含第 11 条之二；其中第 5/8/9/10/14 条共 5 条整条已删除）。

