---
name: leafather-report-audit
slug: leafather-report-audit
displayName: 数鉴-报告审计
display_name: "数鉴-报告审计"
display_name_en: "Report Number Audit"
version: 3.6.1
license: MIT
author: leafather
summary: "报告里的每个数字，要么能追到出处，要么不许发。不改出报告的方式：跑报告时自动录像记账，事后审计；结论强制披露审计覆盖率，查得太少不许说通过。"
tags: ["数字审计", "数据报告", "可追溯", "交付质检", "报告自动化", "数据治理", "数据质量", "审计", "report-audit", "data-audit", "traceability"]
agent_created: true
description: "数鉴-报告审计技能。做报告时就用：算数即记账，交付前对账。两条路产同一本账本——①有指标定义（ledger.yaml + indicators.yaml）→ rla_ledger 生成账本，模板里写 [[id]] 渲染，数字天生带出处、数据变了拒绝渲染；②有脚本跑数 → rla_report 录像自动记账。审计时把报告数字逐个追溯回账本，追不到即拦；覆盖率不足不许判定通过。适用三时机：出报告（算数记账）、改报告（改完拿现有账本重核，防只改一份漏其余）、查问题（数字对不上、客户质疑出处）。触发词：出数据报告、做报告、改报告、更新数据、数据补录、口径调整、重新生成报告、交付前检查、数字对不上、可追溯、审计报告。项目里已有 ledger.yaml / indicators.yaml 时，改动报告前后都应复核。产出四件套：audit.md 结论、audit.html 审计凭证、evidence.csv 证据清单、manifest.json 机检回执。不适用：改的是纯文字（不含数字）、或报告里没有需要追溯的指标。"
description_zh: "数鉴-报告审计技能。做报告时就用：算数即记账，交付前对账。两条路产同一本账本——①有指标定义（ledger.yaml + indicators.yaml）→ rla_ledger 生成账本，模板里写 [[id]] 渲染，数字天生带出处、数据变了拒绝渲染；②有脚本跑数 → rla_report 录像自动记账。审计时把报告数字逐个追溯回账本，追不到即拦；覆盖率不足不许判定通过。适用三时机：出报告（算数记账）、改报告（改完拿现有账本重核，防只改一份漏其余）、查问题（数字对不上、客户质疑出处）。触发词：出数据报告、做报告、改报告、更新数据、数据补录、口径调整、重新生成报告、交付前检查、数字对不上、可追溯、审计报告。项目里已有 ledger.yaml / indicators.yaml 时，改动报告前后都应复核。产出四件套：audit.md 结论、audit.html 审计凭证、evidence.csv 证据清单、manifest.json 机检回执。不适用：改的是纯文字（不含数字）、或报告里没有需要追溯的指标。"
description_en: "Report audit skill that runs while you build the report, not just before delivery. Numbers are recorded in a ledger at calculation time and reconciled at handover. Two paths feed one ledger: (1) with metric definitions (ledger.yaml + indicators.yaml), run rla_ledger, then render numbers via [[id]] placeholders so each figure carries provenance and stale data refuses to render; (2) with a build script, rla_report records SQL automatically. Pandas-only projects use rla_note.note(). Audit traces each number back to the ledger and blocks delivery when it cannot be traced; it never passes when coverage is insufficient. Use when producing a report, revising a report, or investigating a disputed number. Triggers: build report, revise report, update numbers, backfill data, change caliber, regenerate report, pre-delivery check, number mismatch, traceability. Not applicable: text-only edits with no numbers."
---

# leafather-report-audit｜数鉴-报告审计

> 一句话：**报告里的每个指标数字，要么能追溯到底，要么不许发。**

---

## 平台说明

- **Windows**：把示例里的 `python3` 换成 `python`（或 `py`）。
- **技能目录不要带空格**：Node 侧靠 `NODE_OPTIONS` 注入，路径带空格会失效（Python 侧不受影响）。
- **duckdb 报 `DLL load failed ... 应用程序控制策略已阻止此文件`**：被安全策略拦了，不是没装。
  把 site-packages 下的 `duckdb` 加白；或不用 duckdb —— 走 `--command`（自带 `cmd_sqlite.py`），自检自动降级。
缺什么会直接告诉你：`python3 scripts/deps_check.py`

---

## 30 秒看它能干什么

```bash
python3 scripts/rla_selftest.py
```

自造小库跑 7 个用例：正确报告通过、改数被拦、跨件被抓、泄漏被拦、编数被拦，
外加"多文件不一致要报并标红""产物完整且编号稳定"。
**7/7 通过，说明它真的在检查，不是一个绿灯装饰。** 没有 duckdb 会自动降级到 sqlite3，同样 7/7。

---

## 它解决什么问题

真实事故：一份报告 6 个交付件，数据补录 1 条后池子从 15,596 变成 15,597，只有 1 个件更新，
另 5 个还是旧数字；而"自检报告"写着 24/24 PASS —— **它比的是写死的常数，不是对账**。

这类错误人眼看不出来，"自检"更看不出来。唯一可靠的办法：**把每个数字的出处记下来再对账**。

---

## 三步上手

### 1. 用一条命令跑报告（推荐入口）

```bash
python3 scripts/rla_report.py --out report.md --ledger ledger.json \
    --mount "data=/path/your.parquet" --report-name "某报告" --data-as-of 2026-09-30 \
    -- python3 build_report.py
```

它做三件事：**跑你的报告脚本（自动录像）→ 生成账本 → 审计报告**。
你的 `build_report.py` **一行都不用改**——钩子藏在子进程里，记录它跑过的每条 SQL。

### 2. 看结论

`audit.md` 的第一屏长这样（v3.5.0 起）：

```
## 一句话结论
**✅ 通过**　—　覆盖率 96%（追溯 72 / 应审 75）

## 判定依据
| 应审数字 | 75 个（另有 12 个日期/序号/年份，按规则豁免） |
| 追溯到出处 | 72 个（指标 70 / 支撑数据 2） |
| 复算（重跑 SQL 对数） | 34 / 34 条 |
| 检查执行情况 | 复算 34/34｜跨件一致 2 份｜必现 跳过（未配置 must）｜泄漏 1 份客户版 |
| 覆盖率红线 | 90%（本次 96%，✅ 达标） |
```

**两处必须看**：「审计覆盖率」= 数字到底查了多少；「检查执行情况」= 哪些检查真跑了、哪些跳过。
不看，你手里可能只是一份"空转的通过"。

拦下的问题会**带改法**，不用自己猜怎么修：
```
1. **来源不明**：99 @ report_c.md L3
   > 怎么改：①在账本里补一条（可用 --export-missing 生成模板）；②把报告这个数删掉或换成有出处的数
```

### 3. 想更准？给数字配个稳定身份

可选。项目根放一个 `metrics.yaml`：

```yaml
metrics:
  - id: ship.amt_net
    label: 净发货额
    unit: 元
    caliber: 含税金额，扣退货
    match_sql: "sum(amt_tax)"      # 子串匹配录像里的 SQL
```

不写也能跑（label 靠 SQL 猜）。写了之后：label 确定、跨报告能认出同一指标、客户版台账能直接交付。

---

## 两条路，同一本账本（v3.6.0）

报告怎么产出的，决定你走哪条路 —— **两条路写出的是同一种账本**，审计器不区分。

| 你的项目 | 入口 | 账本怎么来 |
|---|---|---|
| 有指标定义（`ledger.yaml` + `indicators.yaml`，SQL 写在里面） | `rla_ledger.py` | 按定义跑一遍，值自动入账 |
| 有出数脚本（pandas / SQL 跑数） | `rla_report.py` | 录像自动记账 |
| **纯 pandas 计算（没有 SQL）** | `rla_report.py` + `rla_note.note()` | **手动登记一行**（录像看不见 groupby） |
| 两者都有 | 都用 | 同一本账本，双保险 |
| 手写 / 外部生成 | `rla_audit.py --files` | 事后扫数字配账本 |

### 走「pandas」这条路（没有 SQL 的项目）

`pd.read_parquet()` 之后做 groupby / merge / apply 算出来的数，录像钩子**一条都录不到**。
这时在脚本里手动登记一行：

```python
from rla_note import note

pool = len(df[df.tag == "高血压"])
note("htn.pool", pool, label="高血压人群", unit="人",
     caliber="主标签=高血压，排除测量", expr="len(df[df.tag=='高血压'])")
```

**`label` 一定要写人话**（"高血压人群"），别用 id 当 label——报告里写"高血压人群 7 人"，
审计靠 label 锚定才认得出；label 写成 `htn.pool` 就锚不住，覆盖率会掉到 0%。

这类条目标 `verifiable: false`：能证明"报告里的数来自这次计算"，但**不能复算**（没有 SQL），
结论里会单独标注。

### 走「定义」这条路（推荐新项目）

```bash
python3 scripts/rla_ledger.py          # 读 ledger.yaml + indicators.yaml → 生成 ledger.json
python3 scripts/rla_render.py --ids    # 看账本里有哪些指标
```

项目根放两个文件：

```yaml
# ledger.yaml —— 所有"项目相关"的东西都在这
meta:  { name: 9月发货小结, cap: '2026-09-30' }
pool:  { where: "sale_date <= DATE '{{cap}}'" }     # 换主题只改这一处
source: { adapter: duckdb, duckdb: { path: data/x.duckdb },
          fingerprint: { files: ['data/x.duckdb'] } }   # 数据指纹，用来判断账本是否过期
catalog: metrics/indicators.yaml
```

```yaml
# metrics/indicators.yaml —— 指标定义（带 SQL）
indicators:
  - id: rt.ship.docs
    name: 发货单据数
    unit: 单
    caliber: 去重 doc_no 数
    sql: "SELECT COUNT(DISTINCT doc_no) AS v FROM raw_shipment_detail WHERE sale_date <= DATE '{{cap}}'"
invariants:                       # 指标之间的大小关系，违反算 FAIL
  - { left: rt.ship.docs, op: '<=', right: rt.ship.rows, name: 单据数不超过明细行数 }
```

**报告模板里别写死数字，写 `[[指标id]]`：**

```markdown
本期发货 [[rt.ship.docs]] 单，最大客户占比 [[P:rt.ship.top1_share]]。
```

渲染（命令行或代码里 `import rla_render as RN; RN.sub(text)`）：

```bash
python3 scripts/rla_render.py --sub "本期发货 [[rt.ship.docs]] 单"
```

**渲染前会校验数据快照**：数据文件变了但没重算账本 → 直接拒绝渲染，不给你一个"看起来对但是旧数"的文档。

好处：数字从生成那一刻就带出处，事后不用"扫数字猜配对"。

---

## 跑完你会拿到什么（四件产出物）

默认一次产出四件，**各有各的读者，别混着发**：

| 产出物 | 给谁看 | 里面有什么 | 能不能外发 |
|---|---|---|---|
| `audit.md` | **审报告的人**（老板/PM） | 一句话结论 + 判定依据 + 拦下的问题（带改法）+ 需复核项 + 局限 | 可直接附录 |
| `audit.html` | **出报告的人**（分析师） | 全量证据（可点开定位）、SQL 与复算值并排、跨件矩阵、凭证元信息 | ❌ 含内部口径与 SQL，**仅内部** |
| `evidence.csv` | **要自己再筛的人** | 一行一个数字（21 列），Excel 可筛可排序，带 BOM 不乱码 | ⚠️ 含 caliber/sql 时不外发 |
| `manifest.json` | **合规 / 半年后追责** | 审计编号、环境指纹、输入 hash、复现命令、结论、完整性自检 | ✅ 可外发（路径已脱敏） |

三个开关（默认全开，都是"关掉"用的）：

- `--no-html`：不出 `audit.html`
- `--no-manifest`：不出 `evidence.csv` 与 `manifest.json`（回执属机检凭证，与展示层解耦）
- `--no-write`：一个文件都不落，只在终端打印结论

**审计编号**形如 `RLA-20260930-a1b2c3d4`（数据截止日 + 账本 hash 前 8 位），
同一账本 + 同一数据截止日**永远同一个编号** —— 拿它就能查"这份凭证是哪次审计"。

---

## Node 出的报告怎么接

```bash
python3 scripts/rla_report.py --out report.md --ledger ledger.json \
    --mount "data=/path/your.parquet" --report-name "某报告" --data-as-of 2026-09-30 \
    -- node build_report.mjs --out report.md
```

**业务代码一行都不用改**——钩子靠 `NODE_OPTIONS=--require` 挂进 Node 进程。

三条前提：业务项目里有 `@duckdb/node-api`（找不到用 `RLA_NODE_MODULES` 指）、目录不带空格、只支持 duckdb。

位置参数、命名参数、prepared+bind、stream 都能录，**参数会被内联成可复算的 SQL**。
追不到内联的类型会打 `bound_unresolved`，审计报未就绪，不静默放过。
**不做常驻服务内的分段录像**（服务常驻时"哪一次是出报告"没有边界）——细节见 `references/usage-notes.md`。

---

## 数据源怎么接（详细见 `references/usage-notes.md`）

| 你的数据 | 怎么写 |
|---|---|
| parquet / csv | `--mount "data=/path/x.parquet"` |
| duckdb 库（多表） | `--mount "=/path/x.duckdb"`（等号左边留空 = 当主库） |
| MySQL / PG / 任何库 | `--command "python3 my_query.py"`（SQL 进 stdin、CSV 出 stdout） |

**非 duckdb 也能用**：复算走 `--command`，技能自带 `scripts/cmd_sqlite.py` 当例子。

---

## 判定三态

| 情况 | 判定 | 退出码 |
|---|---|---|
| 全可追溯 + 复算一致 + 覆盖率够 | ✅ 通过 | 0 |
| 未复算 / 弱锚定 / 跨件写法不同 / 泄漏未配置 / **覆盖率<90%** / **零指标** / **policy 没归类** | ⚠️ 需人工复核 | 3 |
| 账本与复算不符 / 报告有账本外的指标数字 / 跨件不一致 / 客户版泄漏 | ❌ 不通过 | 1 |
| 账本字段缺失 / 文件不存在 / 数据源挂不上 | ⛔ 未就绪（**不算通过**） | 2 |

**优先级：FAIL > REVIEW > PASS。** 严格发布流只认 0；务实流 0 发、3 附结论后发、1 不发。

---

## 六个最常见的坑（详细见 `references/usage-notes.md`）

1. **账本 `value` 用基本单位**：写 `340000 元`，别写 `34.0 万元`
2. **`--files` 相对「账本所在目录」**，不是当前目录（常见错：`deliverables/deliverables/r.md`）
3. **值 < 10 的小数字天然不可区分**，上下文没锚定就判「无法判定」
4. **PPT / 图片里的数字扫不到**，结论会标「未覆盖 N 张图片」——事后审计的天花板
5. **数字分三类**：交付指标（必须可追溯）/ 支撑数据（`role: support`）/ 技术参数（`audit-skip` 圈起）
6. **「通过」不等于「都查了」**：永远先看「审计覆盖率」

---

## 边界（不吹）

没跑过 SQL 的数字**验不了**（只能判"来源不明"）；**口径对不对不管**（防不了"一开始就想错"）；
**图片里的数字管不了**（只标"未覆盖"）；**分类可能误判**（结论里列了豁免明细供抽查）。
`audit.html` 与 `evidence.csv` 里含**内部口径与 SQL 原文**，默认只给内部人看，别随报告发给客户。

---

## 文件

| 文件 | 作用 |
|---|---|
| `SPEC.md` | **数字身份证契约** —— 第三方照这个交账，不用我们的脚本也能被审 |
| `policy.yaml` | 审计策略（舍入、哪些算 FAIL/REVIEW、必现、泄漏规则）。**未知键会报错**，拼错不会静默失效 |
| `scripts/rla_report.py` | 一条命令：录像 → 记账 → 审计 |
| `scripts/rla_selftest.py` | 自带数据自检（30 秒证明它真的在检查） |
| `scripts/rla_audit.py` | 审计内核：复算 + 配对 + 三态判定 + 七道检查 |
| `scripts/rla_ledger.py` | **从指标定义生成账本**（ledger.yaml + indicators.yaml，v3.6.0） |
| `scripts/rla_note.py` | **非 SQL 数字登记**：`note(id, value, label=..., expr=...)`（v3.6.0） |
| `scripts/rla_health.py` | **记账体检**：跑完脚本告诉你哪几条数会没出处（v3.6.0） |
| `scripts/rla_render.py` | **渲染层**：`[[id]]` → 数字，渲染前校验数据快照（v3.6.0） |
| `rla_track.py` / `rla_collect.py` / `rla_track_node.cjs` | 录像（Python）/ 记账 / 录像（Node 钩子） |
| `examples/build_report.mjs` | Node 出报告的最小可用示例（照抄即可） |
| `examples/cross-file-build.py` | 多交付件 demo 第一步：造数据 + 账本 + 两份交付件（**零依赖**，不用 duckdb） |
| `examples/cross-file-demo.md` | demo 说明：漏改怎么被抓、矩阵怎么读、能力边界 |
| `scripts/metrics.py` / `rla_xlsx.py` | `metrics.yaml` 认领 / 内部+客户双版 Excel 台账 |
| `scripts/rla_derive.py` / `rla_replay.py` | 派生候选建议 / 换策略后的判决回放 |
| `scripts/deps_check.py` | 依赖体检（缺包/DLL 被拦时给人话，不给 traceback） |
| `scripts/cmd_sqlite.py` | `--command` 接法的现成例子（SQL→CSV，背后 sqlite3） |
| `references/usage-notes.md` | 细节：数据源接法、六个坑、Node 细节、依赖降级 |

**非 duckdb 用户**：写 10 行把 SQL 变成 CSV 就能接（`--command`），例子见 `references/usage-notes.md`。

**依赖**：Python 3.10+、`duckdb`、`pyyaml`；解析 docx/pptx/xlsx/html 另需 `python-docx`、`python-pptx`、`openpyxl`、`beautifulsoup4`（缺了只是少支持一种格式，不影响主流程）。
**Node 报告**另需业务项目自带 `@duckdb/node-api`（本技能不替你装驱动）。
