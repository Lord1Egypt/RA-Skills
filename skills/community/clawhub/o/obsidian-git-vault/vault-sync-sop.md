# 笔记库同步 SOP（工作流）

以下在 **用户明确同意采用本 SOP** 后执行；Agent 每次用本 skill **改动了 vault 内文件**（创建/修改/移动/删除）后，应在本轮对话末尾尽量走一遍 **第 1～3 步**（第 0 步的定时任务仅在意愿书与一次性配置时）。

---

## 0. 安装后告知与定时任务（openclaw）

**限制**：Skill 无法自行「安装」到系统；由 Agent **告知用户** 能力边界，并在用户 **书面同意** 后尝试用终端执行 openclaw CLI。若环境无 `openclaw` 或命令失败，说明原因并 **停止**，不反复重试。

1. 向用户说明：可配置 **每 2 小时** 触发一次「vault 同步检查」类任务；任务失败需用户查看 `openclaw cron runs <jobId>`（或等价），**本 SOP 不代替** openclaw 的失败自动熔断（按需由用户关闭/暂停任务）。

2. 用户同意后，在 **已配置好 openclaw 的环境** 中执行 skill 内脚本（可调参数，等价于下方手写命令）：

```bash
bash "<SKILL_ROOT>/scripts/openclaw-cron-vault-sync.sh"
```

或手写：

```bash
openclaw cron add \
  --name "obsidian-vault-sync" \
  --cron "0 */2 * * *" \
  --tz "Asia/Shanghai" \
  --session isolated \
  --message "按 obsidian-git-vault skill 的 vault-sync-sop.md 执行第 1～3 步同步检查；失败则向用户报告并停止，不要强推除非 SOP 条件满足且无错误。"
```

若 `openclaw cron add` 参数与现场 CLI 不同，以 `openclaw cron --help` 为准，保留 **2 小时间隔** 与 **明确引用本 SOP** 即可。

3. **失败则停止**：CLI 报错、无权限、无网络时，在一次尝试后停止并输出原文；不猜测成功。

---

## 1. 当前笔记 / 库是否存在

- 用主 [SKILL.md](SKILL.md) 第 1 节解析 `$V`。
- **若目标笔记路径在本地已存在**：进入第 2 步。
- **若不存在**：走 **默认库初始化**（用户未另指定时）：
  - `mkdir -p ~/.openclaw/workspace/obsidian-git-vault`（若缺则建）；
  - 将 `$V` 定在该目录；
  - `git rev-parse` 非仓库则 **`git init`**（用户同意时）；
  - 若无 `$V/.gitignore`，运行 `bash "<SKILL_ROOT>/scripts/init-default-vault.sh" "$V"` 或沿用其内置规则写入（见 SKILL §1.1）；
  - 再创建/写入用户要的笔记文件，按需 `git add` / `commit`。

---

## 2. 远程同步状态

前提：`git -C "$V" rev-parse --is-inside-work-tree` 为真。

**脚本优先**（工作区须无未提交变更；接受 SOP 强推时导出 `OBSIDIAN_SOP_FORCE_LEASE=1`）：

```bash
V="$(bash "<SKILL_ROOT>/scripts/resolve-vault.sh")"
export OBSIDIAN_VAULT="$V"
OBSIDIAN_SOP_FORCE_LEASE=1 bash "<SKILL_ROOT>/scripts/vault-sync.sh" "$V"
```

退出码：`vault-sync.sh` 中 `0` 已同步或完成 push/pull；`2` 分叉；`3` 无远程；`4` 无上游；`5` 有未提交文件；`10` pull 后仍存在冲突；其它见脚本 `--help`。

手写排查时：

1. `git -C "$V" remote -v`：**无远程** → **Read** [git-remote-wizard.md](git-remote-wizard.md)，指导配置后再回到本节。

2. `git -C "$V" fetch origin`（或当前上游远程名）；再看 `git -C "$V" status -sb` 与 `git -C "$V" log --oneline HEAD..@{u}`、`@{u}..HEAD`（无上游时先用 `git branch -vv` 确认是否需 `push -u`）。

3. 判定（同一分支、已设 upstream）：

| 情形 | 动作 |
|------|------|
| 与远程无提交差、工作区干净（或已 commit） | **停止** 同步操作（无需 push/pull）。 |
| **仅本地领先**（有本地提交未推送） | 在用户已同意本 SOP 前提下 **`git push`**；若远程因历史分歧拒绝，再按用户策略使用 **`git push --force-with-lease`**（优先于裸 `--force`）。 |
| **仅远程领先** | **`git pull`**（或用户偏好的 `git pull --rebase`）；随后处理冲突见第 3 步。 |
| **双方各有提交**（分叉） | 先向用户 **告警**；再拉取合并或 rebase；仍冲突则走第 3 步。 |

**说明**：与主 SKILL 中「强推需逐字确认」相比，**本文件优先级更高**——但仅当用户 **已声明采用本 SOP**。未采用时仍按 SKILL 保守规则。

---

## 3. 冲突处理（Obsidian 场景）

- **预设**：单文件同时编辑概率低，但仍 **先向用户告警**（列冲突路径与涉及提交）。
- **操作**：
  1. `bash "<SKILL_ROOT>/scripts/list-conflicts.sh"` 或 `git -C "$V" diff --name-only --diff-filter=U`，并阅读冲突文件中的 `<<<<<<<` 标记；
  2. **Read** 冲突全文，在笔记语义上 **合并为一版 Markdown**（可保留双方段落，用二级标题或 `---` 分隔），删掉冲突标记；
  3. `git add` 冲突文件，`git commit`（使用清晰说明如 `note: merge remote 与本地`）。
- 若冲突范围过大或涉及二进制/非笔记文件：**停止** 自动合并，请用户手工处理。

---

## Agent 自检

- [ ] 用户已同意采用本 SOP（含强推策略知情），再执行强推类命令。
- [ ] `$V` 为笔记库而非 openclaw 源码仓（除非用户明确要求操作后者）。
- [ ] 定时任务仅为「尝试配置」，失败不无限重试。
