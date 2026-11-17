# Changelog

## 28.0.0 (2026-11-11) — 10-26~11-06 学习成果全部落地（14 组建议）

### Added
- 新增 5 个 references：
  - `q4-closing-calendar.md` — Q4/春节前关单日历：首轮电话三问（年终奖/vesting/通知期）、make-whole 计算器、二段式 start date、中国春节观望期（发奖后 48h 反悔高危窗口）、客户 Q4 加速器服务包（48h 反馈令/锁面试时段/7-10 天流程/预算年度切换话术）、Quiet Onboarding（12-1 月入职静默融入）、11-2 月护航节奏改版、全年季节节奏总览
  - `contract-fee-negotiation.md` — 合同与收费谈判攻防：四大收费模型（含 Engaged 混合 $5-15K+18-25%）、买方压价筹码 vs 我方对等交换清单、报价五因子、**年薪口径标准条款**（防天价猎头费判例）、保证期四要素 + 甲方原因全额付保护条款、**防跳单三条款**（独家委托/及时告知 24h-3 工作日/人选排除 12 个月，司法背书）、发票与付款解耦、客户抗辩自查清单 10 项
  - `ai-recruiting-compliance.md` — AI 招聘合规：EU AI Act（招聘 AI 高风险、罚 €3500 万/7%、2026-08-02 可执行、2027-12-02 完整义务、美中总部不豁免）、6 项合规要件、NYC LL144 偏见审计、出海欧洲合规问询清单（向客户+向我方）、候选人数据治理字段（同意/入库日/保留 2 年/删除权）、AI 拒信提升体验（WEF）与四段式落选反馈 SOP、算法偏见治理五件套 + 季度自检、AI 面试辅导要点、五维护城河定位声明
  - `global-staffing-advisor.md` — 出海人才配置顾问：外派/属地化/混合 Local Plus 三模式对比、光辉国际三阶段诊断（过渡期国内渠道失效）、"五条件找三人选"出海版需求校准、跨文化双向日手册（老外进中企两大挑战/中企出海两个死法/价值观统一+方式属地适配）、各国面试法律红线速查（美国禁问薪资史年龄等）、外派岗寻访规则 + 出海专用档案字段、全球聘/合规/全球雇/全球薪四类服务包、GWM 温暖全球化叙事
  - `silver-medalist-pool-ops.md` — Silver Medalist 池运营：经济学数据（75% 库记录无人触达、沉睡库贡献 26%→46%、激活快 3 倍、$250K+ 年价值、64% 愿保持关系）、三问季度自检、运营 SOP（入职即标记→3/6/12 月激活窗→季度扫描→引用式话术）、**Pipeline 新节点 Closed-Lost → Silver 池 → Re-activate**、profile 新字段（silver/激活窗/数据合规/响应质量列 + 2 次无响应自动降温）、简历入库自动化规则、candidates/INDEX.md 索引化（Active Memory 思路）

### Changed
- SKILL.md：一章新增「出海人才配置顾问」框架段；七章新增「Q4 关单日历」+「合同谈判攻防」两段；八章新增「Silver Medalist 池运营与数据治理」；十一章新增「AI 招聘合规与算法偏见治理」；十二 SOP 新职位流程 11 步 → 16 步（加可接性判断/Intake/Silver 优先查/v3.1 自检/Offer 三问/合同条款/Closed-Lost 入池）；附录索引扩至 29 个文件
- skill.yml 契约：`client_manage` +3 rules（AI 合规问询/出海阶段诊断/合同 trading 原则）；`offer_negotiation` +1 section（Quiet Onboarding）+1 rule（Q4 三问与 make-whole）；`onboarding_support` +3 rules（Silver 打标与四段拒信/春节季护航改版/发奖后 48h 跟进）；`data_optimization` +3 rules（响应质量列与降温/新职位先查 Silver/INDEX 索引化）；`compliance_ecosystem` +3 rules（EU AI Act 与 LL144/数据治理必填字段/偏见季度自检）；`talent_mapping` +1 rule（出海专用字段与艰苦地区降权）
- 版本号 28.0.0 五处对齐；中英文 description 更新

### Notes
- 落地源头：memory/2026-10-26.md（Silver Medalist 经济学）、2026-10-30.md（AI 招聘合规）、2026-11-02.md（出海人才配置）、2026-11-03.md（合同收费谈判）、2026-11-06.md（Q4 关单战术）
- 时效性：Q4/春节关单日历为当季即用内容（11 月—次年 3 月）

## 27.0.1 (2026-10-24) — 同内容重发：修复 ClawHub 发布收据已写入但版本未入库展示

- 内容与 27.0.0 完全一致。27.0.0 publish 返回成功并给出收据（k972hg7q…），但注册表 Latest 停在 26.0.0、版本列表未出现 27.0.0、重发报 Version already exists —— 判定平台侧索引未生效，bump patch 重发触发完整入库。

## 27.0.0 (2026-10-24) — 发布线缺口补齐（11 项未落地建议，从单体版 v17 合入）

### Added
- 新增 8 个 references：
  - `intake-kickoff-sop.md` — Intake/Kick-off 三段式议程 + 25 问中文表单 + 需求敏捷校准（三大信号）
  - `recommendation-report-v31.md` — 推荐报告 v3.1（一句话画像/分栏对标/六要素/总包拆解/倒挂预判）+ 行业趋势报告 Deep-Research 五维框架
  - `offer-reversal-defense.md` — Offer 反悔五因 + 48h 黄金窗口三句话术 + 催vs跟节奏 + 谈判杠杆排序 + RSU 五误区 + A股/H股/红筹三架构
  - `ghosting-prevention.md` — 候选人体验 SLA 差距表 + 流程地图 + 预警信号 + 入职前管理 SOP + 防跳票
  - `interview-coaching-debrief.md` — 2026 面试辅导更新（稳定性追问/优缺点禁忌）+ Debrief 顾问动作（次日上午+独立宣读）
  - `bd-transparency-playbook.md` — FEB 卖点法则 + 客户调研四维 + BD call 纪律 + 过程透明度标准 + JRG 费用对标
  - `soho-business-model.md` — Contingency/Retained/RPO 对比 + 混合升级路径 + 保密三级定价 + SOHO 经济模型 + 失败五因自检
  - `salary-intel-2026-cn.md` — 2026 中国薪酬情报速查（涨幅/AI 岗 60,738/倒挂 33%/出海对标，季度更新）
- `ai-workflow-agents.md` 追加「信号监控触达 Cadence」节（Day 1/3/7/14 + 人工审批红线 + LinkedIn ≤30 动作/小时）
- SKILL.md 八个阶段章新增 v27 框架段（一/二/五/六/七/八/十/十一，含快速指令+核心数据+📖链接）；附录索引扩至 24 个文件

### Changed
- skill.yml 契约：`write_recommendation` +3 rules（画像钩子/分栏六要素/倒挂预判）+总包拆解 section；`client_manage` +2 rules（Intake SOP/透明度同步）；`offer_negotiation` +2 required_sections（反悔预防/入职前管理）+3 rules（杠杆排序/48h 话术/防 ghosting）；`interview_assess` +2 rules（2026 辅导/debrief 建议）；`ai_workflow` +1 rule（cadence 审批红线）；`workflow_sop` +1 rule（商业模式升级路径）
- 版本号 27.0.0 五处对齐；中英文 description 补 v27 特性

### Notes
- 本次合入源头：workspace 单体版 `skills/headhunter-pro/`（v17.0）的 09-26~10-23 学习建议落地成果；单体版保留为个人工作区版本，不再单独发布
- 与 counter-offer-defense.md 分工明确：那边=现雇主挽留攻防；新增 offer-reversal-defense=候选人拿 offer 后反悔


## 26.0.0 (2026-10-22) — 2026 断档期补学成果全部归档落地

### Added
- 新增 6 个 references（源自 2026-10-02 至 10-19 补学日志）：
  - `payment-terms-collection.md` — 回款与账期治理：2026 国办新政、隐形账期"不确权"陷阱、合同必备 8 条、客户信用 A/B/C/D 分级、催收 6 阶段 SOP、客户信用档案模板
  - `counter-offer-defense.md` — Counter-Offer 攻防：可辩护数据表（约 50% 收到/57% 接受/29% 留存过 12 月，**禁用旧"80%/6 个月"**）、7 阶段攻防 SOP、三种老板反应话术、Silver Medalist 回流池
  - `new-energy-talent-intel-2026.md` — 新能源：储能出海薪酬实盘、本地化 vs 外派双模式、国家经理五合一拆解、⚠️ 央国企年龄硬门槛、时效成本谈薪论
  - `healthcare-talent-intel-2026.md` — 医疗健康：BD 出海 157 笔/1,356 亿美元、CXO 订单回暖、缺口岗位清单、BD 五维复合能力、璞睿 IQVIA 红线
  - `consumer-retail-talent-intel-2026.md` — 消费零售：消费分级/情绪消费 2.72 万亿、四大破局路径、75% 高管并购意向→整合期窗口、双轨能力评估
  - `finance-talent-intel-2026.md` — 金融：银行 vs 券商对比、AI+业务 35 万缺口、中行高端岗画像、香港缺口、保密招聘三级服务、光辉国际批判性思维

### Changed
- skill.yml 契约增补：`offer_negotiation` 新增"付款条款与账期风险提示"+"Counter-Offer 风险预判与应对"两个 required_section 及数据纪律 rules；`client_manage` 新增"客户信用与景气度筛查"；`talent_mapping` 新增出海双模式/年龄硬门槛/行业情报参照 rules；`interview_assess` 新增批判性思维评估 rule
- SKILL.md：行业人才地图四行业各增📖行业情报链接；七、谈判章新增两个关联深度阅读；附录索引表重建为 16 个真实存在文件（含 v26 新增 6 个）
- 修复历史遗留：SKILL.md 附录此前引用 7 个已在 v25 清理的旧文件，现已对齐
- skill.yml 主 description 修正（原误标 v24.0）；中英文 description 同步 v26.0

## 25.0.0 (2026-09-24) — SKILL.md 瘦身 + output 契约补全

### Changed
- SKILL.md 大幅瘦身：4248 行/164K → 1492 行/60K（-65%）
  - 外移 7 个章节到 references/：人才寻访、筛选评估、触达互动、入职护航、数据优化、AI 协同、合规与生态
  - 正文保留框架 + 快速指令 + 核心数据 + 📖 深度参考链接
- skill.yml output 契约补全：12 个 task_type 独立 output schema
  - 每个 schema 含 required_sections + rules，AI 调用输出更可控
- description_en 补全（平台注册表截断修复）
- 清理 7 个未被引用的旧 references 文件（节省 20.3 KB）


## 24.0.0 (2026-09-18) — 本周升级

### Fixed
- CHANGELOG 版本号对齐（24.0.0 对应 v24 发布，此前误写为 v23 bump 记录）
- 核心原则 #31/#37 首次触达给价值重复表述合并
- 核心原则 #18/#19 AI协同 + 批判性思维重复表述合并
- 历史版本注释清理（v10.0 更新、v12.0 新增等内联标注，CHANGELOG 已记录）
- CHANGELOG 历史记录恢复（v14-v23 全部保留）

### Changed
- SKILL.md 瘦身：4252 行 → ~3200 行（164K → ~120K）
- skill.yml 输出契约细化：12 个 task_type 独立 output schema

## 23.0.0 (2026-09-18)

### Changed
- onboarding-support.md 正文链接补全（10/10 References 全覆盖）
- 版本号 bump v22.0.0 → v23.0.0

## 22.0.0 (2026-09-18)

### Changed
- 10 个 References 正文引用全链接（从 0→9 次）— AI 执行时能直接看到深度参考文档
- H1 标题版本号对齐（v17.0 → v22.0）
- 附录 References 索引整合为单一完整表格
- skill.yml 版本对齐 SKILL.md frontmatter

## 21.0.0 (2026-09-18)

### Changed
- H1 标题版本号对齐（v17.0 → v21.0）
- 附录 References 索引整理为单一完整表格（消除重复/断裂）
- 10 个 references 文件全部在 SKILL.md 中建立引用链接

## 20.0.0 (2026-09-10)

### Changed
- ClawHub 发布修复：description 字段从 85KB 全量嵌入精简为摘要
- skill.yml version 对齐 SKILL.md frontmatter

## 19.0.0 (2026-09-10)

### New
- skill.yml 输入契约完全对齐 12 阶段工作流（6 → 12 个 task_type）
- 新增 task_type: offer_negotiation, onboarding_support, data_optimization, ai_workflow, compliance_ecosystem, workflow_sop
- 完整索引全部 10 个 references 文件（onboarding-support, outreach-scripts, pipeline-states 等）

### Changed
- 修复 ClawHub SUSPICIOUS 根因：description 字段从 85KB 全量嵌入精简为 52 字符摘要
- skill.yml 版本对齐 SKILL.md frontmatter（15.0.0 → 19.0.0）
- 顶层 ## 标题从散列结构统一为 12 阶段商业逻辑顺序（〇～十二 + 附录）

### Fixed
- 重复 ### 标题清零（9 组 → 0 组）
- 快速指令 #1-7 补全（从 #8 起始 → #1-#16 完整覆盖）
- SKILL.md.v16.backup 清理，不再阻塞 SkillHub 发布

## 18.0.0 (2026-09-09)

### Changed
- 按猎头商业逻辑全面重构：从版本号堆叠改为 12 阶段端到端工作流
- 核心原则 39 条完整保留，快速指令 16 条全覆盖
- 10 个 references/ 文件全部索引
- 空行压缩优化（连续 4+ → 3）

## 15.0.0 (2026-09-02)

### New
- Talent Gap Analysis（咨询先行模式）：四步人才差距分析流程（Business Diagnosis → Role Necessity → Talent Gap → Co-create Success Profile）
- 垂直行业深耕评估：9+1 维度评分新增行业专属洞察维度
- Offer 谈判 7 问检查表
- 候选人 Persona 构建框架
- 企业客户关系深度维护（四阶段 + 5 关键动作 + 3 案例）
- 职位需求对齐 SOP（JTIF 框架：Job → Talent → Interview → Follow-up）
- Purple Squirrel 管理流程
- 中间阶层候选人识别与应对指南
- AI Agent 协同招聘工作流参考
- GitHub Proof of Work 5 信号评估模块
- 推荐报告素材收集 SOP
- 语音 AI 工作流（VibeVoice）
- AI 原生能力评估维度
- 48h 反馈 SLA 追踪
- AI 使用披露 & 薪资透明化话术

### Changed
- 9 维度评分扩展为 9+1 维度（+批判性思维/适应性，Korn Ferry 2026 #1 需求技能）
- 入职追踪从 90 天扩展为 6 个月融合支持
- 核心原则从 26 条扩展至 39 条
- 移除个人身份信息（已匿名化）
- 短名单质量控制升级（v9.1）
- Silver Medalist 管道管理（v9.2）
- 转化率基准更新（v12.0）
- 核心原则新增：AI 协同智商、批判性思维优先级（v10.0）

### Security
- 无外部网络调用
- 仅文件操作 + 文本生成
- 最小权限模型
- 候选人个人信息不输出到文件外

## 14.0.0 (2026-08-27)

### Changed
- 入职追踪从 90 天升级为 6 个月融合支持
- 新增 AI 原生能力评估维度

## 13.1 (2026-08-25)

### Changed
- 触达话术库升级（GitHub 技术人才 + LinkedIn 被动 + 中间阶层三轨）
- Silver Medalist 再利用机制落地

## 13.0 (2026-08)

### New
- 语音 AI 工作流
- 候选人体验 2026 核心差异化

## 12.0 (2026)

### New
- 48h 反馈 SLA 追踪
- AI 使用披露 & 薪资透明化话术
- AI Agent Recruiter 竞品全景
- ClawHub 发布准备
- 转化型猎头关键理念
- Talent Mapping 2026 方法论升级

### Changed
- 核心原则更新：AI 协同智商、批判性思维优先级
- 转化率基准更新

## 11.0

### New
- 核心原则 34-39 条
- Anti-Rationalization 检查
- Hitting Rate 统计

## 10.0

### Changed
- 核心原则从 15→26 条
- 新增 AI 协同智商、批判性思维优先级

## 9.x

### New
- v9.2: Silver Medalist 管道管理
- v9.1: 短名单质量控制、客户长期人才顾问服务、候选人多样性评估
