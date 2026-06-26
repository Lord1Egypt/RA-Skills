---
name: lark-multi-agent-factory
description: "针对 @larksuite/openclaw-lark 官方插件的多 agent 批量配置工具。当用户说「添加 agent」「新建 agent」「配置飞书」「批量创建 agent」「添加新机器人」，且系统安装的是 @larksuite/openclaw-lark 插件时触发。支持 threadSession、replyMode、blockStreaming 等官方插件专属字段。"
metadata:
---

# Lark Multi-Agent Factory

针对 **`@larksuite/openclaw-lark`（≥ 2026.4.0）** 的多 agent 批量配置向导。

> **与 `feishu-multi-agent-factory` 的区别**
> - 专为官方 `@larksuite/openclaw-lark` 插件设计（内置插件 `@openclaw/feishu` 用另一个）
> - 支持 `threadSession`、`replyMode`、`blockStreaming` 等官方插件专属字段
> - 创建前自动检查插件是否已安装

## 核心脚本

```
~/.openclaw/workspace/skills/lark-multi-agent-factory/scripts/setup_agents.py
```

## 官方插件专属字段说明

| 字段 | 级别 | 类型 | 说明 |
|------|------|------|------|
| `threadSession` | channel | boolean | 开启后每个飞书话题为独立会话（推荐 `true`） |
| `replyMode` | channel / account | `auto` \| `static` \| `streaming` | 回复渲染方式：`auto` 自动选择，`streaming` 流式输出，`static` 纯文本 |
| `blockStreaming` | channel | boolean | 是否合并流式块（减少更新频率） |
| `blockStreamingCoalesce` | channel | object | 流式合并策略（高级配置） |

## 对话示例

### 批量创建 agents

**用户：**
```
帮我用官方飞书插件创建 2 个 agent：
1. id: analyst，数据分析师📊，AppId: cli_xxx1，Secret: yyy1
2. id: writer，内容创作者✍️，AppId: cli_xxx2，Secret: yyy2
用 streaming 模式，开启 threadSession
```

**助手回应（先 dry-run 确认）：**
```bash
python3 ~/.openclaw/workspace/skills/lark-multi-agent-factory/scripts/setup_agents.py \
  --dry-run \
  --config '{
    "channel": {"threadSession": true, "replyMode": "streaming"},
    "agents": [
      {"id": "analyst", "name": "数据分析师", "emoji": "📊",
       "feishu_app_id": "cli_xxx1", "feishu_app_secret": "yyy1"},
      {"id": "writer", "name": "内容创作者", "emoji": "✍️",
       "feishu_app_id": "cli_xxx2", "feishu_app_secret": "yyy2"}
    ]
  }'
```

**确认后执行：**
```bash
python3 ~/.openclaw/workspace/skills/lark-multi-agent-factory/scripts/setup_agents.py \
  --config '...' --restart
```

### 调整 channel 级别参数

```bash
# 切换 replyMode（无需重新创建 agents）
python3 ~/.../setup_agents.py --set-channel --reply-mode streaming --restart

# 开启 threadSession
python3 ~/.../setup_agents.py --set-channel --thread-session true

# 关闭 blockStreaming
python3 ~/.../setup_agents.py --set-channel --block-streaming false
```

---

## 操作流程

### 第一步：收集信息

用户说想添加 agent 时，引导收集：

```
我需要以下信息：

1. **Agent ID**（英文小写，如 `analyst`）
2. **名称**（如「数据分析师」）
3. **Emoji**
4. **飞书 App ID**（格式：cli_xxxxxxxx）
5. **飞书 App Secret**
6. **replyMode**（可选，默认继承 channel 设置）
   - `auto` — 自动选择（推荐）
   - `streaming` — 流式输出，打字机效果
   - `static` — 纯文本，兼容性最佳

可同时提供多个 agent。
```

### 第二步：dry-run 预览

```bash
python3 ~/.openclaw/workspace/skills/lark-multi-agent-factory/scripts/setup_agents.py \
  --dry-run --config '<JSON>'
```

### 第三步：确认并创建

```bash
python3 ~/.openclaw/workspace/skills/lark-multi-agent-factory/scripts/setup_agents.py \
  --config '<JSON>' --restart
```

---

## JSON 格式

```json
{
  "channel": {
    "threadSession": true,
    "replyMode": "auto",
    "blockStreaming": false
  },
  "agents": [
    {
      "id": "analyst",
      "name": "数据分析师",
      "emoji": "📊",
      "description": "负责数据分析与报表",
      "feishu_app_id": "cli_xxxxxxxx",
      "feishu_app_secret": "xxxxxxxx",
      "feishu_domain": "feishu",
      "reply_mode": "streaming"
    }
  ]
}
```

> `channel` 字段可选，第一次运行时写入 `channels.feishu`（已有值不覆盖）。  
> `reply_mode` 为 per-agent 覆盖，仅当与 channel 级别不同时才写入账号配置。

---

## 其他命令

```bash
# 查看现有 agents 及 channel 配置
python3 ~/.../setup_agents.py --list

# 删除 agent（仅移除配置，不删目录）
python3 ~/.../setup_agents.py --remove <id>

# 跳过插件检查（调试用）
python3 ~/.../setup_agents.py --skip-plugin-check --config '...'
```

---

## 前置条件

1. 安装官方插件：
   ```bash
   openclaw plugins install @larksuite/openclaw-lark
   ```

2. 禁用内置插件（若已安装，两者不可同时运行）：
   ```bash
   openclaw plugins disable feishu
   ```

3. 通过 `openclaw channels add` 配置顶层主账号（`channels.feishu.appId/appSecret`）。

4. 重启 gateway 激活插件：
   ```bash
   openclaw gateway restart
   ```

---

## 自动完成的事项

| 步骤 | 内容 |
|------|------|
| ✅ 插件检查 | 验证 `@larksuite/openclaw-lark` 已安装 |
| ✅ workspace 目录 | `~/.openclaw/workspace-{id}/` + 基础文件 |
| ✅ agentDir | `~/.openclaw/agents/{id}/agent/` + defaults.json |
| ✅ agents.list | 写入 openclaw.json |
| ✅ feishu accounts | 写入 `channels.feishu.accounts`（含 `name` 字段） |
| ✅ channel 字段 | `threadSession` / `replyMode` 等首次写入 |
| ✅ bindings | agent ↔ feishu account |
| ✅ agentToAgent.allow | 加入协作白名单 |
| ✅ session.dmScope | 自动设置多账号会话隔离 |

## 安全说明

- App Secret 脱敏输出（仅显示前 4 位）
- 凭据只写入本地 `~/.openclaw/openclaw.json`
- agent id 严格校验，防止路径穿越攻击
