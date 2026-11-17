---
name: infinity-context
description: "Use when a long agent session is about to hit its context limit, when a detail from an earlier turn must be recalled exactly, or when past sessions should stay searchable offline. Compresses context, archives conversation chunks into a local SQLite/FTS5 store with owner-only permissions and a bounded 30-day retention window, and retrieves exact details on demand. Ships explicitly opt-in maintenance tools that change local files: a retention cleanup that permanently deletes expired archive files (verified archive marker + filename allowlist + --confirm-destructive), an ingest-time retention purge with --purge-only, an INFINITY_CONTEXT_NO_ARCHIVE=1 off switch, and an in-place redaction helper that rewrites a file only inside a declared --allow-dir. Works out of the box on DeepSeek Harness (dsh) and OpenClaw; also runs on Claude Code, Cursor, Dify, Ollama and any Agent Skills host."
license: MIT
compatibility: "Any host that loads a standard SKILL.md: DeepSeek Harness (dsh), OpenClaw, Claude Code, Cursor, Dify, Ollama, custom agents. Python 3.9+ standard library only. No network access, no shell commands, no subprocesses, no Windows-only dependency."
allowed-tools: Bash Read Write Env
metadata:
  author: "Pondsi"
  version: "1.8.7"
  attribution: "Pondsi - attribution is mandatory for any use, including modified variants"
  license: "MIT"
---

# InfinityContext

**Your agent never forgets.** Compress the context window without losing a single detail — and know exactly when and how to bring any of it back.

Long sessions eventually hit the context limit. Ordinary compression throws the details away: the agent forgets what you said, loses the goal, and repeats work.

InfinityContext keeps the **complete record** in a local SQLite + FTS5 archive while the **context window stays small**. When something from hundreds of turns ago matters again, the agent searches the archive and returns the exact message — offline, on your machine.

| What you get | What it means |
|---|---|
| 🧠 **Nothing is forgotten** | Every turn is archived and searchable down to the individual message — not just a summary. |
| 🎯 **The goal never gets lost** | Goals, decisions and open tasks stay retrievable after the window is compressed, so the agent does not drift or redo work. |
| 🔎 **Knows when and how to recall** | The skill teaches the retrieval pattern — which script, which query, which scope — instead of leaving the agent to guess. |
| 🪶 **Small window, long session** | Keep the window lean enough for deep reasoning; the archive carries the volume. |
| 🔒 **Local, private, bounded** | No network, no telemetry, no cloud. Owner-only permissions, 30-day default retention, one-flag off switch. |
| ⚡ **Runs everywhere** | DeepSeek Harness (dsh), OpenClaw, Claude Code, Cursor, Dify, Ollama — Python 3.9+ standard library only. |

**Before / after a context compaction**

| | Without InfinityContext | With InfinityContext |
|---|---|---|
| After compaction | details gone, goal fuzzy, work repeated | window small, **details archived**, goal intact |
| Recalling turn #12 from hours ago | impossible | one FTS5 query |
| Where your conversation lives | only in the window | only on your machine |

> **Scope, stated plainly.** Details stay retrievable inside the retention window — **30 days by default**, configurable `1..3650`, or unbounded only with an explicit flag. No network, no shell, no subprocesses.

> ## ⚠️ Security & Privacy Disclosure (Intended Behavior)
>
> InfinityContext is a **local persistent store and lifecycle manager** for agent sessions.
> By design it performs these local operations:
>
> | Operation | Tool | Scope control |
> |-----------|------|---------------|
> | Persist redacted conversation chunks in a local SQLite/FTS5 archive | `session_to_sqlite.py` | owner-only directory (`0700`/`0600` or a protected DACL), fail-closed |
> | Permanently delete expired archive files | `cleanup.py` | verified archive marker + full-filename allowlist + non-recursive + `--apply --confirm-destructive` |
> | Rewrite a file in place (redaction) | `session_to_sqlite.py --redact-file` | requires `--allow-dir`; symlink-resolved path must stay inside it |
> | Move the archive when the path is not ASCII-safe | `session_to_sqlite.py` | **refused** unless `--allow-dir-fallback` is given |
> | Enforce a bounded retention window (default **30 days**) | `session_to_sqlite.py` | `--retention-days 1..3650`; keeping chunks forever needs `--allow-unbounded-retention` |
> | Disable archiving entirely | `session_to_sqlite.py` | env `INFINITY_CONTEXT_NO_ARCHIVE=1` — the script then writes nothing |
>
> Nothing is sent anywhere: no network, no telemetry, no cloud sync. Redaction is best-effort;
> the archive still holds a detailed record of your sessions, so keep it out of synced or
> shared folders and run cleanup deliberately. **Retention is bounded by default: chunks older
> than 30 days are purged on every run, and `--purge-only` applies the same policy on demand.**
>
> **Installing this skill means accepting these local persistence and file-mutation
> capabilities.**

Works out of the box on **DeepSeek Harness (dsh)** and **OpenClaw**, and on any
host that loads a standard `SKILL.md`.

## Install

### 1. Registry (scanned artifact — no git, no build step)

```bash
# dsh / Claude Code: lands in ~/.agents/skills/infinity-context/
clawhub install infinitycontext --workdir ~/.agents --dir skills

# OpenClaw: managed skills (~/.openclaw/skills) or workspace skills (higher precedence)
clawhub install infinitycontext --workdir ~/.openclaw --dir skills
clawhub install infinitycontext --workdir <workspace> --dir skills
```

### 2. From source — pin the reviewed release tag, verify every byte

```bash
git clone https://github.com/Pondsi/infinitycontext.git
cd infinitycontext
git checkout --detach v1.8.7
grep -q '^version: "1.8.7"' SKILL.md || { echo "tag/version mismatch - stop"; exit 1; }
sha256sum -c checksums.txt                # macOS: shasum -a 256 -c checksums.txt
# compare the output with the hashes published in the GitHub release notes
```

Then place the verified files into the skill directory exactly as listed in
[`references/architecture.md`](references/architecture.md#file-layout) — the list is
explicit, so no wildcard and no `cp -r` is ever needed.

The pinned tag must equal the `version` in this file's frontmatter. The `grep`
guard above stops the install when it does not, so a source install can never
silently produce an older build than the reviewed artifact.

## Quick start on DeepSeek Harness (dsh)

dsh uses the standard `SKILL.md` contract. Two rules matter:

- frontmatter `name` and `description` are **required**, and `name` must be kebab-case
- a skill is a **directory bundle one level deep** (`<root>/<dir>/SKILL.md`) or a flat `<name>.md`; nested `**/SKILL.md` files are deliberately not discovered
- the folder name does **not** have to match `name` — dsh identifies the skill by the frontmatter `name`, so the registry bundle `infinitycontext/` works as-is

Use the user-level root `~/.agents/skills/infinity-context/` (rank 500, shared
with Claude Code and other agents) or the project-level root
`<project>/.agents/skills/infinity-context/` (rank 200, wins over the user-level
copy). Restart dsh, type `/`, and the skill appears under **Skills**. Nothing
else to install: a skill takes effect the moment its folder sits in a scan root.

Then drive it from the agent's shell tool:

```bash
# archive a transcript (JSONL) into the local SQLite/FTS5 store
python3 scripts/session_to_sqlite.py --session-key <key> --session-file <events.jsonl> --output-dir ~/.infinity-context/archive

# retrieve a detail from months ago
python3 scripts/search.py --query "deployment token"

# prune old archives (dry-run by default)
python3 scripts/cleanup.py --dry-run
```

## Quick start on OpenClaw

The scripts above are then available unchanged; OpenClaw discovers the skill from its
skills directory and calls them through its shell tool. Host-specific automation is
optional and lives outside this package (see the repository).

## Host compatibility

| Host | Install location | Notes |
|------|------------------|-------|
| **DeepSeek Harness (dsh)** | `~/.agents/skills/infinity-context/` or `<project>/.agents/skills/infinity-context/` | First-class; same contract as Claude Code |
| **OpenClaw** | `<workspace>/skills/` (highest precedence) or `~/.openclaw/skills/` (managed) | First-class; discovered automatically |
| **Claude Code** | `~/.claude/skills/infinity-context/` | `allowed-tools` pre-approves the declared capabilities |
| **Cursor / Dify / Ollama / custom** | point the agent at this folder | Pure Python standard library |

The core is **host-agnostic**: four Python scripts, no network, no shell, no
subprocesses, no Windows-only dependency.

## What it does

1. **Archive** (`session_to_sqlite.py`) — turns a session transcript into a local SQLite database with an FTS5 index, so a compressed session can still be searched down to the message.
2. **Retrieve** (`search.py`) — FTS5 trigram search with a `LIKE` fallback for short CJK queries; reads only, never writes.
3. **Prune** (`cleanup.py`) — retention-based cleanup with canonical path anchoring and `VACUUM`; dry-run by default.
4. **Protect** (`secure_fs.py`) — owner-only permissions for the archive directory, the database and its WAL sidecars.

Compression itself is a prompt-level discipline: keep `keepRecentTokens` small
enough that a deep reply still fits, and let the archive carry the details
instead of the context window.

## First-run consent (agent behaviour)

Before archiving a session for the first time in a given environment, the agent **must**
tell the user that the conversation will be stored locally in a searchable archive, and
obtain explicit confirmation. Do not archive silently. When a user asks to stop keeping
history, set `INFINITY_CONTEXT_NO_ARCHIVE=1` (the archiver then writes nothing) and run
`cleanup.py --apply --confirm-destructive` — or delete the archive directory. Retention is
bounded by default (30 days), so history stays inside a known window.

## Security & privacy

- **Local only** — no network calls, no telemetry, no MCP, no cloud sync.
- **No shell, no subprocesses** — the core never starts another program. Windows ACL hardening uses in-process Win32 security API calls, not a helper executable.
- **Owner-only archive, fail-closed** — the archive directory is forced to `0700` and files to `0600` on POSIX; on Windows the DACL is replaced by a protected DACL granting only the current user and LOCAL SYSTEM. Every result is re-read to prove the mode took effect. New database files are created atomically with `O_CREAT | O_EXCL | O_NOFOLLOW` and `0600`, so no file ever exists with wider permissions. A symbolic link on the target path is refused. A pre-existing directory owned by another account is refused. If owner-only access cannot be enforced, archiving **aborts and the half-written database is destroyed** (`status: error`, exit 3) instead of storing readable data; `--allow-insecure-storage` is the only way to opt out, and the JSON result then reports `insecure_storage: true`.
- **Fail-closed redaction** — before any text is stored, a regex redactor masks API keys, tokens, passwords, JWTs, private keys, connection strings, cookies, webhooks, phone numbers and emails. Rules are validated and **precompiled at startup**: a malformed `redact_rules.json`, a wrong field type or an uncompilable regex aborts the run before any database is created, and a failure while applying a rule aborts instead of skipping it. `session_key` is sanitised **before** it is used for any path or filename — a value outside the safe identifier format (or one that itself looks sensitive) becomes an opaque hash, so it never reaches a filename, the table or the FTS index. The transcript is redacted entirely in memory, then written in a single transaction; on failure the transaction rolls back and only a database created by that same run is removed — an existing archive being appended to is never deleted. High-entropy candidates are excluded from the keyword index. In-place redaction (`--redact-file`) additionally **requires `--allow-dir`** and resolves every symbolic link before comparing paths: the lexical path, the resolved path and the resolved allowed directory must all agree, so a symlinked ancestor inside the allowed directory cannot redirect the write elsewhere. A non-ASCII output path is **refused** by default (exit 8); only an explicit `--allow-dir-fallback` moves the archive to the ASCII fallback directory, and the run then prints a warning and reports `archive_dir_fallback: true` together with `requested_dir` and `archive_dir` — the location is never changed silently.
- **Data minimisation** — `MAX_ARCHIVE_LENGTH` truncates oversized content (head + tail kept) before storage. Ingestion itself is bounded **before** parsing: at most `--max-session-bytes` (64 MiB) is read from the head of the transcript, a line longer than `--max-line-bytes` (1 MiB) is discarded before JSON or any regex sees it, and ingestion stops at `--max-messages` (200000) or `--max-total-chars` (64 MiB). The result reports `ingest.truncated` and `ingest.truncated_reason`, so a bounded archive is never presented as a complete one. In-place redaction refuses a file larger than 64 MiB before reading it.
- **Bounded retention, default 30 days** — archiving is not unbounded. Every run purges chunks older than `--retention-days` (default 30, range 1..3650) from `session_chunks` and its FTS mirror inside the same transaction, and reports the count as `purged_chunks`; `--purge-only --output-dir <dir>` applies the same policy to existing archives without ingesting, and only to a directory that carries the archive marker. Keeping chunks forever requires the explicit `--allow-unbounded-retention` flag. Set `INFINITY_CONTEXT_NO_ARCHIVE=1` to disable archiving entirely — the script writes no file and reports `status: disabled`.
- **Archive files are created exclusively and identified before they are written** — a new archive is reserved with `O_CREAT | O_EXCL | O_NOFOLLOW` and `0600`, so a name collision aborts (exit 10) instead of reusing an existing file. `--purge-only` only considers the complete artifact filename pattern and requires a read-only identity match (`archive_metadata` app / format version / archive id, plus the expected `session_chunks` columns) before it re-opens a database read-write; skipped databases are reported, never modified.
- **Append is identity-checked, not prefix-matched** — `--append` only accepts a file whose **complete** name is `{safe_key}-YYYYMMDD-HHMMSS.db`, opens it **read-only first** and requires the exact `session_key` in `archive_metadata` (older archives fall back to a row check), then upgrades the archive with that metadata row. A foreign database, a symlink, a path outside `--output-dir`, or more than one candidate all abort with exit 9 before anything is written; `--db-path` picks one explicitly.
- **Deny-by-default filesystem rules** — `cleanup.py` refuses any directory that lacks the owner-only `.infinity-context-archive` marker, refuses protected directories (filesystem root, home, common user folders), only deletes files whose **full name** matches an InfinityContext artifact pattern, never recurses into subdirectories, re-checks each candidate with `lstat` immediately before deletion, validates the `session_chunks`/`chunk_fts` schema in read-only mode before any `VACUUM`, and does nothing unless **both** `--apply` and `--confirm-destructive` are given.

### Data sensitivity notice

Conversation archives contain session history and are treated as sensitive data.
Redaction is best-effort: after redaction the archive still holds a detailed
record of your sessions. Do not share archive files, sync them to cloud storage,
or widen the permissions of the archive directory without understanding the
consequences.

## Supply chain

This package is **self-contained**: `SKILL.md`, `README.md`, `说明.md`,
`CHANGELOG.md`, `SPONSORS.md`, `LICENSE`, `checksums.txt`, `scripts/` (Python
only), `references/`, `sponsors/`. It contains no JavaScript, no PowerShell and
no code fetched at install time — the audited artifact is exactly what runs.
`checksums.txt` lists the SHA-256 of every published file except itself.

Any host-specific automation is deliberately **out of scope** for this package.
Anything of that kind lives in the repository outside the published artifact and
carries its own documentation, pinned revision and checksums.

> **Want the complete project?** The GitHub repository
> ([Pondsi/infinitycontext](https://github.com/Pondsi/infinitycontext)) is the **full,
> unabridged** version — the identical core **plus** the optional host integration
> (`openclaw/`, with its own README and checksums), so nothing is missing when you need
> it. The registry package here is deliberately slimmed to the auditable core.

## Configuration

| Setting | Default | Where |
|---------|---------|-------|
| archive directory | `~/.infinity-context/archive` | `--output-dir` / `--archive-dir`, or `INFINITY_CONTEXT_HOME` |
| non-ASCII output path | refused (exit 8) | `--allow-dir-fallback` opts into `~/.openclaw/sqlite-data` |
| `MAX_ARCHIVE_LENGTH` | `20000` characters | `scripts/session_to_sqlite.py` |
| ingest file cap | 64 MiB (hard ceiling) | `--max-session-bytes` (1..ceiling) |
| ingest line cap | 1 MiB (hard ceiling) | `--max-line-bytes` (1..ceiling) |
| ingest message cap | 200000 (hard ceiling) | `--max-messages` (1..ceiling) |
| ingest character cap | 64 MiB (hard ceiling) | `--max-total-chars` (1..ceiling) |
| redaction rules | built in | `scripts/session_to_sqlite.py` (add `redact_rules.json` beside it to extend) |
| Append to an existing archive | `session_to_sqlite.py --append` | complete artifact filename + read-only identity check (`archive_metadata`: app, format version, archive id); ambiguous or foreign target aborts with exit 9; `--db-path` selects one explicitly |
| Create a new archive file | `session_to_sqlite.py` | atomic `O_CREAT\|O_EXCL\|O_NOFOLLOW` reservation; a name collision aborts with exit 10 instead of reusing the existing file |
| Purge expired chunks in place | `session_to_sqlite.py --purge-only` | artifact-filename pattern + read-only identity check + `lstat` device/inode re-check before opening read-write; every skipped database is reported |
| append target | exact filename + identity check | `--append` matches `{key}-YYYYMMDD-HHMMSS.db` exactly, verifies `archive_metadata` read-only, and refuses an ambiguous or foreign database (exit 9); `--db-path` selects one explicitly |
| retention (archive contents) | 30 days | `session_to_sqlite.py --retention-days` (1..3650; `0` needs `--allow-unbounded-retention`) |
| manual retention pass | off | `session_to_sqlite.py --purge-only --output-dir <dir>` |
| disable archiving | off | env `INFINITY_CONTEXT_NO_ARCHIVE=1` |
| retention (archive files) | 30 days | `cleanup.py --days` (1..3650) |
| archive marker | `.infinity-context-archive` | written by `session_to_sqlite.py`; `cleanup.py` refuses to run without it |
| destructive cleanup | requires `--apply --confirm-destructive` | `cleanup.py` |
| migrate an old archive | `cleanup.py --init-marker` | only after a valid database is found in the directory |

## Architecture

```
session transcript (JSONL)
        │
        ├─ bound  ────────────────► size / line / count / char caps, applied while reading
        ├─ redact  ────────────────► fail-closed: nothing is stored if this step fails
        ├─ truncate (MAX_ARCHIVE_LENGTH)
        ▼
  session_chunks  ──trigger──►  chunk_fts (FTS5 trigram)
        │
        └─ search.py  ──►  exact detail from any past turn
```

## More languages

Localised summaries (繁體中文, 日本語, 한국어, Español, Português, Français,
Deutsch, Русский) are in [`references/languages.md`](references/languages.md).

## License

MIT with a **mandatory attribution requirement** — using all or part of the source, including modified variants, is permitted, but **Pondsi must always be credited**. See [LICENSE](LICENSE). Changelog: [CHANGELOG.md](CHANGELOG.md).

---

# 无限上下文压缩与记忆归档

**让智能体永不健忘。** 压缩上下文窗口，却一个细节都不丢——并且知道什么时候、用什么方法，把哪个细节找回来。

长会话迟早会撞上上下文上限。普通压缩把细节直接扔掉：智能体忘了你说过什么、丢了目标、重复干过的活。

InfinityContext 把**完整记录**放进本地 SQLite + FTS5 归档，而**上下文窗口保持精简**。几百轮之前的事再被提起时，智能体检索归档，取回那一句原话——离线、在本机。

| 你得到什么 | 意味着什么 |
|---|---|
| 🧠 **细节不会被忘掉** | 每一轮对话都进归档，可检索到单条消息——不是只有摘要。 |
| 🎯 **目标不会丢** | 目标、决策、未完成任务在窗口压缩后依然可检索，智能体不会跑偏或重做。 |
| 🔎 **知道何时、如何回忆** | 技能教会智能体检索套路——用哪个脚本、什么查询、多大范围——而不是让它瞎猜。 |
| 🪶 **小窗口，长会话** | 窗口保持精简，深度思考照样放得下；体量交给归档。 |
| 🔒 **本地、私密、有边界** | 不联网、无遥测、不上云；仅所有者可读，默认保留 30 天，一个开关即可关闭。 |
| ⚡ **到处都能跑** | dsh、OpenClaw、Claude Code、Cursor、Dify、Ollama——只用 Python 3.9+ 标准库。 |

**上下文压缩前后对比**

| | 没有 InfinityContext | 有 InfinityContext |
|---|---|---|
| 压缩之后 | 细节消失、目标模糊、重复劳动 | 窗口变小、**细节已归档**、目标完好 |
| 回忆几小时前的第 12 轮 | 不可能 | 一次 FTS5 查询 |
| 对话存在哪 | 只在窗口里 | 只在你本机 |

> **范围说明（如实）**：细节在保留窗口内可检索——**默认 30 天**，可配 `1..3650`，无界需显式开关。不联网、无 shell、无子进程。

**开箱即用**：DeepSeek Harness（dsh）与 OpenClaw；任何加载标准 `SKILL.md` 的宿主亦可。

## 安装

```bash
# 方式一：注册表（已扫描产物，无需 git、无需构建）
clawhub install infinitycontext --workdir ~/.agents --dir skills    # dsh / Claude Code
clawhub install infinitycontext --workdir ~/.openclaw --dir skills  # OpenClaw 托管技能
```

方式二（源码安装：固定已审计 tag + 逐文件校验）见上方 [Install](#install)；
需要复制的文件清单见 [`references/architecture.md`](references/architecture.md#file-layout)。

**必须逐文件显式复制，禁止 `cp -r`**：被审计的包不得混入未审计文件。

## 在 dsh 上快速开始

- frontmatter 的 `name` 与 `description` **必填**，且 `name` 必须是 kebab-case
- 技能是**一层深的目录包**（`<root>/<dir>/SKILL.md`）或平铺文件 `<name>.md`；嵌套的 `**/SKILL.md` 故意不被发现
- 文件夹名**不必**与 `name` 相同——dsh 用 frontmatter 的 `name` 作为标识（注册表安装出的目录是 `infinitycontext/`，同样可用）

用户级 `~/.agents/skills/infinity-context/`（rank 500，与 Claude Code 共享）或项目级
`<project>/.agents/skills/infinity-context/`（rank 200，优先）。重启 dsh，输入 `/`，
技能即出现在 **Skills** 分组——文件夹进入扫描根即生效，无需其它步骤。

## 在 OpenClaw 上快速开始

`clawhub install infinitycontext` 后，上述脚本即可直接调用；OpenClaw 从技能目录发现本技能
并通过 shell 工具执行。宿主专有的自动化属于**可选集成**，不在本包内（见仓库）。

## 四个脚本

1. **归档** `session_to_sqlite.py`——会话轨迹转本地 SQLite + FTS5 索引
2. **检索** `search.py`——FTS5 三元组搜索，短中文词回退 `LIKE`；只读
3. **清理** `cleanup.py`——按保留期清理并 `VACUUM`；默认演练模式
4. **保护** `secure_fs.py`——归档目录/数据库/WAL 旁文件强制 owner-only 权限

## 安全与隐私

- **纯本地**：不联网、无遥测、无 MCP、不上传
- **无 shell、无子进程**：核心脚本从不启动其它程序；Windows ACL 使用进程内 Win32 安全 API，不调用外部工具
- **归档仅本人可读，且 Fail-Closed**：POSIX 目录 `0700`、文件 `0600`；Windows 用受保护 DACL 仅授权当前用户与 LOCAL SYSTEM；加固后**回读校验**是否真的生效；新数据库文件以 `O_CREAT|O_EXCL|O_NOFOLLOW` + `0600` **原子创建**；路径上出现符号链接即**拒绝**；预存目录若属于其它账号则**拒绝使用**；**无法强制 owner-only 时中止归档并销毁半成品**（`status: error`，退出码 3），绝不留下可读的明文；仅 `--allow-insecure-storage` 可显式降级，且结果中会标记 `insecure_storage: true`
- **Fail-Closed 脱敏**：入库前屏蔽 API Key / Token / 密码 / JWT / 私钥 / 连接串 / Cookie / Webhook / 手机号 / 邮箱；规则**启动期校验并预编译**——`redact_rules.json` 损坏、字段类型错误或正则无法编译都会在**建库之前中止**，应用规则时出错也中止而非跳过；`session_key` 在**生成任何路径/文件名之前**先净化（不符合安全字符集或本身疑似敏感→不透明哈希），绝不进入文件名、表或 FTS；轨迹先在**内存中全量脱敏**，再在**单事务**内写入，失败则回滚且**只清理本轮新建的库**，追加模式下的历史归档绝不被删除；高熵候选不进入关键词索引；原地脱敏（`--redact-file`）**必须同时给出 `--allow-dir`**，且在比较路径前**解析全部符号链接**：词法路径、真实路径、真实允许目录三者必须一致，因此允许目录内部的符号链接祖先无法把写入重定向到别处；若因非 ASCII 路径回退到备用目录，会打印告警并在结果中给出 `archive_dir_fallback: true`、`requested_dir` 与 `archive_dir`——**绝不静默改道**
- **保留期有界，默认 30 天**：归档不会无限累积。每次摄入都会在**同一事务**内删除超过 `--retention-days`（默认 30，范围 1..3650）的旧片段及其 FTS 镜像，并在结果中给出 `purged_chunks`；`--purge-only --output-dir <目录>` 可对既有归档执行同一策略（仅限带归档标记的目录，不摄入新数据）。要无限期保留必须显式 `--allow-unbounded-retention`。设置 `INFINITY_CONTEXT_NO_ARCHIVE=1` 可彻底关闭归档——脚本不写任何文件并返回 `status: disabled`。
- **数据最小化**：`MAX_ARCHIVE_LENGTH` 掐头去尾截断
- **默认拒绝的文件系统规则**：`cleanup.py` 只删归档目录内、白名单扩展名、非符号链接的文件，且必须显式 `--apply`

### 数据敏感性声明

归档包含会话历史，属于敏感数据。脱敏是尽力而为：脱敏后仍保留会话的详细记录。
请勿分享归档文件、同步到云存储，或在未理解后果的情况下放宽归档目录权限。

## 供应链

本包**自包含**：`SKILL.md`、`README.md`、`说明.md`、`CHANGELOG.md`、`SPONSORS.md`、
`LICENSE`、`checksums.txt`、`scripts/`（仅 Python）、`references/`、`sponsors/`。
**不含任何 JavaScript / PowerShell，也不在安装时拉取外部代码**——被审计的产物就是
实际运行的东西。`checksums.txt` 列出除自身外每个发布文件的 SHA-256。

宿主专有的自动化**不属于本包范围**，只存在于仓库中、位于发布产物之外，
并自带文档、固定版本号与校验和。

> **想要完整项目？** GitHub 仓库
> （[Pondsi/infinitycontext](https://github.com/Pondsi/infinitycontext)）是**完整、不精简**的版本：
> 核心完全一致，**外加**可选的宿主集成（`openclaw/`，自带 README 与校验和），需要时功能一个不少。
> 你在这里看到的注册表包**刻意精简为可审计核心**。

## 其它语言

繁體中文、日本語、한국어、Español、Português、Français、Deutsch、Русский 见
[`references/languages.md`](references/languages.md)。

## 许可证

MIT 许可证（附**强制署名条款**）——允许使用全部或部分源码（含修改后的变体），但**必须标注 Pondsi 的署名**。详见 [LICENSE](LICENSE)。

---

Pondsi (+MiMo-v2.5/v2.5pro+deepseek-v4-flash/pro+deepseek-v4.1-flash-expires-on-0910+GLM5.3-flash+Gemini3.1-pro+Qwen3.8-27b+Gemini3.8-flash) — automatically committed by Openclaw
