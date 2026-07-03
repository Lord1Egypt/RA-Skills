---
name: jiebang-timezone-convert
description: 时区转换工具，提供全球时区查询和时间转换功能。当用户提到时区转换、世界时钟、不同时区时间对比、时差计算、UTC转换、北京时间转纽约时间、时区查询、跨时区会议时间等需求时使用此技能。
---

# 捷帮时区转换

时区转换工具，基于捷帮工具站API，提供全球时区查询和时间转换功能。

## 何时使用

当用户有以下需求时触发本技能：
- 查询某个时区的当前时间
- 将一个时区的时间转换为另一个时区
- 计算两个时区之间的时差
- 跨时区安排会议时间
- UTC时间与本地时间互转

## 工作流程

1. 确定用户需要的操作类型（convert/query）
2. 调用对应的API接口
3. 返回转换结果

### 1. 时区转换 (convert)

调用 `main.py` 的 `timezone_convert` 函数：
- `time`: 要转换的时间（格式：YYYY-MM-DD HH:MM 或时间戳）
- `from_tz`: 源时区（如 Asia/Shanghai、America/New_York、UTC）
- `to_tz`: 目标时区

### 2. 时区查询 (query)

调用 `main.py` 的 `timezone_query` 函数：
- `timezone`: 要查询的时区名称

## 常用时区名称

- 北京：Asia/Shanghai
- 东京：Asia/Tokyo
- 纽约：America/New_York
- 伦敦：Europe/London
- 悉尼：Australia/Sydney
- 洛杉矶：America/Los_Angeles
- UTC：UTC

## 输出格式

所有操作返回JSON格式结果，包含转换后的时间和时区信息。
