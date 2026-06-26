---
name: openclaw-aligenie-push
version: "1.0.0"
description: 主动向天猫精灵推送消息的技能。触发时机：(1) 用户要求"推送到天猫精灵"、"播报到天猫精灵"时 (2) 需要通过天猫精灵语音播报通知用户时 (3) 将任务完成状态或提醒推送到天猫精灵设备时。触发时机：(1) 用户要求"推送到天猫精灵"、"播报到天猫精灵"时 (2) 需要通过天猫精灵语音播报通知用户时 (3) 将任务完成状态或提醒推送到天猫精灵设备时。
---

# openclaw-aligenie-push

> 通过天猫精灵主动播报消息的 OpenClaw Skill

## 快速使用

### 命令模式

```
@小爪子 播报到天猫精灵 明天早上8点有会议
@小爪子 推送到天猫精灵 任务已完成
@小爪子 天猫精灵播报 游戏第三章已解锁！
```

### 函数模式

```python
from skills.openclaw-aligenie-push.push import push

# 异步调用
result = await push("任务完成，请查看结果")

# 成功返回: {"success": true, "messageId": "xxx"}
# 失败返回: {"success": false, "error": "错误描述"}
```

### 参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `text` | 必填 | 要播报的文字内容 |
| `device_type` | `speaker` | `speaker`=无屏音箱, `screen`=带屏设备 |
| `open_id` | 配置默认 | 覆盖默认设备 |
| `push_server` | 配置默认 | 覆盖默认服务器地址 |

## 配置 (TOOLS.md)

```markdown
### 天猫精灵推送配置
ALIGENIE_PUSH_SERVER=http://你的云服务器公网IP:58472/push
ALIGENIE_APP_ID=2026032918608
ALIGENIE_APP_SECRET=审批通过后获取
ALIGENIE_DEVICE_OPEN_ID=天猫精灵设备openId
```

## 前置条件

1. 阿里云技能「消息推送_定制机版」审批通过
2. 云服务器已部署 push-server.py
3. 天猫精灵 App 已添加「OpenClaw主动播报」技能

→ **完整部署文档**: `DEPLOY.md`
