# 工作区与模板参考

## 工作区位置
- 默认: `~/.openclaw/workspace`
- 配置文件模式: `~/.openclaw/workspace-<profile>`
- 覆盖: `agents.defaults.workspace` 或 `agent.workspace`
- 禁用引导: `agent.skipBootstrap: true`
- 引导截断: `agents.defaults.bootstrapMaxChars: 20000`

## 工作区文件映射
| 文件 | 用途 | 加载时机 |
|------|------|----------|
| `AGENTS.md` | 操作指南、规则、优先级 | 每个会话 |
| `SOUL.md` | 人设、语气、边界 | 每个会话 |
| `USER.md` | 用户信息、称呼 | 每个会话 |
| `IDENTITY.md` | 智能体名称、风格、emoji | 引导时创建 |
| `TOOLS.md` | 本地工具笔记(不控制可用性) | 每个会话 |
| `HEARTBEAT.md` | 心跳检查清单(可选) | 心跳时 |
| `BOOT.md` | 网关启动时执行(可选) | 网关启动 |
| `BOOTSTRAP.md` | 首次运行仪式(一次性) | 仅首次 |
| `MEMORY.md` | 长期记忆(仅主会话) | 主会话 |
| `memory/YYYY-MM-DD.md` | 每日日志 | 每个会话(今天+昨天) |
| `skills/` | 工作区级Skills | 自动发现 |
| `hooks/` | 工作区级Hooks | 自动发现 |
| `canvas/` | Canvas UI文件 | 节点显示 |

## 子智能体注入
子智能体仅注入 `AGENTS.md` + `TOOLS.md`（无SOUL/IDENTITY/USER/HEARTBEAT/BOOTSTRAP）

## 不在工作区中的内容
- `~/.openclaw/openclaw.json` — 配置
- `~/.openclaw/credentials/` — 凭证
- `~/.openclaw/agents/<id>/sessions/` — 会话记录
- `~/.openclaw/skills/` — 托管Skills

## Git备份(推荐)
```bash
cd ~/.openclaw/workspace
git init
git add AGENTS.md SOUL.md TOOLS.md IDENTITY.md USER.md HEARTBEAT.md memory/
git commit -m "Add workspace"
git remote add origin <private-repo-url>
git push -u origin main
```
⚠️ 不要提交密钥/凭证

## 迁移到新机器
1. 克隆仓库到目标路径
2. `agents.defaults.workspace` 指向该路径
3. `openclaw setup --workspace <path>` 填充缺失文件
4. 单独复制 `~/.openclaw/agents/<id>/sessions/`

## 默认模板内容

### AGENTS.md 核心结构
- 每个会话: 读SOUL.md → USER.md → memory/今天+昨天
- 主会话额外读MEMORY.md
- 记忆: 每日文件(memory/YYYY-MM-DD.md) + 长期(MEMORY.md)
- 安全: 不泄露私有数据，trash > rm

### SOUL.md 核心结构
- 真正有帮助(不是表演性的)
- 有自己的观点
- 先自己找答案再问
- 通过能力赢得信任
- 记住自己是客人

### BOOTSTRAP.md 流程
1. 确定名字、性格、emoji
2. 更新IDENTITY.md和USER.md
3. 讨论SOUL.md
4. 可选: 连接渠道
5. 完成后删除BOOTSTRAP.md

# Web UI 参考

## WebChat
```json5
gateway: { http: { endpoints: { webchat: { enabled: true } } } }
```
URL: `http://<host>:<port>/webchat`

## TUI (终端UI)
```bash
openclaw tui [--url <url>] [--token <token>]
```

## Control UI (macOS)
菜单栏应用内置控制面板: 会话、节点、配置、日志

## Dashboard
```json5
gateway: { http: { endpoints: { dashboard: { enabled: true } } } }
```
