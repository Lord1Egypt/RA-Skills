# reminders-cli 命令参考

reminders-cli 是一个原生 macOS CLI 工具，通过 EventKit 框架访问 Reminders，比 osascript 快得多。

GitHub: <https://github.com/keith/reminders-cli>

## 安装

```bash
brew install keith/formulae/reminders-cli
```

## 基础命令

### 查看所有列表

```bash
reminders show-lists
```

### 查看指定列表的提醒

```bash
reminders show "工作"
```

### 查看所有未完成提醒

```bash
reminders show-all
```

### 按截止日期筛选

```bash
# 今日到期
reminders show-all --due-date today

# 本周到期
reminders show "工作" --due-date "this week"

# 已过期
reminders show-all --due-date overdue
```

## 创建提醒

### 基础创建

```bash
reminders add "列表名" "提醒内容"
```

### 带截止日期

```bash
# 自然语言日期
reminders add "工作" "完成报告" --due-date "tomorrow 5pm"
reminders add "工作" "周会" --due-date "next monday 9am"
reminders add "个人" "约会" --due-date "2024-12-25 18:00"
```

### 带优先级

```bash
# 优先级: low, medium, high
reminders add "工作" "紧急任务" --priority high
reminders add "工作" "普通任务" --priority medium
```

### 带备注

```bash
reminders add "工作" "任务标题" --notes "详细备注内容"
```

### 组合使用

```bash
reminders add "工作" "提交报告" --due-date "friday 5pm" --priority high --notes "Q1 季度报告"
```

## 完成/取消完成

```bash
# 完成提醒（按索引，索引从 show 命令输出获取）
reminders complete "工作" 0

# 取消完成
reminders uncomplete "工作" 0
```

## 编辑提醒

```bash
reminders edit "工作" 0 "新的提醒内容"
```

## 删除提醒

```bash
reminders delete "工作" 0
```

## 输出格式

默认输出格式：

```text
列表名: 索引: 提醒内容 (截止时间) (priority: 优先级)
```

示例：

```text
工作: 0: 完成报告 (in 2 days) (priority: high)
工作: 1: 周会准备 (tomorrow)
个人: 2: 买牛奶 (today)
```

## 与 osascript 对比

| 功能 | reminders-cli | osascript |
|------|---------------|-----------|
| 查询速度 | **极快** (~2秒) | 非常慢（可能卡死） |
| 创建提醒 | 支持 | 支持 |
| 完成提醒 | 支持 | 支持 |
| 删除提醒 | 支持 | 支持 |
| 批量操作 | 不支持 | 支持 |
| 复杂查询 | 有限 | 灵活 |
| 安装依赖 | 需要 brew | 系统内置 |

**建议**：

- **日常操作** → 使用 reminders-cli
- **批量操作/复杂查询** → 使用 osascript（但要有耐心）

## 常见问题

### 权限问题

首次运行会请求 Reminders 访问权限。如果拒绝了，需要在系统设置中手动授权：

系统设置 → 隐私与安全性 → 提醒事项 → 允许终端

### 列表名包含特殊字符

使用引号包裹：

```bash
reminders show "工作（Work）"
```

### 查看帮助

```bash
reminders --help
reminders add --help
reminders show --help
```

## 常用工作流

### 每日规划

```bash
echo "=== 今日待办 ===" && reminders show-all --due-date today
```

### 快速收集

```bash
reminders add "收件箱" "新想法"
```

### 清理已完成

通过 Reminders.app 或 osascript 批量删除已完成的提醒。

## 更多信息

- GitHub: <https://github.com/keith/reminders-cli>
- 版本: 2.5.1+
