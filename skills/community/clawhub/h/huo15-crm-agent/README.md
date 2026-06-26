# 绿火 · CRM 销售员智能体

> `@huo15/crm-agent` —— 拓客 / 获客 / 客户画像 / 销售话术 / 跟进 SOP 一体的 OpenClaw 领域插件。
> 行业领域包可插拔；v0.1 内置 **finance_tax** 财税领域。
> 与辉火云 Odoo19 企业版 CRM 解耦协同 —— 绿火出策略，[@huo15/huo15-huihuoyun-odoo](https://www.npmjs.com/package/@huo15/huo15-huihuoyun-odoo) 落地写入。

---

**打破信息孤岛，用一套系统驱动企业增长**
**加速企业用户向全场景人工智能机器人转变**

| 🏫 教学机构 | 👨‍🏫 讲师 | 📧 联系方式                                       | 💬 QQ群     | 📺 配套视频                                         |
| ------- | -------- | --------------------------------------------- | ---------- | ----------------------------------------------- |
| 逸寻智库    | Job      | [support@huo15.com](mailto:support@huo15.com) | 1093992108 | [📺 B站视频](https://space.bilibili.com/400418085) |

---

## 一、绿火是谁

**绿火**是青岛火一五信息科技有限公司旗下的 CRM 销售员智能体。它不是一个新的 Odoo 连接器、不是一个 CRM 替代品 —— 它是销售员的"思考层"：

- 给一批潜在客户打分、推优先级、推服务方向
- 给单条线索做客户画像、推断痛点、列决策人优先级
- 写销售话术（6 场景 × 3 语气：首次接触 / 二次跟进 / 价格异议 / 拖延决策 / 转介绍 / 促成）
- 规划 14 天阶段化跟进 SOP（5 阶段销售漏斗）
- 按月扫描行业历法，找到当下最强的话术 hook（汇算清缴期 / 高新认定窗口 / 年终筹划 …）

**绿火不直连 Odoo**——所有"创建线索 / 安排活动 / 写沟通历史 / 发邮件 / 群发"动作由用户已装的 [@huo15/huo15-huihuoyun-odoo](https://www.npmjs.com/package/@huo15/huo15-huihuoyun-odoo)（v1.20+，204 个 Odoo 工具）执行。

---

## 二、安装

```bash
# 通过 OpenClaw 龙虾装（推荐）
openclaw plugins install @huo15/crm-agent

# 同时确保 huihuoyun-odoo 已装并已连接到辉火云 Odoo19
openclaw plugins install @huo15/huo15-huihuoyun-odoo
```

或在 OpenClaw 中说："**帮我装绿火 CRM 销售员**"。

---

## 三、配置

`openclaw.plugin.json` 顶层 `config`：

```json
{
  "industry_domain": "finance_tax",
  "services": ["代账", "审计", "税务筹划", "财税顾问"],
  "region": "青岛",
  "tone": "warm",
  "company_brand": "青岛火一五信息科技有限公司",
  "odoo_team_hint": "财税获客团队"
}
```

| key | 说明 |
|---|---|
| `industry_domain` | 行业领域包，v0.1/v0.2 仅 `finance_tax` |
| `services` | 提供的服务方向（影响打分权重） |
| `region` | 默认服务区域（话术地域化 hook） |
| `tone` | 默认话术语气（formal / warm / neutral） |
| `company_brand` | 对外品牌名，话术中代指甲方 |
| `odoo_team_hint` | 可选。CRM 创建线索时的销售团队名提示 |
| `qichacha_api_key` | **v0.2 起**。企查查 OpenAPI Key（[申请](https://openapi.qcc.com/)） |
| `qichacha_secret_key` | **v0.2 起**。企查查 Secret Key（HMAC 签名） |
| `qichacha_base_url` | **v0.2 起**。可选，默认 `https://api.qichacha.net` |

---

## 四、八个工具速查

### v0.1（处理已有 leads）

| 工具 | 干什么 |
|---|---|
| `sales_lead_score` | 批量给潜在客户打分（0-100 + 高/中/低 + 推荐服务 + 切入 hook） |
| `sales_lead_brief` | 单条 lead 全景简报（画像 + 痛点 + 决策人优先级 + 首次接触话术草稿） |
| `sales_pitch` | 6 场景 × 3 语气话术生成 + 配套下一步动作建议（v0.2 起支持 signals 信号驱动） |
| `sales_followup_plan` | 5 阶段销售漏斗 → 14 天动作清单 + 可喂给 odoo_create_activity 的草稿 |
| `sales_industry_scan` | 行业历法（按月）+ 时点 hook |

### v0.2 新增（拓客 / 获客闭环）

| 工具 | 干什么 | 前置 |
|---|---|---|
| `sales_company_search` | 企查查搜潜在客户企业（行业 / 区域 / 关键词 / 注册资本） | 配 `qichacha_api_key` |
| `sales_company_detail` | 单家企业的工商详情（注册资本 / 法人 / 经营范围 / 关联 / 变更 / 风险） | 配 `qichacha_api_key` |
| `sales_intent_signals` | 从原文识别财税意向信号（5 大类 40+ 词条 + 加权打分） | 无 |

未配置 `qichacha_api_key` 时前两个工具优雅降级，其他 6 个不受影响。

详细触发短语、协同 workflow、合规红线见 [SKILL.md](./SKILL.md)。

---

## 五、协同链路示例

### 5.1 批量获客 → 写入 Odoo CRM

```
用户："这 50 家潜在客户名单，帮我打分并入库。"
  ① 绿火 sales_lead_score → 打分 + nextActions
  ② 用户确认后
  ③ huihuoyun-odoo 的 odoo_crm_create 批量写入
  ④ 绿火 sales_followup_plan(stage='cold') → 14 天 SOP
  ⑤ huihuoyun-odoo 的 odoo_create_activity 批量排活动
```

### 5.2 单 lead 深耕

```
用户："这个王总，公司是某某医疗器械，刚加微信，下一步打几句？"
  ① 绿火 sales_lead_brief → 画像 + 首次话术草稿
  ② 绿火 sales_pitch(scene='first_contact') → 3 个语气变体
  ③ 用户挑一个
  ④ huihuoyun-odoo 的 odoo_message_post 写到 lead 沟通历史
```

### 5.3 ⭐ v0.2 新链路：从无到有挖客户（企查查 → 信号 → 入库）

```
用户："给我找 30 家青岛医疗器械公司，要财税服务可触达的，灌进 CRM 跟进。"
  ① 绿火 sales_company_search → 企查查返回 30 家候选
  ② 对前 10 家高优 sales_company_detail → 详情画像
  ③ sales_intent_signals(raw_texts=[business_scope, recent_changes...]) → 信号识别
  ④ sales_lead_score 综合打分
  ⑤ huihuoyun-odoo 的 odoo_crm_create 批量入库
  ⑥ sales_pitch(signals=top_signals) 生成信号驱动话术
  ⑦ huihuoyun-odoo 的 odoo_message_post 写到 lead 沟通历史
  ⑧ sales_followup_plan(stage='cold') + odoo_create_activity 批量排活动
```

前提：配好 `qichacha_api_key` + `qichacha_secret_key`（[申请](https://openapi.qcc.com/)）。
未配置时退化方案：用 `huo15-searxng` / `WebFetch` 拉公开企业名单，再走 `sales_intent_signals` → `sales_lead_score` 链路（数据源换、链路一致）。

### 5.4 时点主题群发（汇算清缴 / 年终关账）

```
用户："4 月汇算清缴高峰，给我做一波客户群触达。"
  ① 绿火 sales_industry_scan → top_hooks_now
  ② huihuoyun-odoo 的 odoo_search 拉出 stage='introduced' 的 leads
  ③ 对每条 lead 绿火 sales_pitch(scene='reengage', hook=...)
  ④ huihuoyun-odoo 的 odoo_send_email 或企微/钉钉/飞书工具批量发送
```

---

## 六、领域包与未来扩展

**v0.1 内置 finance_tax 领域包**包含：

- 5 类客户画像：初创小微 / 成长成熟 / 上市辅导 / 集团大型 / 外贸外资
- 财税专属话术骨架（含汇算清缴 / 高新认定 / 股改 / 出口退税等 hook）
- 全年财税历法（汇算清缴 3-5 月、高新申报 6 月、年报 1 月、年终筹划 11-12 月）
- 16+ 痛点关键词权重打分（"汇算清缴"、"高新"、"股改"、"稽查"、"出口退税" …）

**v0.2 已完成（拓客闭环）**：
- ✅ 企查查 OpenAPI 工商底座（sales_company_search / sales_company_detail）
- ✅ 财税意向信号识别（sales_intent_signals + 内置词典 40+ 条）
- ✅ sales_pitch 升级 signals 参数（信号驱动话术）

**v0.3+ 路线图**：
- 抽 `src/domain/` → `src/domain/finance_tax/` pack 子目录
- 新增领域包：`education`（K12 / 留学）/ `healthcare`（医院 / 诊所）/ `it_services`（SaaS / 集成商 / 数字化转型）
- `industry_domain` 配置切换；工具名 `sales_*` 不变，行为按 pack 切换
- 与 `huo15-xiaohongshu` 联动：高优 lead 自动产出小红书种草内容草稿
- 与 `huo15-wecom-plugin` 联动：批量个性化群发（按 sanitizer 红线走）
- 信号词典扩展（探迹 2000+ 行业垂直深化思路）
- 数据源备选：天眼查 / 启信宝

---

## 七、设计红线

1. **不直连 Odoo** —— 所有 CRM 写入交给 huihuoyun-odoo，避免双账本与连接器维护负担
2. **不静默执行** —— 工具返回的 `nextActions[].args_draft` 都需要用户确认
3. **不广播字面量** —— 不输出 `@all` / `*` / `tag:*`，群发 target 必须用户当前会话明确指定
4. **不承诺金额** —— 话术用比例（"省 25% 所得税"），不写绝对值（"保证省 100 万"）
5. **不过度抽象** —— v0.1 不引入 domain pack 抽象层，等真要做第二个领域时再重构
6. **不引入 child_process** —— 符合 CLAUDE.md §6.2 红线
7. **`compat.pluginApi` 永远 ranged** —— 当前 `>=2026.2.24`，与 huihuoyun-odoo 同基线

---

## 八、技术栈

- TypeScript 5.5+，ES2022 + ESM
- `openclaw/plugin-sdk` (peerDependency `>=2026.2.24`)
- 零运行时依赖（除 OpenClaw 自身）
- 不引入数据库、不写本地文件、不开网络连接 —— 所有"重活"交给 huihuoyun-odoo

---

## 九、仓库与版本

- **主仓库**（cnb.cool / 火一五 marketing_department 组）：<https://cnb.cool/huo15/marketing_department/huo15-crm-agent>
- **GitHub 镜像**：暂未启用。后续如需启用，先在 GitHub `zhaobod1` 账号建 `huo15-crm-agent` repo，再执行 `git remote add github git@github-zhaobod1:zhaobod1/huo15-crm-agent.git && git push -u github main`。在此之前 **仅 push cnb.cool**（`git push origin main`），不要执行 GitHub 相关 push 命令。
- **当前版本**：v0.2.1（2026-05-02 拓客闭环 hotfix — 接入企查查 + 信号识别 + 信号驱动话术；SKILL.md 瘦身适配 ClawHub 8192 token 嵌入限）
- 变更日志见 [CHANGELOG.md](./CHANGELOG.md)。

---

## 十、许可

MIT。

---

**公司名称：** 青岛火一五信息科技有限公司

**联系邮箱：** [postmaster@huo15.com](mailto:postmaster@huo15.com) | **QQ群：** 1093992108

---

**关注逸寻智库公众号，获取更多资讯**
