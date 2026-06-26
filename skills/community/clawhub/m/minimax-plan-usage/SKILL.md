---
name: minimax-usage
description: |
  查询 MiniMax Token Plan 剩余用量。slash command。
  查询 MiniMax Token Plan 剩余次数和重置时间，支持 M2.7/Speech/视频/图片/音乐等模型的用量查询。
  Query MiniMax Token Plan usage and reset time. Supports M2.7, Speech, Video, Image, and Music models.
homepage: https://platform.minimax.io/subscribe/token-plan
user-invocable: true
disable-model-invocation: true
command-dispatch: tool
command-tool: exec
metadata:
  {
    "openclaw":
      {
        "version": "1.0.0",
        "requires":
          {
            "bins": ["python"],
            "env": ["MINIMAX_API_KEY"],
          },
      },
  }
---

# MiniMax Token Plan 用量查询

实时查询 MiniMax Token Plan 各模型的剩余额度，无需打开网页。

## 功能

- 查询 M2.7 文本模型的窗口剩余次数和重置倒计时
- 查询 Speech 2.8 语音模型的窗口剩余次数
- 查询视频、图片、音乐等模型的窗口剩余次数
- 显示各模型窗口重置剩余时间

## 使用方式

在 Discord 中输入 `/minimax_usage`

## 技术细节

脚本调用 MiniMax 官方接口：
```
GET https://www.minimaxi.com/v1/api/openplatform/coding_plan/remains
```

返回数据包含 `model_remains` 数组，每项对应一种模型。

## 环境变量

| 变量 | 必填 | 默认值 | 说明 |
|------|------|--------|------|
| `MINIMAX_API_KEY` | 是 | — | Token Plan API Key |
| `MINIMAX_API_HOST` | 否 | `https://www.minimaxi.com` | API 地址，国内版用此地址 |

## 输出示例

```
**MiniMax Token Plan 用量**

**M2.7**
  剩余次数: 431 / 600
  重置倒计时: 2h 0m 46s

**Speech 2.8**
  剩余次数: 0 / 0
  重置倒计时: 6h 0m 46s
```

## 注意事项

- 需要已设置 `MINIMAX_API_KEY` 环境变量（Token Plan 专属 Key，非普通 API Key）
- 返回的 `remaining` 是本窗口剩余次数，`total` 是窗口总限额
- `remains_time` 单位为毫秒，表示距离窗口重置的剩余时间
- 适用于 MiniMax Token Plan 订阅用户
