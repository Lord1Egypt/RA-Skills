# MemOS Cloud Plugin for Claude Code

MemOS Cloud 记忆插件 - 在 Claude Code 中实现跨会话记忆功能。

## 功能

- **召回 (Recall)**: 在对话中自动搜索相关记忆
- **存储 (Store)**: 将重要信息保存到 MemOS Cloud
- **命令 (Commands)**: `/memos` 手动管理记忆

## 安装

### 1. 获取 API Key

访问 https://memos-dashboard.openmem.net/cn/apikeys/ 创建 API Key。

### 2. 配置环境变量

```bash
# 创建配置文件
cat > ~/.claude/.env << 'EOF'
MEMOS_API_KEY=your_api_key_here
MEMOS_USER_ID=openclaw-user
MEMOS_BASE_URL=https://memos.memtensor.cn/api/openmem/v1
EOF
```

### 3. 验证安装

```bash
node ~/.claude/plugins/memos-cloud/memos-api.js status
```

## 使用

### 自动召回

当对话涉及之前的内容时，Claude 会自动调用：
```bash
node ~/.claude/plugins/memos-cloud/memos-api.js search "查询内容"
```

### 自动存储

当你说"记住"或有重要信息时，Claude 会自动调用：
```bash
node ~/.claude/plugins/memos-cloud/memos-api.js add "记忆内容"
```

### 手动管理

```bash
/memos search 关键词    # 搜索记忆
/memos add 内容        # 添加记忆
/memos status          # 查看状态
```

## 文件结构

```
~/.claude/plugins/memos-cloud/
├── .claude-plugin/
│   └── plugin.json          # 插件元数据
├── .mcp.json                # MCP 配置
├── commands/
│   └── memos.md             # /memos 命令定义
├── skills/
│   ├── memos-recall/        # 记忆召回技能
│   │   └── SKILL.md
│   └── memos-store/         # 记忆存储技能
│       └── SKILL.md
├── memos-api.js             # API 客户端 (Node.js)
├── memos-api.sh             # API 客户端 (Bash)
└── README.md                # 本文档
```

## 与 OpenClaw 插件的区别

| 特性 | OpenClaw 插件 | Claude Code 插件 |
|------|--------------|------------------|
| 自动召回 | ✅ 对话前自动 | ⚠️ 技能触发 |
| 自动存储 | ✅ 对话后自动 | ⚠️ 技能触发 |
| 需要 OpenClaw | ✅ 必须 | ❌ 不需要 |
| 安装复杂度 | 高 | 低 |

## 故障排除

### API Key 未设置
```
❌ Error: MEMOS_API_KEY not set
```
**解决**: 创建 `~/.claude/.env` 并添加 `MEMOS_API_KEY=your_key`

### 网络错误
检查网络连接和 `MEMOS_BASE_URL` 配置。

### 技能未触发
Claude Code 技能触发依赖关键词和上下文，手动使用 `/memos` 命令更可靠。

## 参考

- MemOS Cloud: https://memos.memtensor.cn
- API Dashboard: https://memos-dashboard.openmem.net
- OpenClaw Plugin: https://github.com/MemTensor/MemOS-Cloud-OpenClaw-Plugin
