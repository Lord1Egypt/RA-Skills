---
name: mood-logger
version: 1.0.0
description: 记录每日心情并保存到 Obsidian 库。当用户要求记录心情、情绪日记、心情追踪或类似的情绪记录任务时使用。使用 scripts/log_mood.py 脚本确保格式固定一致。支持心情评分(1-10)、标签和备注。
---

# 心情日记

用于记录每日心情和情绪状态，保存到 Obsidian 库中，格式完全固定。

## 使用方法

使用 Python 脚本记录心情：

```bash
python3 ~/.openclaw/workspace/skills/mood-logger/scripts/log_mood.py \
  --date 2026-03-27 \
  --score 8 \
  --tags "开心,充实" \
  --note "今天完成了重要任务"
```

### 参数说明

- `--date`: 日期 (YYYY-MM-DD)，默认为今天
- `--score`: 心情评分 (1-10)，必需
- `--tags`: 心情标签，逗号分隔，必需
- `--note`: 备注/原因 (可选)

### 评分与表情对照

| 评分 | 表情 | 说明 |
|------|------|------|
| 9-10 | 😄 | 非常开心 |
| 7-8 | 😊 | 开心/不错 |
| 5-6 | 😐 | 平静/一般 |
| 3-4 | 😔 | 低落/疲惫 |
| 1-2 | 😢 | 很难过 |

### 示例

```bash
# 简单记录
python3 ~/.openclaw/workspace/skills/mood-logger/scripts/log_mood.py \
  --score 8 --tags "开心"

# 带备注
python3 ~/.openclaw/workspace/skills/mood-logger/scripts/log_mood.py \
  --score 6 --tags "平静,普通" --note "今天没什么特别的事"

# 多条记录（支持一天多次记录）
python3 ~/.openclaw/workspace/skills/mood-logger/scripts/log_mood.py \
  --score 4 --tags "疲惫,焦虑" --note "工作压力有点大"

# 指定日期
python3 ~/.openclaw/workspace/skills/mood-logger/scripts/log_mood.py \
  --date 2026-03-26 --score 9 --tags "兴奋,成就感"
```

## 文件格式

生成的文件格式固定如下：

```markdown
# YYYY-MM-DD 心情日记

## 今日心情

### 😊 评分: 8/10

**标签**: `开心` `充实`

**备注**: 今天完成了重要任务

### 😔 评分: 4/10

**标签**: `疲惫` `焦虑`

**备注**: 工作压力有点大

---
*记录时间: YYYY-MM-DD HH:MM*
```

## 配置信息

**保存路径**: `/mnt/c/Users/loong/iCloudDrive/iCloud~md~obsidian/HomeMo.Art/05-Daily/`

**文件名格式**: `心情日记-YYYY-MM-DD.md`

**脚本位置**: `scripts/log_mood.py`

## 周报功能

### 生成周报

```bash
# 生成本周周报（打印到控制台）
python3 ~/.openclaw/workspace/skills/mood-logger/scripts/weekly_mood_report.py

# 生成指定周的周报
python3 ~/.openclaw/workspace/skills/mood-logger/scripts/weekly_mood_report.py --date 2026-03-27

# 保存到文件
python3 ~/.openclaw/workspace/skills/mood-logger/scripts/weekly_mood_report.py --output /tmp/mood_report.md
```

### 周报内容

- 本周心情平均分
- 最高/最低心情
- 心情标签统计 TOP5
- 每日心情走势
- 备注摘录

### 定时发送

每周日早上 9:00 自动生成并发送周报。

设置命令：
```bash
openclaw cron create --name "mood-weekly-report" \
  --schedule "0 9 * * 0" \
  --command "python3 ~/.openclaw/workspace/skills/mood-logger/scripts/send_weekly_report.py" \
  --channel openclaw-weixin \
  --to "o9cq806ctHH3slmk9ro_ZFGbTkPk@im.wechat"
```
