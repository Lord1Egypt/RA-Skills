# Hook Engine — 事件驱动的行为守卫系统

> 借鉴 Claude Code Hook 系统，为 OpenClaw 提供可配置的事件拦截与行为守卫。

## 事件类型

| 事件 | 触发时机 | 输入数据 |
|------|----------|----------|
| `PreExec` | exec 命令执行前 | `{command, workdir, env}` |
| `PostExec` | exec 命令执行后 | `{command, exitCode, stdout, stderr, duration}` |
| `PreMessage` | 消息发送前 | `{content, channel, target}` |
| `PostMessage` | 消息发送后 | `{content, channel, messageId, status}` |
| `Stop` | 会话结束前 | `{session, reason, summary}` |

## 规则引擎

规则定义在 `rules/` 目录下，每个 `.md` 文件包含：

```yaml
---
name: rule-name
enabled: true
event: PreExec          # 绑定的事件类型
matcher: "rm -rf"       # regex 匹配模式（支持多行）
action: block           # allow | warn | block | log
priority: 10            # 数字越大优先级越高
---
```

规则 body 部分定义：
- 匹配条件的详细说明
- 触发后的提示消息
- 豁免条件（白名单）

## 动作类型

- **allow**：放行，记录日志
- **warn**：放行但输出警告信息
- **block**：阻止执行，返回拒绝原因
- **log**：仅记录，不影响流程

## Hook 脚本规范

所有 hook 脚本位于 `hooks/` 目录：

1. 从 stdin 读取 JSON 事件数据
2. 加载 `rules/` 下匹配的规则
3. 按优先级逐条评估
4. 输出 JSON 结果到 stdout：

```json
{
  "decision": "allow|warn|block",
  "message": "人类可读的说明",
  "matched_rules": ["rule-name-1"],
  "timestamp": "2026-06-26T22:00:00Z"
}
```

## 与 daily-agent 集成

在 daily-agent 调度流程中嵌入 hook 检查点：

```
用户消息 → daily-agent 分类
  → [PreMessage hook] 验证消息格式
  → 任务执行
    → [PreExec hook] 每次 exec 前检查
    → [PostExec hook] 每次 exec 后记录
  → [PostMessage hook] 发送前验证
  → [Stop hook] 会话结束清理
```

集成方式：daily-agent 在关键节点调用对应 hook 脚本，根据返回的 `decision` 决定是否继续。

## 使用方法

### 添加新规则

在 `rules/` 下创建 `.md` 文件，按 YAML frontmatter 格式定义：

```yaml
---
name: no-format-disk
enabled: true
event: PreExec
matcher: "format|diskpart|chkdsk"
action: block
priority: 100
---
禁止执行磁盘格式化操作。此规则不可豁免。
```

### 禁用规则

将 `enabled` 设为 `false`，或删除对应规则文件。

### 查看已触发记录

所有 hook 触发记录写入 `memory/hook-audit.log`，格式：

```
[timestamp] [event] [decision] [rule] message
```

## 文件结构

```
hook-engine/
├── SKILL.md                    # 本文件
├── hooks/
│   ├── pre-exec-check.sh       # 执行前安全检查
│   ├── post-exec-log.sh        # 执行后日志记录
│   └── pre-message-format.sh   # 消息格式验证
├── rules/
│   ├── security-rules.md       # 安全规则集
│   └── format-rules.md         # 格式规则集
└── references/
    └── hook-api.md             # Hook API 完整文档
```
