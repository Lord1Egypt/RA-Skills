---
name: pdf-finance-parser
description: 解析金融行业 PDF 文档（A股年报、港股财报、美股10-K、招股说明书等）为结构化 Markdown + JSON。专为跨页表格、无边框表格、多级表头、密集数值、多栏排版等金融场景设计。底层调用火山 LAS las_pdf_parse_doubao 算子做通用解析，再经 6 层金融后处理（HTML 表格解析 / 多级表头 / 跨页合并 / 数值规整 / 财务术语对齐 / 业务规则校验）输出 schema-compliant JSON。
user-invocable: true
metadata: {"openclaw":{"emoji":"📊","skillKey":"pdf-finance-parser","requires":{"bins":["python3"],"env":["LAS_API_KEY","TOS_ACCESS_KEY","TOS_SECRET_KEY","TOS_BUCKET"]},"primaryEnv":"LAS_API_KEY","version":"0.3.0","author":"zhuyijun"}}
---

# PDF Finance Parser Skill

**金融场景 PDF → 结构化 Markdown + JSON**。底层调用火山方舟 LAS 算子 `las_pdf_parse_doubao` 做通用解析，再经 **6 层金融后处理**还原为符合 [assets/output_schema.json](assets/output_schema.json) 的业务 JSON（含 value/unit/source_page/validation）。

## 设计模式

- **Engine + Post-process 解耦**：LAS 是通用解析引擎（黑盒），金融业务规则是独立后处理层，引擎可替换、业务可独立迭代
- **Pipeline**：`输入归一化 → LAS submit/poll → HTML 表解析 → 多级表头 → 跨页合并 → 数值规整 → 财务术语对齐 → 业务校验 → schema-compliant 输出`
- **Inversion**：调用前先与用户确认解析模式（normal / detail）；不私自决定
- **Best-effort 校验**：业务规则违反时标 warning 而非修改原值；保留可追溯性

## Gotchas

- 必须配置 `LAS_API_KEY`（火山方舟 LAS）
- 本地 PDF 上传 LAS 必须先经过 TOS（火山对象存储），所以也必须配置 `TOS_ACCESS_KEY` / `TOS_SECRET_KEY` / `TOS_BUCKET`
- 若 TOS 桶 region 不是 `cn-beijing`（LAS 默认 region），需要 `export TOS_REGION="<region>"` 单独指定（tos:// 协议跨 region 由 LAS 解析）
- TOS 对象 key 不能含中文字符（LAS 后端 URL parser 不接受），本 skill 已在 `tos_uploader.py` 做 ASCII sanitize
- LAS 并发限制 1 QPM，多文档批跑会自动退避；不要并行 spawn 多个进程
- 长报告（>200 页）建议用 `--pages 1-50` 分段
- 财报跨页表格（"(续)" 标志）由后处理层 `cross_page_merger.py` 自动合并；想关掉后处理传 `--no-postprocess`

## 工作流

复制此清单并跟踪进度：

```text
解析进度：
- [ ] 步骤 0：确认解析模式（normal / detail）
- [ ] 步骤 1：环境就绪（venv + env.sh 凭证）
- [ ] 步骤 2：执行 parse-las
- [ ] 步骤 3：检查 meta.json.postprocess + output.json.validation
- [ ] 步骤 4：按"结果回复模板"汇报
```

### 第 0 步：确认解析模式（必须先执行）

```
请选择 PDF 解析模式：

| 模式   | 说明                                          | 价格      |
|--------|-----------------------------------------------|-----------|
| normal | 默认，单次推理，速度更快，适用于结构清晰的文档 | 0.02 元/页 |
| detail | 深度分析，对复杂表格/扫描件/印章精度更高       | 0.04 元/页 |

推荐：A股/港股标准年报选 normal；财报附注、合并报表跨页、扫描合同选 detail。
```

- 用户未明确指定 → 默认 `normal`

### 第 1 步：环境就绪（仅首次）

```bash
cd {skill_directory} && \
  (test -d .venv || (python3 -m venv .venv && \
   .venv/bin/pip install -r ../../requirements.txt)) && \
  .venv/bin/python3 scripts/skill.py info
```

`info` 命令验证 VLM 配置（仍用于 v0.2 fallback 路径的健康检查）。

**首次使用必须先填好 `env.sh`** —— 把 `LAS_API_KEY` / TOS 凭证替换成你自己的值。
框架会在 skill 目录自动加载 `env.sh`，无需手动 `source`。

### 第 2 步：执行解析

```bash
.venv/bin/python3 scripts/skill.py parse-las \
  --input <pdf_path | http(s)://... | tos://bucket/key> \
  --output <output_dir> \
  --parse-mode normal
```

- stdout 输出一行 JSON：`{"status":"COMPLETED","task_id":"...","page_count":N,"table_count":N,"postprocess":{...},"preview":"..."}`
- stderr 输出过程日志（TOS 上传、LAS submit/poll、后处理进度、validator warnings）
- 默认开启金融后处理；传 `--no-postprocess` 跳过（通用文档场景）

### 第 3 步：检查 meta.json + output.json.validation

`meta.json` 必读字段：

| 字段 | 含义 | 处理 |
|------|------|------|
| `status` | COMPLETED / FAILED | FAILED 时看 `error_msg` |
| `page_count / table_count` | LAS 解析的页数 / 表格数 | 对比 GT 检查漏抽 |
| `postprocess.merged_table_count` | 跨页合并后的表数 | 通常 < raw_table_count 表示有合并 |
| `postprocess.validation_warning_count` | 业务规则不一致计数 | > 0 时看 output.json 的 `tables[].validation` |
| `wall_time_seconds` | 端到端耗时 | 评测对比用 |

`output.json` 关键 sub-field（v0.3 新增）：

- `tables[].statement_type`：`balance_sheet` / `income_statement` / `cash_flow` / `equity_change`
- `tables[].declared_unit`：从表头声明文本中识别的单位（如 "百万元"）
- `tables[].column_paths`：每列多级表头展平的 path（如 "本集团 / 2026年3月31日(未经审计)"）
- `tables[].source_pages`：跨页合并后的源页号数组
- `tables[].validation`：业务规则校验结果（warnings 列表）

### 第 4 步：结果回复模板

```
✅ 解析完成

📄 文档信息
- 文件：{filename}
- 页数：{page_count} | 表格：{table_count}（合并后 {postprocess.merged_table_count}）
- 模式：{parse_mode} | 耗时：{wall_time}s

📁 输出
- 业务 JSON：{output_dir}/output.json（符合 assets/output_schema.json）
- 整篇 Markdown：{output_dir}/output.md
- LAS 原始响应：{output_dir}/result.full.json
- 单页 markdown：{output_dir}/pages/p{N}.md

⚠️ 注意（若有）
- 业务规则 {N} 处不一致：查看 output.json.tables[].validation.warnings
```

## 输出目录结构

```
{output_dir}/
├── output.json          # ★ 金融业务 JSON（cells 含 value/unit/source_page/validation）
├── output.md            # 整篇 markdown（≈ result.md）
├── meta.json            # task_id / wall_time / postprocess 摘要
├── result.md            # LAS 原始 markdown（表格为 HTML <table>）
├── result.full.json     # LAS 完整响应（含 detail[].text_blocks / bbox）
└── pages/
    ├── p1.md            # 单页 markdown（评测 / 对比用）
    ├── p2.md
    └── ...
```

## 金融后处理 6 层

| 层 | 模块 | 职责 |
|---|---|---|
| 1 | [html_table_parser.py](scripts/html_table_parser.py) | BS4 解析 LAS 的 `<table>`，rowspan/colspan 展开为网格 |
| 2 | [multi_header_detector.py](scripts/multi_header_detector.py) | 数 header_rows + 计算每列 column_path |
| 3 | [cross_page_merger.py](scripts/cross_page_merger.py) | `(续)` 关键词 + 列结构匹配 → 多张分页表合一 |
| 4 | [numeric_normalizer.py](scripts/numeric_normalizer.py) | 千分位 / `(负数)` / 万/亿/百万元 / percent / `-`→null |
| 5 | [finance_terms_aligner.py](scripts/finance_terms_aligner.py) | statement_type 识别 + group / subtotal / grand_total 关键词 |
| 6 | [finance_validator.py](scripts/finance_validator.py) | 资产 = 负债 + 权益、Σ明细 = subtotal（best-effort，标 warning 不修值）|

## 异常处理决策树

| 现象 | 来源 | 处理 |
|---|---|---|
| `LAS_API_KEY 未配置` | env.sh 缺失或未加载 | 检查 skill 目录下 env.sh 是否存在、值是否非占位符 |
| `TOS_BUCKET 未配置` | TOS 凭证缺失 | 同上；如桶在非 LAS region，再 export TOS_REGION |
| `NoSuchBucket` / 404 | 桶名拼错 / region 不一致 | 用 `clawhub auth whoami` 或 TOS 控制台确认桶 region，更新 TOS_REGION |
| `Url.Invalid` | TOS key 含特殊字符 / 跨 region 拉不到 | `tos_uploader.py` 已 sanitize；若仍出现，检查 TOS 桶是否在 LAS region |
| LAS task 持续 `RUNNING` 不返回 | 单次大文档 | 已自动退避；超过 max-poll-attempts (60×30s) 仍未返回 → 拆分页范围 |
| `validation_warning_count > 0` | 业务规则不一致 | 看 output.json.tables[].validation.warnings；不阻塞流程，best-effort |
| `Url.Invalid: invalid url tos://...` 含中文 | 中文路径未 sanitize | 已修，若复现请上报 |

## 进阶用法

### 仅解析某些页（连续范围）

```bash
.venv/bin/python3 scripts/skill.py parse-las \
  --input <pdf> --output <dir> --pages 1-10
```

LAS 仅支持连续页范围（start_page + num_pages），不支持 `1,3,5` 离散页。

### 强制使用 `detail` 模式（2× 价，更精细）

```bash
.venv/bin/python3 scripts/skill.py parse-las \
  --input <pdf> --output <dir> --parse-mode detail
```

### 跳过金融后处理（通用文档场景）

```bash
.venv/bin/python3 scripts/skill.py parse-las \
  --input <pdf> --output <dir> --no-postprocess
```

只生成 `result.md / result.full.json / pages/`，不生成 `output.json`。适合非金融场景或想观察 LAS 原始输出。

### 与评测脚本对接

```bash
# 批量预测（仓库内 evaluation/scripts/）
python3 evaluation/scripts/run_lasbench_predictions.py \
  --images-dir <dataset>/images --out-dir <pred_dir>

# 一键算指标
python3 evaluation/scripts/run_omnidocbench_eval.py \
  --gt <gt.json> --pred-dir <pred_dir> --out <report.json>

# 渲染 HTML 报告
python3 evaluation/scripts/render_omnidocbench_report.py \
  --input <report.json> --output <report.html>
```

## 重要约束

1. **业务层与解析层解耦**：金融后处理只接受 LAS 已结构化的输入；不要在后处理里塞 VLM 提示词 / 渲染逻辑
2. **不修改原始 PDF**：只读，TOS 上传也是只读复制
3. **不做数值"创意修正"**：原文 `1,234` → `value=1234`（去千分位 + 按声明单位归一化到 yuan），但不做上下文猜测
4. **保留可追溯性**：每个 cell 带 `source_page`，跨页合并表带 `source_pages[]`
5. **业务规则 best-effort**：不一致只标 warning，不改写 value；评测层负责打分

## 参考资料

- [命令参数详解](references/commands.md)
- [API 与提示词约定](references/api.md)
- [配置说明](references/configuration.md)
- [常见问题 FAQ](references/faq.md)
- [输出 JSON Schema](assets/output_schema.json)
- [财务术语词表](references/finance_terms.md)
- [常见财报表格模板](references/table_patterns.md)
