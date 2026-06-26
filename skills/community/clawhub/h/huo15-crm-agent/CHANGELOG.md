# Changelog

> **绿火 · CRM 销售员智能体** — 行业领域包可插拔的拓客 / 获客 / 跟进引擎。

本项目版本变更记录。遵循 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/) 与 [SemVer 2.0](https://semver.org/lang/zh-CN/)。

## [0.2.1] - 2026-05-02

### Fixed

- **SKILL.md 瘦身**：v0.2.0 发版时 SKILL.md 17.8KB 触发 ClawHub 嵌入器 8192 token 上限，clawhub publish 失败。本版砍 35% 至 11.6KB（保留 frontmatter 触发词、工具速查、所有协同 workflow、SOP / 画像 / 历法 / 信号词典 / 配置 / 红线，砍详细 workflow 案例细节与 12 月历法详表）。
- npm 0.2.0 已发出但 ClawHub 0.2.0 缺失，本 hotfix 让两个 registry 同步到 0.2.1。

### Notes

- 不改任何工具行为 / 接口；纯文档瘦身 + 版本号 +1 patch。
- npm 0.2.0 仍可见但不再是 latest。

---

## [0.2.0] - 2026-05-02

### Added — 拓客 / 获客 闭环（按调研报告 takeaways）

- **`sales_company_search`** —— 通过企查查 OpenAPI 搜索潜在客户企业（按行业 / 区域 / 关键词 / 注册资本）。返回候选名单 + 建议 nextActions 喂给 sales_lead_score 批量打分。
- **`sales_company_detail`** —— 单家企业的工商详情（注册资本 / 法人 / 经营范围 / 关联企业 / 近期变更 / 风险信号）。输出可喂给 sales_lead_brief 做画像、或喂给 sales_intent_signals 抽取意向。
- **`sales_intent_signals`** —— 从用户喂入的原文（招聘 / 招标 / 工商变更 / 新闻 / 风险通告）中识别财税意向信号。基于内置《财税行业获客信号词典》（5 大类 40+ 条），命中加权打分，输出"高 / 中 / 低 / 无"意向等级。
- **新 client**：`src/clients/qichacha.ts` —— 企查查 API 客户端（瘦客户端：fetch + HMAC，未配置 / 网络异常时 graceful fallback，不引入 child_process）。
- **新 domain 模块**：`src/domain/signal_dictionary.ts` —— 财税意向信号词典（5 大类：招标 / 招聘 / 融资 / 经营变更 / 风险，40+ 词条 + 权重 + 财税解读）。

### Changed

- **`sales_pitch`** 升级 —— 新增 `signals` 参数。传入 sales_intent_signals 输出的具体信号后，话术会基于强度最高的信号生成场景化措辞（参考 Apollo AI Research 模式：信号驱动话术 vs 模板话术，14 天预约率 +36%）。
- **配置项**新增 3 项：`qichacha_api_key` / `qichacha_secret_key` / `qichacha_base_url`（可选）。未配置时 sales_company_* 两个工具优雅降级，其他 6 个工具不受影响。
- **index.ts logger** 信息更新为 8 个工具。

### Architecture / 设计取舍

参考调研对象：探迹 Tungee、企查查、卫瓴科技、Apollo.io、ZoomInfo（详见 `docs/v02-prospect-research.md`）。

- ✅ **借鉴企查查作为工商底座**：财税获客 90% 信号依赖工商数据，绿火不自建。
- ✅ **借鉴探迹 / ZoomInfo 的意向信号识别**：但用本地词典 + 规则匹配，不调用 LLM 解析（绿火不绑定 LLM token 成本到工具内）。
- ✅ **借鉴 Apollo AI Research 的信号驱动话术**：让 sales_pitch 接受 signals 直接生成具体措辞。
- ❌ **避开自建爬虫**（CLAUDE.md §6.2 不引 child_process / 不内嵌 puppeteer）；公开网搜由用户的 huo15-searxng / WebFetch 执行。
- ❌ **避开复制 wecom 触达**（CLAUDE.md §11.4 不重复龙虾原生功能）；触达交给 @huo15/wecom。
- ⏸ **暂搁自建联系人 / 邮件库**（v0.3+ 或不做）—— 绿火定位是"销售员"，不是"数据公司"。
- ⏸ **暂搁自动外呼 / AI 通话** —— 合规风险高 + 重资产，财税场景慎做。

### Notes

- 兼容基线：`compat.pluginApi: ">=2026.2.24"`（不变）。
- 不引入 `child_process`，不引入新 npm 运行时依赖（`fetch` / `crypto` 都是 Node 25 内置）。
- 8 个工具命名仍 `sales_*` 前缀；行业切换不改工具名。
- **本版本为 branch 草稿，未发 npm / ClawHub**。等用户验过反馈再合 main → 发 0.2.0 正式版（按 CLAUDE.md §7 ClawHub 六坑流程）。

---

## [0.1.0] - 2026-05-02

### Added

- 初始化 `huo15-crm-agent` 仓库与脚手架。智能体品牌"**绿火**"。
- 5 个通用销售工具（行业无关，行为由 `industry_domain` 驱动）：
  - `sales_lead_score` — 线索批量打分（高/中/低 + 0-100 分 + 推荐服务 + 切入 hook）。
  - `sales_lead_brief` — 单线索全景简报（公司画像 + 痛点推断 + 决策人优先级 + 首次接触话术草稿）。
  - `sales_pitch` — 场景化话术生成（首次接触 / 二次跟进 / 价格异议 / 拖延决策 / 转介绍 / 促成 共 6 场景 × 3 语气）。
  - `sales_followup_plan` — 阶段化跟进计划（5 阶段销售漏斗 → 14 天动作清单 + 可喂给 huihuoyun-odoo 的 mail.activity 草稿）。
  - `sales_industry_scan` — 行业历法扫描（按月/按季的政策节点 + 配套外呼话术 hook）。
- v0.1 内置 **finance_tax 领域包**（代账 / 审计 / 税务筹划 / IPO 辅导）：5 类客户画像、汇算清缴/高新认定/股改等历法、财税专属话术骨架。
- 内嵌 SKILL.md：销售 SOP（5 阶段）、客户分层（5 类）、话术骨架、合规红线、与 huihuoyun-odoo / wecom 的协同 workflow。
- 配置项：`industry_domain` / `services` / `region` / `tone` / `company_brand` / `odoo_team_hint`。

### Architecture

- **绿火**只做"思考层"：打分、画像、话术、跟进 SOP、行业历法。
- **执行层**完全交给同时已装的 `@huo15/huo15-huihuoyun-odoo`（v1.20+）—— 写线索 / 建活动 / 发邮件 / 群发消息均由它执行。
- 与辉火云 Odoo19 企业版 CRM 解耦协同，不重复造连接器。

### Notes

- 兼容基线：`compat.pluginApi: ">=2026.2.24"`，与 huihuoyun-odoo 同基线。
- 不引入 `child_process`，符合 CLAUDE.md §6.2 红线。
- 工具命名一律 `sales_*` 前缀 —— 行业切换不改工具名，只改 `industry_domain` 配置。
- v0.2 计划：抽离 `src/domain/finance_tax/` pack 子目录，新增 education / healthcare / it_services 等领域包。
