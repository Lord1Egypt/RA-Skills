# openclaw-git-manager

**给 OpenClaw 配置文件装上 git 版本控制。**

---

## 一句话

每次改配置都自动记录 diff，改崩了可以一键回滚，再也不用"我不知道改了什么导致坏了"。

---

## 解决了什么问题

你在 OpenClaw 里改了配置，过了一周发现某个功能不 work 了，但你：
- 不记得改了什么
- 不记得是什么时候改的
- 只能一个个试

这个技能把你的 `openclaw.json`、`credentials/`、`agents/` 等配置文件全部纳入 git 版本控制，每次变更都有记录、可比较、可撤销。

---

## 核心功能

| 命令 | 作用 |
|------|------|
| `commit` | 一键提交当前配置状态，自动生成 key 级别的 diff 说明 |
| `log` | 查看历史提交，每条都说明"什么文件、什么变化" |
| `diff` | 比较任意两个版本之间的差异 |
| `restore <hash>` | 回滚到指定版本，自动验证 + 提示重启 |
| `undo` | 撤销上次 restore 操作 |

---

## 安全保证

- **Credentials 自动 redact**：真实 API key 永远不进 git 提交，commit 里只显示 `[REDACTED-api-key]`
- **敏感文件隔离**：日志、媒体、记忆文件完全不跟踪
- **完整 audit trail**：`.secrets-log.json` 记录每次 redact 的时间、文件、类型

---

## 使用示例

```
# 第一次使用
python3 git_manager.py init

# 每次改配置后
python3 git_manager.py commit
# → 自动显示 diff 说明，比如：
#   ~agent:main:dashboard.estimatedCostUsd: 0.066 → 0.005

# 出问题了回滚
python3 git_manager.py log          # 找到好用的版本
python3 git_manager.py restore a1b2c3d  # 回滚
# → 自动跑 openclaw doctor 验证，告诉你下一步做什么
```

---

## 安装

将此技能目录放入 `~/.openclaw/workspace/skills/` 即可。

触发词：`commit the config` / `save this version` / `what changed` / `restore` / `rollback` / `git manager`

---

MIT License · Author: wangjipeng