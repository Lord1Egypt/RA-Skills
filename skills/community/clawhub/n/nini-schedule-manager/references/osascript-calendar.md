# Apple Calendar osascript 参考

## 对象模型

```text
Calendar Application
└── calendars (list)
    └── calendar
        ├── name (text)
        ├── description (text)
        └── events (list)
            └── event
                ├── summary (text)
                ├── start date (date)
                ├── end date (date)
                ├── description (text)
                ├── location (text)
                ├── allday event (boolean)
                ├── recurrence (text)
                ├── url (text)
                └── alarms (list)
                    └── display alarm / sound alarm
                        └── trigger interval (integer, minutes)
```

## 日历操作

### 列出所有日历

```bash
osascript -e 'tell application "Calendar" to get name of calendars'
```

### 创建日历

```bash
osascript -e '
tell application "Calendar"
    make new calendar with properties {name:"新日历", description:"描述"}
end tell'
```

### 删除日历

```bash
osascript -e '
tell application "Calendar"
    delete calendar "要删除的日历"
end tell'
```

## 事件操作

### 创建事件

**基础创建：**

```bash
osascript -e '
tell application "Calendar"
    tell calendar "个人"
        set startDate to (current date) + (1 * days)
        set hours of startDate to 14
        set minutes of startDate to 0
        set seconds of startDate to 0
        set endDate to startDate + (1 * hours)
        make new event with properties {summary:"会议标题", start date:startDate, end date:endDate}
    end tell
end tell'
```

**带完整属性：**

```bash
osascript -e '
tell application "Calendar"
    tell calendar "工作"
        set startDate to (current date) + (2 * days)
        set hours of startDate to 10
        set minutes of startDate to 0
        set endDate to startDate + (2 * hours)
        make new event with properties {
            summary:"项目讨论会",
            start date:startDate,
            end date:endDate,
            description:"讨论 Q1 计划",
            location:"会议室 A"
        }
    end tell
end tell'
```

**全天事件：**

```bash
osascript -e '
tell application "Calendar"
    tell calendar "个人"
        set eventDate to (current date) + (3 * days)
        make new event with properties {
            summary:"休假",
            start date:eventDate,
            allday event:true
        }
    end tell
end tell'
```

### 事件属性

| 属性 | 类型 | 说明 |
|------|------|------|
| `summary` | text | 事件标题 |
| `start date` | date | 开始时间 |
| `end date` | date | 结束时间 |
| `description` | text | 详细描述 |
| `location` | text | 地点 |
| `allday event` | boolean | 是否全天事件 |
| `recurrence` | text | 重复规则（RRULE 格式） |
| `url` | text | 相关链接 |

### 查询事件

**查询今日事件：**

```bash
osascript -e '
tell application "Calendar"
    set today to current date
    set todayStart to today - (time of today)
    set todayEnd to todayStart + (1 * days)
    set allEvents to {}
    repeat with cal in calendars
        try
            set calEvents to (every event of cal whose start date ≥ todayStart and start date < todayEnd)
            repeat with evt in calEvents
                set end of allEvents to {summary of evt, start date of evt}
            end repeat
        end try
    end repeat
    return allEvents
end tell'
```

**查询指定日期范围：**

```bash
osascript -e '
tell application "Calendar"
    set startRange to (current date)
    set endRange to startRange + (7 * days)
    tell calendar "工作"
        get every event whose start date ≥ startRange and start date < endRange
    end tell
end tell'
```

**按标题搜索：**

```bash
osascript -e '
tell application "Calendar"
    tell calendar "工作"
        get every event whose summary contains "会议"
    end tell
end tell'
```

### 修改事件

```bash
osascript -e '
tell application "Calendar"
    tell calendar "个人"
        set targetEvent to first event whose summary is "原标题"
        set summary of targetEvent to "新标题"
        set location of targetEvent to "新地点"
    end tell
end tell'
```

### 删除事件

**按标题删除：**

```bash
osascript -e '
tell application "Calendar"
    tell calendar "个人"
        delete (every event whose summary is "要删除的事件")
    end tell
end tell'
```

**删除指定日期范围内的事件：**

```bash
osascript -e '
tell application "Calendar"
    set targetDate to (current date) + (1 * days)
    set targetStart to targetDate - (time of targetDate)
    set targetEnd to targetStart + (1 * days)
    tell calendar "个人"
        delete (every event whose start date ≥ targetStart and start date < targetEnd)
    end tell
end tell'
```

## 闹钟设置

### 添加提醒闹钟

```bash
osascript -e '
tell application "Calendar"
    tell calendar "工作"
        set targetEvent to first event whose summary is "重要会议"
        tell targetEvent
            make new display alarm at end with properties {trigger interval:-30}
        end tell
    end tell
end tell'
```

`trigger interval` 为分钟数，负数表示事件开始前。

### 闹钟类型

- `display alarm`: 显示通知
- `sound alarm`: 播放声音

## 日期运算

```applescript
-- 基本运算
(current date) + (1 * days)
(current date) + (2 * hours)
(current date) + (30 * minutes)

-- 设置具体时间
set myDate to current date
set hours of myDate to 14
set minutes of myDate to 30
set seconds of myDate to 0

-- 获取今天零点
set today to current date
set todayStart to today - (time of today)
```

## 重复事件

AppleScript 对重复事件的处理有限。推荐使用 icalBuddy 查询重复事件。

创建重复事件需要使用 RRULE 格式：

```bash
osascript -e '
tell application "Calendar"
    tell calendar "工作"
        make new event with properties {
            summary:"周会",
            start date:(current date),
            end date:(current date) + (1 * hours),
            recurrence:"FREQ=WEEKLY;BYDAY=MO"
        }
    end tell
end tell'
```

常用 RRULE：

- `FREQ=DAILY` - 每天
- `FREQ=WEEKLY;BYDAY=MO,WE,FR` - 每周一三五
- `FREQ=MONTHLY;BYMONTHDAY=1` - 每月 1 日
- `FREQ=YEARLY` - 每年

## 错误处理

```applescript
tell application "Calendar"
    try
        tell calendar "不存在的日历"
            get events
        end tell
    on error errMsg
        return "错误: " & errMsg
    end try
end tell
```

## 注意事项

- 首次运行需要授权日历访问权限
- 修改共享日历可能需要额外权限
- 重复事件的查询建议使用 icalBuddy
- 日期比较使用 `≥` 和 `<` 符号
