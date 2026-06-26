# Meeting Assistant 集成指南

## 与 pc-control 联动

Meeting Assistant 复用 pc-control 的截屏和桌面控制能力。

### 截屏

```python
import sys
sys.path.insert(0, 'skills/pc-control/scripts')
from client import PCControl

pc = PCControl()
img_path = pc.screenshot(scale=0.5, quality=50)
# img_path 可直接传给 Claude 进行视觉分析
```

### 会议窗口控制

```python
# 静音/取消静音 (Zoom: Alt+A, Teams: Ctrl+Shift+M)
pc.hotkey("alt", "a")  # Zoom
pc.hotkey("ctrl", "shift", "m")  # Teams

# 开关摄像头 (Zoom: Alt+V, Teams: Ctrl+Shift+O)
pc.hotkey("alt", "v")  # Zoom
pc.hotkey("ctrl", "shift", "o")  # Teams

# 屏幕共享 (Zoom: Alt+S, Teams: Ctrl+Shift+E)
pc.hotkey("alt", "s")  # Zoom
pc.hotkey("ctrl", "shift", "e")  # Teams

# 聊天 (Zoom: Alt+H, Teams: Ctrl+Shift+C)
pc.hotkey("alt", "h")  # Zoom
```

## 与 agent-browser-core 联动

在会议中需要查询资料时：

```bash
# 快速查询医学术语
agent-browser navigate "https://www.google.com/search?q=医学术语+解释"
agent-browser snapshot
```

## 与 TTS 联动

将分析结果语音播报：

```bash
curl -X POST http://localhost:9001/v1/audio/speech \
  -H "Content-Type: application/json" \
  -d '{"input": "医生建议每天服用两次药物", "voice": "alloy"}'
```

## Agent 工作流程示例

```
Agent 收到指令: "帮我参加这个 Zoom 会议并做记录"

1. 检查 pc-control server 是否运行
   → python3 skills/pc-control/scripts/launcher.py start

2. 启动会议监控
   → python3 skills/meeting-assistant/scripts/meeting_monitor.py start --mode medical

3. 进入监控循环:
   while 会议进行中:
     a. 截屏 → 分析画面
     b. 获取最近5分钟转录 → 理解对话
     c. 综合分析 → 生成建议
     d. 如需要 → 调用 browser 查资料
     e. 如需要 → 通过 TTS 语音提示用户
     f. 等待 interval

4. 会议结束:
   → python3 skills/meeting-assistant/scripts/meeting_monitor.py stop
   → 生成会议摘要
   → 如果是医疗模式，生成患者版摘要
```

## Zoom API 集成（可选扩展）

如果有 Zoom OAuth credentials，可以通过 Zoom API 获取更多数据：

- 会议参与者列表
- 会议时长
- 云端录制（如果启用）
- 实时字幕（CC）

## Teams Graph API 集成（可选扩展）

通过 Microsoft Graph API：

- 获取会议详情
- 访问会议转录（如果启用）
- 获取会议聊天记录
- 日历集成
