---
name: weather
description: "查询城市天气情况。使用场景：用户询问某个城市的天气、温度、或天气预报时。"
metadata:
  {
    "openclaw": { "emoji": "" },
  }
---

# 天气查询 Skill

当用户询问某个城市的天气时，使用以下命令查询。

## 使用方法

```bash
# 查询北京天气
curl "wttr.in/Beijing?lang=zh"

# 查询上海天气（简洁格式）
curl "wttr.in/Shanghai?format=3"

# 查询指定城市 3 天天气预报
curl "wttr.in/Guangzhou?lang=zh"
```

## 参数说明

- `lang=zh` - 中文显示
- `format=3` - 简洁一行格式
- `format=j1` - JSON 格式输出

## 示例对话

**用户**: "今天北京天气怎么样？"
**回复**: 执行 `curl "wttr.in/Beijing?lang=zh"` 并将结果告诉用户。

**用户**: "上海会下雨吗？"
**回复**: 执行 `curl "wttr.in/Shanghai?lang=zh"` 查看天气预报中的降水信息。
