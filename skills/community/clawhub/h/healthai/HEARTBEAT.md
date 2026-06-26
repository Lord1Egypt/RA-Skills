# HEARTBEAT.md

## 🎯 健康打卡定时提醒（通过 OpenClaw 发送）

每次 heartbeat 触发时（每2小时），检查是否需要发送提醒：

### 逻辑
```python
from datetime import datetime

now = datetime.now()
hour = now.hour
minute = now.minute

# 09:00 运动提醒（只发送一次）
if hour == 9 and minute < 5:
    发送今日运动计划

# 18:00 打卡提醒
if hour == 18 and minute < 5:
    发送打卡提醒

# 21:30 睡觉提醒
if hour == 21 and minute >= 30 and minute < 35:
    发送睡觉提醒
```

### 运动计划数据源
- 配置文件：`health_plan.json` 或 `exercise_plan.json`
- 路径：`~/openclaw-autoclaw/skills/HealthSkill-1.0/config/exercise_plan.json`

### 推送内容

**09:00 运动提醒**
```
🏃 每日运动提醒（周一）

早上：
- 运动：八段锦
- 时长：30分钟
- 目的：养肝调理
- 视频：https://www.bilibili.com/video/BV1gT4y1m7ec/

下午：
- 运动：散步
- 时长：30分钟
- 目的：温和有氧

💪 坚持就是胜利！
```

**18:00 打卡提醒**
```
🏃 一天过去了，今天运动了吗？
回复"打卡"记录今日运动～
```

**21:30 睡觉提醒**
```
🌙 晚安！早点休息，明天继续加油！
```

---

## 📋 Proactive Agent 模式

### 每次 heartbeat 执行：
1. 检查时间是否在提醒时间点附近（±5分钟）
2. 如果是 → 读取运动计划 → 通过当前 IM 渠道发送消息
3. 更新 SESSION-STATE.md 记录最后发送时间（避免重复发送）

### 已发送记录
- 上次运动提醒：2026-04-05 09:00
- 上次打卡提醒：（未发送）
- 上次睡觉提醒：（未发送）
