---
name: obsidian-git-vault
description: >-
  在 Obsidian 库（Markdown + Git）内检索笔记、创建与管理 .md；用 Git 查看历史与提交变更，并管理远程与同步（fetch/pull/push）。
  当用户提及 Obsidian、vault、笔记检索、新建笔记、改笔记、移动重命名、Git、版本、提交、推送、拉取、远程、Git 初始化、配置 origin、SSH/HTTPS、token 权限、GitHub/GitLab 托管笔记库、vault 同步 SOP、定时同步时触发；需分步配置远程或权限说明时 Read git-remote-wizard.md；用户同意完整自动化同步工作流时 Read vault-sync-sop.md。
---

# Obsidian 库（Git）简易操作

以 **vault 根目录下的 Markdown 文件** 为真源；不依赖 Obsidian 应用 API。文件操作用 Glob、Grep、Read 与编辑工具；Git 操作用 `git -C "<vault>" ...`，且 **仅在该 vault 目录已是 Git 仓库时** 执行（用户要求 `git init` 时再初始化）。

## 0. 变更后是否走同步 SOP

- **用户已声明**采用「vault 同步 SOP」或同意安装后定时同步：每次对本 vault 的笔记 **创建/修改/移动/删除** 后，在同一轮对话中尽量按 [vault-sync-sop.md](vault-sync-sop.md) 执行第 1～3 步；定时任务（每 2h）仅在用户同意后在有 `openclaw` CLI 的环境尝试配置（详见该文件第 0 节）。
- **未声明**：日常仍可按第 5～6 节操作，**不**主动强推、不自动注册 cron。
- **能力边界**：Skill 不会在无用户同意时自行创建定时任务；`openclaw` 不可用则说明并停止。

## 1. 解析 vault 根目录（每次先定根）

按优先级取 **第一个有效** 的目录（须为已存在的目录；解析路径时把 `~` 展开为用户主目录）：

1. 环境变量 `OBSIDIAN_VAULT`（可在终端执行 `echo "$OBSIDIAN_VAULT"` 判断）。
2. 用户在本对话中给出的 **vault 绝对路径**（仅本对话内沿用，不写入其它文件除非用户要求）。
3. 当前 Cursor **工作区根目录**：若根下存在 `.obsidian` 目录，可视为 vault 根。
4. **约定默认目录**：`~/.openclaw/workspace/obsidian-git-vault`（即 `$HOME/.openclaw/workspace/obsidian-git-vault`）在磁盘上已存在时作为 vault 根。

若以上皆无效：向用户索要 vault 绝对路径，或说明可 `mkdir -p ~/.openclaw/workspace/obsidian-git-vault` 后作为默认库再操作。禁止把上述列表以外的路径当作默认去猜。禁止操作落在所选 vault 根以外的未授权路径（防路径穿越）。

下文记 `V="<vault 绝对路径>"`，命令统一写 `git -C "$V"`。

### 1.1 默认 `.gitignore`

不单独提供 `default.gitignore` 文件。新建库时运行 `bash "$SKILL_ROOT/scripts/init-default-vault.sh"`，若尚无 `$V/.gitignore` 会 **内联写入** 规则：系统杂项、`.env`/密钥、编辑器、可选用「不同步的」`.obsidian/workspace*.json`、`.trash/`、以及 **默认排除常见非文本附件**（图片/音视频/压缩包/Office/字体等）；若 vault 需把图片或 PDF 纳入 Git，删掉 `$V/.gitignore` 里对应段或改规则。

### 1.2 Bash 脚本（`scripts/`）

`SKILL_ROOT` 指含本 `SKILL.md` 的目录（openclaw 内多为 `.cursor/skills/obsidian-git-vault`）。优先用脚本代替手写长命令：

- `bash "$SKILL_ROOT/scripts/resolve-vault.sh"`：打印 `$V`；可传覆盖路径为第一个参数；支持 `OBSIDIAN_VAULT`、`CURSOR_WORKSPACE`、当前目录含 `.obsidian`、`~/.openclaw/workspace/obsidian-git-vault`（须已存在）。
- `bash "$SKILL_ROOT/scripts/init-default-vault.sh"`：创建默认目录、`git init`、缺省时写入内置 `.gitignore`（含非文本附件忽略，见 §1.1）；可选参数为目标目录，默认 `~/.openclaw/workspace/obsidian-git-vault`。
- `bash "$SKILL_ROOT/scripts/vault-sync.sh"`：干净工作区下 `fetch`、判断领先/落后/分叉并 `push` / `pull`；见脚本内 `--help`。接受 SOP 强推时设 `OBSIDIAN_SOP_FORCE_LEASE=1`；`OBSIDIAN_PULL_REBASE=1` 则落后时 `pull --rebase`。
- `bash "$SKILL_ROOT/scripts/list-conflicts.sh"`：列出合并冲突文件。
- `bash "$SKILL_ROOT/scripts/openclaw-cron-vault-sync.sh"`：在本机有 `openclaw` 时注册约每 2 小时任务（需用户事前同意）；可用环境变量改 `OBSIDIAN_CRON_EXPR` 等。

**冲突合并**仍以人工/Agent 编辑 Markdown 为主；脚本不自动改冲突正文。

## 2. 检索

- **按文件名**：在 vault 根下 `Glob`，如 `**/*.md` 或 `**/某目录/**/*.md`。
- **按正文 / 链接 / 标签**：在 vault 根下 `Grep`，可搜关键词、`[[`、`tags:`、`aliases:`、正文 `#tag` 等。
- **精读**：对命中列表再 `Read` 必要文件；回答中引用内容须来自已读文件，勿编造。
- **按 Git 历史**（用户要「谁改过 / 某文件历史」时）：`git -C "$V" log --oneline -n 20 -- path/笔记.md`，必要时 `git -C "$V" log -p -n 3 -- path/笔记.md`。
- `.obsidian` 下配置默认不当成「笔记正文」去搜，除非用户明确要求。

输出时列出 **相对 vault 的路径** 与简短命中说明即可。

## 3. 管理

### 3.1 修改

小步修改正文或 YAML frontmatter，保持 Markdown 与 frontmatter 语法有效。不大段重写用户未要求的内容。

### 3.2 移动与重命名

用 `git -C "$V" mv 旧路径 新路径`（已纳入 Git 跟踪时优先）或普通 `mv` 后再 `git add`。完成后：

- 对已知的 **旧文件名 / 旧路径**，在 vault 内 `Grep` 是否仍有 `[[旧名]]` 或旧相对链接。
- 向用户说明是否断链；若用户要求批量替换链接，再逐文件修改。**不**在未确认时大规模自动改链。

### 3.3 删除

仅当用户 **明确要求删除** 某文件时执行；恢复未提交删除可用 `git -C "$V" restore --staged 路径` / `git restore 路径`（按当时状态）。

## 4. 创建

- 路径与文件名由用户指定或按 vault 现有习惯（如 `inbox/`、`notes/`）；文件名避免非法字符，空格可保留或与用户约定用 `-`。
- 新建后若需纳入版本控制：`git -C "$V" add 路径`（用户要求提交时再与其它变更一起 `commit`）。
- 可选 YAML frontmatter，例如：`title`、`date`、`tags`；无模板时最小可用：

```yaml
---
title: 笔记标题
date: YYYY-MM-DD
tags: []
---
```

- 若需在索引/MOC 中挂链，仅在用户指定目标文件时向其中追加 `[[新笔记名]]`。

## 5. Git 版本控制（本地）

前提：`git -C "$V" rev-parse --is-inside-work-tree` 为真；否则仅在用户明确要求时 `git init`（初始化后提醒用户设置 `user.name` / `user.email` 若尚未配置）。

用户未要求时，不主动执行破坏性命令（见本节末）。

| 意图 | 典型命令（均在 `$V` 下） |
|------|---------------------------|
| 看工作区 | `git status` |
| 看未暂存差异 | `git diff`；看已暂存 `git diff --staged` |
| 暂存 | `git add 路径` 或 `git add -A`（用户确认范围后再用 `-A`） |
| 提交 | `git commit -m "说明"`；说明应简短、可辨（如 `note: 添加 xxx`、`note: 修改 xxx`） |
| 最近提交记录 | `git log --oneline -n 20` |
| 某文件历史 | `git log --oneline -- path` |
| 分支 | `git branch` / `git switch -c 新分支名`（用户要求时） |
| 暂存手头改动 | `git stash push -m "说明"`；恢复 `git stash pop` 或 `git stash apply` |
| 撤销未提交修改 | `git restore 路径`（丢弃工作区改动前需用户确认） |
| 取消暂存 | `git restore --staged 路径` |

**高风险**：`git reset --hard`、裸 `git push --force`、`git rebase` 等——默认仅用户 **逐字明确要求** 时执行。若用户 **已采用** [vault-sync-sop.md](vault-sync-sop.md)，则其中写明的「本地领先时推送 / `push --force-with-lease`」条件 **优先于** 本句的保守默认。

不要直接编辑 `.git` 目录内文件；不把 `.git` 当笔记检索。

## 6. 远程仓库与同步

前提：网络与认证由用户环境解决（SSH key、credential、GitHub CLI 等）；推送/拉取需 **full_network** 类权限时由用户在环境中授权。

| 意图 | 典型命令 |
|------|-----------|
| 查看远程 | `git -C "$V" remote -v` |
| 添加远程 | `git remote add origin <url>`（名称按用户习惯，不限于 `origin`） |
| 修改远程 URL | `git remote set-url origin <url>` |
| 删除远程 | `git remote remove 名称`（用户明确要求时） |
| 取回远程分支（不合并） | `git fetch origin` 或 `git fetch --all` |
| 与当前分支合并 | `git pull` 或 `git pull --rebase`（用户偏好 rebase 时再使用后者） |
| 推送到远程 | `git push`；**首次**跟踪上游：`git push -u origin 当前分支名` |
| 查看分支与跟踪关系 | `git branch -vv` |

合并冲突：默认提示冲突路径并手工清标记后 `git add`、`git commit`。若用户已采用 [vault-sync-sop.md](vault-sync-sop.md)，按其中 **第 3 节**（告警 + 按范围合并 Markdown）执行。

用户说「备份到 GitHub / 同步」时：先 `status`，再按需 `add`/`commit`，最后 `push`；若远程为空分支首次推送，可能需要 `-u`。

### 6.1 配置向导（检测 Git、远程与权限）

从零检测 Git、初始化、添加/修改远程、选择 SSH 或 HTTPS、**权限收敛**（最小 scope、不把密钥写进仓库），或说明 **openclaw 仓库拉取 skill** 与 **笔记 vault 单独 `git pull`** 的区别时：**Read** [git-remote-wizard.md](git-remote-wizard.md)：先按其中 **「使用前：向用户提示的最小配置」** 说明仅需 `user.name` / `email` 与 remote，其余默认；再按该文件分步与用户确认。远程已配置且只做日常同步时可不读。

## 7. 能力边界（本 skill 不含）

批量重构全库链接、Canvas（`.canvas`）自动改写、Dataview 查询执行、Obsidian 插件设置修改——有需求时再单独约定。已采用 `vault-sync-sop.md` 时合并策略以该文件为准，不与此条冲突。
