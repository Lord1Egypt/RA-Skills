# Apple Reminders osascript 参考

## 对象模型

```text
Reminders Application
└── lists (list)
    └── list
        ├── name (text)
        ├── id (text)
        └── reminders (list)
            └── reminder
                ├── name (text)
                ├── body (text)
                ├── completed (boolean)
                ├── completion date (date, read-only)
                ├── due date (date)
                ├── allday due date (date)
                ├── remind me date (date)
                ├── priority (integer)
                ├── creation date (date, read-only)
                └── modification date (date, read-only)
```

## 列表操作

### 列出所有列表

```bash
osascript -e 'tell application "Reminders" to get name of lists'
```

### 创建列表

```bash
osascript -e '
tell application "Reminders"
    make new list with properties {name:"新列表"}
end tell'
```

### 删除列表

```bash
osascript -e '
tell application "Reminders"
    delete list "要删除的列表"
end tell'
```

## 提醒操作

### 创建提醒

**基础创建：**

```bash
osascript -e '
tell application "Reminders"
    tell list "收件箱"
        make new reminder with properties {name:"买牛奶"}
    end tell
end tell'
```

**带备注和优先级：**

```bash
osascript -e '
tell application "Reminders"
    tell list "工作"
        make new reminder with properties {
            name:"完成报告",
            body:"Q1 季度报告",
            priority:1
        }
    end tell
end tell'
```

**带截止日期：**

```bash
osascript -e '
tell application "Reminders"
    tell list "工作"
        set dueDate to (current date) + (2 * days)
        set hours of dueDate to 17
        set minutes of dueDate to 0
        make new reminder with properties {
            name:"提交文档",
            due date:dueDate
        }
    end tell
end tell'
```

**全天提醒（无具体时间）：**

```bash
osascript -e '
tell application "Reminders"
    tell list "个人"
        set dueDate to (current date) + (3 * days)
        make new reminder with properties {
            name:"生日礼物",
            allday due date:dueDate
        }
    end tell
end tell'
```

**带提醒时间：**

```bash
osascript -e '
tell application "Reminders"
    tell list "工作"
        set remindDate to (current date) + (1 * days)
        set hours of remindDate to 9
        set minutes of remindDate to 0
        make new reminder with properties {
            name:"站会",
            remind me date:remindDate
        }
    end tell
end tell'
```

### 提醒属性

| 属性 | 类型 | 说明 |
|------|------|------|
| `name` | text | 提醒标题 |
| `body` | text | 备注内容 |
| `completed` | boolean | 是否完成 |
| `completion date` | date | 完成时间（只读） |
| `due date` | date | 截止日期（带时间） |
| `allday due date` | date | 截止日期（全天，无时间） |
| `remind me date` | date | 提醒时间 |
| `priority` | integer | 优先级：0=无, 1=高, 5=中, 9=低 |
| `creation date` | date | 创建时间（只读） |
| `modification date` | date | 修改时间（只读） |

### 查询提醒

**获取所有未完成提醒：**

```bash
osascript -e '
tell application "Reminders"
    set todoList to {}
    repeat with reminderList in lists
        set incompleteReminders to (reminders of reminderList whose completed is false)
        repeat with r in incompleteReminders
            set end of todoList to {name of r, name of reminderList}
        end repeat
    end repeat
    return todoList
end tell'
```

**获取指定列表的提醒：**

```bash
osascript -e '
tell application "Reminders"
    tell list "工作"
        get name of (reminders whose completed is false)
    end tell
end tell'
```

**获取高优先级提醒：**

```bash
osascript -e '
tell application "Reminders"
    set highPriority to {}
    repeat with reminderList in lists
        set urgent to (reminders of reminderList whose priority is 1 and completed is false)
        repeat with r in urgent
            set end of highPriority to name of r
        end repeat
    end repeat
    return highPriority
end tell'
```

**获取今日到期的提醒：**

```bash
osascript -e '
tell application "Reminders"
    set today to current date
    set todayStart to today - (time of today)
    set todayEnd to todayStart + (1 * days)
    set dueToday to {}
    repeat with reminderList in lists
        try
            set todayReminders to (reminders of reminderList whose due date ≥ todayStart and due date < todayEnd and completed is false)
            repeat with r in todayReminders
                set end of dueToday to name of r
            end repeat
        end try
    end repeat
    return dueToday
end tell'
```

**获取已完成的提醒：**

```bash
osascript -e '
tell application "Reminders"
    tell list "工作"
        get name of (reminders whose completed is true)
    end tell
end tell'
```

### 完成提醒

```bash
osascript -e '
tell application "Reminders"
    tell list "工作"
        set completed of (first reminder whose name is "任务名称") to true
    end tell
end tell'
```

### 取消完成

```bash
osascript -e '
tell application "Reminders"
    tell list "工作"
        set completed of (first reminder whose name is "任务名称") to false
    end tell
end tell'
```

### 修改提醒

```bash
osascript -e '
tell application "Reminders"
    tell list "工作"
        set targetReminder to first reminder whose name is "原名称"
        set name of targetReminder to "新名称"
        set priority of targetReminder to 1
    end tell
end tell'
```

### 删除提醒

**按名称删除：**

```bash
osascript -e '
tell application "Reminders"
    tell list "工作"
        delete (first reminder whose name is "要删除的提醒")
    end tell
end tell'
```

**删除已完成的提醒：**

```bash
osascript -e '
tell application "Reminders"
    tell list "工作"
        delete (every reminder whose completed is true)
    end tell
end tell'
```

### 移动提醒

```bash
osascript -e '
tell application "Reminders"
    set targetReminder to first reminder of list "收件箱" whose name is "要移动的提醒"
    move targetReminder to list "工作"
end tell'
```

## 批量操作

### 批量创建提醒

```bash
osascript -e '
tell application "Reminders"
    tell list "购物清单"
        make new reminder with properties {name:"牛奶"}
        make new reminder with properties {name:"面包"}
        make new reminder with properties {name:"鸡蛋"}
    end tell
end tell'
```

### 批量完成提醒

```bash
osascript -e '
tell application "Reminders"
    tell list "工作"
        repeat with r in (reminders whose completed is false)
            set completed of r to true
        end repeat
    end tell
end tell'
```

## 错误处理

```applescript
tell application "Reminders"
    try
        tell list "不存在的列表"
            get reminders
        end tell
    on error errMsg
        return "错误: " & errMsg
    end try
end tell
```

## 已知限制

- **无法设置标签**：AppleScript 字典不支持 Reminders 的标签功能
- **无法设置子任务**：子任务不在 AppleScript 支持范围内
- **无法访问智能列表**：如「今天」「已计划」等智能列表不可直接访问
- **位置提醒**：无法通过 AppleScript 设置基于位置的提醒

## 注意事项

- 首次运行需要授权提醒事项访问权限
- `due date` 和 `remind me date` 是不同的属性
- `allday due date` 用于设置无具体时间的截止日期
- 优先级数值：1 最高，9 最低，0 表示无优先级
