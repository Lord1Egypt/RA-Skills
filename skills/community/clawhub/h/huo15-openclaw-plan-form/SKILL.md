---
name: huo15-openclaw-plan-form
description: >-
  把客户发来的各种格式的排产/计划/需求 Excel（横向表、T+2 真单、滚动计划、物料到货计划、生产计划下发表等，
  格式五花八门、中英文混杂、单/多 sheet）自动识别归类到三个标准模板之一，熔解内容并填充成统一模板，
  再与库中旧版本逐单元格比对、标注更新之处。Use when 用户上传一个或多个 Excel 计划/排产/需求/预报/交期表单，
  要求「统一成模板格式」「转成标准表」「合并多个表」或「对比新旧版本差异 / 标出哪里改了」。
  三个标准模板：客户需求排产表 / 计划跟踪跟单表 / 工厂DIP排产计划表。
license: 详见仓库 LICENSE
---

# 计划表单统一与差异标注 (plan-form)

把**任意格式**的客户排产/计划/需求 Excel，归一化成公司的**三个标准模板**，并支持新旧版本差异标注。

## 解决的三件事

1. **识别归类** —— 判断一个客户文件属于三个模板中的哪一个。
2. **转换填充** —— 把源文件内容熔解后填进对应模板，**自动去掉模板里的示例数据、用规范名重命名**；多个源文件可合并成一份。
3. **差异标注** —— 把「新文件」和「库里旧文件」按主键（文件名可不同）逐格比对，**红底+批注标出变化、绿底标新增、单列删除项**。

## 三个标准模板（`id` 给脚本用）

| id | 模板 | 形态 | 典型源文件 |
|---|---|---|---|
| `demand_schedule` | **客户需求排产表** | 标识列 + 横向**周/日**需求量 + 合计 + CS备注 | 横向表、T+2 真单/预报、滚动计划、物料到货计划、各客户需求下发表（绝大多数客户表都属这类） |
| `plan_tracking` | **计划跟踪跟单表** | 按成品料号跟踪**库存/已交/未交/结余/在制/欠料/月度预测** | 跟单个人表、到货进度+库存表 |
| `dip_schedule` | **工厂DIP排产计划表** | 工单维度 + **白班/夜班**日排程 + UPH/人力/线体 | 工厂内部 DIP 工单排产表、配料明细、返工工单 |

> 模板的列定义、别名词典、分类关键词、差异主键全部集中在 [`reference/templates_schema.json`](reference/templates_schema.json)（**单一事实来源**，要调整列就改这里）。模板的**画像与判别要点**见 [`reference/classification.md`](reference/classification.md)，**完整操作流程与排错**见 [`reference/workflow.md`](reference/workflow.md)。

## 环境准备（首次）

脚本依赖 `pandas` `openpyxl` `xlrd`（读 .xls 需 xlrd）。缺失时让用户/会话执行：

```bash
pip install -r requirements.txt    # 或: pip install pandas openpyxl xlrd
```

## 核心原则（务必遵守）

- **脚本只「建议」，你（agent）来「定夺」。** 分类置信度低、多 sheet、表头不在第一行、日期列识别不全时，**先看脚本打印的报告再决定**，必要时用参数覆盖。不要盲信自动结果。
- **多 sheet 工作簿先 `inspect_form.py`**，看清每个 sheet 的列数与日期提示，再决定 `--sheet`。自动选 sheet 只是兜底，复杂簿常选错。
- **示例数据自动清除、模板自动重命名** —— 输出是从 schema 现搭的，天然不含旧示例；文件名按模板规范名 + 数据日期 + **生成时刻（精确到分钟）**生成。无需手动删。
- **不臆造数字。** 源文件没有的量就留空；`合计` 用公式自动算。日期解析不确定时在报告里有 `⚠️低` 标记，复核它。

## 标准流程（5 步）

所有命令在 skill 目录下执行，`<file>` 为客户文件路径。

### ① 看结构（多 sheet / 没把握时必做）
```bash
python3 scripts/inspect_form.py "<file>" ["<file2>" ...]
```
打印每个 sheet 的维度、合并单元格、前几行预览、疑似表头行/日期列。据此选定 sheet 与表头行。

### ② 分类
```bash
python3 scripts/classify_form.py "<file>" [...]        # 加 --json 出结构化结果
```
输出每个文件的判定模板 + 置信度。**置信度 = high** 可直接用；**medium/low 必须你打开文件复核**后再敲定 `id`。

### ③ 熔解（源文件 → 规范化 JSON）
```bash
python3 scripts/extract_form.py "<file>" --template <id> --out work/<name>.norm.json
# 复杂文件按需覆盖： --sheet "3月"  --header-row 0  --data-start 2  --year 2026  --mapping map.json
```
打印**列映射报告**（每列 → 标识/数值/日期/略 + 置信度）。**逐行核对**：
- 标识/日期列认错 → 写一个 `map.json` 用 `--mapping` 覆盖（格式见报告提示或 `reference/workflow.md`）。
- 周一/周二这类只有星期的表头，脚本会借相邻行的真实日期补全；补不全的用 `--mapping` 指定 `iso`。

### ④ 填充（规范化 JSON → 统一模板）
```bash
python3 scripts/fill_template.py work/*.norm.json --template <id> --out-dir out/ [--dedup]
```
- 传**多个** `.norm.json` 会合并成**一份**模板（行拼接、日期区取并集）——满足「多个表统一成一个」。
- `--dedup` 按模板主键合并重复料号。输出文件自动命名，**末尾带生成时刻精确到分钟**（如 `客户需求排产表_20260227_20260602-1430.xlsx`：`20260227`=数据日期，`20260602-1430`=生成时刻）。

### ⑤ 差异标注（可选：和库里旧版本比）
```bash
python3 scripts/diff_forms.py --new <新文件|.norm.json> --old <旧文件|.norm.json> \
    --template <id> --out "out/差异标注.xlsx"
```
- `--new/--old` 可直接传**原始 Excel**（脚本内部自动熔解）或已熔解的 `.norm.json`。
- 按模板主键匹配（**文件名可不同**）。输出标注版：🔴变化（批注含原值）/ 🟢新增行 / 🟡删除项独立 sheet，并附 `*.diff.json` 报告。

## 生成/刷新空白模板（交付参考件）

```bash
python3 scripts/build_clean_templates.py        # 输出到 assets/templates/
```
三个**已重命名、无示例数据**的空白模板，给用户当格式参考。实际转换输出由 `fill_template.py` 产生（日期区随数据展开）。

## 一眼速记（典型：一个客户横向表 → 标准排产表，并与上版比）

```bash
python3 scripts/classify_form.py "客户来的表.xlsx"                       # → demand_schedule (high)
python3 scripts/extract_form.py "客户来的表.xlsx" --template demand_schedule --out work/new.norm.json
python3 scripts/fill_template.py work/new.norm.json --out-dir out/        # → out/客户需求排产表_YYYYMMDD.xlsx
python3 scripts/diff_forms.py --new work/new.norm.json --old "库里/上一版.xlsx" --template demand_schedule --out "out/差异标注.xlsx"
```

更细的边界处理（多 sheet 选择、双行表头、月粒度需求、计划版本列误判、`--mapping` 写法）见 [`reference/workflow.md`](reference/workflow.md)。
