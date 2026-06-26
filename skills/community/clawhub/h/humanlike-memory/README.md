# Human-Like Memory Skill for OpenClaw

面向 OpenClaw 的智能触发记忆 Skill，用于由 Agent 按需召回、搜索和保存记忆。

这个 Skill 的定位是“智能触发，不是每轮触发”：

- Agent 可以在判断有价值时主动 recall / save
- 不会每轮自动 recall
- 不会像 plugin 一样通过 hook 静默接管所有对话
- 不会自己读取 `~/.openclaw/secrets.json`
- 配置统一走 OpenClaw config 或环境变量注入

如果你需要**全自动记忆**，请使用 Human-Like Memory Plugin，而不是这个 Skill。

## 会发生什么网络行为

当 Agent 或用户触发该 Skill 时才会联网：

- `recall` / `search` 会发送查询词、`user_id`、`agent_id`、`scenario`
- `save` / `save-batch` 会发送你明确传入的消息内容，并优先使用 procedural memory 的 `v2/add/context`，必要时回退到 `v1/add/message`
- 如果输入里包含 assistant tool call / tool result，且未禁用捕获，写入时会一并带上结构化 `context_blocks`
- 运行时只会读取文档列出的 `HUMAN_LIKE_MEM_*` 白名单环境变量，不会扫描其它环境变量

默认服务地址是 `https://plugin.human-like.me`，也可以改成你自己的地址。

## 安装

### 从 ClawHub 安装

```bash
openclaw skills install human-like-memory
```

### 手动安装

```bash
git clone https://gitlab.ttyuyin.com/personalization_group/human-like-mem-openclaw-skill.git
cp -r human-like-mem-openclaw-skill ~/.openclaw/workspace/skills/human-like-memory
```

## 配置

### 1. 获取 API Key

访问 [plugin.human-like.me](https://plugin.human-like.me) 获取 `mp_xxx` 密钥。

### 2. 写入 OpenClaw 配置

手动方式：

```bash
openclaw config set skills.entries.human-like-memory.enabled true --strict-json
openclaw config set skills.entries.human-like-memory.apiKey "mp_your_key_here"
openclaw config set skills.entries.human-like-memory.env.HUMAN_LIKE_MEM_BASE_URL "https://plugin.human-like.me"
openclaw config set skills.entries.human-like-memory.env.HUMAN_LIKE_MEM_USER_ID "openclaw-user"
openclaw config set skills.entries.human-like-memory.env.HUMAN_LIKE_MEM_AGENT_ID "main"
openclaw config set skills.entries.human-like-memory.env.HUMAN_LIKE_MEM_SCENARIO "openclaw-plugin"
openclaw config set skills.entries.human-like-memory.env.HUMAN_LIKE_MEM_RECALL_ENABLED "true"
openclaw config set skills.entries.human-like-memory.env.HUMAN_LIKE_MEM_AUTO_SAVE_ENABLED "true"
openclaw config set skills.entries.human-like-memory.env.HUMAN_LIKE_MEM_USE_V2_PROTOCOL "true"
openclaw config set skills.entries.human-like-memory.env.HUMAN_LIKE_MEM_CAPTURE_TOOL_CALLS "true"
openclaw config set skills.entries.human-like-memory.env.HUMAN_LIKE_MEM_SAVE_TRIGGER_TURNS "5"
```

如果你已经在当前会话里明确把 API Key 提供给 Agent，也可以让 Agent 代你执行这些 `openclaw config set` 命令；否则默认仍应由用户自己配置。

### 3. 验证

```bash
node ~/.openclaw/workspace/skills/human-like-memory/scripts/memory.mjs config
```

输出里出现 `apiKeyConfigured: true` 即表示配置成功。

## 使用方式

这个 Skill 现在支持 Agent 智能触发，也支持用户显式调用。

- 当模型判断需要连续上下文时，可以调用 recall / search
- 当模型判断出现稳定偏好、重要决策、身份纠正或多轮讨论总结时，可以调用 save / save-batch
- 如果你想每轮自动 recall、生命周期 hook、完全后台化，请改用 plugin

## 典型记忆任务

- 恢复上一次会话里的上下文、项目状态和决策
- 回忆用户偏好、身份信息、命名习惯和长期约束
- 复用稳定流程、操作手册、检查清单等程序化记忆
- 在回答连续性问题前先 search / recall 相关记忆
- 把有长期价值的结论、纠正和摘要保存下来

## 记忆类型

- Semantic memory：事实、偏好、身份、长期上下文
- Procedural memory：流程、习惯、检查清单、可复用的做事方式
- Episodic memory：具体对话、项目过程、阶段性决策

## 示例查询与保存

- Recall：`"roadmap decisions from last week"`
- Search：`"what name preference did I mention"`
- Save：`"I prefer UTC+8 timestamps"`

## 建议保存的内容

- 稳定偏好
- 已确认的重要决策
- 会影响后续协作的身份或背景信息
- 对之前认知的纠正
- 多轮讨论后值得长期保留的摘要

如果一次对话已经形成了可复用流程或 checklist，也可以把它作为程序化记忆保存下来。

## Shared Namespace

如果你希望继续写入或检索和 plugin 相同的记忆池，请确保以下三项一致：

- `user_id`
- `agent_id`
- `scenario`

其中 `scenario` 现在会显式出现在检索和写入请求里，不再只依赖 workflow metadata 传递。

## 错误处理

- 如果 API key 缺失，脚本会输出可直接执行的修复命令
- 如果远端超时或报错，不会静默保存
- 如果没有命中记忆，应按“正常空结果”处理

## CLI 示例

```bash
node ~/.openclaw/workspace/skills/human-like-memory/scripts/memory.mjs config
node ~/.openclaw/workspace/skills/human-like-memory/scripts/memory.mjs recall "我最近在推进什么项目"
node ~/.openclaw/workspace/skills/human-like-memory/scripts/memory.mjs search "上次提到的命名偏好"
node ~/.openclaw/workspace/skills/human-like-memory/scripts/memory.mjs save "我偏好北京时间" "收到，我会在相关场景中记住这一点"
echo '[{"role":"user","content":"你好"},{"role":"assistant","content":"你好！"}]' | node ~/.openclaw/workspace/skills/human-like-memory/scripts/memory.mjs save-batch
```

## 与 Plugin 的区别

| 特性 | Skill | Plugin |
|------|-------|--------|
| 触发方式 | 显式调用 | 生命周期自动 hook |
| 记忆召回 | 仅在调用时发生 | 可自动发生 |
| 记忆存储 | 仅在调用时发生 | 可自动发生 |
| 网络行为 | 可预测、显式 | 更自动化 |
| 适用场景 | 手动精确控制 | 始终开启的长期记忆 |

Plugin 仓库：<https://www.npmjs.com/package/@humanlikememory/human-like-mem>

## 安全说明

详细说明见 [SECURITY.md](./SECURITY.md)。

这次版本调整的重点是：

- 消除对 `secrets.json` 和私有 `config.json` 的直接读取
- 移除 Skill 侧“每轮自动 recall / 静默保存”的默认引导
- 将隐私和联网说明前置
- 改成更符合 OpenClaw 官方配置模型的发布方式

## License

Apache-2.0
