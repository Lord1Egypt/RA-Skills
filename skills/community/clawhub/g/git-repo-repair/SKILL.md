---
name: git-repo-repair
description: "Repair a broken git repository: bad object HEAD, broken ref chains, committing working-tree changes. Backup, rebuild refs and index, then resurrect commits. Produces HEAD + fsck/status verification."
---

# git 仓库修复与工作树提交

用于：主人说「git 坏了 / bad object HEAD / 引用链断了 / 把工作树里未提交的先提交了」；或勘察中发现 git 引用链断、而主人已授权动手修。
产出：**恢复后的 HEAD（哈希可逐字节比对）+ 工作树提交结果 + 复核证据（fsck / status / log）+ 未做的不可逆动作清单**。
（只读勘察走 `repo-orientation` 及其 `references/git-state-triage.md`；工作区文件冗余清理走 `workspace-declutter`；发版走 `clawhub-skill-release`。）

## 步骤

1. **先只读分诊，判定「引用坏」还是「对象丢」**
   `git -C <root> log --oneline -3`（报 `bad object HEAD` 即引用链断）、`git -C <root> fsck --no-progress`、`git -C <root> cat-file -t <sha>` 逐个试候选锚点。
   `fsck` 里 `invalid sha1 pointer` 与 `missing blob` **同时出现** ⇒ commit 对象本身不在库里（不只是指针写错）。
   完成判据：一句话说出「坏在哪个 ref / 对象是否真丢 / 候选锚点是谁」。

2. **验「对象丢」不等于「内容丢」——先算工作区文件的哈希**
   对每个 missing blob 的同名工作区文件跑 `git hash-object <path>`；哈希相同 ⇒ 内容完好，恢复只需把 blob 重新写回对象库。
   完成判据：每个 missing blob 都有「工作区有同哈希副本」或「确实不可得」的结论。

3. **动手前备份 `.git` 三件套**
   `cp -a .git/refs/heads/<branch> .git/packed-refs .git/index /tmp/<name>-git-backup/`
   理由：旧 `.git/index` 里的 `cache-tree` 是重建丢失的树的**唯一依据**。

4. **先接引用，再重建索引（顺序不可反）**
   `git update-ref refs/heads/<branch> <完整的父提交>` → `rm .git/index && git read-tree HEAD`
   注意：索引里含失效 blob 时 `git reset --mixed HEAD` 会报 `unable to read <sha>` 而失败，必须删索引重读。

5. **重建缺失 blob 与丢失的树**
   `git hash-object -w <file>` 逐个写回缺失 blob；用备份索引 `GIT_INDEX_FILE=<备份index> git write-tree` 得到丢失 commit 的树哈希。
   检查：算出的树哈希与 fsck 报的 `invalid sha1 pointer in cache-tree` 那个哈希一致 ⇒ 找对了。

6. **用完整 message + reflog 元数据重建 commit，目标是哈希完全一致**
   完整 commit message（含正文）在 `.git/COMMIT_EDITMSG` —— reflog 只有标题行；author/committer 姓名邮箱时间戳在 `.git/logs/HEAD` 最后一行。
   `GIT_AUTHOR_NAME=… GIT_AUTHOR_DATE="<epoch> +0800" GIT_COMMITTER_NAME=… GIT_COMMITTER_DATE="<epoch> +0800" GIT_COMMITTER_EMAIL=… git commit-tree <tree> -p <parent> -F .git/COMMIT_EDITMSG`
   **验收判据：重建出的哈希必须与丢失的哈希完全相同。** 不相同 = 元数据还没找全（常见缺 message 正文或时间戳），继续找，**不要改成一个新 commit 顶上** —— 新 commit 会丢原作者与原时间戳，审计链断在假提交上。

7. **提交工作树前先判「改动是不是就是那个丢失的 commit」**
   若工作区 tracked 改动的哈希与丢失 commit 的 blob 哈希一致 ⇒ 它**已随复活的 commit 入库**，不要另造 commit。
   完成判据：`git status` clean，且 `git log` 顶部就是那个 commit。

8. **同步进来的文件先补回执行位，再看 diff**
   从 Windows 或其它副本同步进工作区的文件会丢执行位 ⇒ `git status` 出现整片 `100755 => 100644` mode 差异，脚本里 `exec ./bin/x` 直接报「权限不够」。
   先 `chmod +x` 恢复原权限，mode 差异即消失；**否则会把纯 mode 噪声当成内容改动报告并提交进去**。
   完成判据：diff 里不再有 mode-only 行。

9. **临时探针文件本地排除，不入库**
   自述「用完即删」、硬编码本机绝对路径（如 `/root/...`）的诊断测试文件在 CI 上必失败 ⇒ 写 `.git/info/exclude`（不污染仓库的 `.gitignore`），文件留在工作区继续可用。

10. **清理失效 worktree 并复核**
    `git worktree prune` 清掉目录已不存在的 worktree 记录；`git fsck --no-progress` 复核；`git status --short` 应为空。
    完成判据：fsck 只剩无害 dangling 对象。

11. **报告写清四件**：恢复前后的 HEAD 哈希、是否逐字节一致、工作树是否还有未提交内容、**未执行的不可逆动作**（push / gc / reflog expire / 清空回收站）由主人拍板。

## 陷阱

- **文件时间戳不等于代码版本**：判断二进制新旧读内嵌 `grep -ao 'vcs\.revision=[0-9a-f]+' <binary>`，不要看 mtime（实测根目录副本 mtime 更晚却构建自更旧的 commit）。
- **`git --index-file=…` 不是合法 git 全局选项**：用环境变量 `GIT_INDEX_FILE=<路径>`。
- **手写 `-m` 短 message 重建 commit 必然哈希不等**：完整 message 只在 `COMMIT_EDITMSG`。
- **`.git/index` 的 cache-tree 是重建丢失树的唯一依据**：删索引前先备份，删了就再也算不出那棵树。
- **HEAD 悬空时「最近一次提交是 X 天前」不可信**：日期结论要等引用链体检完再给。
- **执行位缺失在部署时才暴露，不在 diff 里**：`chmod +x` 还原后再判断 diff 是内容改动还是只有权限差异。
- **push / gc / reflog expire / 清空回收站都是不可逆动作**：本 skill 只做本地可逆恢复，这些一律列给主人。

## 边界

- 不 push、不打 tag、不发版。
- 不 gc、不 reflog expire、不删 `.git` 内文件。
- 备份放 `/tmp`，不在工作区里留备份副本。
