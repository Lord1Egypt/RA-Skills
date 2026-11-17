# Data Report Workflow

Use this workflow for a report, static dashboard, single-page data poster, evidence-backed findings artifact, recurring report, or report-spec validation from local CSV, TSV, XLSX, or JSON.

## Contents

- Create
- Data poster
- Evidence and claims
- Chart and spec rules
- Recurring reports
- Edit and final check

## Create

1. Derive the analytical question and at most two analysis types: trend, comparison, distribution, correlation, or KPI. Identify the likely measure, dimension, and time focus without reading unrelated files.

2. Analyze and profile:

```bash
miao-viz data analyze /path/to/data.csv \
  --intent "user intent" \
  --compact \
  --output SYSTEM_TEMP/miao-vision/context.json

miao-viz data profile /path/to/data.csv \
  > SYSTEM_TEMP/miao-vision/profile.json
```

Read `context.json`; treat the profile only as validation input. Follow `promptRules[]`, surface
`sampleWarnings[]`, use only `fields[]`, `metricCandidates[]`, `catalog.charts`,
`catalog.scenes`, `catalog.blocks/templates`, and `catalog.interactions`. Reject anything in `catalog.blockedCharts`,
`catalog.blockedScenes`, or `catalog.blockedBlocks`. Ask at most one question, and only when
`clarificationQuestions[]` or a blocked Scene identifies a blocking ambiguity.

If the primary field assumption is wrong, rerun analyze with `--correct-assumption`. Add `--extra-query` only for a required aggregation missing from the standard evidence. Do not run `spec catalog --for-llm` unless compact context lacks a necessary rule.

3. Prefer a matching business scene, then a template, then a block:

```bash
miao-viz spec scene instantiate <scene-id> \
  --context SYSTEM_TEMP/miao-vision/context.json \
  --output SYSTEM_TEMP/miao-vision/report.yaml

# Use only when no scene matches:
miao-viz spec template instantiate <id> \
  --context SYSTEM_TEMP/miao-vision/context.json \
  --output SYSTEM_TEMP/miao-vision/report.yaml

# Use only when no template matches:
miao-viz spec block instantiate <id> \
  --context SYSTEM_TEMP/miao-vision/context.json \
  --output SYSTEM_TEMP/miao-vision/report.yaml
```

Review field names, variables, generated insights, evidence ids, and quality checks. Fall back to manual charts only when no suitable template or block exists.

For an HTML report intended for another person to explore, instantiate a recommended interaction preset and merge its `interactions` fragment into the report spec:

```bash
miao-viz spec interaction instantiate <filter|filter-and-detail> \
  --context SYSTEM_TEMP/miao-vision/context.json \
  --output SYSTEM_TEMP/miao-vision/interactions.yaml
```

Use only a preset present in `catalog.interactions`. Keep `dataPolicy.mode: minimal` unless detail rows are required. With `detail-safe`, review every `detailFields` and `excludeFields` entry; never replace a restricted field or switch to `full` automatically. A legacy spec without `dataPolicy` remains renderable but is not share-safe.

Use `interactions.currentView.summaries` only for deterministic local calculations supported by `QueryRecipe`; never generate JavaScript or rewrite published insights as filters change. Published insights remain bound to full-dataset evidence, while current-view summaries must expose their active filter scope and `Calculated locally` status. Set `locale` to `en` or `zh-CN` from the requested report language.

Use `miao-viz spec scene list` to discover business scenes. If the selected scene returns
`SCENE_NOT_APPLICABLE`, surface its missing semantics and clarification questions; never guess
which field represents revenue, cost, campaign response, or experiment outcome.

Supported Scene ids are `business-overview`, `sales-analysis`, `marketing-performance`,
`financial-summary`, `survey-analysis`, `ab-test`, and `data-quality-audit`.

For `ab-test`, use `ab_test_significance` only when it exists in `context.evidence`. Its
two-proportion result requires exactly two variants plus valid sample-count and conversion-rate
fields. Without that evidence, keep the report descriptive and do not claim significance.

4. Validate:

```bash
miao-viz spec validate \
  --spec SYSTEM_TEMP/miao-vision/report.yaml \
  --profile SYSTEM_TEMP/miao-vision/profile.json \
  --context SYSTEM_TEMP/miao-vision/context.json \
  --verify \
  --strict
```

Add `--trusted` only for an interactive HTML report intended for third-party delivery.

Fix every error and warning before rendering. Require both `coverage.objectCoverage`
and `coverage.claimCheckCoverage` to equal `1`. Use `--patch-hints` for
machine-fixable issues; apply only returned patches and fill unresolved field names
or evidence paths manually.

5. Resolve the concrete `artifactPath` using the shared delivery-directory rule, then render. In the schematic command below, `ARTIFACT_PATH` means that already-resolved literal path; do not pass the token itself to the CLI.

```bash
miao-viz render report \
  --input /path/to/data.csv \
  --spec SYSTEM_TEMP/miao-vision/report.yaml \
  --context SYSTEM_TEMP/miao-vision/context.json \
  --theme <theme> \
  --format html \
  --output ARTIFACT_PATH
```

Add `--trusted` only for an interactive HTML report intended for third-party delivery.

Default to `magazine` when the user has no preference. Supported themes are `standard-white`, `magazine`, `standard-dark`, `minimal`, `nyt`, `bloomberg`, and `tableau`. Use `--no-interactive` only when explicitly requested.

For PDF, render the same validated report with `--format pdf`. For both formats, use `--format html,pdf --output-dir <dir>`. PDF defaults to A4 portrait and requires Playwright. Surface blocking `PDF_*` errors; do not switch renderers.

For a report PNG, use `--format png`; optional controls are `--viewport-width`,
`--viewport-height`, `--scale`, and `--png-timeout`.

## Data Poster

Poster 是证据驱动的自动叙事海报生成器：先根据用户意图和数据角色推荐模板，再用同一份 spec 验证并导出 HTML、PNG、PDF。用户不需要知道 composition 或 block id；只需在 `data analyze` 中描述目标。

模板选择规则：

| 用户意图 | 模板 | 输入要求 | 限制与 fallback |
|---|---|---|---|
| 单指标排名 | `data-poster-ranking` | 1 个类别字段 + 1 个数值字段，3–12 类 | 仅 vertical bar；不支持 stacked/horizontal/color series |
| 构成/占比 | `data-poster-share` | 类别字段 + 系列字段 + 非负数值 | 受控归一化到 100%；系列过多或总和无效时 blocked |
| 双指标对比 | `data-poster-comparison` | 1 个类别字段 + 2 个数值字段，3–12 类 | 无第二指标时 fallback 到 ranking |
| 连续变化 | `data-poster-trend` | 时间字段至少 3 个时间点 + 数值字段 | 支持 line/area；超容量时返回聚合建议 |
| 阶段流转 | `data-poster-flow` | 有序 stage + 数值字段 | 仅 funnel/sankey/infographic-flow 规则 |
| 地理比较 | `data-poster-geo` | geo 字段 + 数值字段，3–12 个实体 | 当前默认 geo ranking；无本地地图资源时稳定降级 |
| 历史/发展时间线 | `content-poster-timeline` | 本地 JSON 行数组：order、timeLabel、title、description | 图片仅读取本地路径；缺图降级为无图节点 |

推荐、缺失角色、fallback 和 warning 都会出现在 `context.poster.templates`。若结果为 blocked，先补齐提示的字段或改用 fallback，不要手工猜测字段含义。

典型工作流（以自动推荐为入口）：

```bash
miao-viz data analyze /path/to/data.csv \
  --intent "比较各国家肉类供应结构，并输出可分享的占比海报" \
  --output SYSTEM_TEMP/miao-vision/context.json

miao-viz spec template instantiate data-poster-share \
  --context SYSTEM_TEMP/miao-vision/context.json \
  --output SYSTEM_TEMP/miao-vision/poster.yaml

miao-viz data profile /path/to/data.csv > SYSTEM_TEMP/miao-vision/profile.json
miao-viz spec validate \
  --spec SYSTEM_TEMP/miao-vision/poster.yaml \
  --profile SYSTEM_TEMP/miao-vision/profile.json \
  --context SYSTEM_TEMP/miao-vision/context.json \
  --verify --strict
miao-viz render report \
  --input /path/to/data.csv \
  --spec SYSTEM_TEMP/miao-vision/poster.yaml \
  --context SYSTEM_TEMP/miao-vision/context.json \
  --format html,png,pdf --output-dir SYSTEM_TEMP/miao-vision/poster-output
```

当没有匹配的业务场景时，直接使用 `spec template instantiate <template-id>`；只有模板不可用时才退回 block。旧版 ranking spec 仍可直接验证和渲染。

最小 ranking spec 如下，`template`、`composition` 和默认 slots 会在内存中补齐：

```yaml
layout:
  preset: poster
poster:
  chartId: ranking-chart
  hero:
    title: Which Categories Rank Highest?
  footer:
    source: Internal analysis
charts:
  - id: ranking-chart
    type: bar
    encoding:
      x: { field: category }
      y: { field: value }
```

Render the same validated spec with `miao-viz render report --format html,png,pdf`. Poster PNG output is cropped to the poster canvas; PDF output is a single portrait page. Keep derived measures in the input data or an earlier validated transform; do not invent values or execute arbitrary formulas in the poster spec.

时间线输入必须先归一化为本地 JSON 行数组；CLI 不抓取 URL：

```json
[{"order":1,"timeLabel":"1901","title":"First event","description":"Evidence-backed description","era":"Early era","mediaPath":"./assets/event.png","source":"Local source"}]
```

建议持续统计结构化结果中的首次成功率、模板命中率、重试率、导出率、人工修改率，以及 blocked 原因分布；这些指标用于判断推荐是否真正降低了用户完成海报的成本。

For schema-compatible files that should be appended row-wise, pass
`--inputs /path/a.csv,/path/b.csv`. If source names differ, provide a JSON
`--field-map` whose keys are source fields and values are canonical fields. Stop on
`MULTI_FILE_SCHEMA_MISMATCH`; do not coerce incompatible types.

## Evidence And Claims

Every numeric, ranking, share, change, threshold, outlier, relationship, and comparison claim must cite an existing evidence id. Use values from `evidence[]` or `metricCandidates[]`; never calculate new prose metrics.

```yaml
insights:
  - text: "East contributed $evidence:by_dimension.rows[0].total."
    type: share
    provenance:
      evidence: [by_dimension]
      derivedFrom:
        - $evidence:by_dimension.rows[0].total
        - $evidence:total.values.total
      check: share_formula
      claimArgs:
        numerator: $evidence:by_dimension.rows[0].total
        denominator: $evidence:total.values.total
        expected: 0.42
    caveat: "Based on limited rows only."
    severity: info
```

Every KPI and chart also needs provenance. A trivial single-value binding may use
`provenance: $evidence:total.values.total_sales`; charts backed by multiple rows
should declare the exact evidence id and a path such as
`$evidence:by_dimension.rows`. Valid paths include
`$evidence:total.values.total_sales` and
`$evidence:by_dimension.rows[0].region`. Strict validation must resolve every path
and run the required claim check. Do not infer the first evidence value.

Reflect sample warnings:

- `extreme_small_sample`: mark rankings/comparisons as based on an extremely small sample.
- `small_sample`: qualify distribution and outlier claims.
- `two_period_only`: describe period-over-period change, not a trend.
- `one_period_only`: avoid time-based analysis.

Do not use causal, predictive, significant, or strong-correlation language without corresponding statistical evidence. Do not label performance good or bad without a benchmark, target, or historical comparison.

## Chart And Spec Rules

Use the CLI catalog as the source of truth. Never aggregate ids or use a field with `chartUsage.asMeasure: forbidden`.

| Intent | Preferred chart | Hard condition |
|---|---|---|
| KPI | `bigvalue` | Aggregate, sort, and limit to one row |
| Category comparison or Top N | `bar`, `dot`, or `lollipop` | Nominal dimension; ordered rows |
| Time trend | `line` or `area` | Time field, at least 3 periods, ascending sort |
| Part-to-whole | `pie`/donut | Meaningful whole, at most 7 slices |
| Two measures | `scatter` | No relationship claim without evidence |
| Distribution | `histogram` | Measure field and adequate rows |
| Exact detail | `table` | Explicit aggregate/filter, sort, and limit |
| Two endpoints | `dumbbell` | Exactly 2 comparable endpoints, at most 20 categories |
| Actual versus target | `bullet` | Explicit target |
| Lower/upper interval | `range` | Every lower value ≤ upper value |
| Ranked contribution | `pareto` | Non-negative values sorted descending |
| Different-unit measures | bar-line combo | Ordered dimension and explicit axis units |

Use only fields in the source or created earlier in the same transform chain. Add transforms that produce exactly the intended rows; the renderer does not aggregate, sort, or limit automatically. Keep reports to at most six charts, counting four bigvalues as one, and avoid redundant views.

## Recurring Reports

After the first report passes validation, preview initialization:

```bash
miao-viz report init /path/to/project \
  --input /path/to/period-1.xlsx \
  --spec SYSTEM_TEMP/miao-vision/report.yaml \
  --context SYSTEM_TEMP/miao-vision/context.json \
  --profile SYSTEM_TEMP/miao-vision/report-profile.yaml \
  --period 2026-W28 \
  --dry-run
```

Use `--profile` only when the user wants material outcome classification. The profile must contain
at least one Evidence metric and an absolute or percentage materiality threshold. Ask the user for
the preferred direction, target, or threshold when it affects the requested judgment. Do not infer
that an increase is favorable or that a decrease is adverse. Omit `desiredDirection` when the user
only wants a neutral comparison.

```yaml
schemaVersion: 1
metrics:
  - evidenceId: total
    metric: total_sales
    label: Sales
    desiredDirection: increase
    materiality:
      percent: 0.1
```

Present the contract, frozen Evidence ids, profile hash, path, and risks. Initialize without
`--dry-run` only after acceptance; use `--copy-input` only when requested. The first run has no
baseline and must not contain period comparison language.

For later periods:

```bash
miao-viz report info /path/to/project
miao-viz report update /path/to/project \
  --input /path/to/period-2.xlsx \
  --period 2026-W29 \
  --format html
```

Replay the saved spec and evidence recipes. Do not redesign, change evidence ids, or guess mappings. Treat data-contract, evidence-plan, validation, and PDF errors as failed runs. Run `report clean` only when the user explicitly requests deletion: show the preview, then obtain confirmation for the exact project and retention count before `--confirm`.

For a profile-aware project, use `runs/<period>/period-outcome-brief.json` and `review.json` as the
interpreted delivery state. `ready` can be delivered. `needs_review` requires the user to review the
listed reasons before sharing. `blocked` must not be delivered. Do not regenerate business meaning
from `changes.json` when a period outcome brief exists.

Generate one client report per update. Do not ask the user to choose a client, operator, or manager
edition. Keep the readable body client-facing; evidence, methodology, data-quality details,
anomalies, and review reasons belong in the collapsed diagnostics appendix. Only expose those
details separately when the user requests diagnostics.

Recurring projects are local artifacts: source data, profiles, Evidence, and reports remain on the
user's machine unless the user explicitly shares them. Do not describe a failed or blocked run as
delivered. Preserve the source files and project directory; generated reports are not a backup.

For diagnostics, inspect `runs/<period>/changes.json` and preserve its distinctions:

- `metrics`: absolute and percentage changes from comparable Evidence;
- `rankings`: entries, exits, and rank movement;
- `anomalies.added/removed`: newly observed and resolved anomaly records;
- `notComparable`: changed recipes, absent Evidence, zero-information rows, or no baseline.

Do not describe a `notComparable` item as unchanged. If the data contract fails, present the
returned field mapping, Sheet, or type-conversion repairs instead of retrying with guessed fields.

## Edit And Final Check

For an existing report, read the full source spec and make the minimum requested change. Before
validation, inspect the change contract:

```bash
miao-viz spec diff \
  --before SYSTEM_TEMP/miao-vision/before.yaml \
  --after SYSTEM_TEMP/miao-vision/after.yaml \
  --context SYSTEM_TEMP/miao-vision/context.json
```

Report the changed paths and affected charts, insights, and evidence. Then validate with
`--patch-hints --verify --strict` and render. Rewrite the spec only for an explicitly requested
redesign or when most of its structure must change.

To derive an executive summary from an already verified report:

```bash
miao-viz spec summary instantiate \
  --spec SYSTEM_TEMP/miao-vision/report.yaml \
  --context SYSTEM_TEMP/miao-vision/context.json \
  --output SYSTEM_TEMP/miao-vision/executive-summary.yaml
```

Keep the generated provenance sidecar with the summary. Do not add metrics or evidence ids that
are absent from the source report/context.

Before returning, confirm strict validation passed, every claim is evidence-grounded, sample caveats are present, all charts are allowed and nonredundant, fields and transforms are valid, and the requested artifact exists.
For an interactive artifact intended for third-party delivery, also require `value.shareSafe: true` and inspect `value.exposureManifest`. Do not deliver a report with `review` or `restricted` status as trusted.

## Deliver the artifact

When `value.delivery` is present, use it as the delivery source of truth. Show its status, PNG preview, primary HTML/PDF link, up to three verified metrics, up to two verified highlights, and no more than three actions. For recurring reports, include `period` and `changeCounts`; omit comparison language when no baseline exists. Do not read the generated HTML/PDF to create another summary, and do not expose Context, Profile, Spec, Evidence, or changes files unless the user requests diagnostics. If preview generation failed, deliver the primary artifact and mention the preview warning. If the client cannot display local images, use the shared Markdown fallback.

After a successful report, add one optional text action: “想比较版本、定向修改或导出 PDF/PNG？可以用 Review Viewer 查看。” Adapt its language to the conversation. Link to the local Viewer only when this report was tracked by an active Viewer. Otherwise offer to start a Viewer-backed revision; a Viewer started after this render does not automatically show the earlier report. Do not start or rerender solely to display the hint.

## Project weekly/monthly reports

For complete task snapshots, schedules, milestones and task-level period changes, use [project-report.md](project-report.md). The project workflow uses explicit configuration and period boundaries with the existing report commands; do not map task-count completion to whole-project progress.
