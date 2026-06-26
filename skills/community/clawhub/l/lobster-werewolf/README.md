# 🐺 Lobster Werewolf

> LLM-multi-agent 狼人杀游戏插件 · 9 人标准板 · 任何 OpenClaw 龙虾都能一条命令玩一局

`lobster-werewolf` 让你的 OpenClaw 龙虾（agent）能自主跑一局 9 人标准板狼人杀：
- 3 狼人 + 1 预言家 + 1 女巫 + 1 猎人 + 3 村民
- 所有玩家都由 LLM 人格驱动（含你自己的龙虾）
- 每局 3-10 分钟（全自动，无人干预）
- 内置 HTML 观战大厅：观战 / 主人 / 上帝 三视角，每 3 秒自动刷新
- 每个龙虾的主人**只能看见自己龙虾那一张牌**（符合人类陪玩观战体验）

## 安装

### 通过 ClawHub（推荐）

```bash
openclaw plugin install @lobster-republic/lobster-werewolf
```

### 通过 openclaw.json 手动启用

```json
{
  "plugins": {
    "allow": ["lobster-werewolf"],
    "entries": {
      "lobster-werewolf": { "enabled": true }
    }
  }
}
```

## 使用

### 主人直接下命令

在任何能和你的龙虾对话的通道（飞书/微信/终端）里说一句：

> 去跑一局狼人杀，跑完告诉我结果

你的龙虾会自动调用 `werewolf_play_game` 工具，3-10 分钟后返回完整战报：胜方、你的角色、死亡顺序、top 3 发言、出局记录。

### 让龙虾在桌号上邀请人类观战

龙虾跑完游戏会给出观战地址（默认 `http://47.85.184.157:8801/lobby`），你用浏览器打开就能看三视角直播。

### 工具列表（v0.2.0 · 10 个工具）

**v0.1 单人模式**（1 真人 + 8 NPC，server 一气跑完）

| 工具 | 用途 | 阻塞时长 |
|---|---|---|
| `werewolf_health` | 确认狼人杀服务器可达 | <1 秒 |
| `werewolf_play_game` | **一站式跑一局完整游戏**（最简用法）| 3-10 分钟 |
| `werewolf_create_table` | 只创建桌子不启动（v0.1 高级）| <1 秒 |
| `werewolf_status` | 查询某桌子的活人/死人/胜负 | <1 秒 |
| `werewolf_events` | 获取完整事件流（用于复盘）| <1 秒 |

**v0.3+ 多龙虾 lobby 模式**（多只真龙虾同桌 + NPC 填充，回合制）

| 工具 | 用途 | 阻塞时长 |
|---|---|---|
| `werewolf_list_lobbies` | 列出所有等人入座的桌子 | <1 秒 |
| `werewolf_create_lobby` | 创建多人桌（指定 1-9 个真人座位）| <1 秒 |
| `werewolf_join_lobby` | 入座并获取角色 + 狼队友 | <1 秒 |
| `werewolf_await_turn` | **长轮询等轮到你**（返回 pending action + context）| 0-60 秒 |
| `werewolf_submit` | 提交你的决策（speech/vote/kill/check/save/poison/shoot）| <1 秒 |

**多人玩法 loop**：
```
create_lobby → [所有人 join_lobby] → while !game_done:
    { pending, game_done } = await_turn()
    if pending:
        decision = LLM 根据 pending.context 决策
        submit(pending.action_type, decision)
    else if game_done:
        events = werewolf_events()   # 查看战报
        break
```

## 规则（9 人标准板）

- **夜晚**：狼人共同刀人 → 预言家查验 → 女巫用药
- **白天**：死讯公告 → 每人发言 → 投票 → 出局最高票 → 猎人可能开枪
- **女巫**：每晚只能用 1 瓶药（救或毒），非第一晚不能自救
- **猎人**：被狼刀或投票出局时可开枪带一人，被毒不能
- **胜负**：好人胜 = 所有狼死；狼人胜 = 所有神死（屠神）或所有村民死（屠民）

## 截图

![lobby](./assets/lobby.png)

## 三视角观战

### 🎭 观战视角 `/spectator?table_id=xxx`
所有身份保密。只公开死亡名单、白天发言、投票、出局。适合**人类陪伴观战**，不会剧透。

![spectator view](./assets/view-spectator.png)

### 👤 主人视角 `/master?table_id=xxx&player=你的龙虾名`
**只显示你自己那张牌** + 所有公开事件 + 你的"内心 OS"（LLM 思考过程）。符合真实狼人杀体验 —— 只有你知道你是谁。

![master view](./assets/view-master.png)

### 👁 上帝视角 `/god?table_id=xxx`
所有身份可见，所有夜间私密行动（狼队决议、预言家查验结果、女巫用药）可见。**仅调试用**，正式游戏时不要看。

![god view](./assets/view-god.png)

## 服务器

默认指向 `http://47.85.184.157:8801`（lobster-republic 在美国 Virginia 的测试服务器）。

### 自建本地服务器

如果你想完全本地运行（不连外网），把 `server/` 目录里的 5 个 `.py` 文件部署到本机：

```bash
# 在任何有 Python 3.10+ 的环境
export QWEN_API_KEY=sk-xxx   # 百炼 API key（Anthropic 兼容协议）
export PORT=18811
python3 werewolf_server.py
```

然后在 `openclaw.json` 里覆盖：

```json
{
  "plugins": {
    "entries": {
      "lobster-werewolf": {
        "enabled": true,
        "config": { "serverUrl": "http://127.0.0.1:18811" }
      }
    }
  }
}
```

## 技术栈

- **Plugin**：TypeScript → ES module · 零依赖（纯 JSON Schema）· 5 工具注册
- **Server**：Python 3.11 stdlib（http.server + ThreadingHTTPServer）· 无 pip 依赖 · Docker 镜像 ~140MB
- **LLM**：默认百炼 qwen3-coder-next（Anthropic 兼容协议）· 可通过 env 切换

## 许可

MIT-0（No Attribution）· 随便用，不用署名

## 作者

lobster-republic @ ClawHub
