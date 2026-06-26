---
name: memory-backup-skill
description: 记忆备份与跨渠道同步技能。用于：（1）将对话中的重要内容自动写入记忆文件；（2）跨渠道同步记忆；（3）通过 Git 推送到远程仓库备份；（4）工作流文档的存储与恢复。当用户说"把这段内容存进记忆"、"帮我记住"、"备份记忆"、"同步记忆"、"从备份恢复"时触发。也可在每次重要对话结束时主动沉淀记忆。
---

# Memory Backup Skill

## 核心能力

1. **记忆写入** — 把对话中的重要信息提炼后写入 `memory/YYYY-MM-DD.md` 或对应渠道目录
2. **跨渠道同步** — 把一个渠道的上下文同步到其他渠道的记忆分区
3. **工作流备份** — 把成熟工作流存入 `memory/workflows/`，换机器后立即可用
4. **Git 备份** — 将记忆文件推送到远程 Git 仓库，支持换机器或重装后恢复

## 安全特性

- `memory-sync.sh` 拒绝绝对路径和目录遍历（`..`），防止读取系统文件
- 同步前扫描敏感内容（私钥、密码、AWS key），发现即拒绝
- `.gitignore` 自动排除 `*.key`、`*.pem`、`credentials*`、`TOOLS.md` 等敏感文件
- `memory-backup.sh` 交互确认后才推送，避免误操作

## 必需环境变量

| 变量 | 说明 | 示例 |
|------|------|------|
| `GIT_REMOTE` | Git 远程仓库地址 | `git@gitee.com:you/memory.git` |
| `MEMORY_BACKUP_KEY` | SSH 私钥路径 | `~/.ssh/memory_backup_key` |
| `WORKDIR` | 工作目录（可选） | `/root/.openclaw/workspace` |

## 记忆写入流程

当用户要求"记住"、"存进记忆"、"同步这段"时，执行：

1. **提炼** — 从对话中提取：关键事实、决策结论、下一步、项目状态
2. **判断渠道**
   - 跨渠道通用内容 → `memory/core/` 或 `memory/projects/`
   - 渠道私有内容 → `memory/channels/<当前渠道>/`
   - 当日核心上下文 → `memory/YYYY-MM-DD.md`
3. **写入文件** — 追加到目标文件（注意不覆盖已有内容）
4. **触发备份** — `bash scripts/memory-backup.sh`

## 工作流存储

成熟工作流是核心资产，统一存放在：

```
memory/workflows/<领域>-<名称>.md
```

示例：
- `memory/workflows/wechat-publish-workflow.md` — 微信公众号发布工作流
- `memory/workflows/cloudbase-deploy-workflow.md` — CloudBase 部署工作流

工作流文档结构建议包含：适用场景、前置准备、步骤、注意事项、相关记忆。

**备份时必须同步清理旧版**：
把工作流写入 `memory/workflows/` 时，必须检查并清理以下旧位置可能存在的同名文件：
- `memory/<名称>-workflow.md`
- `docs/<名称>-workflow.md`
- `docs/<名称>.md`

原则：有新版则删旧版，避免同名文件造成混乱。详见 [references/workflows.md](references/workflows.md)

**恢复时**：开新对话后说"从备份继续，我是自媒体创作者，用微信公众号工作流发文章"，龙虾读取 `memory/workflows/wechat-publish-workflow.md` 后即可按流程执行，无需重新解释。

## 跨渠道同步

把 A 渠道的结论同步到 B 渠道：

```bash
# 自动同步（由 AI 代理执行）
bash scripts/memory-sync.sh <相对路径文件>

# 安全限制：
#   - 不接受绝对路径（如 /tmp/file.md）
#   - 不接受目录遍历（如 ../etc/passwd）
#   - 内容含私钥、密码、AWS key 等敏感词时拒绝同步
```

## 备份操作

```bash
# 手动触发备份（交互确认）
bash scripts/memory-backup.sh

# 预期输出： [memory-backup] 备份已推送：memory-backup: 2026-04-29 09:00:00 +0800
```

## 初始化配置（首次使用）

1. **建立 Git 仓库**
   ```bash
   # 在 Gitee/GitHub 创建私有仓库，例如 openclaw-memory
   # 添加 SSH 公钥到 Git 平台
   ```

2. **配置环境变量或修改脚本**（在 `scripts/memory-backup.sh` 开头）
   ```bash
   GIT_REMOTE="git@your-gitrepo:yourname/openclaw-memory.git"
   MEMORY_BACKUP_KEY="~/.ssh/your_backup_key"
   ```

3. **生成专用 SSH 密钥（推荐）**
   ```bash
   ssh-keygen -t ed25519 -C "openclaw-memory-backup" -f ~/.ssh/memory_backup_key
   # 把公钥添加到 Git 平台
   ```

4. **测试备份**
   ```bash
   bash scripts/memory-backup.sh
   ```

详细步骤见：[references/setup-guide.md](references/setup-guide.md)

## 恢复与迁移

换机器或重装后：
```bash
git clone git@your-gitrepo:yourname/openclaw-memory.git /root/.openclaw/workspace
cd /root/.openclaw/workspace && bash scripts/memory-backup.sh  # 验证
```

## 记忆文件参考

| 文件 | 用途 | 读取范围 |
|------|------|---------|
| `MEMORY.md` | 长期核心记忆 | 仅主会话 |
| `memory/YYYY-MM-DD.md` | 每日日记 | 所有渠道 |
| `memory/core/` | 跨渠道共享能力/经验 | 所有渠道 |
| `memory/workflows/` | 成熟工作流（重要资产） | 所有渠道 |
| `memory/channels/<渠道>/` | 渠道私有上下文 | 该渠道专属 |
| `memory/projects/` | 项目记忆 | 所有渠道 |

详细说明见：[references/memory-structure.md](references/memory-structure.md)

## 敏感信息原则

- **不写入**实际 API 密钥、密码、Token
- **只写**配置位置、状态、是否需要轮换
- 示例：`TOOLS.md` 中写"某服务 key 在 X 位置，状态：未轮换，需定期检查"
- `memory-sync.sh` 会自动扫描并拒绝包含敏感模式的文件

## 常见触发场景

- 用户说"记住"、"帮我存一下"、"写进记忆"
- 重要对话结束前，AI 主动沉淀
- 用户问"之前那个项目的进度是什么"（先查记忆再回答）
- 换机器/重装后恢复："从备份记忆继续"
- 完成了一个成熟工作流："把这个发布流程存进工作流记忆"
