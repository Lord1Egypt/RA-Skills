# Changelog

All notable changes to this skill are documented here.
Format loosely follows [Keep a Changelog](https://keepachangelog.com/); versions follow [SemVer](https://semver.org/).

### v1.0.19 (2026-10-06)
- **新增 SKILL.md §9.4「mono-repo 子目录增量发版」**（`references/opensource_playbook.md` §14.4 补英文对照）：此前只有 v1.0.17 的护栏——它告诉你「不能把 fork 的 main 推到 mono-repo」，却没写「那正确该怎么做」。
  - 写清增量发版完整流程：复用常驻克隆 → `rsync -a --delete` 同步进 `skills/<slug>/` → `git status` 只应见该子树 → commit → push；并说明**首发新成员**与**给已有成员发新版**是同一条路径，只差 commit message。
  - **补两个实测网络坑（2026-10-06）**：① `github.com:443` 被墙但 `api.github.com` 通，push 需走本机代理——症状是长时间挂起，容易被误判成「网络没问题」；② `raw.githubusercontent.com` 不通，验真改走 GitHub API `contents/`（base64 解码查 `**Version**`，并查新增文件是否真进包）。
  - 补「推错后的恢复」：`git reflog` 或 force-push 留下的孤立提交（2026-08-02 从 `63ae4858` 恢复的先例），并强调**先停手**、别再推第二个版本。
- **修正版本号不同步**：SKILL.md 头部停在 `1.0.17`、底部停在 `1.0.10`，而 CHANGELOG 已到 `1.0.18`——v1.0.18 那次提交只改了 CHANGELOG 与脚本，漏改 SKILL.md 这两处。本次统一为 1.0.19。

### v1.0.18 (2026-09-05)
- **修复 skillhub.cn 发版丢失 changelog**：`scripts/skillhub_cn_publish.sh` 的 payload 原先只构造 `slug/name/displayName/summary/description/version/claimSlug/joinContest`，**缺 `changelog` 字段**，导致平台上每个版本都显示默认文案 `Initial release`。
  - **定位**：对比同一 skill 在平台上的两个版本——1.3.3 由另一调用方带 changelog 发布即显示正常，走本脚本发布的 1.3.4 变成 `Initial release`，确认为脚本局限而非发版失败。
  - **改为自动提取**：独立 `CHANGELOG.md` 首条版本标题优先（正则兼容 `## [1.0.0] - date` / `### v1.0.17 (2026-08-03)` / `## 1.0.3` 三种常见写法）→ 回退 SKILL.md 内嵌变更日志首条（自动剥离列表符、加粗标记、结尾孤立冒号）→ 都没有则留空。
  - **不用空串覆盖平台默认**：仅当提取到内容时才带 `changelog` 字段；截取 300 字符。
  - 同时在脚本输出里回显提取结果，提取不到时打 warning，便于发版前自检。

### v1.0.17 (2026-08-03)
- **新增 mono-repo 安全护栏**：
  - **背景**：2026-08-02 `better-office-work-flow` 仓库被本流程冲掉——把单个 skill 当 repo 根目录推到 main，force-overwrite 了 `skills/` 下的 4 个 skill（事后从孤立提交 `63ae4858` 恢复）。
  - **修复**：`github_push.sh` 推送前检测目标 repo 根目录是否含 `skills/` 目录，若是则 **exit 8 拒绝推送**，并给出「子目录模式」手动发布指引（clone → 放进 `skills/<slug>/` → commit → push）。设 `OSG_ALLOW_MONOREPO_OVERWRITE=1` 可显式放行。
  - **SKILL.md** Step 9 同步加告警。
- **修正 Repository 地址**：从不存在的 `github.com/Songhonglei/opensource-skill-to-github` 改为正确的 mono-repo 路径 `github.com/Songhonglei/build-better-skills/tree/main/skills/opensource-skill-to-github`。

### v1.0.16 (2026-07-30)
- **热修复 `skillhub_cn_publish.sh` 的 `set -e` 崩溃（v1.0.15 引入）**：
  - **根因**：v1.0.15 的两级版本提取里，`grep` 无匹配时返回非零，在 `set -euo pipefail` 下直接中断脚本——对「只有正文 `**Version**`、无 frontmatter `version:`」的 skill（本 skill 自己就是）必崩，无任何报错输出。
  - **修复**：两处 `grep` 管道补 `|| true`，无匹配时安全返回空串走回退逻辑。四种场景 + set -e 实跑均验证通过。

### v1.0.15 (2026-07-30)
- **`skillhub_cn_publish.sh` 版本提取修复（优先读 frontmatter）**：
  - **根因**：v1.0.14 及之前版本提取只匹配正文 `**Version**: x.y.z`，但部分 skill（如 invoice-auto-forward）只在 frontmatter 声明 `version: x.y.z`、正文无 Version 行，导致发布时回退成错误的 `1.0.0`，每次都要手动补正文行。
  - **修复**：改为两级提取——优先 frontmatter `version:` 字段 → 回退正文 `**Version**: x.y.z` → 最终兜底 `1.0.0`。四种场景（仅 frontmatter / 仅正文 / 两者都有取 frontmatter / 都没有）均验证通过。

### v1.0.14 (2026-07-28)
- **安全措辞与注释加固（响应 clawhub SkillSpector review，无功能变化）**：
  - `_lib_profile.sh`：在通过 `sh -c "$OSG_GITHUB_TOKEN_CMD"` 取 token 的分支上方补安全注释，明确该值仅应来自用户可信 profile / 环境变量，等同 shell rc 中的命令，不得赋以外部/不可信输入。
  - `setup_profile.sh`：收紧明文 token（`OSG_GITHUB_TOKEN="ghp_xxx"`）选项的注释——标注仅限隔离本地环境、用户明确要求时使用，生产禁用，优先命令式取 token。
  - `SKILL.md`：memory 沉淀章节新增红线声明——复盘笔记严禁写入任何 token/secret/明文凭证及内网路径/域名/平台代号，与 token 绝不落盘的硬规则对齐，消除审查指出的「规则自相矛盾」。

### v1.0.13 (2026-07-22)
- **跨平台修复（`clawhub_publish.sh` 发布在 macOS 默认 bash 3.2 下失败）**：
  - **根因**：v1.0.12 为修 `set -u` 空数组 unbound，把发布命令前缀写成 `"${CLAWHUB_ENV[@]:-}"`。但在 macOS 默认 `/bin/bash` 3.2.57 下，`${ARR[@]:-}` 对**空数组**会展开成「1 个空单词」，使命令变成 `"" clawhub ...` → bash 去 exec 一个空命令名 → **exit 126**，被重试 3 次 × 30s 后报「Publish failed」。该路径正是**最常见**的已登录态。
  - **修复**：彻底弃用空数组前缀，改为 `if [[ -n "${CLAWHUB_TOKEN:-}" ]]` 显式分支——`env "CLAWHUB_TOKEN=$x" clawhub ...` 或直接 `clawhub ...`。两条路径在 bash 3.2(Linux/macOS) 与 4/5 下均安全，无 unbound、无空命令名。
  - **附带加固**：`whoami` 的 ANSI 色码剥离由 `sed 's/\x1b...//g'`（GNU-only，`\xHH` 在旧版 BSD sed 不支持）改为 `sed $'s/\033\[...//g'`（bash ANSI-C 引号提前展开 ESC 字节，GNU/BSD sed 都能匹配字面 ESC），消除旧 macOS 上的潜在残留色码。

### v1.0.12 (2026-07-22)
- **Bug 修复（`clawhub_publish.sh` 在 `set -u` 下静默退出）**：
  1. `WHO: unbound variable`（原 line 48/52/54）——根因① `clawhub whoami` 的 spinner / ✔ 全在 **stderr**（stdout 为空），原 `2>/dev/null` 把用户名也丢了；根因② bash `set -u` 在 `[[ ]] && VAR=...` 命令替换边界会把变量「已设置」标记搞乱，下一行引用误报 unbound。修复：① `whoami` 改 `2>&1` 捕获 + 去 ANSI 色码；② 解析结果存 `WHO_PARSED`，用 `if` 而非 `&&` 赋值；③ echo 用 nounset 安全的 `${WHO:-已登录用户}`
  2. `CLAWHUB_ENV[@]: unbound variable`（原 line 77）——空数组在 `set -u` 下直接引用报 unbound。修复：引用改 `${CLAWHUB_ENV[@]:-}` 兜底返回空

### v1.0.11 (2026-07-22)
- **macOS 兼容修复**：`github_push.sh` 两处 `timeout` 命令在 macOS 原生不存在，改为优先 `gtimeout`（brew coreutils）→ `timeout`（GNU coreutils）→ 无超时直接跑（兜底），消除 `command not found` 导致 push 5 次重试全部假死的问题

### v1.0.10 (2026-07-17)
- Codify the changelog convention into the workflow itself: `scaffold.sh` now generates a standalone `CHANGELOG.md` (Keep a Changelog style) and the README template's Changelog section is a pointer; `strip_scan.sh` warns when SKILL.md embeds a changelog (>=2 version entries) with split guidance; SKILL.md Step 6 docs + anti-pattern table updated

### v1.0.9 (2026-07-17)
- Docs: move changelog out of SKILL.md into this standalone CHANGELOG.md (open-source convention); README/SKILL.md keep pointers

### v1.0.8
- **新增 `_lib_exclude.sh` 发布前统一排除清理**：`github_push.sh` / `clawhub_publish.sh` / `skillhub_cn_publish.sh` 三个发布脚本在动手前自动物理清理派生缓存——`__pycache__/` `.pytest_cache/` `.mypy_cache/` `.ruff_cache/` `.tox/` `htmlcov/` 目录 + `*.pyc` `*.pyo` `.DS_Store` `Thumbs.db` `.coverage` 文件。解决典型坑：audit 阶段 `py_compile` 复活 `__pycache__` → 部分 hub 平台拒收 `.pyc`（此前每次都要手动 `find -name __pycache__ -exec rm`）。支持 fork 根目录放 `.osg-exclude`（每行一个 find 模式，# 注释）追加自定义排除，内置防呆拒绝 `*` / `*.py` / `SKILL.md` 等危险模式；`skillhub_cn_publish.sh` 文件收集白名单同步补 `tests/` / `*.pyc` / `__pycache__/` / `.osg-exclude` 跳过

### v1.0.7
- **Bug 修复（dogfood 自发时暴露）**：`clawhub_publish.sh` 把 clawhub 的 `Version X already exists` 当失败重试——首轮其实已发布成功（clawhub Latest 已更新），但重试再发时平台报"已存在"，脚本误判为失败打出 `❌ Publish failed after 3 retries`。修复：捕获 publish 输出，命中 `already exists` 时识别为**幂等成功**（跳过重试 + 提示"如需重发先 bump 版本号"），不再假报错

### v1.0.6
- **Bug 修复（skill-to-http 开源时实测暴露）**：`clawhub_publish.sh` 在已登录态分支解析 `clawhub whoami` 输出的那行——`WHO="$(clawhub whoami | grep -v Checking | tr -d '✔ ' | tail -1)"`——在 `set -euo pipefail` 下会**静默杀死整个脚本、零输出退出**（真实 CLI 复现 rc=1）。根因：新版 clawhub CLI 把 spinner（`- Checking token` / `✔ <user>`）打到 stdout，管道下游 `tail` 提前关闭 stdout 使 `clawhub whoami` 因 SIGPIPE 非零退出，`pipefail` 采纳该非零码。修复：解析行加 `|| true` 兜底吸收管道非零 + `WHO="${WHO:-已登录用户}"` 空值兜底（whoami 前置判断已确认登录成功，用户名只是提示文案，解析失败不应阻断发布）。现象反直觉：`clawhub whoami` 单独跑明明成功、脚本却零输出退出——优先怀疑 pipefail + spinner SIGPIPE，而非登录态本身

### v1.0.5
- **Bug 修复①（agent-easy-http 开源时实测暴露）**：`git_init.sh` 传**相对路径**（如 `opensourceskills/<slug>`）时，脚本先 `cd "$FORK"` 后又在二次校验 `EXPECTED_GITDIR="$(cd "$FORK" && pwd -P)/.git"` 里对同一相对路径再 `cd` 一次 → 从新 CWD 解析失败报「没有那个文件或目录」→ git init 成功但 commit 未执行。修复：验证目录存在后**立即把 `$FORK` 解析为绝对路径**（`FORK="$(cd "$FORK" && pwd -P)"`），后续所有 `cd` / 校验均基于绝对路径，相对/绝对入参都稳定
- **Bug 修复②（macOS BSD grep 兼容，用户 Mac 实测暴露）**：`run_all.sh` / `git_init.sh` / `skillhub_cn_publish.sh` / `clawhub_publish.sh` 共 6 处用了 `grep -oP '...\K...'`（`-P` = Perl 正则，仅 GNU grep 支持）。macOS 自带 **BSD grep 不支持 `-P`**，直接报 `invalid option -- P` 退出 → 变量解析为空 → 触发 `[[ -z ... ]]` 提前 exit（`run_all.sh` 卡在 fork 之后 / 版本号取不到）。统一改为 BSD+GNU 通用写法：`grep -o '整行前缀.*'` 抓整行 + `sed` / `grep -o` 剥前缀，效果等价 `\K` 后向剥除，全平台可移植（`-m` / `[[:space:]]` 亦 BSD/GNU 通用）

### v1.0.4
- **Bug 修复**（dogfood 自举开源时实测暴露）：`fork.sh` 的 cp 回退分支只删了 node_modules/.git，未清 rsync 分支同样排除的 `.skill-data/output/__pycache__/*.pyc/opensourceskills`，导致 rsync 不可用环境下嵌套子目录被误复制进副本；rsync 分支也补排 `opensourceskills/`
- **Bug 修复**：`skillhub_cn_publish.sh` 用 `-F "payload=$内联字符串"` 发 multipart，当 displayName/summary 含空格或括号时被 curl 截断成非法 JSON（报 `payload JSON 格式错误`）；改为写临时文件 `-F "payload=<file"` 从文件读

### v1.0.3
- **P0 修复**：`git_init.sh` 不再用 `git rev-parse --git-dir`（会穿透父仓库），改为只认 fork 自己的 `.git` + 二次校验，修复「fork 位于 git repo 内时误提交到父仓库」的坑（跨 agent 环境必现）
- **P0 修复**：`fork.sh` 去除 `~/.openclaw/workspace` 硬编码，支持绝对路径 + 多 agent skills 目录探测 + `OPENSOURCE_OUT_DIR`；fork 时排除 node_modules/.git/output
- **P0 修复**：`clawhub_publish.sh` 优先用已登录态（免 token）+ 自动补 `--version`（从 SKILL.md 提取）
- **P1**：`github_push.sh` 默认 `http.version HTTP/1.1` + `http.postBuffer 524288000`（大文件/弱网兜底）+ push 后内建 sha 验真（GitHub API 优先，ls-remote 回退）
- **P1**：新增 `skillhub_cn_publish.sh`（腾讯 skillhub.cn target，multipart，displayName/summary 自动提取，白名单剔除 LICENSE/.gitignore/archive）
- **P1**：`strip_scan.sh` 关键词表支持 `strip_keywords.txt` 外置文件（换公司内网词）
- **P1**：本 skill 自身署名脱敏为 Evan Song
- **P2**：新增 `run_all.sh` 一键串联前 6 步

### v1.0.1 (2026-07-13)
- Fix `fork.sh` cp-fallback branch to clean all rsync-excluded paths (`.skill-data`/`output`/`__pycache__`/`*.pyc`/`opensourceskills`); rsync branch also excludes `opensourceskills/`
- Fix `skillhub_cn_publish.sh` multipart payload truncation — write payload to a temp file and read via `-F "payload=<file"` instead of an inline string

### v1.0.0 (2026-07-13)
- Initial public release
- Configurable internal-keyword scanning (generic defaults + user-configured company words)
- Bundled vendor-neutral open-source playbook
- 4-tier GitHub token source + push sha verification
- Cross-platform (macOS bash 3.2 compatible)
