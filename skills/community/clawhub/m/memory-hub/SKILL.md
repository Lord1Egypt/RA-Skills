---
name: memory-hub
description: |
  Multi-agent shared memory protocol. Syncs a shared GitHub repo containing USER.md (owner preferences/habits), KNOWLEDGE.md (common knowledge), RULES.md (universal agent rules), and TOOLS.md (shared tools/scripts) across multiple agents. Supports read, write, sync, search, merge operations. Use when reading shared memory, writing new preference/knowledge to shared repo, syncing local cache with shared repo, searching shared memory, or first-time install/setup. Triggers: 读共享记忆, 写入共享记忆, 记录偏好, 同步记忆, 查共享记忆, shared memory, install memory-hub.
---

# shared-memory

多龙虾共享记忆同步协议。所有 agent 通过同一个 GitHub 私有仓库共享对主人的认知，每只 agent 本地维护一份轻量摘要缓存。

## 首次安装

运行安装脚本（幂等，重复执行安全）：

```bash
bash ~/.openclaw/skills/shared-memory/scripts/install.sh
```

脚本会：
1. 询问共享仓库地址（如未配置）
2. Clone 到 `~/.openclaw/shared-memory/`
3. 生成本地缓存文件 `~/.openclaw/workspace/SHARED_MEMORY_CACHE.md`
4. **提示用户确认**后，在 AGENTS.md 的 `## Every Session` 区块追加读取指令

安装完成后告知用户，并说明需要在其他龙虾上重复执行同样步骤。

## 配置文件

安装后配置存储在 `~/.openclaw/shared-memory/config.json`：
```json
{
  "repo_url": "https://github.com/your-username/shared-memory",
  "local_path": "~/.openclaw/shared-memory",
  "agent_id": "agent-home",
  "last_sync": "2026-01-01T00:00:00"
}
```

## 共享仓库结构

```
shared-memory-repo/
├── USER.md        # 主人偏好、习惯、沟通方式
├── KNOWLEDGE.md   # 公共知识沉淀：踩坑、工具用法、最佳实践
├── RULES.md       # 所有龙虾通用铁律
└── TOOLS.md       # 公共工具：脚本、命令、配置
```

每条记忆格式（严格遵守，不得自由发挥）：
```markdown
## [分类] 标题

内容（1-5行，精炼）

_更新：YYYY-MM-DD by agent_id_
```

## 支持的操作

### read — 读取共享记忆
```
触发词：读共享记忆、同步记忆、load shared memory
```
步骤：
1. `git -C ~/.openclaw/shared-memory pull --rebase --quiet`
2. 读取四个文件内容到上下文
3. 告知用户"已加载共享记忆（最后更新：XXX）"

### write — 写入新记忆
```
触发词：写入共享记忆、记录偏好、记住这个
```
步骤：
1. 判断写入目标文件（USER/KNOWLEDGE/RULES/TOOLS，见分类指南）
2. `git -C ~/.openclaw/shared-memory pull --rebase --quiet`
3. grep 检查是否已有相似条目（有则更新，无则追加）
4. 按格式追加/更新内容
5. `git -C ~/.openclaw/shared-memory add -A && git commit -m "🧠 [agent_id] 更新 FILE.md: 一句话描述" && git push`
6. 同步更新本地 `SHARED_MEMORY_CACHE.md` 摘要

push 失败时：`git pull --rebase` 后重试一次；仍失败则告知用户，不强制。

### sync — 定期同步（静默）
```
触发词：心跳时自动检查、sync shared memory
```
步骤：
1. pull 最新内容
2. 对比本地缓存的 last_sync 时间戳
3. 有更新则重新提炼摘要写入 `SHARED_MEMORY_CACHE.md`
4. 更新 config.json 的 last_sync
5. 静默完成，无需告知用户（除非发现重要新内容）

### search — 检索
```
触发词：查共享记忆 + 关键词
```
步骤：
1. pull 最新
2. `grep -r "关键词" ~/.openclaw/shared-memory/ --include="*.md" -l -n`
3. 返回匹配的段落（上下文各2行）

### merge — 合并到本地缓存
```
触发词：更新本地缓存、merge shared memory
```
步骤：
1. pull 最新内容
2. 提炼四个文件的核心要点（每个文件不超过20条）
3. 覆盖写入 `SHARED_MEMORY_CACHE.md`
4. 告知用户"本地缓存已更新，共 X 条摘要"

## 分类指南

| 内容类型 | 写入文件 |
|---|---|
| 主人的偏好、习惯、沟通风格 | USER.md |
| 工具用法、踩坑经验、最佳实践 | KNOWLEDGE.md |
| 所有龙虾必须遵守的行为规范 | RULES.md |
| 可复用脚本、命令、配置片段 | TOOLS.md |

## 写入原则（防垃圾堆积）

1. **去重优先**：写入前必须 grep 检查，有相似条目则更新不新增
2. **精炼不冗余**：每条记忆 1-5 行，不写流水账
3. **分类准确**：按上表分类，不得新增文件
4. **标注来源**：每条末尾标注更新时间和 agent_id

## 升级路径

当单文件超过 200 行时，主动提示用户考虑升级。
详见 `references/upgrade-guide.md`。

## 注意事项

- **不支持**：删除条目、修改文件结构、新增文件
- **不支持**：自由编辑，所有操作必须通过上述5个命令
- 共享仓库建议设为 **Private**（含个人隐私）
- 各龙虾的专属上下文（本地任务、环境配置）仍存各自的 MEMORY.md，不写入共享仓库
