# 数字身份证契约 v1（report-ledger/1.0）

> 这份文件是**通用化的地基**。任何 agent、任何语言、任何报告格式，只要按这份契约交出账本，
> 就能被审计。不要求你用我们的脚本，不要求你改报告生产流程。

---

## 一、为什么是"契约"而不是"工具"

技能要通用，就不能限定"你必须用我的 Python 渲染报告"。
它只需要一件事：**每个进了报告的数字，都能说清它是谁、从哪来、怎么算的。**

说清了 → 系统能复算、能比对、能追溯。
说不清 → 判「不可追溯」，拦下。

---

## 二、账本文件

一个审计单元 = 一份 `ledger.json`（UTF-8，UTF-8 BOM 也接受）。

```json
{
  "schema": "report-ledger/1.0",
  "report": {
    "name": "减肥场景 × GLP-1 报告",
    "files": ["report.md", "deck.pptx"],
    "data_as_of": "2026-10-19",
    "generated_at": "2026-10-22T15:09:13+08:00",
    "agent": "某 agent"
  },
  "sources": [
    {
      "id": "src1",
      "type": "duckdb",
      "path": "/path/your.parquet",
      "fingerprint": "33999184f03b2063"
    }
  ],
  "numbers": [
    {
      "id": "n1",
      "label": "减肥场景池",
      "value": 15597,
      "unit": "场景",
      "display": ["15,597", "15597"],
      "numerator": 15597,
      "denominator": null,
      "caliber": "疾病名称含减肥/肥胖，COUNT(DISTINCT 场景ID)，截至 2026-10-19",
      "sql": "SELECT COUNT(DISTINCT \"场景ID\") FROM data WHERE \"疾病名称\" LIKE '%减肥%' AND \"ydate\" <= '2026-10-19'",
      "source": "src1"
    }
  ]
}
```

---

## 三、字段规则

### report（必填）

| 字段 | 必填 | 说明 |
|---|---|---|
| `name` | ✅ | 报告名称 |
| `files` | ✅ | 报告文件列表（相对账本所在目录），审计器会逐个扫 |
| `data_as_of` | ✅ | 数据截止日 `YYYY-MM-DD`。**报告里不许出现晚于它的数据**（物理约束） |
| `generated_at` | ✅ | 账本生成时间（ISO 8601） |
| `agent` | ⬜ | 谁出的报告（审计结论里会标注） |

### sources（必填，可为空数组）

| 字段 | 必填 | 说明 |
|---|---|---|
| `id` | ✅ | 唯一标识，被 numbers.source 引用 |
| `type` | ✅ | `duckdb` / `gateway` / `command` / `module` / `none` |
| `path` / `command` / `module` | ✅ | 按 type 给。`none` 表示"数据是别人给的，没法复算" |
| `fingerprint` | ⬜ | 数据文件指纹；审计时会重算比对，不一致则判「数据已变，账本过期」 |

### numbers（必填，每个进报告的数字一条）

| 字段 | 必填 | 说明 |
|---|---|---|
| `id` | ✅ | 唯一标识 |
| `label` | ✅ | 指标名（人话，比如"成交率"），用于和报告上下文配对 |
| `value` | ✅ | **数值**（机器比对用）。百分比请给百分数本体，如 73.9 |
| `unit` | ✅ | `场景` / `家` / `元` / `pct` / `pct1` / `个` … |
| `display` | ⬜ | 报告里可能的写法，字符串或数组（`"15,597"` / `"1.56万"` / `"73.9%"`）。不填则自动从 value+unit 推导 |
| `numerator` / `denominator` | ⬜ | 分子分母（比率类**强烈建议**给，这是"30 秒答出来源"的关键） |
| `caliber` | ✅ | 一句话口径（人话） |
| `sql` | ⬜ | 可复算的 SQL。**给了就必须能跑出 value** |
| `source` | ⬜ | 指向 sources.id；`sql` 存在时必填 |
| `verifiable` | ⬜ | 默认 `true`；`false` 表示"来源不可复算"，审计降级为「未验证」 |
| `origin` | ⬜ | `verifiable:false` 时必填，说明来历（如"客户提供的 2025 年审计报表"） |
| `role` | ⬜ | `indicator`（默认，交付指标）/ `support`（支撑数据：对照值、样本数、过程计算）。support 不计入"交付指标可追溯率" |
| `data_as_of` | ⬜ | **本条数字自己的数据截止日**，覆盖 `report.data_as_of`。一份报告混用多个口径时必填 |
| `derived_from` | ⬜ | 派生所依赖的指标 id 列表，如 `["n2","n1"]` |
| `expr` | ⬜ | 派生算式，如 `"n2/n1*100"`。**给了就会真算一遍验证**，不能随口编 |

---

## 四、审计器怎么用这份账本

| 检查 | 依据 | 不过的后果 |
|---|---|---|
| **账本自洽** | 每条 number 字段齐全；`verifiable:true` 必须有 sql | 退出码 2（未就绪） |
| **复算一致** | 跑 `sql`，结果 == `value` | 退出码 1（算错了 / 编的） |
| **快照未变** | 重算 `fingerprint` | 退出码 1（数据变了，账本过期） |
| **报告可追溯** | 报告里抽出的每个数字，都能匹配到某条 number | 退出码 1（有来路不明的数字） |
| **报告未失真** | 匹配上的数字，报告写法与账本值一致 | 退出码 1（报告写错了） |

**退出码**：`0` 通过｜`1` 不通过｜`2` 未就绪（**不算通过**）

---

## 四之二、一份报告混用多个口径怎么办

现实里很常见：正文用「截至 10-19」，某章对比用「截至 10-10」。
**不要放宽判定，要让账本表达清楚** —— 每条数字带自己的 `data_as_of`：

```json
{"id": "n9", "label": "场景数（10-10 口径）", "value": 281225,
 "data_as_of": "2026-10-10", "caliber": "感冒场景，截至 10-10", "sql": "..."}
```

审计器会按各自的 `data_as_of` 校验，不会因为"和全局截止日不同"就判错。
**但如果报告里有账本没有的数字，它照样拦** —— 只是会多给一句线索，指出"可能是口径不同"。

## 四之三、报告里的数字有三类角色

| 类 | 例子 | 怎么处理 |
|---|---|---|
| **A 交付指标** | 场景池、成交率、门店数 | 必须写进账本（`role: indicator`），必须可追溯 |
| **B 支撑数据** | 大盘对照值、样本数、过程计算 | 写进账本（`role: support`），有出处即可，不计入指标可追溯率 |
| **C 技术参数** | 置信阈值、字段完整度、页码 | 用 `<!-- audit-skip:start/end -->` 圈起来，**跳过数量会在结论里披露** |

**为什么不干脆放宽**：C 类圈起来是"透明跳过"，结论会写"跳过 N 个数字"；
而 A/B 类照样要账本 —— 举证责任没变，只是不再把"技术说明"当成造假。

## 五、最小可用账本（只填必填）

```json
{
  "schema": "report-ledger/1.0",
  "report": {"name": "演示", "files": ["r.md"], "data_as_of": "2026-10-19", "generated_at": "2026-10-23T10:00:00+08:00"},
  "sources": [],
  "numbers": [
    {"id": "n1", "label": "场景数", "value": 15597, "unit": "场景",
     "caliber": "去重场景ID", "verifiable": false, "origin": "客户口头提供，未复算"}
  ]
}
```

这份账本能过「账本自洽」和「报告可追溯」，但每条都会标「未验证」——**这就是诚实的样子**。

---

## 六、怎么生成账本（三种，任选）

| 方式 | 命令 | 适用 |
|---|---|---|
| 录像 | `python3 -m rla_track --ledger l.json -- python3 build.py` | Python 出报告，零改造 |
| 录像（Node） | `python3 rla_track.py --ledger l.json -- node build.mjs` | Node 出报告，零改造（拦 `@duckdb/node-api`） |
| 回收 | `python3 rla_collect.py --trace run.trace.jsonl --ledger l.json` | 已有 SQL 执行记录 |
| 通用取数 | `--command "python3 my_query.py"` / `--gateway /path/gw.py` | **任何数据库**（MySQL/PG/Oracle/HTTP），只要能把 SQL 变成 CSV |
| 手写/程序生成 | 任何语言按上面格式输出 JSON | 外部 agent、老报告 |

### 附：trace 录像契约（跨语言的最小接口）

如果你不想用我们的钩子，但愿意交出「跑过哪些 SQL」，那比手写账本可靠得多——
手写账本是"选摘记账"，实测漏 40%；录像把跑过的全记，覆盖面从方法上保证。

`.trace.jsonl`，一行一条：

```json
{"sql": "SELECT COUNT(*) AS v FROM data WHERE \"省份\" = '山东省'", "kind": "duckdb.node.run", "file": "/abs/build.mjs", "line": 42, "caller": "build.mjs:38", "bound": true}
```

| 字段 | 必填 | 说明 |
|---|---|---|
| `sql` | ✅ | **必须已把绑定参数内联成字面量**。带 `?`/`$p` 的语句无法复算，会被跳过（等于漏记） |
| `kind` | ⬜ | 来源标记，只用于排障 |
| `file` / `line` | ⬜ | 出处，写进账本的 `caliber` 供人核对 |
| `caller` | ⬜ | 调用者位置（业务把查询封成函数时，靠它区分是哪一句） |
| `bound_unresolved` | ⬜ | `true` = 有参数没能内联。**审计会因此报未就绪，不会静默放过** |

**我们的义务**：任何语言只要按这个格式交 trace + 能提供可复算的数据源，就能进 `rla_collect.py` → 账本 → 审计全链路。

**契约只约束格式，不约束你怎么产生它。**

---

## 七、产出物契约（v3.5.0）

审计一次产出四件。**其中只有 manifest 与另一套系统对接时会用到，但它是唯一"可机检"的那件**，
所以把它的字段写死在这里，任何语言实现都能生成同样结构的回执。

### 7.1 `manifest.json`（`rla-audit-manifest/1.0`）

```json
{
  "schema": "rla-audit-manifest/1.0",
  "audit_id": "RLA-20260930-a1b2c3d4",
  "generated_at": "2026-10-28T11:30:00+08:00",
  "verdict": { "code": "pass|review|fail", "label": "✅ 通过|⚠️ 需人工复核|❌ 不通过", "exit_code": 0 },
  "coverage": { "ratio": 0.9, "percent": 90.0, "matched": 58, "should": 64, "min_ratio": 0.9 },
  "counts": { "ledger", "verifiable", "recomputed_ok", "extracted", "metric",
              "matched", "matched_indicator", "matched_support",
              "unmatched", "weak", "ambiguous", "exempt" },
  "inputs": { "ledger": {"path","sha256_16"}, "policy": {"source","sha256_16"},
              "report_files": [{"path","sha256_16"}] },
  "environment": { "skill_version", "python", "duckdb", "os" },
  "reproduce_cmd": "scripts/rla_audit.py --ledger <path:ledger.json> ...",
  "outputs": { "audit_md", "audit_html", "evidence_csv", "manifest_json" },
  "integrity": { "ok": true, "result_fingerprint": "16 位", "recomputed_count": 119,
                 "checks": [{"name","expected","actual","ok"}] },
  "policy": { "source", "hash", "rounding" },
  "limitations": ["..."]
}
```

**三条硬约定**（别自己发明）：

1. **`coverage` 双写**：`ratio` 是 0~1 比率（引擎内部口径），`percent` 是 0~100（对外口径）。
   两套系统对接时**先看 percent**，省掉"差 100 倍"这类事故。
2. **`verdict` 双写**：`code` 给机器（`pass/review/fail`），`label` 给人（中文三态）。**不要只留一个**。
3. **`audit_id` 不含时刻**：`RLA-<数据截止日去连字符>-<账本 sha256 前 8 位>`。
   同一账本 + 同一数据截止日，**跑多少次都是同一个编号**；时刻只放在 `generated_at`。
   这样"这份凭证是哪次审计的、是不是同一份数据"能直接比对。

**路径一律脱敏**：`path` / `source` 只留文件名，`reproduce_cmd` 里的绝对路径换成 `<path:文件名>`。
回执可能外发，带目录结构等于泄漏客户信息。

### 7.2 `evidence.csv`

一行 = 报告里出现的一个数字。**五类都要进**（含豁免），否则"未纳入审计的数字"在别处查不到。

列（21 列，顺序即文件顺序）：

```
report_file, loc, raw, value, unit, role,
ledger_id, label, caliber, sql, ledger_value, recomputed, delta,
how, verdict, anchor, note,
number_id, block_id, cell_row, cell_col        ← 后四列预留给「生成时绑定」模式，当前留空
```

- `how` ∈ `exact | derived | weak | ambiguous | unmatched | exempt`
- 编码 **`utf-8-sig`**（带 BOM），否则 Windows Excel 打开中文乱码
- **CSV 注入防护**：`raw/label/caliber/sql/note` 若以 `= + - @` 开头，前面加 `'`；
  `value/recomputed/delta` 是数值列，**不转义**（转了 Excel 就不认数了）

### 7.3 `--export-missing` 导出的是什么

**是待补清单，不是可审计的账本**，所以带 `"purpose": "backfill-checklist"`。

```json
{ "schema": "report-ledger/1.0", "purpose": "backfill-checklist",
  "status": "clean | needs_backfill",
  "note": "人话说明",
  "report": {"name","files","data_as_of","generated_at"},
  "numbers": [ { ...账本条目骨架..., "origin": "待补（unmatched|ambiguous）：...",
                 "suggest_sql": "可填空的 SQL 模板" } ] }
```

- `schema` 保持 `report-ledger/1.0`：**补完 label/caliber/sql 后，这个文件要能直接当账本重跑**
- `files` 填**实际审计过的报告文件**，不填空数组
- 无缺失时 `numbers: []` + `status: "clean"` + 一句人话，**不给空壳模板**

---

## 八、v3.6.0 新增：定义驱动与渲染契约

### 8.1 账本新字段（向后兼容，都可缺省）

| 字段 | 位置 | 含义 |
|---|---|---|
| `confidence` | `numbers[]` | 指标可信档（`高` / `中` / `低`）。缺省视为未标注 |
| `numerator` / `denominator` | `numbers[]` | 比率型指标（`ratio: true`）的分子分母，便于人工复核 |
| `data_fingerprint` | `report` | 台账生成时的**数据文件指纹**。审计器据此判断"数据变了但账本没重算" |

`data_fingerprint` 目前是 `rla_collect.fingerprint_files()` 的返回值（16 位十六进制字符串）。

### 8.2 指标定义（`indicators.yaml`）

```yaml
indicators:
  - id: rt.ship.docs           # 必填，唯一
    name: 发货单据数            # → 账本的 label
    unit: 单                   # 单位决定数值换算规则（见 8.3）
    caliber: 去重 doc_no 数     # 口径说明
    confidence: 高             # 可选
    ratio: true                # 可选：SQL 返回 num/den 两列
    sql: "SELECT COUNT(DISTINCT doc_no) AS v FROM ..."
invariants:                    # 可选：指标之间的大小关系
  - { left: rt.ship.docs, op: '<=', right: rt.ship.rows, name: 单据数不超过明细行数 }
```

**不变式违反 = FAIL**（在 policy 的 `verdict.fail` 里，类别 `invariant_violation`）。

### 8.2.1 四种取值方式（v3.6.0）

| 写法 | 含义 | 结果是否比值 |
|---|---|---|
| `sql: "SELECT ..."` | 每条指标一句独立 SQL | 否 |
| `col: 列名` | 从 `source.one_sql`（一条算出所有列的大 SQL）里取列 | 否 |
| `expr: "a - b"` | 已解析指标之间加减（AST 白名单，**不用 eval**） | 否 |
| `num: a` + `den: b` | 两条指标相除 | **是** |

`col` 模式要在 `ledger.yaml` 配 `source.one_sql`：

```yaml
source:
  one_sql:
    module: scripts/wl_defs.py     # 从 Python 函数拿（func 默认 all_indicators_sql）
    # 或 file: sql/all.sql
    # 或 inline: "SELECT ..."
```

**比值规则（重要）**：`num/den` 和 `ratio: true` 算出来的值**一定是比值**，
所以 `unit` 写成 `pct` 还是 `pct1` 都会 ×100 —— 这条是为了跟已有的自研实现
（如星仔那套 `round(n*100/d, 1)`）对齐，避免同一个 `pct1` 在两种实现里差 100 倍。

非比值来源（`sql` / `col` / `expr`）仍按 8.3 的表：`pct` ×100、`pct1` 原样。

### 8.3 单位与数值换算（与 report-ledger 同口径）

| `unit` | SQL 返回值含义 | 账本 `value` |
|---|---|---|
| `pct` / `%` / `％` / `百分比` / `percent` | 0~1 比值 | **×100**，保留 1 位 |
| `pct1` | **已经是百分数**（如 16.9） | 原样，保留 1 位 |
| `元` / `金额` | 金额 | 保留 2 位 |
| 其他 | 计数等 | 最多 4 位 |

⚠️ 常见错误：SQL 返回比值（0.1694）却把 `unit` 写成 `pct1`，会让结果差 100 倍。
判断方法：**SQL 里有没有 `*100`**。有就写 `pct1`，没有就写 `pct`。

### 8.4 渲染契约（`[[id]]`）

报告模板里写 `[[id]]`（千分位数字）或 `[[P:id]]`（百分比），由 `rla_render.sub()` 替换。

```
[[rt.ship.docs]]        → 6,291
[[P:rt.ship.top1_share]] → 16.9%
```

**三条硬规则**：

1. **渲染前校验数据快照**：账本里的 `data_fingerprint` 与当前数据文件不一致 → 拒绝渲染
2. **未知 id 直接报错**，绝不静默返回空（否则文档里会留空白或 0）
3. **成品里不许残留 `[[...]]`**：审计时发现残留判 FAIL（`unrendered_placeholder`）

### 8.5 七道检查（v3.6.0 起）

| # | 检查 | 类别 | 级别 |
|---|---|---|---|
| 1 | 数据快照 / 账本过期 | `snapshot_mismatch` | **FAIL** |
| 2 | 占位符闭合（用了没算 / 未渲染） | `unrendered_placeholder` | **FAIL** |
| 3 | 跨件一致 | `cross_file_mismatch` | REVIEW |
| 4 | 必现 | `must_missing` | REVIEW |
| 5 | 泄漏 | `leak` | REVIEW |
| 6 | 不变式 | `invariant_violation` | **FAIL** |
| 7 | 算了没用（指标未被引用） | `metric_unused` | REVIEW |

### 8.6 非 SQL 数字的登记契约（`rla_note.note()`）

```python
from rla_note import note
note("htn.pool", 251923, label="高血压人群", unit="人",
     caliber="主标签=高血压，排除测量", expr="len(df[df.tag=='高血压'])")
```

生成的账本条目：

```json
{ "id": "htn.pool", "value": 251923, "label": "高血压人群", "unit": "人",
  "caliber": "主标签=高血压，排除测量", "role": "indicator",
  "verifiable": false, "source": "note-api",
  "origin": "rla_note 登记：len(df[df.tag=='高血压'])" }
```

**四条硬规矩**：

1. **必须在 `rla_report.py` 里跑**（它设 `RLA_NOTES` 并负责合并进账本）。
   直接 `python build.py` 会抛 `NoteError` —— 宁可吵，也不给一个假账本。
2. **`label` 必填且要是人话**：审计靠 label 做上下文锚定。写成 id（`htn.pool`）→ 锚不住 → 覆盖率 0%。
3. **`verifiable: false`**：这类条目能证明"报告里的数来自这次计算"，但**不能复算**（没有 SQL）。
4. **`expr` 是给人看的算式说明**（进 `origin`）。只有要声明**派生依赖**时才传
   `derived_from=[...]`，那才写进账本的 `expr` 字段（会被审计校验）。

同 id 重复登记取最后一次；与录像条目重名时以 note 为准，但会在 stderr 吵一声。

### 8.7 记账体检（`rla_health.py`）

`rla_report.py` 在「跑完脚本」与「审计」之间自动调用，输出：

```
② 记账体检（趁报告还没写完，现在补还来得及）
账本：37 条｜已认领 29 条（对上了指标定义）｜未认领 8 条
未认领的 8 条 —— 这些 SQL 算出来的数，写进报告会被判「来源不明」
怎么补：在 metrics.yaml 里给这几条加 match_sql
```

判断依据：账本条目有 `metric_id` = 已被指标定义认领；没有 = label 是从 SQL 猜的。
