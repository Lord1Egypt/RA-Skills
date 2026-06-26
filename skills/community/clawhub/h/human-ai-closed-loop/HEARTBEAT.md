# HEARTBEAT.md — human-ai-closed-loop

## 心跳检查清单

- [ ] 当前是否有进行中的闭环 session？
- [ ] 最近一次 `inject()` 是否在 72h 内（闭环不能长时间停滞）？
- [ ] 当前轮次置信度是否 ≥ 85%？
- [ ] `loop_log/` 目录是否存在且可写？
- [ ] 是否有等待人类反馈超过 48h 的悬挂任务？

## 异常触发条件

| 条件 | 动作 |
|------|------|
| 闭环 session 超过 72h 无人类输入 | 发送提醒："您有一个待反馈的认知闭环" |
| 置信度连续 3 轮下降 | 触发「认知漂移告警」，建议重置清单 |
| `loop_log/` 写入失败 | 暂停闭环，报错 |
| 检测到假设集合为空 | 警告：清单缺少可证伪假设，认知闭环失效 |

## 心跳状态

```json
{
  "skill": "human-ai-closed-loop",
  "version": "1.0.0",
  "last_heartbeat": null,
  "active_sessions": [],
  "pending_human_feedback": 0,
  "last_inject_at": null
}
```
