# Query Scenarios

Single entry point for routing natural language queries to the correct reference file.

## Decision Tree

```
NL Query
    │
    ├─ Contains DDL keywords (CREATE, DROP, INSERT)? ──→ ts-ddl.md
    │
    ├─ "最近"/"latest"/"最新"/"最近一条"/"current" ──→ ts-latest-value.md
    │
    ├─ "滑动"/"session"/"event"/"window"/"STATE_WINDOW"/"COUNT_WINDOW" ──→ ts-window-events.md
    │
    ├─ "填充"/"fill"/"gap"/"missing"/"插值"/"linear" ──→ ts-interpolation.md
    │
    ├─ "每小时"/"每天"/"每X分钟" + 聚合词 ──→ ts-downsampling.md
    │
    ├─ JOIN 时序表 + 关系表? ──→ cross-model.md
    │
    └─ Default ──→ relational.md
```

## Keyword Mapping

### DDL
| CN | EN |
|----|----|
| 创建库 | CREATE DATABASE |
| 创建表 | CREATE TABLE |
| 时序库/时序表 | CREATE TABLE ... TAGS |
| 添加标签 | ADD TAG |

### Latest Value
| CN | EN |
|----|----|
| 最新 | latest, last |
| 最近一条 | most recent |
| 当前 | current |

### Interpolation
| CN | EN |
|----|----|
| 填充 | fill |
| 插值 | interpolate |
| 缺失/gap | missing, gap |

### Downsampling
| CN | EN |
|----|----|
| 每小时 | hourly, every hour |
| 每天 | daily, every day |
| 平均值 | average |
| 统计 | statistics |
| 降采样 | downsampling |

### Window Events
| CN | EN |
|----|----|
| 滑动窗口 | sliding window |
| session | session |
| event | event |
| 状态变化 | state change |

## Quick Reference

| Query Type | Reference | Key Function |
|------------|-----------|--------------|
| 创建时序库/表 | ts-ddl.md | `CREATE TS DATABASE`, `CREATE TABLE ... TAGS` |
| 每小时/每天的平均值 | ts-downsampling.md | `time_bucket()` |
| 填充缺失值 | ts-interpolation.md | `time_bucket_gapfill()` + `interpolate()` |
| 最新/最近一条 | ts-latest-value.md | `last()`, `last_row()` |
| 滑动窗口/session/event | ts-window-events.md | `TIME_WINDOW()`, `SESSION_WINDOW()`, `EVENT_WINDOW()` |
| 时序表 + 关系表 JOIN | cross-model.md | JOIN |
| 标准 SQL | relational.md | - |

## Special Cases

### TWA (Time Weighted Average)
```
"计算时间加权平均温度"
```
→ ts-window-events.md (TWA section)

### diff() Function
```
"计算温度变化率"
```
→ ts-window-events.md (diff section)

## Ambiguity Resolution

1. **Ask user**: "这是时序查询还是普通SQL查询?"
2. **Check schema**: 有 `ts`/`timestamp` 列和 `TAGS` → 时序查询
3. **Default to time-series** if truly ambiguous

## Fallback: Schema-Aware Routing

When no keywords match, check table schema via MCP (if available):
- Has `ts`/`timestamp` column + `TAGS` array → time-series query
- Otherwise → relational.md

## MCP Schema Check

After routing, verify table type via MCP (if available):
1. Read `kwdb://table/{table_name}`
2. Check `table_type`: `"TIME SERIES"` 或 `"relational"`
