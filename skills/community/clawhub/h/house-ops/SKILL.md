---
name: house-ops
description: >-
  驱动 agent 的一体化购房决策体系：需求画像、政策税费、城市规划、市场动态四路输入合成同一套判断；
  扫描挂牌、用成交价锚点交叉验证、六维评分，产出 Markdown 报告与 TUI 操作台。每个数字标注来源档位，
  无法证实存在的房源整份作废而非降权。当用户粘贴房源链接或描述、想明确购房需求、速筛/扫描/对比房源、
  深挖某套房源、审合同、记录带看、要谈判沟通建议或管理关注清单时使用。
  English: Agent-driven home-buying decision system — needs profile, policy and taxes, urban planning
  and market movement folded into one judgment; scans listings, cross-checks asking price against
  deal-price anchors, scores six dimensions, writes Markdown reports and a TUI console. Every figure
  carries a source tier; a property that cannot be verified is voided, not downgraded. Use when the
  user pastes a property listing URL or description, wants to clarify home-buying needs, triage, scan,
  compare or deep-dive listings, review a purchase contract, record a viewing, ask for negotiation
  advice, or manage the watchlist.
arguments: mode
user-invocable: true
argument-hint: "[intake | triage | evaluate | scan | deep-dive | compare | visit | negotiate | contract | watchlist | stats | doctor]"
---

# house-ops 技能路由器

## Project Root 解析

从本 SKILL.md 所在位置向上查找同时包含 `AGENTS.md` 和 `modes/` 的目录，记为 PROJECT_ROOT。

**找不到时**（本技能被装进 Agent 受管技能目录，如 `~/.claude/skills/house-ops/`，那里没有 `AGENTS.md`）
退而查找同时包含 `modes/` 和 `scripts/` 的目录作为 PROJECT_ROOT。

后续所有读写以 PROJECT_ROOT 为基准（不依赖当前工作目录）。

本技能目录自带指向仓库根的软链：`modes/`、`scripts/`、`scrapers/`、`templates/`、`config/`、
`docs/markets/`、`data/`、`reports/`、`package.json`——安装时会被展开为实体副本，所以**任何安装形态下
PROJECT_ROOT 都是自包含的**。只镜像运行时真正读到的部分：`docs/` 下仅 `markets/`（欧洲/亚太市场手册）
被引用，截图、虚构样例、ADR 与仓库协作文档一概不带。
仓库内工作时解析到仓库根（那里有 `AGENTS.md`）；受管目录安装时解析到技能目录本身。

## 调用说明

- ZCode / Claude Code：`/house-ops <mode>`，或自然语言触发（由 AGENTS.md 的语义路由表映射）。
- 受管技能目录安装形态下可能没有 `AGENTS.md`，自然语言触发不可用，请显式使用 `/house-ops <mode>`。
- `$mode` 为空时显示下方 Discovery 菜单。

## Mode Routing

| `$mode` 值 | 加载的 mode 文件 |
|---|---|
| `intake`（别名：需求、画像、onboarding） | `modes/intake.md`（含 Step 0.5 市场轮：市场/币种/金额与面积单位/买家分档/产权形态） |
| `evaluate`（别名：评估、评级、打分） | `modes/evaluate.md` |
| `triage`（别名：速筛、快筛、triage） | `modes/triage.md` |
| `scan`（别名：扫描、采集、查成交、价格核实） | `modes/scan.md` |
| `deep-dive`（别名：深挖、调研、deep） | `modes/deep-dive.md` |
| `negotiate`（别名：谈判、沟通、约看） | `modes/negotiate.md` |
| `compare`（别名：对比、比较、横评） | `modes/compare.md` |
| `visit`（别名：带看、看房记录、复盘） | `modes/visit.md` |
| `contract`（别名：合同、认购书、审合同） | `modes/contract.md` |
| `watchlist`（别名：清单、跟踪、tracker） | `modes/watchlist.md` |
| `stats`（别名：统计、数据、分析） | `modes/stats.md` |
| `doctor`（别名：自检、体检、诊断） | `modes/doctor.md` |
| `map`（别名：地图、在地图上看、房源分布） | `modes/map.md` |
| 空 | Discovery 菜单 |
| 非命令但内容像房源（含 URL、小区名+价格等） | `modes/evaluate.md` |

无法识别的 `$mode`：列出上表让用户选择，不要猜。

## 输出语言

读 `config/profile.yml` 的 `language.output`（缺省 `zh`）。将以下指令注入本模式执行：所有面向用户的输出使用该语言（`zh`=简体中文）。金额与面积单位按同一文件的 `market:` 段：中国市场用"万元"与"元/㎡"；欧洲市场用 `market.currency` 本币整额与 `market.area_unit`（sqm/sqft）。

## Discovery 菜单

```
house-ops — 驱动 agent，帮你把房选好

  /house-ops intake      多轮对话明确你的购房需求，生成需求画像（首次使用先跑这个）
  /house-ops triage      60 秒速筛：粘贴链接快速判断值不值得完整评估
  /house-ops scan        扫描房源链接：识别平台、采集挂牌/成交价，政务数据交叉验证
  /house-ops evaluate    评估一套房源：粘贴链接或描述，输出六维评级报告
  /house-ops deep-dive   对高分房源（≥4.0）深挖：历史价格/周边/政策/竞品/产权/生活圈
  /house-ops compare     2-6 套已评估房源横向对比矩阵与场景化结论
  /house-ops visit       带看前定制核查清单 / 带看后记录复盘
  /house-ops negotiate   高分房源的核实清单、议价策略与沟通话术
  /house-ops contract    审认购书/买卖合同/补充协议/中介协议条款
  /house-ops watchlist   查看/更新候选清单与备注
  /house-ops map        房源决策地图：已评估房源按坐标上图，通勤圈与详情卡
  /house-ops stats       找房数据统计与失分/弃购模式分析
  /house-ops doctor      仓库结构与数据健康自检

也可以直接粘贴一条房源链接，我会自动走评估流程。
```

## 按 Mode 加载上下文

所有模式都先读 `AGENTS.md`（不存在则跳过；会话已注入则跳过）。然后：

1. **评估类**（`evaluate`、`triage`、`deep-dive`、`negotiate`、`compare`、`visit`、`contract`）：
   - `evaluate`/`deep-dive`/`negotiate`：按顺序读 `modes/_shared.md` → `modes/_profile.md`（存在才读）→ `modes/_custom.md`（存在才读）→ 对应 mode 文件。
   - `triage`：只读 `modes/_brief.md`（存在才读）→ 对应 mode 文件（省 token 的关键）。
   - `compare`/`visit`/`contract`：读 `modes/_profile.md`（存在才读）→ `modes/_custom.md`（存在才读）→ 对应 mode 文件 + 相关房源报告。
2. **其他**（`intake`、`watchlist`、`stats`、`doctor`）：读 `modes/_profile.md`（存在才读）→ `modes/_custom.md`（存在才读）→ 对应 mode 文件。
3. 任何模式涉及**政策事实**时按房源所在市场取表：中国大陆读 `templates/policy-notes.cn.yml`，欧洲读 `templates/policy-notes.eu.yml`（英/爱/法/荷/德/西），亚太读 `templates/policy-notes.apac.yml`（中国香港/新加坡/日本），并遵守其"用前联网核实"与"conflict 口径显式提示"规则；`contract` 另读 `templates/contract-checklist.cn.yml`。
5. `stats` 优先跑 `node scripts/stats.mjs`，失败或需要更深解读时按 mode 文件人工汇总。
6. `scan`：只读 `modes/scan.md`；先跑 `node scripts/scan.mjs detect <url>...` 获取平台与字段清单（输出按平台分组，同平台负载只读一次；单次 ≤3 条链接，超预算落 `status: partial` 并把未查项交给用户）；涉及成交价/政务数据时跑 `node scripts/scan.mjs official [关键词] [--market cn|eu|apac|<国别码>]` 查可用的公开数据源登记表（用前联网核实；各表的 tier 字段说明该源能到可靠度四档哪一层，欧洲见 `docs/markets/eu.md`，亚太见 `docs/markets/apac.md`）；可靠度档位以 `modes/_shared.md`「数据可靠度四档」节为准。

加载顺序纪律：系统层（`_shared.md`）先读，用户层（`_profile.md`、`_custom.md`、`_brief.md`）后读并覆盖系统默认。
