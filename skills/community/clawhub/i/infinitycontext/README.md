# InfinityContext

**Open-Source Context Compression & Memory Optimization for AI Agents — DeepSeek Harness (dsh), Claude Code, OpenClaw, Cursor, Dify, Ollama and any Agent Skills host**

[English](#english) | [简体中文](#简体中文) | [繁體中文](#繁體中文) | [日本語](#日本語) | [한국어](#한국어) | [Español](#español) | [Português](#português) | [Français](#français) | [Deutsch](#deutsch) | [Русский](#русский)

---

## ⚡ Why InfinityContext / 为什么需要它

**EN** — Long sessions hit the context limit. Ordinary compression throws the details away: the agent forgets what you said, loses the goal, and repeats work. **InfinityContext keeps the complete record in a local SQLite + FTS5 archive while the context window stays small** — so when something from hundreds of turns ago matters again, the agent finds it and returns the exact message. Offline, on your machine.

**中文** — 长会话迟早撞上上下文上限。普通压缩把细节直接扔掉：智能体忘了你说过什么、丢了目标、重复干过的活。**InfinityContext 把完整记录放进本地 SQLite + FTS5 归档，而上下文窗口保持精简**——几百轮之前的事再被提起时，智能体能找到并取回那一句原话。离线、在本机。

| What you get / 你得到什么 | Why it matters / 意味着什么 |
|---|---|
| 🧠 **Nothing is forgotten / 细节不会被忘掉** | Every turn is archived and searchable down to the single message — not just a summary. |
| 🎯 **The goal never gets lost / 目标不会丢** | Goals, decisions and open tasks stay retrievable after compression, so the agent does not drift or redo work. |
| 🔎 **Knows when and how to recall / 知道何时如何回忆** | The skill teaches the retrieval pattern — which script, which query, which scope — instead of leaving the agent to guess. |
| 🪶 **Small window, long session / 小窗口，长会话** | Keep the window lean for deep reasoning; the archive carries the volume. |
| 🔒 **Local, private, bounded / 本地、私密、有边界** | No network, no telemetry, no cloud. Owner-only permissions, 30-day default retention, one-flag off switch. |
| ⚡ **Runs everywhere / 到处都能跑** | DeepSeek Harness (dsh), OpenClaw, Claude Code, Cursor, Dify, Ollama — Python 3.9+ standard library only. |

**Before / after a compaction / 压缩前后对比**

| | Without InfinityContext | With InfinityContext |
|---|---|---|
| After compaction | details gone, goal fuzzy, work repeated | window small, **details archived**, goal intact |
| Recalling turn #12 from hours ago | impossible | one FTS5 query |
| Where your conversation lives | only in the window | only on your machine |

> **Scope, stated plainly / 范围说明**：details stay retrievable inside the retention window — **30 days by default**, `1..3650` configurable, unbounded only with an explicit flag.

---

## Which package should I install? / 该装哪个包？

| | **ClawHub / registry artifact** | **GitHub repository** |
|---|---|---|
| What it is | the security-audited portable core | **the complete, unabridged project** |
| Files | 15 | 31 |
| OpenClaw hook, watchdog, Windows helpers (`openclaw/`) | — | ✅ |
| Best for | dsh, Claude Code, Cursor, Dify, Ollama, any `SKILL.md` host | OpenClaw on Windows with automation |
| Version | same tag | same tag |

> The registry package is **deliberately slimmed to the auditable core** — that is exactly what the security scan reviews, and nothing outside it is executed. The GitHub repository is the **complete project**: the identical core **plus** the optional host integration, so no capability is missing when you need it.
>
> 注册表包**刻意精简为可审计核心**（安全扫描审查的就是它，它之外没有任何代码会被执行）；GitHub 仓库是**完整项目**：核心完全一致，**外加**可选的宿主集成，需要时功能一个不少。

---

> ⚠️ **Security & Privacy Disclosure — Intended Behavior / 安全与隐私披露（预期行为）**
>
> **EN** — InfinityContext is a **local persistent store and lifecycle manager** for agent
> sessions. By design it performs these local operations:
>
> | Operation | Tool | Scope control |
> |-----------|------|---------------|
> | Persist redacted conversation chunks in a local SQLite/FTS5 archive | `session_to_sqlite.py` | owner-only directory (`0700`/`0600`, or a protected DACL), fail-closed |
> | **Permanently delete** expired archive files | `cleanup.py` | verified `.infinity-context-archive` marker + full-filename allowlist + non-recursive + `--apply --confirm-destructive` |
> | **Rewrite a file in place** (redaction) | `session_to_sqlite.py --redact-file` | requires `--allow-dir`; the symlink-resolved path must stay inside it |
> | Move the archive when the path is not ASCII-safe | `session_to_sqlite.py` | refused unless `--allow-dir-fallback` is given |
>
> Redaction is best-effort and the archive still holds a detailed record of your sessions.
> Nothing is sent anywhere — no cloud sync, no telemetry, no outbound network. Keep the
> archive out of synced or shared folders and run cleanup deliberately.
> **Installing this skill means accepting these local persistence and file-mutation
> capabilities.**
>
> **中文** — 本插件是**本地持久化存储与生命周期管理器**，按设计会执行以下本地操作：
>
> | 操作 | 工具 | 范围控制 |
> |------|------|----------|
> | 把脱敏后的对话片段持久化到本地 SQLite/FTS5 | `session_to_sqlite.py` | 目录 0700 / 文件 0600（Windows 为受保护 DACL），Fail-Closed |
> | **永久删除**过期归档文件 | `cleanup.py` | 必须存在 `.infinity-context-archive` 归档标记 + 完整文件名白名单 + 不递归 + `--apply --confirm-destructive` |
> | **就地改写**文件（脱敏） | `session_to_sqlite.py --redact-file` | 必须指定 `--allow-dir`，解析符号链接后仍须落在该目录内 |
> | 路径非 ASCII 时改存其它目录 | `session_to_sqlite.py` | 默认拒绝，需显式 `--allow-dir-fallback` |
>
> 脱敏是尽力而为，归档仍保留会话的详细记录；不联网、不上传、无遥测。请把归档放在
> **非同步、非共享**目录，并谨慎执行清理。**安装即表示你接受上述本地持久化与文件修改能力。**

## Permissions / 权限声明

Declared capability scope (mirrors the Agent Skills `allowed-tools` field). This is the whole
surface of the published package:

| Capability | Used for |
|-----------|----------|
| File read | Reading the session transcript (JSONL) you pass in, and the archive it created |
| File write | Writing the SQLite archive, its WAL sidecars, the archive marker, and — with `--redact-file` — rewriting one file inside a declared `--allow-dir` |
| Environment | Reading `INFINITY_CONTEXT_HOME`, `INFINITY_CONTEXT_REDACT_RULES` and `INFINITY_CONTEXT_NO_ARCHIVE` |

**Not declared because not used: network, MCP, shell, subprocesses.** The core never starts
another program, and nothing leaves the machine.

> **Package boundary.** The published artifact is exactly the files listed in `checksums.txt`
> (`SKILL.md`, `README.md`, `说明.md`, `CHANGELOG.md`, `SPONSORS.md`, `LICENSE`,
> `checksums.txt`, `scripts/*.py`, `references/*.md`, `sponsors/*`) — **no JavaScript and no
> PowerShell**. Any optional OpenClaw/Windows integration lives in the GitHub repository under
> `openclaw/`, is **not** part of this package, and carries its own documentation and
> `openclaw/checksums.txt`.

## English

### What is this?

InfinityContext is a **portable AI-agent skill** (a standard `SKILL.md` bundle) that keeps long sessions usable: it compresses context, archives **redacted** conversation chunks into a **local** SQLite/FTS5 store, and retrieves exact details from an earlier turn. It runs on **any Agent Skills host** — first-class support for **DeepSeek Harness (dsh)** (drop it into `.agents/skills/` and the harness discovers it) — plus Claude Code, OpenClaw, Cursor, Dify, Ollama and custom agents.

> **Scope, stated plainly.** This package is the portable Python core. It reads a session transcript, writes a local archive, and answers searches. It has **no network access, no shell, no subprocesses and no background service**. Everything it can do to your files is listed in the disclosure table at the top of `SKILL.md`.

### What it does

| Step | Script | What happens |
|------|--------|--------------|
| Archive | `scripts/session_to_sqlite.py` | transcript (JSONL) → redacted chunks in a local SQLite DB with an FTS5 index |
| Retrieve | `scripts/search.py` | read-only FTS5 search (trigram, with `LIKE` fallback for short CJK queries) |
| Prune | `scripts/cleanup.py` | retention cleanup of archive files; dry-run by default |
| Protect | `scripts/secure_fs.py` | owner-only permissions for the archive directory, database and WAL sidecars |

> **File operations this package performs** (full detail in the disclosure table at the top of `SKILL.md`):
>
> | Operation | Tool | Guard |
> |-----------|------|-------|
> | Write redacted chunks into a local archive | `session_to_sqlite.py` | owner-only permissions, fail-closed |
> | **Permanently delete** expired archive files | `cleanup.py` | archive marker + full-filename allowlist + non-recursive + `--apply --confirm-destructive` |
> | Rewrite a file in place (redaction) | `session_to_sqlite.py --redact-file` | requires `--allow-dir`; symlink-resolved path must stay inside it |
> | Move the archive when the path is not ASCII-safe | `session_to_sqlite.py` | **refused** unless `--allow-dir-fallback` is given |

### Retention policy (read this once)

| Setting | Value | Notes |
|---------|-------|-------|
| Default retention | **30 days** | chunks older than 30 days are purged on every run, in the same transaction as the insert |
| Configurable range | `1..3650` days | `--retention-days N` |
| No time limit | **opt-in only** | `--retention-days 0` is rejected unless `--allow-unbounded-retention` is also given |
| Manual pass | `--purge-only --output-dir <dir>` | applies the same policy to existing archives, without ingesting |
| Off switch | `INFINITY_CONTEXT_NO_ARCHIVE=1` | the archiver writes nothing and returns `status: disabled` |

Retention is enforced by code, not by documentation: every run deletes expired chunks from `session_chunks` and its FTS mirror and reports the count as `purged_chunks`.

### Quick start (5 minutes)

**Prerequisite: Python 3.9+.** No Node.js, no build step, no network access.

```bash
# 1. Install (registry — a scanned artifact)
clawhub install infinitycontext --workdir ~/.agents --dir skills   # dsh / Claude Code
clawhub install infinitycontext --workdir ~/.openclaw --dir skills  # OpenClaw

# 2. Archive a transcript
python3 scripts/session_to_sqlite.py \
  --session-key my-session \
  --session-file ~/path/to/events.jsonl \
  --output-dir ~/.infinity-context/archive

# 3. Retrieve a detail later (read-only)
python3 scripts/search.py --db ~/.infinity-context/archive/my-session-*.db --query "deployment token"

# 4. Prune archive files (dry-run first)
python3 scripts/cleanup.py --archive-dir ~/.infinity-context/archive --dry-run
```

**From source** — pin the reviewed tag and verify every byte:

```bash
git clone https://github.com/Pondsi/infinitycontext.git
cd infinitycontext
git checkout --detach v1.8.7
grep -q '^version: "1.8.7"' SKILL.md || { echo "tag/version mismatch - stop"; exit 1; }
sha256sum -c checksums.txt          # macOS: shasum -a 256 -c checksums.txt
```

Then place the verified files into your skills directory exactly as listed in
[`references/architecture.md`](references/architecture.md#file-layout) — the list is explicit, so no wildcard and no `cp -r` is ever needed.

### Where to install

| Host | Location | Notes |
|------|----------|-------|
| DeepSeek Harness (dsh) | `~/.agents/skills/infinity-context/` or `<project>/.agents/skills/infinity-context/` | a skill is one level deep (`<root>/<dir>/SKILL.md`); nested `**/SKILL.md` is deliberately not discovered |
| OpenClaw | `<workspace>/skills/` (highest precedence) or `~/.openclaw/skills/` | discovered automatically |
| Claude Code | `~/.claude/skills/infinity-context/` | same layout |
| Cursor / Dify / Ollama / custom | point the agent at this folder | pure Python standard library |

### Requirements

- Any host that loads a standard `SKILL.md`: dsh, Claude Code, OpenClaw, Cursor, Dify, Ollama or a custom agent.
- **Python 3.9+ only.** The core contains no JavaScript, no PowerShell, no subprocesses and no network code.
- An optional OpenClaw/Windows integration lives in the **repository** under `openclaw/` and is **not** part of this package.

### FAQ

**Where is my data?** In the directory passed as `--output-dir` (default `~/.infinity-context/archive`): a SQLite database plus `-wal`/`-shm` sidecars, owner-only permissions.

**How do I stop archiving completely?** Set `INFINITY_CONTEXT_NO_ARCHIVE=1`; the archiver writes nothing and returns `status: disabled`.

**How do I keep less history?** `--retention-days 7` — expired chunks are deleted on the next run. `--purge-only --output-dir <dir>` applies it immediately without ingesting anything.

**Is anything sent anywhere?** No. There is no network code in the package.

**What about secrets in the transcript?** Redaction runs before anything is stored (API keys, tokens, passwords, JWTs, private keys, connection strings, cookies, webhooks, phone numbers, emails). It is best-effort — treat the archive as sensitive data.

**Why is my non-ASCII output path refused?** SQLite on Windows cannot use it. The run aborts with exit 8; `--allow-dir-fallback` moves the archive to `~/.openclaw/sqlite-data` and reports the change instead of doing it silently.

### Issues & discussions

- **Bug reports**: <https://github.com/Pondsi/infinitycontext/issues>
- **Questions and ideas**: <https://github.com/Pondsi/infinitycontext/discussions>

### Sponsors

If you find this project helpful, consider supporting its development! See [SPONSORS.md](SPONSORS.md) for donation options.

### License

MIT License with a **mandatory attribution requirement**: using all or part of the
source, including modified variants, is permitted — but **Pondsi must always be
credited as the original author**. See [LICENSE](LICENSE).

---

## 简体中文

### 这是什么？

InfinityContext 是一个**可移植的 AI 智能体技能**（标准 `SKILL.md` 包）：压缩上下文、把**脱敏后**的对话片段写入**本地** SQLite/FTS5 归档，并可按需精确检索任意早期细节。它可运行在**任何支持 Agent Skills 的宿主**上——**原生支持 DeepSeek Harness（dsh）**（放进 `.agents/skills/` 即被发现），同样支持 Claude Code、OpenClaw、Cursor、Dify、Ollama 及自研 Agent。

> **边界说明（说清楚）**：本包只包含可移植的 Python 核心——读取会话轨迹、写入本地归档、提供检索。**不联网、不调用 shell、不启动子进程、不常驻后台**。它对文件能做的全部操作，都列在 `SKILL.md` 顶部的能力披露表里。

### 它做什么

| 步骤 | 脚本 | 说明 |
|------|------|------|
| 归档 | `scripts/session_to_sqlite.py` | 会话轨迹（JSONL）→ 脱敏片段写入本地 SQLite + FTS5 索引 |
| 检索 | `scripts/search.py` | 只读 FTS5 搜索（三元组；短中文词回退 `LIKE`） |
| 清理 | `scripts/cleanup.py` | 归档文件按保留期清理，默认演练模式 |
| 保护 | `scripts/secure_fs.py` | 归档目录/数据库/WAL 旁文件强制 owner-only 权限 |

> **本包会执行的文件操作**（完整披露见 `SKILL.md` 顶部表格）：
>
> | 操作 | 工具 | 约束 |
> |------|------|------|
> | 把脱敏片段写入本地归档 | `session_to_sqlite.py` | owner-only 权限，Fail-Closed |
> | **永久删除**过期归档文件 | `cleanup.py` | 归档标记 + 完整文件名白名单 + 不递归 + `--apply --confirm-destructive` |
> | 就地改写文件（脱敏） | `session_to_sqlite.py --redact-file` | 必须 `--allow-dir`；符号链接解析后的路径必须仍在范围内 |
> | 路径非 ASCII 时移动归档 | `session_to_sqlite.py` | 默认**拒绝**，需显式 `--allow-dir-fallback` |

### 保留期策略（看一次就够）

| 设置 | 取值 | 说明 |
|------|------|------|
| 默认保留 | **30 天** | 每次运行都会在同一事务内清理超过 30 天的片段 |
| 可配置范围 | `1..3650` 天 | `--retention-days N` |
| 不限时间 | **必须显式开启** | `--retention-days 0` 会被拒绝，除非同时给出 `--allow-unbounded-retention` |
| 手动清理 | `--purge-only --output-dir <目录>` | 对既有归档执行同一策略，不摄入新数据 |
| 彻底关闭 | `INFINITY_CONTEXT_NO_ARCHIVE=1` | 归档器不写任何文件，返回 `status: disabled` |

保留期是**代码强制**而非文档承诺：每次运行都会删除 `session_chunks` 及其 FTS 镜像中的过期片段，并在结果中返回 `purged_chunks`。

### 快速上手（5 分钟）

**前置条件：Python 3.9+**。不需要 Node.js、不需要构建、不需要联网。

```bash
# 1. 安装（注册表，已扫描产物）
clawhub install infinitycontext --workdir ~/.agents --dir skills   # dsh / Claude Code
clawhub install infinitycontext --workdir ~/.openclaw --dir skills  # OpenClaw

# 2. 归档一份会话轨迹
python3 scripts/session_to_sqlite.py \
  --session-key my-session \
  --session-file ~/path/to/events.jsonl \
  --output-dir ~/.infinity-context/archive

# 3. 以后精确检索（只读）
python3 scripts/search.py --db ~/.infinity-context/archive/my-session-*.db --query "部署令牌"

# 4. 清理归档文件（先演练）
python3 scripts/cleanup.py --archive-dir ~/.infinity-context/archive --dry-run
```

**源码安装**——固定已审计 tag 并逐文件校验：

```bash
git clone https://github.com/Pondsi/infinitycontext.git
cd infinitycontext
git checkout --detach v1.8.7
grep -q '^version: "1.8.7"' SKILL.md || { echo "tag/version mismatch - stop"; exit 1; }
sha256sum -c checksums.txt          # macOS：shasum -a 256 -c checksums.txt
```

随后按 [`references/architecture.md`](references/architecture.md#file-layout) 列出的文件清单逐文件放入技能目录——清单是显式的，不需要通配符，也不需要 `cp -r`。

### 安装到哪

| 宿主 | 位置 | 说明 |
|------|------|------|
| DeepSeek Harness（dsh） | `~/.agents/skills/infinity-context/` 或 `<项目>/.agents/skills/infinity-context/` | 技能是**一层深的目录包**（`<root>/<dir>/SKILL.md`）；嵌套 `**/SKILL.md` 故意不被发现 |
| OpenClaw | `<工作区>/skills/`（优先级最高）或 `~/.openclaw/skills/` | 自动发现 |
| Claude Code | `~/.claude/skills/infinity-context/` | 同样的目录结构 |
| Cursor / Dify / Ollama / 自研 | 让 Agent 指向本目录 | 纯 Python 标准库 |

### 系统要求

- 任意支持标准 `SKILL.md` 的宿主：dsh、Claude Code、OpenClaw、Cursor、Dify、Ollama 或自研 Agent。
- **只需 Python 3.9+**。核心**不含任何 JavaScript、PowerShell，不启动子进程，也没有网络代码**。
- 可选的 OpenClaw/Windows 自动化（钩子 + 看门狗）位于**仓库** `openclaw/` 目录，**不属于本包**。

### 常见问题

**数据存在哪？** 在你传入的 `--output-dir`（默认 `~/.infinity-context/archive`）：一个 SQLite 数据库及其 `-wal`/`-shm` 旁文件，owner-only 权限。

**怎么彻底停止归档？** 设置 `INFINITY_CONTEXT_NO_ARCHIVE=1`，归档器不写任何文件并返回 `status: disabled`。

**怎么只保留更少历史？** `--retention-days 7`，下次运行即删除超期片段；`--purge-only --output-dir <目录>` 可立即执行且不摄入新数据。

**数据会外传吗？** 不会。包内没有任何网络代码。

**轨迹里的密钥怎么办？** 脱敏在写入之前完成（API Key、Token、密码、JWT、私钥、连接串、Cookie、Webhook、手机号、邮箱），但它是尽力而为——请把归档当作敏感数据。

**为什么我的非 ASCII 路径被拒绝？** Windows 上的 SQLite 无法使用该路径。运行会以退出码 8 中止；`--allow-dir-fallback` 会把归档改到 `~/.openclaw/sqlite-data`，并如实上报，绝不静默改道。

### 问题与讨论

- **提交 Bug**：<https://github.com/Pondsi/infinitycontext/issues>
- **提问与想法**：<https://github.com/Pondsi/infinitycontext/discussions>

### 安全与隐私

- **纯本地**：无网络请求、无遥测、无云同步。
- **无 shell、无子进程**：核心脚本从不启动其它程序；Windows ACL 使用进程内 Win32 安全 API。
- **归档仅本人可读，Fail-Closed**：POSIX `0700`/`0600`；Windows 受保护 DACL；加固后回读校验；无法强制 owner-only 时中止并销毁半成品（退出码 3）。
- **脱敏 Fail-Closed**：规则启动期校验并预编译，任何失败都在建库之前中止；`session_key` 在生成任何路径/文件名之前先净化。
- **保留期有界**：默认 30 天，范围 `1..3650`，无限期保留需显式 `--allow-unbounded-retention`。
- **清理需二次确认**：`cleanup.py` 只清理带 `.infinity-context-archive` 标记的目录，必须同时给出 `--apply --confirm-destructive`，不递归，通用 `.json`/`.tmp`/`.bak` 永不删除。

### 许可证

MIT 许可证（附**强制署名条款**）：允许使用全部或部分源码（含修改后的变体），但**必须标注
Pondsi 的署名**。详见 [LICENSE](LICENSE)。

---

## 繁體中文

### 這是什麼？

InfinityContext 是可移植的 AI Agent Skill（標準 `SKILL.md`）：壓縮上下文、把**去識別化**後的對話片段寫入**本機** SQLite/FTS5 封存，並可精確檢索早期細節。支援 dsh、Claude Code、OpenClaw、Cursor、Dify、Ollama 與自訂 Agent。

### 安裝與使用

```bash
clawhub install infinitycontext --workdir ~/.agents --dir skills
```

完整步驟見 [English](#english) 與 [简体中文](#简体中文)。

### 重點

- **只需 Python 3.9+**：純標準庫，**不聯網、無 shell、不啟動子程序**。
- **保留期有界**：預設 30 天（`--retention-days 1..3650`）；不限時間需顯式 `--allow-unbounded-retention`；`INFINITY_CONTEXT_NO_ARCHIVE=1` 可完全關閉封存。
- **僅本機可讀**：封存目錄 0700／檔案 0600（Windows 為受保護 DACL），Fail-Closed。
- **清理需二次確認**：`cleanup.py` 必須 `--apply --confirm-destructive`，且只清理帶標記的目錄。

### 授權

MIT（附**強制署名條款**）：可自由使用（含修改後的變體），但**必須標註 Pondsi 的署名**。

---

## 日本語

### これは何？

InfinityContext は移植可能な AI エージェントスキル（標準 `SKILL.md`）です。コンテキストを圧縮し、**秘匿化済み**の会話断片を**ローカル** SQLite/FTS5 アーカイブへ保存し、過去の詳細を正確に検索できます。dsh、Claude Code、OpenClaw、Cursor、Dify、Ollama、独自エージェントに対応。

### インストールと使い方

```bash
clawhub install infinitycontext --workdir ~/.agents --dir skills
```

完全な手順は [English](#english) と [简体中文](#简体中文) を参照してください。

### 要点

- **Python 3.9+ のみ**：標準ライブラリのみ、**ネットワークなし・shell なし・子プロセスなし**。
- **保持期間は有界**：既定 30 日（`--retention-days 1..3650`）。無期限は明示的な `--allow-unbounded-retention` が必要。`INFINITY_CONTEXT_NO_ARCHIVE=1` でアーカイブを完全に停止。
- **所有者のみ読み取り可**：ディレクトリ 0700／ファイル 0600（Windows は保護 DACL）、Fail-Closed。
- **削除は二重確認**：`cleanup.py` は `--apply --confirm-destructive` が必須で、マーカーのあるディレクトリだけを対象にします。

### ライセンス

MIT（**強制署名条項**付き）：全体または一部（改変版を含む）の利用は自由ですが、**Pondsi のクレジット表記が必須**です。

---

## 한국어

### 무엇인가요?

InfinityContext는 이식 가능한 AI 에이전트 스킬(표준 `SKILL.md`)입니다. 컨텍스트를 압축하고 **비식별화된** 대화 조각을 **로컬** SQLite/FTS5 아카이브에 저장하며, 과거의 세부 내용을 정확히 검색합니다. dsh, Claude Code, OpenClaw, Cursor, Dify, Ollama 및 사용자 정의 에이전트를 지원합니다.

### 설치와 사용

```bash
clawhub install infinitycontext --workdir ~/.agents --dir skills
```

전체 절차는 [English](#english)와 [简体中文](#简体中文)를 참고하세요.

### 핵심

- **Python 3.9+만 필요**: 표준 라이브러리만 사용, **네트워크 없음·shell 없음·하위 프로세스 없음**.
- **보존 기간은 유한**: 기본 30일(`--retention-days 1..3650`). 무제한은 명시적 `--allow-unbounded-retention`이 필요하며 `INFINITY_CONTEXT_NO_ARCHIVE=1`로 완전히 끌 수 있습니다.
- **소유자만 읽기 가능**: 디렉터리 0700/파일 0600(Windows는 보호된 DACL), Fail-Closed.
- **삭제는 이중 확인**: `cleanup.py`는 `--apply --confirm-destructive`가 필요하며 마커가 있는 디렉터리만 정리합니다.

### 라이선스

MIT(**필수 저작자 표시 조항**): 전체 또는 일부(수정본 포함) 사용은 자유이지만 **Pondsi를 반드시 명시**해야 합니다.

---

## Español

### ¿Qué es esto?

InfinityContext es una skill de agente de IA portátil (un paquete `SKILL.md` estándar): comprime el contexto, archiva fragmentos de conversación **anonimizados** en un almacén **local** SQLite/FTS5 y recupera detalles exactos de turnos anteriores. Funciona en dsh, Claude Code, OpenClaw, Cursor, Dify, Ollama y agentes propios.

### Instalación y uso

```bash
clawhub install infinitycontext --workdir ~/.agents --dir skills
```

Los pasos completos están en [English](#english) y [简体中文](#简体中文).

### Puntos clave

- **Solo Python 3.9+**: biblioteca estándar, **sin red, sin shell, sin subprocesos**.
- **Retención acotada**: 30 días por defecto (`--retention-days 1..3650`); sin límite solo con `--allow-unbounded-retention`; `INFINITY_CONTEXT_NO_ARCHIVE=1` detiene el archivado.
- **Solo el propietario puede leer**: directorio 0700 / archivos 0600 (DACL protegida en Windows), fail-closed.
- **Borrado con doble confirmación**: `cleanup.py` exige `--apply --confirm-destructive` y solo actúa sobre directorios con marcador.

### Licencia

MIT (con **cláusula de atribución obligatoria**): se permite usar todo o parte, incluso variantes modificadas, pero **Pondsi debe figurar siempre como autor**.

---

## Português

### O que é?

InfinityContext é uma skill de agente de IA portátil (um pacote `SKILL.md` padrão): comprime o contexto, arquiva trechos de conversa **anonimizados** em um armazenamento **local** SQLite/FTS5 e recupera detalhes exatos de turnos anteriores. Funciona em dsh, Claude Code, OpenClaw, Cursor, Dify, Ollama e agentes próprios.

### Instalação e uso

```bash
clawhub install infinitycontext --workdir ~/.agents --dir skills
```

O passo a passo completo está em [English](#english) e [简体中文](#简体中文).

### Pontos-chave

- **Apenas Python 3.9+**: biblioteca padrão, **sem rede, sem shell, sem subprocessos**.
- **Retenção limitada**: 30 dias por padrão (`--retention-days 1..3650`); sem limite apenas com `--allow-unbounded-retention`; `INFINITY_CONTEXT_NO_ARCHIVE=1` desliga o arquivamento.
- **Somente o proprietário lê**: diretório 0700 / arquivos 0600 (DACL protegida no Windows), fail-closed.
- **Exclusão com dupla confirmação**: `cleanup.py` exige `--apply --confirm-destructive` e só age em diretórios com marcador.

### Licença

MIT (com **cláusula de atribuição obrigatória**): é permitido usar tudo ou parte, inclusive variantes modificadas, mas **Pondsi deve ser sempre creditado**.

---

## Français

### Qu'est-ce que c'est ?

InfinityContext est une skill d'agent IA portable (un paquet `SKILL.md` standard) : elle compresse le contexte, archive des fragments de conversation **anonymisés** dans un stockage **local** SQLite/FTS5 et retrouve des détails exacts de tours antérieurs. Compatible dsh, Claude Code, OpenClaw, Cursor, Dify, Ollama et agents maison.

### Installation et usage

```bash
clawhub install infinitycontext --workdir ~/.agents --dir skills
```

Les étapes complètes sont dans [English](#english) et [简体中文](#简体中文).

### Points clés

- **Python 3.9+ uniquement** : bibliothèque standard, **pas de réseau, pas de shell, pas de sous-processus**.
- **Rétention bornée** : 30 jours par défaut (`--retention-days 1..3650`) ; illimitée uniquement avec `--allow-unbounded-retention` ; `INFINITY_CONTEXT_NO_ARCHIVE=1` désactive l'archivage.
- **Lecture par le propriétaire seul** : répertoire 0700 / fichiers 0600 (DACL protégée sous Windows), fail-closed.
- **Suppression à double confirmation** : `cleanup.py` exige `--apply --confirm-destructive` et n'agit que sur un répertoire portant le marqueur.

### Licence

MIT (avec **clause d'attribution obligatoire**) : l'usage total ou partiel, variantes modifiées comprises, est autorisé, mais **Pondsi doit toujours être crédité**.

---

## Deutsch

### Was ist das?

InfinityContext ist eine portable KI-Agent-Skill (ein Standard-`SKILL.md`-Paket): Sie komprimiert den Kontext, archiviert **entidentifizierte** Gesprächsausschnitte in einem **lokalen** SQLite/FTS5-Speicher und ruft exakte Details früherer Turns ab. Läuft auf dsh, Claude Code, OpenClaw, Cursor, Dify, Ollama und eigenen Agenten.

### Installation und Nutzung

```bash
clawhub install infinitycontext --workdir ~/.agents --dir skills
```

Die vollständigen Schritte stehen in [English](#english) und [简体中文](#简体中文).

### Kernpunkte

- **Nur Python 3.9+**: Standardbibliothek, **kein Netzwerk, keine Shell, keine Subprozesse**.
- **Begrenzte Aufbewahrung**: standardmäßig 30 Tage (`--retention-days 1..3650`); unbegrenzt nur mit `--allow-unbounded-retention`; `INFINITY_CONTEXT_NO_ARCHIVE=1` schaltet die Archivierung ab.
- **Nur der Eigentümer liest**: Verzeichnis 0700 / Dateien 0600 (unter Windows geschützte DACL), fail-closed.
- **Löschen nur mit doppelter Bestätigung**: `cleanup.py` verlangt `--apply --confirm-destructive` und arbeitet nur in einem Verzeichnis mit Marker.

### Lizenz

MIT (mit **verpflichtender Namensnennung**): Nutzung ganz oder teilweise, auch modifiziert, ist erlaubt — **Pondsi muss jedoch immer genannt werden**.

---

## Русский

### Что это?

InfinityContext — переносимый навык ИИ-агента (стандартный пакет `SKILL.md`): сжимает контекст, сохраняет **обезличенные** фрагменты диалога в **локальное** хранилище SQLite/FTS5 и точно находит детали прошлых ходов. Работает в dsh, Claude Code, OpenClaw, Cursor, Dify, Ollama и собственных агентах.

### Установка и использование

```bash
clawhub install infinitycontext --workdir ~/.agents --dir skills
```

Полные шаги — в разделах [English](#english) и [简体中文](#简体中文).

### Ключевое

- **Только Python 3.9+**: стандартная библиотека, **без сети, без shell, без подпроцессов**.
- **Ограниченное хранение**: по умолчанию 30 дней (`--retention-days 1..3650`); без ограничения — только с явным `--allow-unbounded-retention`; `INFINITY_CONTEXT_NO_ARCHIVE=1` полностью отключает архивирование.
- **Чтение только владельцем**: каталог 0700 / файлы 0600 (в Windows — защищённый DACL), fail-closed.
- **Удаление с двойным подтверждением**: `cleanup.py` требует `--apply --confirm-destructive` и работает только в каталоге с маркером.

### Лицензия

MIT (с **обязательным указанием авторства**): использование целиком или частично, включая изменённые варианты, разрешено, но **Pondsi должен быть указан всегда**.

---

## Security / 安全模型

**Fail-closed by default — nothing is written when a safety check cannot be enforced.**

- **Local only**: no network code, no telemetry, no MCP, no cloud sync anywhere in the package.
- **No shell, no subprocesses**: the four Python scripts never start another program; Windows ACL hardening uses in-process Win32 security APIs.
- **Owner-only archive, fail-closed**: the archive directory is forced to `0700` and files to `0600` (POSIX) or a protected DACL (Windows); the result is re-read to prove it took effect. If owner-only access cannot be enforced, archiving aborts and the half-written database is destroyed (exit 3). `--allow-insecure-storage` is the only opt-out and is reported as `insecure_storage: true`.
- **Fail-closed redaction**: rules are validated and precompiled at startup; a malformed rule file aborts before any database is created. `session_key` is sanitised before it is used for any path or filename.
- **Bounded retention**: 30 days by default, `--retention-days 1..3650`; unlimited retention requires the explicit `--allow-unbounded-retention` flag; `INFINITY_CONTEXT_NO_ARCHIVE=1` disables archiving entirely.
- **Deny-by-default filesystem rules**: `cleanup.py` refuses a directory without the `.infinity-context-archive` marker, deletes only full filenames matching InfinityContext artifacts, never recurses, re-checks every candidate with `lstat`, and does nothing without `--apply --confirm-destructive`.

**默认拒绝 — 任何安全检查无法强制执行时，直接中止而不是降级。**

- **纯本地**：包内没有任何网络代码、遥测、MCP 或云同步。
- **无 shell、无子进程**：四个 Python 脚本从不启动其它程序；Windows ACL 使用进程内 Win32 安全 API。
- **归档仅本人可读，Fail-Closed**：POSIX `0700`/`0600`，Windows 受保护 DACL，并回读校验；无法强制时中止并销毁半成品（退出码 3）。唯一例外是 `--allow-insecure-storage`，且结果中会标记 `insecure_storage: true`。
- **脱敏 Fail-Closed**：规则启动期校验并预编译，规则文件损坏会在建库前中止；`session_key` 在生成任何路径/文件名之前先净化。
- **保留期有界**：默认 30 天，`--retention-days 1..3650`；无限期保留需显式 `--allow-unbounded-retention`；`INFINITY_CONTEXT_NO_ARCHIVE=1` 可彻底关闭归档。
- **默认拒绝的文件系统规则**：`cleanup.py` 拒绝没有 `.infinity-context-archive` 标记的目录，只删除完整文件名匹配本应用产物的文件，不递归，删除前用 `lstat` 复核，且必须同时给出 `--apply --confirm-destructive`。

## 隐私声明 / Privacy Statement

本 Skill 会将对话上下文保存在本地纯内网的 SQLite 中以供检索，系统已内置正则脱敏机制屏蔽常见 API 密钥，且不依赖任何云端同步。所有数据仅存储于本机，不会外传。

This skill stores conversation context in a local-only SQLite database for retrieval. Built-in regex redaction masks common API keys. No cloud sync is used; all data stays on the local machine.

---

Pondsi (+MiMo-v2.5/v2.5pro+deepseek-v4-flash/pro+deepseek-v4.1-flash-expires-on-0910+GLM5.3-flash+Gemini3.1-pro+Qwen3.8-27b+Gemini3.8-flash) — automatically committed by Openclaw
