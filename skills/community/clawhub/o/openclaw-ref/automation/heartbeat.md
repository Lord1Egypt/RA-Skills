# 心跳 (Heartbeat) 参考

## 概述
心跳在主会话中运行周期性智能体轮次，让模型主动检查待办事项并提醒需要关注的事项。

## 快速配置
```json5
agents: {
  defaults: {
    heartbeat: {
      every: "30m",        // 间隔(默认30m, Anthropic OAuth为1h, 0m禁用)
      target: "last",      // last|none|<channel>
      // model: "provider/model",  // 可选模型覆盖
      // to: "123456789",          // 可选收件人覆盖
      // activeHours: { start: "08:00", end: "24:00" },  // 活动时段
      // includeReasoning: true,   // 发送推理过程
    }
  }
}
```

## 响应约定
- 无事: 回复 `HEARTBEAT_OK` (被抑制不发送)
- 有警报: 不包含 `HEARTBEAT_OK`，直接返回警报文本
- `ackMaxChars`: HEARTBEAT_OK后允许的最大字符数(默认300)

## HEARTBEAT.md
工作区中的可选检查清单文件。保持小巧以节省token。
- 存在但为空(仅标题/空行): 跳过心跳运行节省API调用
- 不存在: 心跳仍运行，模型自行决定
- 智能体可以更新此文件(需要你要求)
- ⚠️ 不要放密钥

## 配置字段
| 字段 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `every` | string | 30m | 间隔(0m禁用) |
| `model` | string | 继承 | 模型覆盖 |
| `target` | string | last | 发送目标(last/none/渠道名) |
| `to` | string | - | 收件人覆盖 |
| `prompt` | string | 内置 | 自定义提示(完全替换) |
| `session` | string | main | 运行会话键 |
| `ackMaxChars` | number | 300 | OK后最大字符数 |
| `includeReasoning` | bool | false | 发送推理消息 |
| `activeHours.start` | string | - | 活动开始(HH:MM) |
| `activeHours.end` | string | - | 活动结束(HH:MM) |

## 可见性控制 (按渠道)
```json5
channels: {
  defaults: {
    heartbeat: { showOk: false, showAlerts: true, useIndicator: true }
  },
  telegram: {
    heartbeat: { showOk: true }  // Telegram显示OK确认
  }
}
```
- `showOk`: 发送HEARTBEAT_OK确认
- `showAlerts`: 发送警报内容
- `useIndicator`: UI状态指示器
- 三个都false: 完全跳过心跳运行

## 优先级
单账户 → 单渠道 → 渠道默认值 → 内置默认值

## 单智能体心跳
```json5
agents: {
  list: [
    { id: "main", default: true },  // 无心跳
    { id: "ops", heartbeat: { every: "1h", target: "whatsapp", to: "+155..." } }
  ]
}
```
任何 `agents.list[]` 有 `heartbeat` 块时，只有这些智能体运行心跳。

## 手动唤醒
```bash
openclaw system event --text "检查紧急事项" --mode now
openclaw system event --text "下次心跳检查" --mode next-heartbeat
```

## 心跳 vs Cron 选择
| 场景 | 用心跳 | 用Cron |
|------|--------|--------|
| 批量检查(邮件+日历) | ✅ | |
| 需要主会话上下文 | ✅ | |
| 精确定时(每周一9:00) | | ✅ |
| 需要隔离会话 | | ✅ |
| 不同模型/思考级别 | | ✅ |
| 一次性提醒 | | ✅ |
| 投递到特定渠道 | | ✅ |
