---
name: lunar-reminder
description: 按农历日期设置提醒（生日、节日等）。当用户需要：(1) 按农历添加提醒事件 (2) 查看农历事件列表 (3) 农历日期与公历日期转换 (4) 设置农历生日/节日提醒 时使用此 skill。触发词：农历、农历生日、农历节日、阴历提醒。
metadata:
  openclaw:
    requires:
      bins: []
    install:
      - id: lunar-javascript
        kind: node
        package: lunar-javascript
        label: 安装 lunar-javascript
---

# Lunar Reminder

按农历日期设置提醒，支持生日、节日等重要日期的农历提醒。

## 数据文件

事件数据保存在：`{{skillDir}}/data/events.json`

## Agent 工作流

### 1. 用户添加农历提醒

**解析输入**：从用户输入中提取事件名、农历月份、农历日期、提前天数（默认1）。

**农历月份映射**：
| 名称 | 数字 |
|------|------|
| 正月/正/一月 | 1 |
| 二月/杏月 | 2 |
| 三月/桃月 | 3 |
| 四月/槐月 | 4 |
| 五月/榴月 | 5 |
| 六月/荷月 | 6 |
| 七月/兰月 | 7 |
| 八月/桂月 | 8 |
| 九月/菊月 | 9 |
| 十月/露月 | 10 |
| 十一月/冬月/冬 | 11 |
| 十二月/腊月/腊 | 12 |

**农历日期映射**：
| 名称 | 数字 |
|------|------|
| 初一~初十 | 1~10 |
| 十一~二十 | 11~20 |
| 廿一/二十一~廿九/二十九 | 21~29 |
| 三十 | 30 |

**执行步骤**：

1. 读取现有事件（文件不存在则创建空数组）
2. 检查事件名是否已存在，存在则报错
3. 计算当年公历日期（运行下方命令）
4. 保存事件到文件
5. 确认添加成功

**农历转公历命令**（在 `{{skillDir}}` 目录执行）：

```bash
node -e "const {Lunar}=require('lunar-javascript');const l=Lunar.fromYmd(YEAR,MONTH,DAY);const s=l.getSolar();console.log(s.getYear()+'-'+String(s.getMonth()).padStart(2,'0')+'-'+String(s.getDay()).padStart(2,'0'));"
```

将 `YEAR`、`MONTH`、`DAY` 替换为实际值（如 2026, 2, 11）。

### 2. 用户查看提醒列表

读取 `{{skillDir}}/data/events.json` 文件，格式化输出每个事件的：
- 事件名
- 农历日期（月名+日名）
- 今年公历日期
- 提前提醒天数

### 3. 用户删除提醒

1. 读取事件文件
2. 过滤掉指定名称的事件
3. 保存文件
4. 删除对应 cron 任务：`openclaw cron rm "lunar_<事件名>"`

### 4. 用户要求日期转换

**农历转公历**：

```bash
cd {{skillDir}} && node -e "const {Lunar}=require('lunar-javascript');const l=Lunar.fromYmd(YEAR,MONTH,DAY);const s=l.getSolar();console.log(s.getYear()+'-'+String(s.getMonth()).padStart(2,'0')+'-'+String(s.getDay()).padStart(2,'0'));"
```

**公历转农历**：

```bash
cd {{skillDir}} && node -e "const {Solar}=require('lunar-javascript');const s=Solar.fromYmd(YEAR,MONTH,DAY);const l=s.getLunar();const m=['','正月','二月','三月','四月','五月','六月','七月','八月','九月','十月','冬月','腊月'];const d=['','初一','初二','初三','初四','初五','初六','初七','初八','初九','初十','十一','十二','十三','十四','十五','十六','十七','十八','十九','二十','廿一','廿二','廿三','廿四','廿五','廿六','廿七','廿八','廿九','三十'];console.log(m[l.getMonth()]+d[l.getDay()]);"
```

### 5. 用户要求同步提醒

1. 读取所有事件
2. 对每个事件：
   - 计算公历日期
   - 减去提前天数得到提醒日期
   - 执行 cron 命令

**Cron 命令格式**：

```bash
# 先删除旧任务
openclaw cron rm "lunar_<事件名>"

# 创建新任务
openclaw cron add --name "lunar_<事件名>" --cron "<分> <时> <日> <月> *" --message "🔔 农历提醒：<事件名>将在<N>天后到来" --tz "Asia/Shanghai"
```

## 数据格式

```json
[
  {
    "name": "妈妈生日",
    "lunarMonth": 2,
    "lunarDay": 11,
    "lunarMonthName": "二月",
    "lunarDayName": "十一",
    "advanceDays": 1,
    "reminderTime": "09:00",
    "note": "",
    "createdAt": "2026-03-10T00:00:00.000Z"
  }
]
```

## 使用示例

```
添加农历提醒：妈妈生日，二月十一，提前1天提醒
查看所有农历提醒
删除农历提醒：妈妈生日
农历二月十一是公历几号
同步农历提醒到定时任务
```