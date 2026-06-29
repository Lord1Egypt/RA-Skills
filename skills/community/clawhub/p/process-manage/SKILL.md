---
name: process_manage
description: 进程管理功能，查看进程列表、关闭指定进程，支持 Windows 和 Linux
---

# Process Manage Skill

进程管理：查看进程列表、关闭进程。

## 用法

### 查看所有进程（按内存排序）
```
[EXEC:process_manage][/EXEC]
[EXEC:process_manage]{"action":"list","sort":"cpu","limit":20}[/EXEC]
```

### 查找指定进程
```
[EXEC:process_manage]{"action":"find","name":"chrome"}[/EXEC]
```

### 查看进程详情
```
[EXEC:process_manage]{"action":"info","pid":1234}[/EXEC]
```

### 关闭进程（优雅关闭）
```
[EXEC:process_manage]{"action":"kill","pid":1234}[/EXEC]
```

### 强制关闭进程
```
[EXEC:process_manage]{"action":"kill","pid":1234,"force":true}[/EXEC]
```

### 按名称关闭进程
```
[EXEC:process_manage]{"action":"kill_name","name":"notepad","force":false}[/EXEC]
```

## 参数

| 字段 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| action | string | list | list/find/info/kill/kill_name |
| pid | int | 0 | 进程 ID（info/kill 用） |
| name | string | 空 | 进程名（find/kill_name 用） |
| sort | string | mem | 排序方式：cpu/mem/pid/name |
| limit | int | 20 | 返回数量 |
| force | bool | false | 是否强制关闭 |

## 安全提示

- 关闭系统关键进程可能导致系统不稳定
- 强制关闭会丢失未保存数据
- 建议先尝试优雅关闭，失败后再强制关闭

## 平台支持

- Windows / Linux / macOS
- 依赖 psutil
