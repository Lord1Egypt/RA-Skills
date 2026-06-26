# 心情周报定时设置

## 方案一：OpenClaw Cron（推荐）

当 OpenClaw CLI 可用时，运行：

```bash
openclaw cron create mood-weekly-report \
  --schedule "0 9 * * 0" \
  --task "每周心情周报" \
  --command "生成并发送上周的心情周报"
```

## 方案二：系统 Cron（备用）

添加到系统定时任务：

```bash
# 编辑 crontab
crontab -e

# 添加以下行（每周日 9:00 运行）
0 9 * * 0 cd /home/loong/.openclaw/workspace && python3 ~/.openclaw/workspace/skills/mood-logger/scripts/weekly_mood_report.py >> /tmp/mood_report.log 2>&1
```

## 方案三：手动生成

随时手动生成周报：

```bash
# 生成本周周报
python3 ~/.openclaw/workspace/skills/mood-logger/scripts/weekly_mood_report.py

# 生成上周周报
python3 ~/.openclaw/workspace/skills/mood-logger/scripts/weekly_mood_report.py --date $(date -d 'last sunday' +%Y-%m-%d)
```

## 周报示例输出

```
# 📊 心情周报 (03月23日 - 03月29日)

## 本周概览
| 指标 | 数值 |
|------|------|
| 平均心情 | 8.0/10 😊 |
| 最高心情 | 8/10 |
| 最低心情 | 8/10 |
| 记录次数 | 1 次 |
| 整体趋势 | 平稳 |

## 心情标签 TOP5
- `开心`: 1 次
- `满足`: 1 次

## 每日心情
- **周一**: 无记录
- **周二**: 无记录
- **周三**: 无记录
- **周四**: 无记录
- **周五**: 😊 8.0/10
- **周六**: 无记录
- **周日**: 无记录
```
