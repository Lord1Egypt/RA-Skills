# 使用细节（正文的展开版）

> SKILL.md 只放"够用就行"的部分；这里放会踩到的细节。按需查阅。

---

## 一、数据源怎么接

| 你的数据 | 怎么写 |
|---|---|
| 单个 parquet / csv | `--mount "data=/path/x.parquet"`（挂成视图 `data`，SQL 里写 `FROM data`） |
| duckdb 库文件（多表） | `--mount "=/path/x.duckdb"`（**等号左边留空** = 直接当主库，SQL 里写 `FROM 表名`） |
| 只读网关脚本 | `--gateway /path/gw.py`（`--sql`/`--out` 协议） |
| **MySQL / PG / SQL Server / 任何库** | `--command "python3 my_query.py"`（SQL 从 stdin 进、CSV 从 stdout 出） |
| sqlite3 | 直接用自带的 `--command "python3 scripts/cmd_sqlite.py --db /path/x.db"` |
| Excel | 先转 duckdb/parquet（推荐），或用 `--command` 包装 |
| 没有源可复算 | 直接给 `--ledger`，跳过复算（结论会标"未复算"→ 需人工复核） |

### 非 duckdb 用户：写 10 行就能接

```python
# my_query.py：把 SQL 变成 CSV 吐出来，背后是 MySQL / PG / 什么库都行
import sys, csv, pymysql
sql = sys.stdin.read()
conn = pymysql.connect(host="...", user="...", password="...", database="...")
cur = conn.cursor(pymysql.cursors.DictCursor)
cur.execute(sql)
rows = cur.fetchall()
w = csv.DictWriter(sys.stdout, fieldnames=[d[0] for d in cur.description])
w.writeheader(); w.writerows(rows)
```

然后：

```bash
python3 scripts/rla_report.py --command "python3 my_query.py" ...
```

**审计器不关心背后是什么数据库，只要你能把 SQL 变成 CSV。**
没有 duckdb 的环境（装不上、或原生 DLL 被安全策略拦）也走这条路，功能完整。

---

## 二、常见坑（都是真踩过的）

### ① 账本的 `value` 必须用基本单位

```yaml
✅ value: 340000, unit: "元"      # 报告写「34.0 万元」→ 能对上
❌ value: 34.0,   unit: "万元"    # 报告写「34.0 万元」→ 被解析成 340000，对不上
```

用了"万元/千/亿"这类换算单位，审计会警告并列出条目。

### ② `--files` 的相对路径以「账本所在目录」为基准

```bash
--out deliverables/r.md --ledger deliverables/l.json
--files "deliverables/r.md"        # ← 会变成 deliverables/deliverables/r.md
--files "r.md"                     # ← 对（相对账本目录）
--files "/abs/path/r.md"           # ← 也对
```

用 `rla_report` 时脚本会帮你两边都试；直接调 `rla_audit` 时要注意这条。

### ③ 值太小的数字天然不可区分

「贝那鲁肽 1 场景」里的「1」，和账本里任何值为 1 的指标都能对上。
规则：值 < 10 且上下文没有指标名锚定 → 判「无法判定」，不算命中。

### ④ PPT / 图片里的数字扫不到

会在结论里标「未覆盖 N 张图片」。要管住图表数字，只能是**图表也用账本渲染**——这是事后审计的天花板。

### ⑤ 报告里的数字有三类，别一锅炖

- 交付指标 → 必须有出处
- 支撑数据（对照值、样本数）→ 写进账本，`role: support`
- 技术参数（阈值、完整度、页码）→ 用 `<!-- audit-skip:start/end -->` 圈起来

不分类的话，一份真报告会产生 40% 的假警报。

### ⑥ 「通过」不等于「都查了」——先看审计覆盖率

一个数字要不要追，系统先看它上下的词（场景/门店/率/占比/数量/行数…）。词表永远不全：
实测把「总行数」改成「样本池规模」，4 个数字能全部被豁免，**结论照样 ✅ 通过**。

所以有三道防线：

| 防线 | 规则 |
|---|---|
| ① 大数默认追 | 带千分位 / 百分比 / ≥1000 的数字，**不管怎么写**都要给出处（举证责任在报告方） |
| ② 覆盖率披露 | 结论里永远有「审计覆盖率 = 追溯到的 / 应审的」 |
| ③ 不许空章 | 覆盖率低于 90%，或一个指标都没认定出来 → 结论降为「需人工复核」，不许说通过 |

只需要看一行：

```
| 审计覆盖率 | 100%（追溯 4 / 应审 4） |     ← 好
| 审计覆盖率 |  33%（追溯 1 / 应审 3） |     ← 有 2 个数字没查到出处，去看「未纳入审计」
```

剩下漏的只有一类：**没有千分位、小于 1000、又不带单位的小数字**（「样本池 850」）。
这种不一定是数据（也可能是"共 3 类"这类行文用词），所以不强制追 —— 但它会拉低覆盖率，让你看见。

### ⑦ policy 的 `verdict` 两张表必须列全

`policy.yaml` 里 `verdict.fail` / `verdict.review` 是"哪些问题算拦、哪些算复核"的白名单。
**某类问题抓到了、却不在这两张表里 → 它会被丢掉。**

这一条踩过：review 只写了 3 类，而代码实际产生 8 类，于是跨件一致、必现、泄漏、弱锚定、无法判定
全部被静默丢弃，结论照样显示 ✅ 通过。

现在代码兜了一层：`dropped` 非空 → 强制降为「需人工复核」并把内容列出来。
即便如此，自定义类别时仍要检查这两张表。

---

## 三、四种接入方式（按强度）

| # | 怎么用 | 覆盖 | 强度 |
|---|---|---|---|
| T1 | `rla_report.py -- python build.py` | 脚本出报告 | 强 |
| T2 | 生成器内置审计，非 0 退出不产出文件 | 关键报告 | 最强 |
| T3 | AGENTS.md / 提示词里写死"出报告必跑" | 对话式 agent | 中 |
| T4 | 第三方按 `SPEC.md` 交 `ledger.json` | 任何 agent | 看配合 |

---

## 四、依赖与降级

```bash
python3 scripts/deps_check.py          # 体检：缺什么、怎么装、装不上怎么办
```

- 缺 `duckdb`：本地复算不可用，但 `--command` 接法照样能复算；自检自动降级到 sqlite3（仍 7/7）
- duckdb 报 `DLL load failed ... 应用程序控制策略已阻止此文件`：这是**被安全策略拦了，不是没装**。
  把 site-packages 下的 `duckdb` 目录加白，或改用 `--command`
- 缺 `python-docx` / `python-pptx` / `openpyxl` / `beautifulsoup4`：只是少支持一种格式，md/txt 不受影响

---

## 五、自检怎么读

`python3 scripts/rla_selftest.py` 跑 5 个用例：正确报告应通过、改数应被拦、跨件写法不同应报、
客户版泄漏应被拦、账本编数应被拦。

**7/7 才有意义**。它证明的不是"代码没报错"，而是"四类问题真的会被抓"。
若某天变成 4/5，说明有检查在空转——别急着用它出报告。

---

## 六、Node 出报告的细节

```bash
python3 scripts/rla_report.py --out report.md --ledger ledger.json \
    --mount "data=/path/your.parquet" --report-name "某报告" --data-as-of 2026-09-30 \
    -- node build_report.mjs --out report.md
```

钩子靠 `NODE_OPTIONS=--require` 挂进 Node 进程（Python 侧是 `PYTHONPATH`+`sitecustomize`，同一思路的两种形态）。
一个入口同时支持两种语言，谁跑谁录。

**三条前提**（缺一条会"装上了但一条没录到"）：

1. 业务项目里装了解析得到的 `@duckdb/node-api`；不在默认位置时用 `RLA_NODE_MODULES=<含 node_modules 的目录>` 指过去
2. 技能目录路径**不要带空格**（`NODE_OPTIONS` 不解析引号）
3. 目前**只支持 duckdb**；MySQL / PG 用 `--command` 接法（语言无关）

**能录到的写法（都实测过）**：

| 业务写法 | 能不能录 |
|---|---|
| `conn.run(sql)` / `conn.runAndReadAll(sql)` | ✅ |
| `conn.run(sql, [v1, v2])` 位置参数 | ✅ 参数内联成字面量，账本里是可复算的 SQL |
| `conn.prepare(sql)` → `stmt.bind({p:'x'})` → `stmt.run()` | ✅ 命名参数同样内联 |
| `conn.streamAndReadAll(sql)` | ✅ |
| 字符串本身带 `?`（`WHERE '?' = '?'`） | ✅ 不会被误当占位符 |

**为什么要内联**：录下来的 SQL 若带 `?` 就没法复算，只能被当"参数化语句"跳过——账本会悄悄少一个数。
内联不了的类型会打 `bound_unresolved`，**审计直接报未就绪，不静默放过**。

**出处精确到"哪一句算的"**：业务常把查询封成一个函数，几十条 SQL 出处都一样。
Node 侧会多记一层调用者：`来自 build_report.mjs:26（调用自 build_report.mjs:38）的查询结果列「v」`。

**边界**：不做常驻服务内的分段录像。服务常驻时"哪一次是出报告"没有天然边界，
硬做要在进程里按请求切窗口、还要处理并发会话串话——那是给具体服务定制适配器，不是通用技能该背的包袱。
需要审计服务产出的报告，用包装脚本出稿后再跑本技能。

---

## 产出物怎么用（v3.5.0）

一次审计落四件，别混着发：

| 文件 | 谁看 | 外发 |
|---|---|---|
| `audit.md` | 老板/PM，判"能不能签" | ✅ 可附录 |
| `audit.html` | 分析师，查"错在哪一行"（全量证据、可点开、含 SQL） | ❌ 仅内部 |
| `evidence.csv` | 要自己二次筛的人（Excel 可筛） | ⚠️ 含 caliber/sql 时不外发 |
| `manifest.json` | 合规/追责（编号 + hash + 复现命令） | ✅ 路径已脱敏 |

**审计编号** `RLA-<数据截止日>-<账本 hash 前 8 位>`：同一账本同一数据，跑几次都是同一个号。
拿它去 `manifest.json` 里比对 `generated_at`，就知道是不是同一次审计。

**跨件矩阵怎么读**：行=指标，列=交付件，红格=少数派写法。
注意它抓的是"写法不统一"；数值一旦不同、账本里查不到，会更早被判成「来源不明」拦下。

**多交付件 demo**（零依赖，30 秒）：
```bash
python3 examples/cross-file-build.py
python3 scripts/rla_audit.py --ledger rla-demo/ledger.json --files report_a.md report_b.html \
    --command "python3 scripts/cmd_sqlite.py --db rla-demo/demo.sqlite" --out rla-demo/audit.md
```
详见 `examples/cross-file-demo.md`。
