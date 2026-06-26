# 详细流程、`--mapping` 写法与边界处理

配合 `SKILL.md` 的 5 步用。本文覆盖脚本参数全集、覆盖映射写法、以及踩过的边界。

## 规范化中间格式（normalized JSON）

`extract_form.py` 产物、`fill_template.py` / `diff_forms.py` 输入。一行 = 一条记录：

```json
{
  "template_id": "demand_schedule",
  "sheet": "T+2周", "header_row": 0, "data_start": 1, "year_hint": 2026,
  "n_rows": 28, "dates": ["2026-02-27", "..."],
  "rows": [
    { "identity": {"生产工厂":"黄岛工业园","客户料号":"0151801003","规格型号":"真单需求（新A）"},
      "scalars":  {"合计": 594},
      "remark":   {},
      "series":   {"2026-02-27": 0, "2026-03-05": 264} }
  ]
}
```

- `identity` 标识列（谁/什么）；`scalars` 非日期数值/文本；`remark` 备注；`series` = {ISO日期: 数量}。
- 四个桶都按模板**规范列名**存。脚本把客户乱列名通过别名词典映射到规范名。

## `extract_form.py` 参数

| 参数 | 作用 |
|---|---|
| `--template <id>` | 必填，目标模板 |
| `--sheet "名"` | 指定 sheet（多 sheet 必用；不传则自动选，复杂簿常选错） |
| `--header-row N` | 表头所在行（0 基）。标题/说明占了第一行时要指定 |
| `--data-start N` | 数据起始行（0 基）。表头下面还有子表头/合计行时指定 |
| `--year YYYY` | 年份提示，补全 `0227`/`5月1日`/`周一` 这类缺年表头 |
| `--mapping map.json` | 覆盖任意列的角色/规范名/日期，见下 |
| `--out path` | 规范化 JSON 输出路径 |

### `--mapping` 覆盖写法

报告里某列认错时，写一个 JSON 用 key=**列序号(0基)** 或 **表头原文** 指定：

```json
{
  "sheet": "3月",
  "header_row": 0,
  "data_start": 2,
  "columns": {
    "1":  {"role": "identity", "canonical": "客户料号"},
    "互联工厂": {"role": "identity", "canonical": "生产工厂"},
    "30": {"role": "date", "iso": "2026-03-02"},
    "5":  {"role": "ignore"}
  }
}
```

`role` ∈ `identity` / `scalar` / `remark` / `date` / `ignore`。`date` 必带 `iso`（`YYYY-MM-DD`）。`identity/scalar/remark` 带 `canonical`（必须是该模板 schema 里的规范列名）。

## 边界与坑

1. **多 sheet 工作簿**：务必先 `inspect_form.py` 看清。主表常不是第一个 sheet（第一个可能是空的 `Kangatang` 或封面）；也别被「两器短板能力 / 大盘规划 / 到线体产能」这种**纯日期辅助表**带偏——它们日期列很多但不是主需求表。认准**有标识列（整机编码/客户料号/物料号）的那张**。

2. **标题行占第一行**（如 `W11周生产计划2.27下发` 独占 R0）：脚本一般能跳过；跳不过就 `--header-row 1`。

3. **双行表头（周X 在上、日期在下）**：如横向表 R0=`周一/周二`、R1=`2026-03-02`。脚本会对「只有星期」的表头借**相邻行**真实日期补全。补不全/补错的列用 `--mapping` 显式给 `iso`。

4. **月粒度需求**（`4月需求`/`5月新`/`5月计划`）：
   - `X月需求`/`X月新` 想当月度桶 → `--mapping` 把该列设 `{"role":"date","iso":"2026-04"}`（注意 schema 日期区按天展开，月度数据会落到该月；如需严格月度列，在 demand 模板里另议）。
   - `X月计划`/`0417版计划` 是**计划版本号不是日期**，脚本默认**不**当日期（已在排除名单）。确属版本列就让它 `ignore` 或落 `scalar`。

5. **`厂家1/厂家2/供应商`** 等供应商列：demand/tracking 模板没有对应规范列，默认丢弃。要保留就 `--mapping` 落到某 `scalar`（或在 schema 加列）。

6. **合计/小计/汇总行**：`extract` 自动跳过（标识列含「合计/总计/小计/汇总/total」或全空的行）。若客户把小计混在中间且没这些字样，需要人工 `--data-start` 或后续清理。

7. **.xls 读不了**：确保装了 `xlrd`。个别 `.XLS` 实为 HTML 伪装，pandas 也能读；真读不了就让用户另存为 .xlsx。

## `fill_template.py` 合并多文件

```bash
python3 scripts/fill_template.py work/a.norm.json work/b.norm.json work/c.norm.json \
    --template demand_schedule --out-dir out/ --dedup
```
- 行拼接、日期区取并集 → **一份**统一模板。
- `--dedup` 按模板 `diff_key` 合并同料号行（后到的 series/scalar 覆盖累加）。
- `--name-date 20260501` 自定义文件名里的**数据日期**段；不传取数据最早日期。
- 自动命名的文件名**末尾固定追加生成时刻**（`YYYYMMDD-HHMM`，精确到分钟），用于区分同一批数据的多次生成版本，如 `客户需求排产表_20260227_20260602-1430.xlsx`。显式传 `--out` 时尊重你给的完整路径，不再追加。

## `diff_forms.py` 细节

- 主键 = 模板 schema 的 `diff_key`（demand: `1088号`+`客户料号`；tracking: `1088号`+`客户号`；dip: `整机工单号`等）。**靠内容主键匹配，文件名无所谓**。
- 比对维度：identity / scalar / series 逐格；合计这类公式列也比（源端原值存在 scalars）。
- 输出标注版 xlsx：
  - 🔴 浅红底 + 批注「原值: X」= 该格数值变了
  - 🟢 浅绿底（标识列）= 整行新增（旧表没有）
  - 🟡 独立 sheet「本次删除(旧有新无)」= 旧表有、新表没了的料号
  - A2 单元格批注 = 图例与计数
- 同时产出 `*.diff.json` 结构化报告（added/removed/changed 清单），可喂给后续自动化。
- 不传 `--out` 时默认名也**末尾带生成时刻**（如 `差异标注_客户需求排产表_20260602-1430.xlsx`），精确到分钟。

## 调 schema（加列/改别名/换主键）

只改 `reference/templates_schema.json`：
- 加客户常见的新表头叫法 → 往对应列 `aliases` 里加；
- 加一个规范列 → 在该模板 `columns` 里加一项（`role` 选对）；
- 改差异主键 → 改 `diff_key`。
改完**重新生成空白模板**：`python3 scripts/build_clean_templates.py`。脚本无需改动。
