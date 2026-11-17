<!-- DOCKEY: dash-5a2d6 -->
# Informat Dashboard UI Preset Quick Reference

Follow this file when generating dashboard cards. If the user does not specify visual details, use the default theme, layout, and beautified fields. If the user specifies one item, override only that item and keep the rest of the preset.

## §0 Mandatory Rules

1. All cards in one dashboard must use the same theme palette.
2. Before creating multiple cards, choose a layout template, assign `width` / `height` / order, then create cards one by one.
3. The dashboard grid has 24 columns; each row's `width` sum must equal 24 exactly.
4. Top-level `enableCardStyle` must be `true`, otherwise `cardStyle` is ignored.
5. Colors must be 6-digit HEX. Do not use pure black, pure white, or gray-scale values as primary colors. `cardStyle.bgGradientColor` may use CSS `linear-gradient(...)`.
6. Number cards must set `xPosition: "center"` and `yPosition: "center"`.
7. `DashboardCardDefine.subTitle` must not duplicate `name`, `numberSetting.title`, or series names; omit it when redundant.
8. ProChart must have a real data source: non-empty `proChartSetting.dataset` bound to a real `tableId` or `expression`, and non-empty `series`.
9. `orderByList` must be an object array, e.g. `{"field":"amount","type":"desc"}`; never use `"amount#desc"`.
10. Data labels, gradients, rounded corners, and shadows are on by default. Never generate raw ECharts defaults.
11. Business fields must not be named `id` or `seq`.

## §1 Theme Palettes

| Theme | Use | palette | primary | gradient | text | bg |
|---|---|---|---|---|---|---|
| Aqua Sky Default | General business | `#5B8FF9,#5AD8A6,#5D7092,#F6BD16,#E8684A,#6DC8EC,#945FB9,#FF9845` | `#5B8FF9` | `#85B4FF -> #3366E5` | `#5D7092` | `#FFFFFF` |
| Enterprise Violet | Enterprise/IT/finance/project | `#7262FD,#8861E4,#5B8FF9,#6DC8EC,#945FB9,#5AD8A6,#FAAD14,#F6BD16` | `#7262FD` | `#A593FF -> #4D3CCC` | `#5D7092` | `#FFFFFF` |
| Vivid Multi | Ops/marketing/growth/content | `#FF6B6B,#4ECDC4,#FFD93D,#6BCB77,#4D96FF,#FF9F40,#9D4EDD,#FF8FA3` | `#FF6B6B` | `#FF9B9B -> #E54B4B` | `#4A4A4A` | `#FFFFFF` |
| Forest | ESG/agriculture/health | `#27AE60,#6FCF97,#219653,#F2C94C,#56CCF2,#2D9CDB,#9B51E0,#EB5757` | `#27AE60` | `#5DD995 -> #1B7E45` | `#3D5849` | `#FFFFFF` |
| Sunset | Retail/catering/service | `#F2994A,#F2C94C,#EB5757,#FF7A45,#FFA940,#FFC53D,#73D13D,#36CFC9` | `#F2994A` | `#FFB873 -> #D9711B` | `#664423` | `#FFFFFF` |
| Dark Cyber | Big screen/monitoring/IoT | `#00D9FF,#7C3AED,#F472B6,#FBBF24,#34D399,#60A5FA,#F87171,#A78BFA` | `#00D9FF` | `#5BEAFF -> #0095B3` | `#C8D3E5` | `#1F2937` |
| Morandi | Brand/design/art | `#C8A2C8,#A8C5DA,#B8C5A6,#E8B4B8,#D4A5A5,#F4C2C2,#9FB8C8,#C9C5BA` | `#C8A2C8` | `#E0C3E0 -> #9B73A6` | `#7A6B73` | `#FAFAFA` |

Use Aqua Sky by default. If the app or dashboard name matches a business keyword in the table, use that theme.

## §2 Common Fields

### Default cardStyle

```json
{"bgType":"image","bgColor":"<theme.bg>","padding":16,"paddingTop":12,"paddingRight":16,"paddingBottom":12,"paddingLeft":16,"paddingControl":true,"borderWidth":0,"borderRadius":12,"titleFontSize":"16px","titleFontWeight":"600","titleColor":"<theme.text>","titlePosition":"left","subTitleFontSize":"12px","subTitleColor":"<theme.text>","subTitlePosition":"titleRight","enableBorderImage":false}
```

### KPI Number override

```json
{"bgType":"gradient","bgColor":"<kpiTint>","bgGradientColor":"linear-gradient(135deg, <light> 0%, #FFFFFF 100%)","borderRadius":16,"padding":20,"paddingControl":false,"borderWidth":0,"titleFontSize":"13px","titleFontWeight":"500","titleColor":"<theme.text>","titlePosition":"left"}
```

For Dark Cyber KPI gradients, end at `#1F2937`; ProChart cards use `#1F2937` as background without an extra card gradient.

### Top-level switches

```json
{"enableCardStyle":true,"enableRefresh":false,"refreshTime":30,"disableToolbar":false,"enableButton":false,"filterLabelPosition":"top","disableFilterCache":false}
```

## §3 Card Sizes

| Card | Scenario | width | height | Key requirement |
|---|---|---:|---:|---|
| Number compact 4 | Top KPIs | 6 | 4 | fontSize 36, centered |
| Number compact 6 | Many KPIs | 4 | 4 | fontSize 30, centered |
| Number standard | Single key metric | 8 | 6 | fontSize 56, centered |
| Number hero | 1-2 focus metrics | 12/24 | 8 | fontSize 80, centered |
| ProChart main | Main trend/analysis | 16/24 | 8 | grid leaves label room |
| ProChart secondary | Distribution/ranking | 8/12 | 8 | clear legend |
| Record | Detail list | 12/24 | 8 | 4-6 fields |
| Pivot | Cross table | 12/24 | 8 | clear row/column dimensions |
| Table | Expression/automation table | 12/24 | 8 | stable column widths |

Number defaults: `aggregation=true`, `aggregationSplitMultiValue=false`, `groupByFieldList=[]`, `orderByList=[]`, `format="comma"`, `precision=0`, `unit=""`, `fontWeight="bold"`. Do not invent a unit when the business does not require one.

## §4 Layout Templates

| Template | Use | Row layout |
|---|---|---|
| A KPI Dashboard default | General | 4 KPIs: `6+6+6+6`; main trend + ranking: `16+8`; distribution + details: `12+12` |
| B Trend Monitor | Ops/growth | 4 KPIs; large trend `24`; channel/group charts `12+12` |
| C Analytics Deep Dive | Reporting | 3 metrics `8+8+8`; main analysis `24`; pivot + details `12+12` |
| D Comprehensive | Rich dashboard | 6 KPIs: `4*6`; main + side `16+8`; three small charts `8+8+8` |
| E Simple Feed | Clean list view | 2 KPIs: `12+12`; main list `24`; two charts `12+12` |
| F Single Focus | One topic | Hero Number/Chart `24`; supporting `12+12` |
| G 6-KPI Top | Many metrics | KPIs `4*6`; main chart `24`; bottom `8+8+8` |
| H 4-Column Small Charts | Dense small charts | 4 KPIs; four charts `6+6+6+6`; details `24` |
| I Complex Split | Big-screen view | 6 KPIs; left/middle/right `6+12+6`; bottom `8+8+8` |
| J Three KPI Rows | Dense numbers | Three KPI rows, each `6+6+6+6`; bottom trend `24` |

## §5 ProChart Choice

| Data intent | Chart |
|---|---|
| Time trend / continuous change | line, default gradient area |
| Category comparison / Top N | bar, default rounded gradient; use horizontal bars for long categories |
| Share / composition | pie, default solid pie + outside labels; use donut only for center emphasis |
| Relationship between two measures | scatter |
| Multi-dimensional capability | radar |
| Progress / completion rate | gauge |
| Funnel conversion | funnel |
| Two-dimensional density | heatmap |
| Hierarchical share | treemap / sunburst |
| Financial OHLC | candlestick |
| Distribution spread | boxplot |
| Calendar heat | Do not generate by default unless explicitly requested |

## §6 ProChart Beautification Defaults

1. `tooltip.trigger`: use `axis` for coordinate charts, `item` for pie/funnel/tree charts.
2. `legend` defaults to centered `top: 0`; use scroll when there are many series.
3. Coordinate chart `grid`: `{left: 48,right: 24,top: 48,bottom: 40,containLabel: true}`.
4. Axes use subtle axis/grid lines, theme secondary label color, and avoid crowded rotation.
5. line: `smooth=true`, `symbolSize=6`, `lineStyle.width=3`, with gradient `areaStyle`.
6. bar: `barMaxWidth=36`, `itemStyle.borderRadius=[8,8,0,0]`, theme gradient.
7. pie: `radius=["0%","68%"]`, `center=["50%","55%"]`, outside labels, white sector border.
8. donut: `radius=["42%","68%"]`, only when center space is needed.
9. radar/gauge/funnel/heatmap/treemap/sunburst must have readable labels, theme colors, gradients or hierarchy color ramps.

## §7 Generation Workflow

1. Query tables and fields to get real `tableId` / `fieldId`.
2. Choose one theme and record palette/primary/text/bg.
3. Pick a layout template based on card count and business purpose; each row width must sum to 24.
4. Choose each card type: Number / ProChart / Record / Pivot / Table.
5. Fill top-level switches, `cardStyle`, and the card-specific setting. Number cards must be centered; KPI cards do not send top-level `subTitle`.
6. For ProChart, choose chart type first, then fill dataset, series, axes, grid, legend, tooltip, and beautification.
7. Create cards serially, then verify theme consistency, row width 24, no duplicate subtitle, and chart data source.

## §8 Anti-Patterns

- Mixing themes in one dashboard, or giving every card arbitrary `width=12`.
- Row width below 24 causing empty right space, or above 24 causing unexpected wrapping.
- Left-aligned Number cards, duplicate KPI subtitles, or invented units.
- ProChart without dataset / series, or raw ECharts default colors.
- Defaulting pies to donut or rose; use them only when requested or clearly appropriate.
- String sorting, invented field IDs, or configuring aggregation before querying field structure.
