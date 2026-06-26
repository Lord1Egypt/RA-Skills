# Examples: Core Interaction Flows

> 3 个核心交互流程，覆盖最常见的使用场景。
> 完整交互规范见 `docs/interaction.md`。

---

## Flow 1: Query Historical Data (Chat)

### User Input
```
3号设备上周的土壤湿度
```

### Agent Thinking
1. alias="3号" → resolve sn via `query_device`
2. time="上周" → range = last Monday ~ last Sunday
3. param="土壤湿度" → includeParams = moisture
4. output intent = chat (implicit)

### Tool Calls
```
query_device(alias="3号")
  → sn = "00000000000001"

query_data(sn="00000000000001", time_expression="上周", includeParameters="moisture")
  → GET /v3/device/00000000000001/data?range=20250505,20250511&includeParams=moisture
```

### Output
```markdown
📊 3号大棚 — 上周土壤湿度 (2025-05-05 ~ 2025-05-11)

| 日期 | 10cm | 20cm | 30cm | 40cm |
|------|------|------|------|------|
| 05-05 | 22.1 | 23.5 | 25.1 | 26.5 |
| ... | ... | ... | ... | ... |

📈 趋势小结:
- 各层湿度平稳，40cm深层保持最高
- 10cm表层受蒸发影响日间波动稍大
```

---

## Flow 2: Export Data (File)

### User Input
```
导出3号设备上个月数据为CSV
```

### Agent Thinking
1. alias="3号" → resolve sn
2. time="上个月" → range = 20250401,20250430
3. format="CSV" → export_csv
4. Validate: 30 days ≤ 365 days → OK

### Tool Calls
```
query_device(alias="3号") → sn = "00000000000001"

export_csv(sn="00000000000001", range="20250401,20250430", output="3号_2025-04.csv")
  → 成功导出 720 条数据
```

### Output
```
✅ 导出成功

📄 文件: 3号_2025-04.csv
📊 数据条数: 720 条
📅 时间范围: 2025-04-01 至 2025-04-30
📥 文件路径: /absolute/path/to/3号_2025-04.csv
```

---

## Flow 3: Generate Report (Data Availability Mismatch)

### User Input
```
分析11684501348336近三个月的数据，生成报告
```

### Agent Thinking
1. alias="11684501348336" → resolve sn
2. time="近3个月" → requested range = 2026-02-22 ~ 2026-05-22 (90 days)
3. query_data → retrieve actual data
4. **数据可用性校验**: actual = 2025-05-10 ~ 2025-05-22 (13 days)
5. coverage = 13/90 = 14% < 50% → **STOP and confirm**

### Tool Calls
```
query_device(alias="11684501348336") → sn = "11684501348336"

query_data(sn="11684501348336", time_expression="最近3个月")
  → actual range: 2025-05-10 ~ 2025-05-22 (13 records)
```

### Agent Confirmation
```
您请求的『近3个月』共约 90 天，
但该设备实际仅有 2025-05-10 至 2025-05-22 共 13 天的数据。

可能原因：
- 设备在该时间段尚未部署或激活
- 设备期间出现离线/故障导致数据缺失

是否继续基于现有 13 天数据生成报告？
```

### User Response
```
继续
```

### Analysis & Report Generation
```
→ 统计摘要: 均值、最大、最小、标准差
→ 趋势分析: 线性变化率
→ 异常检测: 扫描 battery, moisture, temperature
→ 构建 HTML (ECharts line chart + summary cards)
→ write_html → report.html
```

### Output
```
✅ 报告已生成

📄 文件: report_11684501348336.html
📊 分析数据: 13 条 (2025-05-10 至 2025-05-22)
⚠️  注: 基于实际可用数据，非完整 3 个月
📥 文件路径: /absolute/path/to/report_11684501348336.html
```

---

## Other Scenarios

更多场景（多设备对比、批量导出、实时查询、告警检测）见：
- `examples/queries.md` — 查询类对话示例
- `examples/reports.md` — 报告生成示例
- `docs/interaction.md` Section 5 — 完整确认策略
