# Git 与远程仓库配置向导（交互）

本文件供 Agent 在 **需要从零配置 Git、挂远程、或说明权限边界** 时 **Read**；日常检索/改笔记不必读。与 vault 根 `$V` 相关的命令一律写 `git -C "$V"`。

---

## 与 openclaw 仓库的关系（更新本 skill）

本 skill 文件位于 **openclaw 仓库**（例如 `.cursor/skills/obsidian-git-vault/`）时：

- 你在 **另一台机器或远端环境** 使用 openclaw：要先在 openclaw 目录执行 **`git pull`**（或等价同步），才能拿到最新的 `SKILL.md` / 本向导。
- **笔记 vault** 与 **openclaw 代码仓** 是两个不同的 Git 仓库，不要混用路径；配置远程时始终明确当前终端所在目录是 `$V` 还是 openclaw 根。

向用户说明时一句话即可：**「skill 随 openclaw 更新；笔记库单独 `git pull`。」**

---

## 向导触发条件

在以下情况走本向导（按步执行、逐步向用户确认结果）：

- 用户要「把笔记推到 GitHub / 配远程 / 克隆下来的库怎么同步」；
- `git -C "$V" rev-parse --is-inside-work-tree` 失败，或 `remote -v` 为空且用户要云端备份；
- 用户问 HTTPS 还是 SSH、token 权限、会不会太危险。

---

## 使用前：向用户提示的最小配置

进入本向导、**尚未开始执行具体 Git 命令前**，先用几句话告知用户：笔记库要正常工作，**需要用户明确提供或确认的只有下面两项**；**其它一律用本 skill 默认**（见主 [SKILL.md](SKILL.md)：vault 路径解析顺序、约定默认目录、`init-default-vault.sh` 写入的内置 `.gitignore`、[scripts/vault-sync.sh](scripts/vault-sync.sh) 的远程名默认 `origin` 等）。

**必须由用户配置（或确认已配置）的：**

1. **`user.name` 与 `user.email`**（提交身份）：可在 vault 根执行  
   `git -C "$V" config user.name "…"`、`git -C "$V" config user.email "…"`，或使用 `git config --global …`；以用户选择为准。
2. **远程仓库**：托管平台上的仓库地址（SSH 或 HTTPS），以及本地 remote 名称；**未特别说明时 remote 名称为 `origin`**，执行 `git remote add origin <url>` 即可。

**在用户确认「其余用默认」时 Agent 的行为：**

- 不额外追问分支命名规范、合并策略偏好、是否 rebase 等，除非执行时报错需要用户决定。
- vault 路径、`gitignore` 模板、同步脚本、openclaw 定时表达式等，均按 SKILL 与 [vault-sync-sop.md](vault-sync-sop.md) 已有默认，**不在向导里逐项展开**。

---

## 第 0 步：确认操作对象

1. 用前文规则解析 **vault 根** `$V`（`OBSIDIAN_VAULT` / 用户给定 / 工作区含 `.obsidian` / 已存在的 `~/.openclaw/workspace/obsidian-git-vault`）。
2. 向用户确认：**「以下 Git 命令均在笔记库目录执行：`<$V>`」**；若用户实际想操作的是 openclaw 仓库，改用 openclaw 根路径，并说明与 vault 不同。

---

## 第 1 步：检测是否为 Git 仓库

在 `$V` 执行：

```bash
git -C "$V" rev-parse --is-inside-work-tree 2>/dev/null && echo OK || echo NO_REPO
```

| 结果 | 动作 |
|------|------|
| `OK` | 进入第 2 步（身份与状态）。 |
| `NO_REPO` | 询问用户是否 **`git init`**；仅当用户同意时执行 `git -C "$V" init`，然后进入第 2 步。 |

**禁止**在未确认 `$V` 时初始化，避免在错误目录创建 `.git`。

---

## 第 2 步：身份与干净状态

1. 检查提交身份（无则提醒用户自行设置，不替用户编造）：

```bash
git -C "$V" config user.name
git -C "$V" config user.email
```

若为空：提示用户在 `$V` 或全局设置：

```bash
git -C "$V" config user.name "显示名"
git -C "$V" config user.email "邮箱"
```

2. 看工作区：`git -C "$V" status -sb`。若有未提交修改且用户即将改远程 URL 或首次 push，提醒先 **commit 或 stash**，避免与后续操作混淆。

---

## 第 3 步：检测远程

```bash
git -C "$V" remote -v
```

| 情况 | 动作 |
|------|------|
| 已有 `origin`（或其它名）且 URL 正确 | 进入第 5 步（权限与协议）；用户若仅要同步，可直接 `fetch`/`pull`/`push`（第 6 步）。 |
| 无远程，用户要关联 GitHub/GitLab | 进入第 4 步。 |
| URL 错误需更换 | 用户确认后 `git -C "$V" remote set-url <名称> <新 URL>`。 |

---

## 第 4 步：添加远程仓库

1. 请用户提供 **HTTPS 或 SSH** 克隆地址（示例：`git@github.com:user/repo.git` 或 `https://github.com/user/repo.git`）。
2. 添加（名称默认 `origin`，若已占用则用用户指定名）：

```bash
git -C "$V" remote add origin <url>
```

已存在同名远程时：**不要**盲目 `add`；改用 `set-url` 或先 `remote remove`（需用户确认）。

3. 验证：`git -C "$V" remote -v`。

---

## 第 5 步：协议选择与权限收敛

### 5.1 SSH（推荐长期自用）

- **凭据形态**：本机 `~/.ssh/id_ed25519`（或 rsa）公钥登记到 GitHub/GitLab。
- **权限收敛**：密钥 **只加在个人账户**，仓库用 **私有** 若笔记敏感；Deploy Key 仅绑定单一仓库、只读或读写按需要选。
- **Agent 说明要点**：私钥不出库、不贴进聊天；远程 URL 用 `git@host:...`，不要在笔记仓提交任何密钥文件。

### 5.2 HTTPS + PAT（Personal Access Token）

- **权限收敛（GitHub 示例）**：勾选 **repo**（私有库读写）即可；**不要**勾选 `delete_repo`、workflow、整账户 admin，除非用户明确需要。
- **GitLab**：`write_repository` / `read_repository` 按私有与只读需求选最小集。
- **存储**：用系统钥匙串 / `git credential` / `gh auth`，**不要**把 token 写入仓库内 `.env` 或笔记；若必须落盘，路径加入 `.gitignore` 且永不提交。

### 5.3 与 Cursor / Agent 执行环境

- 终端执行 `git push`/`pull` 可能需 **网络权限**；认证失败时提示用户在本机终端或已登录的 `gh`/`glab` 重试，而非在对话里索要密码全文。

---

## 第 6 步：首次跟踪与同步

1. 取远程引用：`git -C "$V" fetch origin`（或用户指定的远程名）。
2. 若本地无提交、远程有默认分支：按用户意图 **`git pull origin main`**（或 `master`，以远程为准）或先建立初始提交再拉取；**有冲突**时列出冲突文件，指导解决标记后 `add` + `commit`。
3. 首次推送当前分支并设上游：

```bash
git -C "$V" push -u origin HEAD
```

分支名以 `git branch --show-current` 为准。

4. 若远程为空仓库：用户先本地 `commit` 再 `push -u`；必要时说明 **空仓库无默认分支** 的提示属正常。

---

## 第 7 步：收尾话术（给用户）

- **更新 skill**：openclaw 侧改动后需 **`git pull`** openclaw 仓库；与 vault 的 `pull` 分开操作。
- **日常笔记同步**：`status` → `add`/`commit` → `push`；拉取协作前先 `pull`。
- **权限**：能 SSH 就不用宽 scope PAT；PAT 能私有 `repo` 就不开整站权限。

---

## Agent 自检清单（执行前扫一眼）

- [ ] 当前 `$V` 是用户确认的笔记库根，不是 openclaw 根（除非用户明确要求操作 openclaw）。
- [ ] 未在仓库中创建含 token/私钥的文件。
- [ ] `init` / `remote add` / `push --force` 均有用户明确同意。
- [ ] 失败时给出 **认证失败 / 无权限 / 冲突** 三类之一的原因方向，不重复索要敏感信息全文。
