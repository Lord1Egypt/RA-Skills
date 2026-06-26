# compare 命令 JSON 输出 Schema 定义

> **Late Brake 项目文档**
>
> 本文档完整定义 `late-brake compare` 命令使用 `--json` 参数输出的 JSON 结构。
> 这个定义用于给 LLM 分析对比结果提供清晰的 schema 参考，确保 LLM 能正确理解每个字段含义。

本文档完整定义 `late-brake compare` 命令使用 `--json` 参数输出的 JSON 结构。

## 1. 顶层结构

```json
{
  "file1_path": "string",
  "file2_path": "string",
  "lap1_number": "integer",
  "lap2_number": "integer",
  "track_id": "string",
  "track_name": "string",
  "lap1": {
    "total_time": "float",
    "total_distance": "float"
  },
  "lap2": {
    "total_time": "float",
    "total_distance": "float"
  },
  "total_time_diff": "float",
  "sector_diff": [
    ... // 分段对比数组，见下文
  ],
  "turn_diff": [
    ... // 弯道对比数组，见下文
  ]
}
```

### 顶层字段说明

| 字段 | 类型 | 单位 | 说明 |
|------|------|------|------|
| `file1_path` | string | - | 第一个对比文件路径 |
| `file2_path` | string | - | 第二个对比文件路径 |
| `lap1_number` | int | - | 第一个对比圈号（用户输入的圈号） |
| `lap2_number` | int | - | 第二个对比圈号（用户输入的圈号） |
| `track_id` | string | - | 赛道ID |
| `track_name` | string | - | 赛道名称 |
| `lap1.total_time` | float | 秒 | 圈1总圈时 |
| `lap1.total_distance` | float | 米 | 圈1总行驶距离 |
| `lap2.total_time` | float | 秒 | 圈2总圈时 |
| `lap2.total_distance` | float | 米 | 圈2总行驶距离 |
| `total_time_diff` | float | 秒 | 总圈时差 = `lap2.total_time - lap1.total_time` <br> 规则：**正值表示圈2比圈1慢，负值表示圈2比圈1快** |
| `sector_diff` | array | - | 分段对比结果数组，如果赛道没有分段信息则为空数组 |
| `turn_diff` | array | - | 弯道对比结果数组，如果赛道没有弯道信息则为空数组 |

### 浮点精度

所有浮点数字段遵循 `docs/data-format.md` 中的精度约定：

- 时间字段保留 4 位小数
- 距离字段保留 2 位小数
- 速度字段保留 2 位小数

---

## 2. 分段对比结构 (`sector_diff[]`)

```json
{
  "sector_id": "string",
  "sector_name": "string",
  "start_distance": "float",
  "end_distance": "float",
  "time1": "float",
  "time2": "float",
  "time_diff": "float",
  "avg_speed1": "float",
  "avg_speed2": "float",
  "avg_speed_diff": "float"
}
```

### 分段字段说明

| 字段 | 类型 | 单位 | 说明 |
|------|------|------|------|
| `sector_id` | string | - | 分段ID |
| `sector_name` | string | - | 分段名称 |
| `start_distance` | float | 米 | 分段起点距离赛道起点的距离 |
| `end_distance` | float | 米 | 分段终点距离赛道起点的距离 |
| `time1` | float | 秒 | 圈1通过该分段的用时 |
| `time2` | float | 秒 | 圈2通过该分段的用时 |
| `time_diff` | float | 秒 | 用时差 = `time2 - time1`，正值表示圈2慢 |
| `avg_speed1` | float | km/h | 圈1在该分段的平均速度 |
| `avg_speed2` | float | km/h | 圈2在该分段的平均速度 |
| `avg_speed_diff` | float | km/h | 平均速度差 = `avg_speed2 - avg_speed1`，正值表示圈2更快 |

---

## 3. 弯道对比结构 (`turn_diff[]`)

```json
{
  "turn_name": "string",
  "turn_type": "string",
  "start_distance": "float",
  "apex_distance": "float",
  "end_distance": "float",
  "time1": "float",
  "time2": "float",
  "time_diff": "float",
  "speed_entry1": "float",
  "speed_entry2": "float",
  "speed_entry_diff": "float",
  "speed_apex1": "float",
  "speed_apex2": "float",
  "speed_apex_diff": "float",
  "speed_exit1": "float",
  "speed_exit2": "float",
  "speed_exit_diff": "float",
  "avg_speed1": "float",
  "avg_speed2": "float",
  "avg_speed_diff": "float"
}
```

### 弯道字段说明

| 字段 | 类型 | 单位 | 说明 |
|------|------|------|------|
| `turn_name` | string | - | 弯道名称（一般是编号，如"T1"） |
| `turn_type` | string | - | 弯道类型（"left"/"right"） |
| `start_distance` | float | 米 | 弯道起点距离赛道起点距离 |
| `apex_distance` | float | 米 | 弯心距离赛道起点距离 |
| `end_distance` | float | 米 | 弯道终点距离赛道起点距离 |
| `time1` | float | 秒 | 圈1通过该弯道的用时 |
| `time2` | float | 秒 | 圈2通过该弯道的用时 |
| `time_diff` | float | 秒 | 用时差 = `time2 - time1`，正值表示圈2慢 |
| `speed_entry1` | float | km/h | 圈1入弯速度 |
| `speed_entry2` | float | km/h | 圈2入弯速度 |
| `speed_entry_diff` | float | km/h | 入弯速度差 = `speed_entry2 - speed_entry1`，正值表示圈2更快 |
| `speed_apex1` | float | km/h | 圈1弯心速度 |
| `speed_apex2` | float | km/h | 圈2弯心速度 |
| `speed_apex_diff` | float | km/h | 弯心速度差 = `speed_apex2 - speed_apex1`，正值表示圈2更快 |
| `speed_exit1` | float | km/h | 圈1出弯速度 |
| `speed_exit2` | float | km/h | 圈2出弯速度 |
| `speed_exit_diff` | float | km/h | 出弯速度差 = `speed_exit2 - speed_exit1`，正值表示圈2更快 |
| `avg_speed1` | float | km/h | 圈1整个弯道平均速度 |
| `avg_speed2` | float | km/h | 圈2整个弯道平均速度 |
| `avg_speed_diff` | float | km/h | 平均速度差 = `avg_speed2 - avg_speed1`，正值表示圈2更快 |

---

## 4. 完整示例

```json
{
  "file1_path": "PGEAR-Tianma-M4.vbo",
  "file2_path": "tianma_0125_1.vbo",
  "lap1_number": 1,
  "lap2_number": 2,
  "track_id": "tianma",
  "track_name": "Shanghai Tianma Circuit",
  "lap1": {
    "total_time": 68.95,
    "total_distance": 2056.30
  },
  "lap2": {
    "total_time": 76.00,
    "total_distance": 2058.12
  },
  "total_time_diff": 7.05,
  "sector_diff": [
    {
      "sector_id": "s1",
      "sector_name": "Main Straight",
      "start_distance": 0,
      "end_distance": 550,
      "time1": 10.2340,
      "time2": 10.8500,
      "time_diff": 0.6160,
      "avg_speed1": 193.25,
      "avg_speed2": 182.30,
      "avg_speed_diff": -10.95
    }
  ],
  "turn_diff": [
    {
      "turn_name": "T1",
      "turn_type": "right",
      "start_distance": 550,
      "apex_distance": 620,
      "end_distance": 680,
      "time1": 5.1230,
      "time2": 5.6800,
      "time_diff": 0.5570,
      "speed_entry1": 145.20,
      "speed_entry2": 138.50,
      "speed_entry_diff": -6.70,
      "speed_apex1": 68.30,
      "speed_apex2": 62.10,
      "speed_apex_diff": -6.20,
      "speed_exit1": 88.40,
      "speed_exit2": 82.10,
      "speed_exit_diff": -6.30,
      "avg_speed1": 78.50,
      "avg_speed2": 72.30,
      "avg_speed_diff": -6.20
    }
  ]
}
```

## 5. 符号约定总结

| 差值类型 | 计算方式 | 正号含义 | 负号含义 |
|----------|----------|----------|----------|
| 时间差 | `value2 - value1` | 圈2比圈1慢 | 圈2比圈1快 |
| 速度差 | `value2 - value1` | 圈2比圈1快 | 圈2比圈1慢 |

这个约定在文本输出和JSON输出中保持一致。
