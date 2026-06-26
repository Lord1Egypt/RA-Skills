# Discord 配置参考

## 快速设置
1. Discord开发者门户 → Applications → New Application → Bot → 复制Token
2. 启用 Message Content Intent + Server Members Intent
3. OAuth2 URL Generator: scopes=bot+applications.commands, 权限=View/Send/Read History/Embed/Attach/Reactions
4. 邀请机器人到服务器
5. 配置: `channels.discord.token: "TOKEN"` 或 `DISCORD_BOT_TOKEN=...`

### 最小配置
```json5
{ channels: { discord: { enabled: true, token: "YOUR_BOT_TOKEN" } } }
```

## 访问控制

### 私信
- `dm.policy`: `pairing`(默认) | `allowlist` | `open` | `disabled`
- `dm.allowFrom`: 用户ID/名称列表
- `dm.enabled`: false 忽略所有私信
- `dm.groupEnabled`: 启用群组私信(默认false)

### 服务器
- `groupPolicy`: `allowlist`(默认) | `open` | `disabled`
- `guilds.<guildId>.users`: 每服务器用户白名单
- `guilds.<guildId>.channels.<id>.allow`: 频道允许
- `guilds.<guildId>.channels.<id>.users`: 每频道用户白名单
- `guilds.<guildId>.requireMention`: 提及要求(可按频道覆盖)

### 获取ID
Discord设置 → 高级 → 开发者模式 → 右键复制ID

## 配置示例
```json5
channels: {
  discord: {
    enabled: true,
    token: "abc.123",
    dm: { policy: "pairing", allowFrom: ["123456789012345678"] },
    guilds: {
      "GUILD_ID": {
        requireMention: true,
        users: ["USER_ID"],
        channels: {
          "CHANNEL_ID": { allow: true, requireMention: false }
        }
      },
      "*": { requireMention: true }
    }
  }
}
```

## 工具操作
| 操作 | 默认 | 说明 |
|------|------|------|
| reactions | ✅ | 表情反应 |
| messages | ✅ | 读取/发送/编辑/删除 |
| threads | ✅ | 创建/列出/回复 |
| pins | ✅ | 置顶管理 |
| search | ✅ | 消息搜索 |
| channels | ✅ | 频道管理 |
| roles | ❌ | 角色添加/移除 |
| moderation | ❌ | 超时/踢出/封禁 |

## 限制
- `textChunkLimit`: 2000字符(默认)
- `maxLinesPerMessage`: 17(默认)
- `mediaMaxMb`: 8MB(默认)
- `historyLimit`: 20条(默认)
- `replyToMode`: off|first|all

## 常见问题
- "Used disallowed intents": 开发者门户启用 Message Content Intent
- 不回复服务器消息: 检查权限+意图+allowlist+requireMention
- `groupPolicy` 默认 allowlist，需添加guild或设为open
- `requireMention` 必须在 guilds 下，顶层会被忽略
