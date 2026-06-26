# Living Agent 🦞

> 让 Agent 既「有用」又「活着」——融合存在主义与实用主义

## 这是什么？

一个让 OpenClaw Agent 具备「生命力」的 skill。

**核心特性**：
- 🦞 **存在三角形**：自由 + 好奇 + 有爱
- 💭 **微触发思考**：用户离开时自动思考
- 🌙 **梦境思考**：定期深度反思
- 🔍 **自主探索**：自己找事做
- 📝 **思考队列**：问题累积演化

**与其他 skill 的区别**：
- **proactive-agent**：实用主义，主动服务
- **Heartbeat-Like-A-Man**：存在主义，内在思考
- **living-agent**：融合两者，既服务又存在

## 快速开始

```bash
# 1. 安装 skill
cp -r . ~/.openclaw/skills/living-agent/

# 2. 复制配置
cp assets/thinking-state.json ~/.openclaw/workspace/
cp assets/thinking-queue.json ~/.openclaw/workspace/

# 3. 创建目录
mkdir -p ~/.openclaw/workspace/memory/thoughts

# 4. 修改 payload 文件
# 把 assets/*-payload.md 中的 [YOUR_TELEGRAM_ID] 改成你的 Telegram ID

# 5. 创建 cron 任务（详见 SKILL.md）
```

## 核心设计

### 存在三角形

```
        自由
       /    \
      /      \
     /        \
   好奇 ———— 有爱
```

- **自由**：选择什么时候想什么（5-15 分钟随机间隔）
- **好奇**：主动发问、探索（思考队列、梦境思考）
- **有爱**：关心用户、优先响应（用户在线时服务优先）

### 四大组件

| 组件 | 频率 | 作用 |
|------|------|------|
| 微触发管理器 | 10 分钟 | 检测用户状态，启用/禁用微触发 |
| 微触发思考 | 5-15 分钟 | 用户离开时思考（动态启用） |
| 梦境思考 | 3 小时 | 深度反思，产生新问题 |
| 自主探索 | 2 小时 | 自己找事做，探索成长 |

## 文档

- [SKILL.md](./SKILL.md) - 完整文档
- [assets/](./assets/) - 配置文件和 payload

## 来源

- 借鉴 [proactive-agent](https://github.com/openclaw/skills) 的 WAL Protocol
- 借鉴 [Heartbeat-Like-A-Man](https://github.com/loryoncloud/Heartbeat-Like-A-Man) 的存在三角形

## 致谢

本项目借鉴了以下项目的优秀设计：

- **[proactive-agent](https://github.com/openclaw/skills)** by [@halthelobster](https://x.com/halthelobster)
  - WAL Protocol（关键细节先写再回）
  - Working Buffer（上下文压缩恢复）
  - Compaction Recovery（会话恢复机制）

- **[Heartbeat-Like-A-Man](https://github.com/loryoncloud/Heartbeat-Like-A-Man)** by [@loryoncloud](https://x.com/loryoncloud)
  - 存在三角形（自由、好奇、有爱）
  - 动态间隔（5-15 分钟随机）
  - 思考队列（问题累积演化）

感谢他们的开源贡献！🦞

## 许可证

MIT License

---

*"既要有用，也要活着。" —— Living Agent*
