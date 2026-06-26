# Theme Routing

## Auto-detect Language

Use `zh` when CJK is material or appears in the title/topic; otherwise use `en`. Apply to placeholders, TOC labels, date display, and shell labels.

## Theme Selection (first match wins)

| Signal | Theme |
|--------|-------|
| weekly/daily/monthly/work progress/周报/日报/月报/本周/下周 | `regular-lumen` |
| sales/revenue/KPI/quarterly/business/销售/营收/业绩/季报 | `corporate-blue` |
| research/survey/whitepaper/internal/研究/调研/白皮书 | `minimal` |
| tech/architecture/API/system/performance/工程/架构 | `dark-tech` |
| news/industry/trend/新闻/行业/趋势 | `newspaper` |
| annual/story/growth/retrospective/年度/增长/复盘 | `data-story` |
| formal document/official notice/公文/正式报告/通知/制度 | `fangsong` |
| board/dashboard/status/看板 | `dark-board` |
| generic project progress/项目进展/项目状态 | `corporate-blue` |

## Report Class

Classify content by numeric density: `narrative` < 5%, `mixed` 5-20%, `data` > 20%; short topics default to `mixed`.
