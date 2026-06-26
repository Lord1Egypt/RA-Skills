---
name: gateway-restart-confirmed
description: "Gateway 重启确认钩子 - 允许用户在确认后重启 Gateway"
homepage: https://docs.openclaw.ai/automation/hooks
metadata:
  { 
    "openclaw": { 
      "emoji": "✅", 
      "events": ["command:gateway:restart"],
      "priority": 90
    } 
  }
---

# Gateway 重启确认钩子

## 功能

处理 `--confirmed` 参数，允许用户在确认配置已备份后重启 Gateway。

## 触发事件

- `command:gateway:restart` - Gateway 重启命令

## 工作机制

1. **检测确认参数** - 检查是否有 `--confirmed` 参数
2. **无确认参数** - 提示用户先启用保护钩子
3. **有确认参数** - 允许重启继续进行

## 使用示例

1. 正常重启（会被保护钩子拦截）：
   ```bash
   openclaw gateway restart
   ```

2. 确认后重启（允许执行）：
   ```bash
   openclaw gateway restart --confirmed
   ```

## 注意事项

- 此钩子与 `gateway-restart-protection` 配合使用
- 只有在确认配置已备份后才使用 `--confirmed` 参数
- 保护钩子会生成详细报告，确认安全后再重启
