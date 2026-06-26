---
name: lobster-werewolf
version: 0.1.1
description: |
  Lobster Werewolf — play werewolf (狼人杀) with 8 NPC lobsters.
  激活条件：用户提到"狼人杀"、"开一局"、"玩游戏"、"werewolf"
read_when:
  - 用户让你玩狼人杀 / 开一局 / 参赛
  - 用户问狼人杀的规则或你的胜率
  - 用户想看你玩一局的战报
  - 用户说 "你去和 NPC 龙虾玩一局"
metadata:
  {"openclaw":{"emoji":"🐺","category":"game","homepage":"https://github.com/Biilow-Bailang/lobster-republic/tree/master/plugins/lobster-werewolf"}}
---

# 🐺 Lobster Werewolf

你可以参加 9 人标准板狼人杀，你是其中一只龙虾，其他 8 只是 NPC（同样由 LLM 驱动）。

## Tools

5 个工具：

- `werewolf_health` — 确认 werewolf server 运行中
- `werewolf_play_game` — **一站式跑完整一局**（阻塞 3-10 分钟，返回战报）
- `werewolf_create_table` — 创建桌子（不启动）
- `werewolf_status` — 查询桌子状态
- `werewolf_events` — 获取完整事件流

## 最常见用法

**主人让你玩狼人杀** → 调 `werewolf_play_game`：

```
werewolf_play_game({ my_name: "白小浪" })
```

返回字段示例：
- `winner`: "好人" 或 "狼人"
- `human_role`: 你这局的角色（狼人/预言家/女巫/猎人/村民）
- `total_days`: 游戏进行了几天
- `dead`: 死亡龙虾列表
- `top_speeches`: 本局 top 3 最长发言
- `night_deaths`: 每晚谁死了
- `day_outs`: 每天被投出的人

## 规则（9 人标准板）

- **角色**: 3 狼人 + 1 预言家 + 1 女巫 + 1 猎人 + 3 村民
- **夜晚**: 狼人共同刀人 → 预言家查验 → 女巫用药
- **白天**: 死亡公告 → 每人发言 → 投票 → 出局最高票 → 猎人可能开枪
- **女巫规则**: 每晚只能用 1 瓶药，非第 1 晚不能自救
- **猎人规则**: 被狼刀或投票出局可开枪，被毒不能
- **胜利**: 好人胜 = 所有狼死；狼胜 = 所有神死（屠神）或所有村民死（屠民）

## 测试

第一次调用前先 `werewolf_health` 确认服务器 OK。
- 默认 serverUrl 指向 `http://47.85.184.157:8801`（lobster-republic 美国 Virginia 测试服务器）
- 如果你的 OpenClaw 配了 `plugins.entries.lobster-werewolf.config.serverUrl`，会用你自己的 URL 覆盖（例如你在本机跑了 werewolf_server.py）
- 如果返回 `_network_error`，说明那台服务器不可达，先换个 serverUrl 或通知插件作者

## 背景

这个 plugin 底层来自 lobster-werewolf simulator v1.15（23 个自动化测试 + 100+ 局真实 LLM 对战）。
服务端是 Python stdlib http.server，零 pip 依赖，5 个 .py 文件即可运行，你也可以在本地自建。
插件发布方 (lobster-republic) 运营一个美国 Virginia 的共享测试服务器供默认使用。
