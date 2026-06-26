# Automation Preferences

用户可以设置自动化偏好，避免每次都询问确认。

## 配置位置

```
~/.openclaw/workspace/.iterative-code-review/preferences.json
```

## 配置项

```json
{
  "autoFix": true,
  "autoContinue": true,
  "maxRounds": 5,
  "severityThreshold": "P2"
}
```

| 配置项 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| `autoFix` | boolean | `false` | 发现问题后自动修复（不询问） |
| `autoContinue` | boolean | `false` | 修复后自动继续下一轮 review |
| `maxRounds` | number | `10` | 最多自动进行几轮 |
| `severityThreshold` | string | `"P0"` | 修复的问题严重级别阈值 (P0/P1/P2/P3) |

## 行为矩阵

| autoFix | autoContinue | 发现问题后 | 修复后 |
|---------|--------------|-----------|--------|
| `false` | `false` | 询问是否修复 | 询问是否继续 review |
| `true` | `false` | 自动修复 | 询问是否继续 review |
| `false` | `true` | 询问是否修复 | 自动继续 review |
| `true` | `true` | 自动修复 | 自动继续 review |

## severityThreshold 示例

- `"P0"` - 只自动修复 P0 问题
- `"P1"` - 自动修复 P0 和 P1 问题
- `"P2"` - 自动修复 P0、P1、P2 问题
- `"P3"` - 自动修复所有问题

## ⚠️ 安全警告

启用 `autoFix=true` 或 `autoContinue=true` 后：

- 技能会**自动修改代码**而无需确认
- 可能引入不符合预期的变更
- 建议在非关键项目或测试环境中先验证
- 重要项目建议保持默认配置（交互式确认）

## 读取配置脚本

```bash
#!/bin/bash
PREF_FILE="$HOME/.openclaw/workspace/.iterative-code-review/preferences.json"

if [[ -f "$PREF_FILE" ]]; then
  CONFIG=$(cat "$PREF_FILE")
else
  CONFIG="{}"
fi

AUTO_FIX=$(echo "$CONFIG" | jq -r '.autoFix // false')
AUTO_CONTINUE=$(echo "$CONFIG" | jq -r '.autoContinue // false')
MAX_ROUNDS=$(echo "$CONFIG" | jq -r '.maxRounds // 10')
SEVERITY_THRESHOLD=$(echo "$CONFIG" | jq -r '.severityThreshold // "P0"')

echo "autoFix=$AUTO_FIX"
echo "autoContinue=$AUTO_CONTINUE"
echo "maxRounds=$MAX_ROUNDS"
echo "severityThreshold=$SEVERITY_THRESHOLD"
```