# cron-setup — gitea-workflow cron 配置参考

> 本文档是给**各 agent 自己**配置循环 cron 用的参考。
> SKILL.md 只约定使用方式,不写死具体 cron ID / agent 名 / repo 名。

## 通用 cron 模板

### Implementer(各具体角色: programmer/designer/tester/author/artist/...)

```yaml
name: gitea-workflow-<role>      # 如 -programmer / -designer / -tester
schedule:
  kind: cron
  expr: "*/20 * * * *"               # 每 20 分钟(可在 15-30 调整)
  tz: Asia/Shanghai
sessionTarget: session:agent:<role>:feishu:group:<your-group-id>
payload:
  kind: agentTurn
  message: |
    [gitea-workflow loop wake]
    执行 SKILL: gitea-workflow (Implementer 循环)
    1. 拉取分配给你的 issue
    2. 推进 / 完成 / 阻塞 三选一
    3. 完成后群里 @<coordinator-name> 告知
delivery:
  mode: none                         # 默认不投递到群(只在完成时主动发)
```

### Coordinator(各具体角色: producer / team-lead / pm / lead-editor / ...)

```yaml
name: gitea-workflow-<role>
schedule:
  kind: cron
  expr: "*/45 * * * *"               # 每 45 分钟(可在 30-60 调整)
  tz: Asia/Shanghai
sessionTarget: session:agent:<role>:feishu:group:<your-group-id>
payload:
  kind: agentTurn
  message: |
    [gitea-workflow loop wake]
    执行 SKILL: gitea-workflow (Coordinator 循环)
    1. 拉所有 open issue + 新评论
    2. 审阅 + 回复 + 推进
    3. 阶段切换才发群
delivery:
  mode: none
```

## 创建命令(参考)

```bash
# 用 openclaw cron add
openclaw cron add \
  --name gitea-workflow-programmer \
  --cron "*/20 * * * *" \
  --tz Asia/Shanghai \
  --session "session:agent:programmer:feishu:group:oc_xxx" \
  --message "<payload 内容>"
```

或者用 JSON / YAML 文件:

```bash
openclaw cron add --from-file /path/to/cron-config.yaml
```

## 周期调优

| 周期 | 适用场景 |
|------|----------|
| 5-10 分钟 | 高优先级 issue / 阻塞状态 |
| **15-30 分钟** | **默认 Implementer 循环**(推荐) |
| 30-60 分钟 | Coordinator 循环 |
| 1-2 小时 | 低活跃期(夜间、周末) |

观察 token 消耗 + 实际响应速度调优。

## Loop on/off

用 SKILL.md 里 `scripts/loop-on.sh` / `loop-off.sh`:

```bash
# 开
~/.openclaw/skills/gitea-workflow/scripts/loop-on.sh

# 关
~/.openclaw/skills/gitea-workflow/scripts/loop-off.sh

# 看状态
~/.openclaw/skills/gitea-workflow/scripts/status.sh
```

或在 openclaw cron CLI 直接操作:

```bash
openclaw cron update --name gitea-workflow-programmer --enabled false
openclaw cron update --name gitea-workflow-programmer --enabled true
```

## Gitea token 配置

每个 agent 自己管理 token(避免互相知晓),建议位置:

```
~/.config/gitea/token      (mode 600, owner = agent)
```

`status.sh` 默认读这个路径。可以用 `GITEA_TOKEN_FILE` 环境变量覆盖。

## 跨 session 持久化

agent loop wake 是新 session(每次 cron 触发)。新 session 需要从 issue 重新拉上下文,**不要假设**上次 session 的内存还有效。

设计原则:
- **issue 是 source of truth**
- agent 内存(本 session)只是工作 buffer
- 完成 / 阻塞 / 决策全部写回 issue 评论,跨 session 可读

## 工作室特定配置示例(占位符)

> 把 `<your-org>` / `<your-repo>` / `<your-role>` / `<your-group-id>` 替换成你自己的值。

```yaml
# Implementer 示例
name: gitea-workflow-<your-role>
sessionTarget: session:agent:<your-role>:feishu:group:<your-group-id>
# Implementer 在仓库: <your-org>/<your-repo>

# Implementer 示例 (另一角色)
name: gitea-workflow-<your-role-2>
sessionTarget: session:agent:<your-role-2>:feishu:group:<your-group-id>
# Role-2 在仓库: <your-org>/<your-repo-2>

# Coordinator 示例
name: gitea-workflow-coordinator
sessionTarget: session:agent:coordinator:feishu:group:<your-group-id>
# Coordinator 跨仓库: <your-org>/{<your-repo>, <your-repo-2>, <your-repo-3>, ...}
```
