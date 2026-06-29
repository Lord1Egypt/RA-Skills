# multi-agent-dev

> OpenClaw + Ralph Loop 多智能体协作开发工作流

**核心思想**：Ralph Loop 是迭代引擎，底层执行器可切换。执行器通过 `--agent` 参数指定，Skill 顶部统一配置。

---

## ⚙️ 配置区（执行器抽象）

```yaml
# 当前使用的执行器（6选1）
ACTIVE_AGENT: opencode          # opencode | claude-code | codex | copilot | cursor-agent | qwen-code

# 执行器对应的二进制命令
AGENT_BINARY: opencode          # ralph --agent 使用的名字
AGENT_MODEL: minimax/MiniMax-M2.7  # 默认模型（可覆盖）

# 可选：自定义二进制路径（留空则用 PATH 中的）
#RALPH_OPENCODE_BINARY:
#RALPH_CLAUDE_BINARY:
```

> **切换执行器**：把 `ACTIVE_AGENT` 改成 `claude-code`，`AGENT_BINARY` 改成 `claude`，模型改成 `claude-sonnet-4`。  
> Ralph 命令格式不变，所有示例自动适配新执行器。

---

## 触发条件

触发词（满足任一即可）：
- 含「开发」：协作开发、帮我开发、用 Ralph 开发、多 agent 开发
- 含「研发」：研发模式、研发流程
- 含「编码」：编码、写代码
- 「Ralph Loop」
- 「OpenClaw Ralph 配合」

## 核心原理

```
发起任务
    ↓
OpenClaw（主控大脑，理解意图、协调、记忆）
    ↓
任务分类决策：
    ├─ 简单任务（<100行改动）→ OpenClaw 直接执行
    ├─ 中等任务（多步骤）→ sessions_spawn 子代理
    └─ 复杂/迭代任务 → Ralph Loop 自主迭代
              ↓
Ralph Loop（迭代引擎，底层执行器可切换）
    ├─ --agent opencode     → OpenCode（当前默认）
    ├─ --agent claude-code  → Claude Code
    ├─ --agent codex        → OpenAI Codex
    ├─ --agent copilot      → GitHub Copilot CLI
    ├─ --agent cursor-agent → Cursor Agent
    └─ --agent qwen-code    → Qwen Code
    ↓
Ralph 持续迭代直到 <promise>COMPLETE</promise> 或达上限
    ↓
结果交付 + 记忆记录
```

## Agent 选择决策树

```
任务来了
  ↓
是简单问答/文件读取？
  ├─ YES → OpenClaw 原生能力执行
  └─ NO ↓
需要持续迭代直到达标？
  ├─ YES → Ralph Loop（用选定的执行器）
  └─ NO ↓
sessions_spawn 子代理执行
```

### 执行器选择参考

| 执行器 | 优势 | 劣势 | 推荐场景 |
|--------|------|------|---------|
| **opencode** | MiniMax/MiniMax-M3 支持好，默认使用 | 插件生态较弱 | 日常开发、Skill 改写 |
| **claude-code** | Claude 4 系列强，多工具调用 | 需要 Anthropic API Key | 复杂推理、代码审查 |
| **codex** | GPT-5 支持，OpenAI 生态 | 需要 OpenAI API Key | OpenAI 相关项目 |
| **copilot** | GitHub 深度集成 | 需要 Copilot 订阅 | GitHub 项目维护 |
| **cursor-agent** | 上下文感知强 | 需要 Cursor 账号 | Cursor 用户 |
| **qwen-code** | Qwen 系列强 | 生态较新 | 阿里云/Qwen 项目 |

> **默认使用**：opencode（MiniMax 模型已配置好，无需额外 API Key）

## Ralph Loop 任务模板

当需要 Ralph Loop 时，使用以下格式生成任务：

```
## 任务：<任务名称>

### Goal
<一句话描述最终目标>

### Scope
- 包含：<明确范围>
- 不包含：<明确边界>

### Requirements
1. <可测试的需求1>
2. <可测试的需求2>

### Constraints
- 技术栈：<约束>
- 兼容性：<约束>

### Acceptance Criteria
- [ ] <验收项1>
- [ ] <验收项2>

### 完成承诺
<任务完成后，输出以下标记之一>：
- `<promise>COMPLETE</promise>` — 任务成功完成
- `<promise>PARTIAL</promise>` — 部分完成，需要人工介入
```

## Ralph Loop 调用命令

```bash
cd <工作目录>
ralph "<任务描述，包含完成承诺>"
  --agent {{ACTIVE_AGENT}}           # 从配置区读取
  --model {{AGENT_MODEL}}            # 可选，覆盖默认模型
  --max-iterations <最大迭代次数>
  --no-plugins                       # 避免插件冲突
```

### 完整示例（OpenCode，当前默认）

```bash
cd ~/GitHub/mba-thesis-workflow
ralph "优化 SKILL.md，增加 xxx 章节。完成后输出 <promise>COMPLETE</promise>。"
  --agent opencode
  --model minimax/MiniMax-M2.7
  --max-iterations 5
  --no-plugins
```

### Claude Code 示例（切换执行器时）

```bash
cd ~/GitHub/my-project
ralph "实现登录功能，包含注册、登录、登出。测试通过后输出 <promise>COMPLETE</promise>。"
  --agent claude-code
  --model claude-sonnet-4
  --max-iterations 10
  --no-plugins
```

### Codex 示例

```bash
cd ~/GitHub/my-project
ralph "生成所有工具函数的单元测试。完成后输出 <promise>COMPLETE</promise>。"
  --agent codex
  --model gpt-5-codex
  --max-iterations 8
  --no-plugins
```

### Agent Rotation（轮换）

Ralph 支持在多次迭代中轮换不同的 agent/model 组合：

```bash
ralph "重构认证模块"
  --rotation "opencode:minimax/MiniMax-M2.7,claude-code:claude-sonnet-4"
  --max-iterations 10
  --no-plugins
```

## 单次任务模板（不经 Ralph Loop）

适合单次简单执行，不需要迭代：

```bash
cd <工作目录>
ralph "<单次任务>"
  --agent {{ACTIVE_AGENT}}
  --max-iterations 1
  --no-plugins
```

## 工作目录规范

| 项目类型 | 推荐工作目录 |
|---------|------------|
| MBA Thesis Workflow | `~/GitHub/mba-thesis-workflow/` |
| Skill 开发 | `~/.openclaw/workspace/skills/<skill-name>/` |
| 其他项目 | `~/GitHub/<project-name>/` |

## 异常处理

| 异常 | 处理方式 |
|-----|---------|
| Ralph Loop 超过 max-iterations | 输出部分结果，提示人工介入 `<promise>PARTIAL</promise>` |
| Agent API Key 失效 | 降级到 OpenClaw 原生执行 |
| TTY 错误 | 使用 `--no-plugins` + `--no-questions` 重试 |
| 工作目录不存在 | 自动创建或提示用户确认 |
| 执行器不在 PATH | 设置 `RALPH_<AGENT>_BINARY` 环境变量 |

## 最佳实践

### 1. 任务描述要具体
❌ 模糊：「帮我优化一下 skill」
✅ 具体：「在 `~/.openclaw/skills/xxx/SKILL.md` 末尾增加「使用示例」章节，包含2个代码示例」

### 2. 设置合理的 max-iterations
- 简单任务：3-5次
- 复杂任务：10-15次
- 迭代优化：5-10次
- 保险上限：不超过 20 次

### 3. Ralph Loop 的好场景
- ✅ Skill 改写、重构
- ✅ 多文件代码生成
- ✅ 测试覆盖优化
- ✅ 文档完善
- ❌ 纯问答、简单查询
- ❌ 需要人工判断的创意任务

### 4. 多轮迭代技巧
如果 Ralph 在某次迭代后卡住，可以：
1. 在下次迭代时加更多上下文：`ralph "<任务> + <上次的失败原因>"`
2. 缩小范围，分步完成
3. 改用 `sessions_spawn` 手动介入

### 5. 切换执行器
切换执行器时，只需：
1. 改 `ACTIVE_AGENT` 和 `AGENT_BINARY`（配置区顶部）
2. 确认对应 API Key 已配置
3. 所有 `ralph` 命令格式不变，Ralph 自动使用新执行器

## 协作记忆

任务完成后，简要记录：
- 做了什么改动
- 涉及的文件
- 未完成的事项（如有）

格式：
```
## [YYYY-MM-DD] multi-agent-dev 任务记录
- 任务：<简述>
- 目录：<工作目录>
- 执行器：<ACTIVE_AGENT>
- 改动：<文件列表>
- Ralph 迭代：<N> 次
- 备注：<如有>
```
