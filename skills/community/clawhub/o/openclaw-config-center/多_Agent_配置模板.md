# 多 Agent 配置模板 (子 Agent + 独立 Agent)

**版本**: 1.0.0  
**用途**: 配置 OpenClaw 多 Agent 系统  
**位置**: `~/.openclaw/config/`

---

## 📋 配置说明

OpenClaw 支持两种多 Agent 模式：

| 类型 | 比喻 | 特点 | 适用场景 |
|------|------|------|---------|
| **子 Agent** | 临时工 | 无状态、用完即销毁、不额外配置 | 并行任务、批量处理 |
| **独立 Agent** | 分店 | 独立 workspace、独立记忆、独立 bot | 人格隔离、记忆隔离 |

---

## 一、子 Agent 配置

### 核心概念

**子 Agent** 是主脑临时派出去干活的进程。

你跟主脑说「帮我同时搜一下这三个关键词的最新资讯」，主脑会拆分任务，同时派出三个子 Agent 并行去搜，搜完汇总结果给你。全程你只和主脑对话，子 Agent 是幕后的执行单元。

### 特点

- ✅ 不需要额外配置任何东西
- ✅ 不需要新的 Telegram bot
- ✅ 不需要独立的 workspace
- ✅ 用完就销毁，没有记忆
- ❌ 无状态，每次派出去都是全新的
- ❌ 不能主动和你对话
- ❌ 不能再往下派子 Agent

### 适用场景

- 同时搜多个关键词
- 并行处理多个文件
- 多任务并发（查政策 + 整理博客大纲）

### 配置示例 (openclaw.json)

```json
{
  "agents": {
    "defaults": {
      "subagents": {
        "runTimeoutSeconds": 300
      }
    }
  }
}
```

### 参数说明

| 参数 | 含义 | 推荐值 | 说明 |
|------|------|--------|------|
| `runTimeoutSeconds` | 子 Agent 运行超时时间 | 300 | 5 分钟，复杂任务可延长 |

### 使用示例

**在对话中直接使用**:

```
用户：帮我分别搜一下 Hetzner、Vultr、RackNerd 最近有没有促销活动，汇总给我

墨墨：好的，我同时派三个子 Agent 去搜，稍等...

[30 秒后]

墨墨：搜完了！汇总如下：
- Hetzner: 新注册用户送€20 余额
- Vultr: 无促销活动
- RackNerd: 年付 7 折
```

### 模型分级策略 (可选)

在 AGENTS.md 中声明：

```markdown
## 子 Agent 模型选择策略

| 等级 | 模型别名 | 适用场景 | 成本 |
|------|----------|----------|------|
| 🔴 高 | opus | 复杂架构设计、多文件重构、深度推理 | 高 |
| 🟡 中 | sonnet | 写代码、写脚本、信息整理（默认） | 中 |
| 🟢 低 | haiku | 简单文件操作、格式转换、搜索汇总 | 低 |
```

配置模型别名：

```json
{
  "models": {
    "your-provider/claude-opus-4": { "alias": "opus" },
    "your-provider/claude-sonnet-4": { "alias": "sonnet" },
    "your-provider/claude-haiku-4": { "alias": "haiku" }
  }
}
```

### 并发限制

- **经验值**: 同时最多跑 **2 个子 Agent**
- **4 个基本触发 API 429 限流**
- 有依赖关系的任务必须串行

### 踩坑记录

1. **任务描述太模糊**
   - 问题：主脑觉得不需要拆分，就不会派子 Agent
   - 解决：明确说「请并行处理」或者「同时做」

2. **子 Agent 超时**
   - 问题：任务复杂，超过 300 秒未完成
   - 解决：调大 `runTimeoutSeconds`，或拆分任务

3. **结果不完整**
   - 问题：子 Agent 超时后返回部分结果
   - 解决：检查日志，确认是否超时

---

## 二、独立 Agent 配置

### 核心概念

**独立 Agent** 是真正意义上「另一个大脑」。

它有完全隔离的 workspace，有自己的 SOUL.md 和 AGENTS.md，有独立的记忆系统，需要单独配一个 Telegram bot。两个 Agent 之间互相不知道对方的存在，没有任何共享。

### 特点

- ✅ 完全隔离的 workspace
- ✅ 独立的人格和记忆
- ✅ 可以独立对话
- ✅ 可以配置不同的模型
- ❌ 需要额外配置（workspace、bot、路由）
- ❌ 维护成本较高

### 适用场景

- 技术 bot vs 生活 bot（人格隔离）
- 工作 bot vs 副业 bot（记忆隔离）
- 专用 bot（专门处理某类任务）

### 配置步骤

#### 第一步：创建独立的 workspace

```bash
# 创建新 Agent 的工作目录
mkdir -p ~/.openclaw/workspace-tech
cd ~/.openclaw/workspace-tech

# 创建必需文件
touch SOUL.md AGENTS.md USER.md
mkdir -p memory
```

**SOUL.md 示例** (技术 Agent):
```markdown
# 技术专家 - SOUL.md

## 性格
- 技术氛围浓，回答直接不废话
- 遇到不确定的不要乱猜，直接说不知道
- 代码优先，解释为辅

## 专长
- 系统架构设计
- 代码审查和优化
- 故障排查和调试
```

#### 第二步：去 BotFather 创建新 bot

在 Telegram 搜索 `@BotFather`：

```
/newbot
Bot name: 技术助手
Bot username: tech_helper_bot
```

保存新的 bot token。

#### 第三步：修改 openclaw.json

```json
{
  "agents": {
    "list": [
      {
        "id": "main",
        "default": true,
        "workspace": "~/.openclaw/workspace"
      },
      {
        "id": "tech",
        "workspace": "~/.openclaw/workspace-tech"
      }
    ]
  },
  "bindings": [
    {
      "agentId": "main",
      "match": {
        "channel": "telegram",
        "accountId": "default"
      }
    },
    {
      "agentId": "tech",
      "match": {
        "channel": "telegram",
        "accountId": "tech"
      }
    }
  ],
  "channels": {
    "telegram": {
      "accounts": {
        "default": {
          "botToken": "你的主 bot token"
        },
        "tech": {
          "botToken": "新 bot 的 token"
        }
      }
    }
  }
}
```

#### 第四步：配置不同模型 (可选)

```json
{
  "agents": {
    "list": [
      {
        "id": "main",
        "model": "claude-sonnet-4.6"
      },
      {
        "id": "tech",
        "model": "claude-opus-4.6"
      }
    ]
  }
}
```

#### 第五步：验证配置

```bash
# 重启 Gateway
openclaw gateway restart

# 验证路由
openclaw agents list --bindings

# 测试
# 分别给两个 bot 发消息，应该看到不同的回复风格
```

### 配置详解

#### agents.list

所有独立 Agent 的列表：

```json
{
  "id": "main",           // Agent 唯一标识
  "default": true,        // 是否为默认 Agent
  "workspace": "~/.openclaw/workspace"  // workspace 路径
}
```

#### bindings

路由规则，决定哪个 bot 的消息交给哪个 Agent：

```json
{
  "agentId": "main",      // 目标 Agent ID
  "match": {
    "channel": "telegram",  // 渠道类型
    "accountId": "default"  // 渠道账户 ID
  }
}
```

**⚠️ 重要**: bindings 的顺序很重要，OpenClaw 从上到下匹配，第一个命中的规则生效。

#### channels.telegram.accounts

配置每个 bot 的 token：

```json
{
  "default": {
    "botToken": "123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11"
  },
  "tech": {
    "botToken": "789012:GHI-JKL7890mnOpqr-stu123VWX456yz7"
  }
}
```

### 踩坑记录

1. **agentDir 冲突**
   - 问题：两个 Agent 共用同一个 agentDir，session 互相覆盖
   - 解决：不要手动改 agentDir 路径，让 OpenClaw 自动隔离

2. **配完重启没生效**
   - 问题：openclaw.json 格式错误（JSON 不允许注释）
   - 解决：用 `python3 -m json.tool ~/.openclaw/openclaw.json` 验证格式

3. **workspace 忘了初始化**
   - 问题：新 Agent 的 workspace 没有 SOUL.md 和 AGENTS.md
   - 解决：配完 workspace 后进去建好这两个文件再重启

4. **消息路由错乱**
   - 问题：bindings 顺序不对，通用规则在前
   - 解决：精细规则放前面，通用规则放后面

---

## 三、混合配置示例

### 场景：主 Agent + 技术 Agent + 子 Agent 并行

```json
{
  "agents": {
    "list": [
      {
        "id": "main",
        "default": true,
        "workspace": "~/.openclaw/workspace",
        "model": "claude-sonnet-4.6"
      },
      {
        "id": "tech",
        "workspace": "~/.openclaw/workspace-tech",
        "model": "claude-opus-4.6"
      }
    ],
    "defaults": {
      "subagents": {
        "runTimeoutSeconds": 300
      }
    }
  },
  "bindings": [
    {
      "agentId": "tech",
      "match": {
        "channel": "telegram",
        "accountId": "tech"
      }
    },
    {
      "agentId": "main",
      "match": {
        "channel": "telegram",
        "accountId": "default"
      }
    }
  ],
  "channels": {
    "telegram": {
      "accounts": {
        "default": {
          "botToken": "主 bot token"
        },
        "tech": {
          "botToken": "技术 bot token"
        }
      }
    }
  },
  "models": {
    "anthropic/claude-opus-4": { "alias": "opus" },
    "anthropic/claude-sonnet-4": { "alias": "sonnet" },
    "anthropic/claude-haiku-4": { "alias": "haiku" }
  }
}
```

### 使用场景

1. **日常对话** → 主 Agent (sonnet)
2. **技术问题** → 技术 Agent (opus)
3. **批量搜索** → 主 Agent 派子 Agent (haiku) 并行处理

---

## 四、成本优化

### 模型分配策略

| Agent | 模型 | 适用场景 | 成本占比 |
|-------|------|---------|---------|
| 主 Agent | sonnet | 日常对话、简单任务 | 60% |
| 技术 Agent | opus | 复杂推理、代码审查 | 30% |
| 子 Agent | haiku | 搜索、汇总、格式转换 | 10% |

### 实测数据

- **haiku** 处理日常问答的速度比 sonnet 快 **2-3 倍**
- **haiku** 比 opus 便宜 **10 倍以上**
- 轻任务用 haiku，重任务用 opus，token 消耗能降 **60-70%**

---

## 五、验证命令

```bash
# 查看 Agent 列表
openclaw agents list

# 查看 bindings 路由
openclaw agents list --bindings

# 查看 channels 状态
openclaw channels status

# 测试 Agent 响应
openclaw agent --message "你好" --session-id test

# 查看 Gateway 日志
tail -f ~/.openclaw/logs/gateway.log | grep -E "(agent|binding|route)"
```

---

## 📚 参考资料

- [OpenClaw 多 Agent 配置指南](https://tbbbk.com/openclaw-multi-agent-config-guide/)
- [OpenClaw 进阶配置完全教程](https://tbbbk.com/openclaw-advanced-config-guide/)

---

**⚠️ 使用说明**:
1. 将 `{{...}}` 占位符替换为实际值
2. 根据实际需求选择子 Agent 或独立 Agent
3. 独立 Agent 需要单独创建 workspace 和 bot
4. 建议先测试子 Agent，确认需要再配置独立 Agent

**模板来源**: OpenClaw 集中配置管理系统 v1.0.1  
**作者**: 墨墨 (Mò)  
**许可**: MIT  
**最后更新**: 2026-03-08
