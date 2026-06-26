# 统计分析

统计命令用于查看观看、并发、观众分布和导出报表。

## 每日观看统计

```bash
<CLI> statistics view \
  -c <频道ID> \
  --start-day 2024-01-01 \
  --end-day 2024-01-31

<CLI> statistics view \
  -c <频道ID> \
  --start-day 2024-01-01 \
  --end-day 2024-01-31 \
  -o json
```

## 历史并发数据

```bash
<CLI> statistics concurrency \
  -c <频道ID> \
  --start-date 2024-01-01 \
  --end-date 2024-01-31
```

## 历史最高并发

```bash
<CLI> statistics max-concurrent \
  -c <频道ID> \
  --start-time 1704067200000 \
  --end-time 1706745600000
```

`max-concurrent` 的时间范围不要超过 3 个月。

## 观众统计

```bash
<CLI> statistics audience device -c <频道ID>
<CLI> statistics audience region -c <频道ID>
```

## 导出观看日志

```bash
<CLI> statistics export viewlog \
  -c <频道ID> \
  --start-time "2024-01-01 00:00:00" \
  --end-time "2024-01-31 23:59:59"
```

导出 CSV 文件：

```bash
<CLI> statistics export viewlog \
  -c <频道ID> \
  --start-time "2024-01-01 00:00:00" \
  --end-time "2024-01-31 23:59:59" \
  --watch-type live \
  --output-file ./viewlog.csv
```

| 参数 | 说明 |
| --- | --- |
| `-c, --channel-id` | 频道 ID |
| `--start-time` | 开始时间，格式 `yyyy-MM-dd HH:mm:ss` |
| `--end-time` | 结束时间，格式 `yyyy-MM-dd HH:mm:ss` |
| `--watch-type` | `live` 或 `vod` |
| `--output-file` | 导出 CSV 文件路径 |
| `-o, --output` | `table` 或 `json` |

## 导出场次报表

```bash
<CLI> statistics export session \
  -c <频道ID> \
  --session-id fv3ma84e63

<CLI> statistics export session \
  -c <频道ID> \
  --session-id fv3ma84e63 \
  -o json
```

场次报表返回下载链接，下载链接有效期以接口返回和平台规则为准。

## 常用参数

| 参数 | 说明 |
| --- | --- |
| `-c, --channel-id` | 频道 ID |
| `--start-day`、`--end-day` | `statistics view` 使用，格式 `YYYY-MM-DD` |
| `--start-date`、`--end-date` | `statistics concurrency` 使用，格式 `YYYY-MM-DD` |
| `--start-time`、`--end-time` | 时间戳或日期时间，按具体子命令帮助为准 |
| `-o, --output` | `table` 或 `json` |

## 使用注意

- 统计数据可能存在处理延迟，刚结束的直播不一定立即可查。
- 导出观看日志的开始和结束时间需要在同一个月内。
- 自动化脚本优先使用 `-o json` 或 `--output-file`，不要解析表格输出。
