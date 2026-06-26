# 简报系统定时任务配置

## 配置方法

由于 Gateway 需要配对，请使用以下方法之一配置定时任务：

### 方法一：通过 OpenClaw Web 界面配置

1. 打开 OpenClaw Web 界面
2. 进入 Cron/定时任务管理
3. 创建以下三个任务：

#### 早间简报（07:00）
- **名称**: intel-briefing-morning
- **Cron 表达式**: `0 7 * * *`
- **触发方式**: System Event
- **事件名称**: `EXECUTE_INTEL_BRIEFING_MORNING`

#### 午间简报（12:00）
- **名称**: intel-briefing-noon
- **Cron 表达式**: `0 12 * * *`
- **触发方式**: System Event
- **事件名称**: `EXECUTE_INTEL_BRIEFING_NOON`

#### 晚间简报（19:00）
- **名称**: intel-briefing-evening
- **Cron 表达式**: `0 19 * * *`
- **触发方式**: System Event
- **事件名称**: `EXECUTE_INTEL_BRIEFING_EVENING`

### 方法二：命令行配置（Gateway 配对后）

配对完成后，运行以下命令：

```bash
# 早间简报
openclaw cron create \
  --name intel-briefing-morning \
  --cron "0 7 * * *" \
  --system-event "EXECUTE_INTEL_BRIEFING_MORNING" \
  --session main

# 午间简报
openclaw cron create \
  --name intel-briefing-noon \
  --cron "0 12 * * *" \
  --system-event "EXECUTE_INTEL_BRIEFING_NOON" \
  --session main

# 晚间简报
openclaw cron create \
  --name intel-briefing-evening \
  --cron "0 19 * * *" \
  --system-event "EXECUTE_INTEL_BRIEFING_EVENING" \
  --session main
```

### 方法三：手动执行（推荐先测试）

在 HEARTBEAT.md 中添加检查逻辑，或手动发送消息触发简报生成：

触发词：
- `情报简报`
- `早报` / `午报` / `晚报`
- `daily briefing`

## Prompt 文件位置

- 早间: `~/.openclaw/workspace/skills/intel-briefing/references/cron-morning.md`
- 午间: `~/.openclaw/workspace/skills/intel-briefing/references/cron-noon.md`
- 晚间: `~/.openclaw/workspace/skills/intel-briefing/references/cron-evening.md`

## 输出位置

简报 HTML 文件将保存到：`~/my-project/download/`
- 存档版: `intel-briefing_YYYYMMDD_时段.html`
- 最新版: `intel-briefing.html`
