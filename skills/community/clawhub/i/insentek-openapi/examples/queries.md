# Examples: Query Conversations — 查询类对话示例

> 展示用户如何用自然语言查询设备数据，以及 Agent 的完整处理过程。
> 完整交互规范见 [`docs/interaction.md`](../docs/interaction.md)。

---

## Example 1: 查看设备列表

### User Input
```
查看我的所有设备
```

### Agent Thinking
1. 用户没有提供 sn 或 alias → 调用设备列表查询
2. 无时间线索 → 不需要 query_data
3. 若 `${SKILL_ROOT}` / `${PYTHON}` 未知 → `info --json` 解析安装路径与 python 命令
4. 脚本自动从本地凭据读取 token；若未连接则展示 login 引导文案

### Tool Calls
```
info --json  →  installDir = ~/.openclaw/workspace/skills/insentek-openapi
            →  python.command = python3
query_device(page=1, limit=20)
  → ${PYTHON} ${SKILL_ROOT}/scripts/insentek_cli.py devices --page 1 --limit 20
  → GET /v3/devices?page=1&limit=20
```

### Formatted Output
```
📋 设备列表（共 3 台）

┌─────┬──────────────┬──────────┬────────┬──────────┐
│ 序号 │ 别名         │ 类型     │ 状态   │ 位置     │
├─────┼──────────────┼──────────┼────────┼──────────┤
│ 1   │ 1号大棚      │ 土壤监测 │ 工作中 │ 甘肃兰州 │
│ 2   │ 2号大棚      │ 土壤监测 │ 工作中 │ 甘肃兰州 │
│ 3   │ 气象站A      │ 气象监测 │ 工作中 │ 甘肃兰州 │
└─────┴──────────────┴──────────┴────────┴──────────┘

💡 提示: 直接说"1号大棚的温度"即可查询具体设备数据
```

---

## Example 2: 查询实时数据

### User Input
```
1号大棚现在的土壤温度和湿度
```

### Agent Thinking
1. 用户提供了 alias="1号大棚" → 需要先解析为 sn
2. 时间线索: "现在" → 调用 /latest 端点
3. 参数过滤: "土壤温度" → temperature, "湿度" → moisture

### Tool Calls
```
query_device(alias="1号大棚")
  → GET /v3/devices (find matching alias)
  → sn = "00000000000001"
  → GET /v3/device/00000000000001/description

query_data(sn="00000000000001", time_expression="现在", includeParameters="temperature,moisture")
  → GET /v3/device/00000000000001/latest
```

### Formatted Output
```
📍 1号大棚 (0001)
─────────────────────────
🕐 2025-05-13 14:32:18

🌡️ 土壤温度:
   10cm: 18.5 ℃
   20cm: 17.2 ℃
   30cm: 16.8 ℃
   40cm: 16.1 ℃

💧 土壤水分:
   10cm: 23.4 %
   20cm: 24.1 %
   30cm: 25.6 %
   40cm: 27.2 %

─────────────────────────
状态: 工作中 | 位置: 甘肃兰州
```

---

## Example 3: 查询历史数据（带趋势分析）

### User Input
```
1号大棚最近7天的土壤温度变化趋势
```

### Agent Thinking
1. alias="1号大棚" → 解析 sn
2. 时间线索: "最近7天" → range = today-7d ~ today
3. 参数: "土壤温度" → temperature
4. 用户要求"趋势" → 需要计算平均值、最大值、最小值、变化率

### Tool Calls
```
query_device(alias="1号大棚")
  → sn = "00000000000001"

query_data(sn="00000000000001", time_expression="最近7天", includeParameters="temperature")
  → GET /v3/device/00000000000001/data?range=20250506,20250513&includeParameters=temperature
```

### Formatted Output
```
📊 1号大棚 — 最近7天土壤温度

| 日期       | 10cm  | 20cm  | 30cm  | 40cm  |
|-----------|-------|-------|-------|-------|
| 05-06     | 17.2  | 16.5  | 16.1  | 15.8  |
| 05-07     | 18.1  | 17.0  | 16.5  | 16.0  |
| 05-08     | 19.5  | 17.8  | 17.0  | 16.3  |
| 05-09     | 20.3  | 18.5  | 17.4  | 16.5  |
| 05-10     | 19.8  | 18.2  | 17.2  | 16.4  |
| 05-11     | 18.6  | 17.5  | 16.8  | 16.1  |
| 05-12     | 18.0  | 17.0  | 16.5  | 15.9  |
| 05-13     | 18.5  | 17.2  | 16.8  | 16.1  |

📈 趋势小结（10cm 层）:
• 平均: 18.75 ℃
• 最高: 20.3 ℃ @ 05-09
• 最低: 17.2 ℃ @ 05-06
• 变化: +1.3 ℃ (+7.6%) — 总体平稳略升
```

---

## Example 4: 查询指定时刻数据

### User Input
```
气象站A昨天中午12点的数据
```

### Agent Thinking
1. alias="气象站A" → 解析 sn
2. 时间线索: "昨天中午12点" → /moment/{datetime}
3. datetime = "2025-05-12 12:00:00"

### Tool Calls
```
query_device(alias="气象站A")
  → sn = "00000000000003"

query_data(sn="00000000000003", time_expression="昨天中午12点")
  → GET /v3/device/00000000000003/data/moment/2025-05-12%2012:00:00
```

### Formatted Output
```
📍 气象站A — 2025-05-12 12:00:00

🌡️ 空气温度: 24.5 ℃
💧 相对湿度: 58.3 %
💨 风速: 3.2 m/s (东南)
🌧️ 降雨量: 0.0 mm
☀️ 太阳辐射: 856 W/m²
```

---

## Example 5: 多设备对比

### User Input
```
对比一下1号大棚和2号大棚的土壤湿度
```

### Agent Thinking
1. 两个 alias 需要分别解析
2. 时间: 无 → 默认"现在"（/latest）
3. 参数: "土壤湿度" → moisture
4. 需要并排比较并计算差异

### Tool Calls
```
query_device(alias="1号大棚") → sn1 = "00000000000001"
query_device(alias="2号大棚") → sn2 = "00000000000002"

query_data(sn="00000000000001", time_expression="现在", includeParameters="moisture")
query_data(sn="00000000000002", time_expression="现在", includeParameters="moisture")
```

### Formatted Output
```
📊 土壤湿度对比 — 实时数据

| 深度  | 1号大棚 | 2号大棚 | 差异     │
|-------|---------|---------|----------│
| 10cm  | 23.4 %  │ 19.8 %  │ +3.6 % ↑ │
| 20cm  | 24.1 %  │ 21.5 %  │ +2.6 % ↑ │
| 30cm  | 25.6 %  │ 24.2 %  │ +1.4 % ↑ │
| 40cm  | 27.2 %  │ 26.8 %  │ +0.4 % ↑ │

💡 分析: 1号大棚各层湿度均高于2号大棚，10cm层差异最大（+3.6%）
```
