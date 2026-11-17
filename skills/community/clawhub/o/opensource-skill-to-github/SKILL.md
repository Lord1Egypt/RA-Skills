---
name: opensource-skill-to-github
description: >
  Quickly open-source a local skill to GitHub (primary) and optionally clawhub.com.
  Workflow: slug pre-check, fork to opensourceskills, strip internal info, normalize
  SKILL.md, generate LICENSE/README, init git, push to GitHub with configurable token
  source, and optionally publish to clawhub. Use when the user says "open-source this
  skill", "把这个 skill 开源", "发到 github", "publish skill publicly", or "把本地 skill 发开源".
  Hard rules: never modify the original skill in place, never auto-add force/yes flags,
  never write tokens to git/remote/memory, and ask the user at decision points.
---

# Open-source a Local Skill to GitHub (+ optional clawhub.com)

- **Version**: 1.0.19
- **License**: MIT
- **Author**: Evan Song · [github.com/Songhonglei](https://github.com/Songhonglei)
- **Repository**: https://github.com/Songhonglei/build-better-skills/tree/main/skills/opensource-skill-to-github

> 把一个本地 skill 端到端开源到 **GitHub**（主）+ **clawhub.com**（可选）。
> 基于多个 skill 开源实践沉淀的完整方法论（见 `references/opensource_playbook.md`）+ 11 条剔除清单 + 16 项 checklist。
> **质量优先**：每个决策点（LICENSE / slug 冲突 / 内网信息残留 / token）必须等用户拍板。

## 设计哲学

- **副本而非演进**：原 skill 一行不动；副本放 `opensourceskills/<slug>/`，独立 commit / 版本号 / sign。
- **混合形态**：能脚本化的（剔除扫描、git init、frontmatter 校验）走脚本；需要决策的（LICENSE、slug rename、token、敏感部门 visibility）走对话。
- **首版 v1.0.0**：clawhub 用户期望"成熟" first release，不用 v0.x 试探。
- **GitHub 主、clawhub 副**：本 skill 默认走 GitHub，clawhub 在 §6 可选。skills.sh 通过 GitHub 自动同步无需单独操作。
- **不硬编码身份 + 一次配置永久用**：所有作者/handle/邮箱通过持久化 profile 自动读取，跨 agent / 跨 workspace / skill 重装都不丢。

## 首次使用：配置开源身份（一次性，跨 agent 持久化）

```bash
bash scripts/setup_profile.sh
# 交互式问 3 个字段:
#   Author name        (如 "Evan Song")
#   GitHub handle      (如 "Songhonglei")
#   Author email       (推荐 GitHub noreply: "<handle>@users.noreply.github.com")
# 写入 ~/.config/opensource-skill-to-github/profile.env (chmod 600)
```

**为什么这么放**：
- 在用户 `$HOME` 而非 skill 目录 → skill 升级/重装不丢
- 在用户 `$HOME` 而非 workspace → 换 agent / 换 workspace 仍有效（适配 OpenClaw / Claude Code / Cursor 等任意环境）
- XDG 兼容（`$XDG_CONFIG_HOME` 优先），符合 Linux / macOS 用户文件规范

**身份取值优先级**（高 → 低）：
1. 脚本命令行参数显式传入
2. `OSG_AUTHOR_NAME` / `OSG_GITHUB_HANDLE` / `OSG_AUTHOR_EMAIL` 环境变量（适合 CI/CD 或临时覆盖）
3. **`~/.config/opensource-skill-to-github/profile.env`** ← 主要载体
4. `git config --global user.name/user.email` 兜底
5. 仍缺失 → 报错并指引跑 `scripts/setup_profile.sh`

**常用命令**：
```bash
bash scripts/setup_profile.sh             # 首次/重新引导
bash scripts/setup_profile.sh --show      # 查看当前生效配置 + 来源
bash scripts/setup_profile.sh --path      # 打印 profile 路径
bash scripts/setup_profile.sh --non-interactive  # CI 模式，从 env 读
```

**GitHub push token 配置（可选）**：

`github_push.sh` 支持把 token 做成配置项，避免每次真实 repo 发布都重新让用户粘贴。
优先级为：

1. `GITHUB_TOKEN`（一次性环境变量）
2. `OSG_GITHUB_TOKEN`（长期环境变量或 profile；明文，不推荐）
3. `OSG_GITHUB_TOKEN_CMD`（推荐；命令 stdout 第一行返回 token）
4. `gh auth token`（已登录 GitHub CLI 时自动读取）

推荐写法：

```bash
# 放进 ~/.config/opensource-skill-to-github/profile.env
OSG_GITHUB_TOKEN_CMD="gh auth token"

# 或使用 macOS Keychain，不把 PAT 明文写入 profile
OSG_GITHUB_TOKEN_CMD="security find-generic-password -a $USER -s opensource-skill-to-github.github-token -w"
```

脚本不会把 token 写入 git remote、命令输出或 memory。若使用一次性 PAT，推送后仍应撤销。

## 工作流总览（10 步）

每步后面标注「类型」：🔧 脚本（可直接跑）/ 💬 对话（需用户拍板）/ 🔗 引用（调其他 skill）。

> ⚠️ **首次使用先跑** `scripts/setup_profile.sh` 配置开源身份（见上节）。已配置过的用户跳过此步。

| 步骤 | 类型 | 工具 |
|---|---|---|
| 0. slug 预检 | 🔧 | `scripts/precheck.sh <slug>` |
| 1. 决策框架 4 问 | 💬 | 对话 |
| 2. 副本化 | 🔧 | `scripts/fork.sh` |
| 3. 11 条剔除清单扫描 + 拍板 | 🔧 → 💬 | `scripts/strip_scan.sh` 跑完用户拍板每处 |
| 4. SKILL.md frontmatter 规范化 | 🔧 → 💬 | `scripts/check_frontmatter.py` + 手工 edit |
| 5. LICENSE 拍板 + 生成 | 💬 → 🔧 | 对话选类型 → `scripts/gen_license.sh`（author 自动从 profile 读） |
| 6. README + CHANGELOG + .gitignore 生成 | 🔧 | `scripts/scaffold.sh`（author/handle 自动从 profile 读；changelog 独立文件） |
| 7. 本地 git init | 🔧 | `scripts/git_init.sh`（user.name/email 自动从 profile 读） |
| 8. UGLIC 自审（推荐） | 🔗 | 调 `glic-check` skill |
| 9. GitHub repo 创建（用户手工）+ push | 💬 → 🔧 | 用户建 repo + `scripts/github_push.sh <fork> <repo-name>`（handle 自动拼）；**mono-repo 改走子目录增量发版 → §9.4** |
| 10. clawhub 发版（可选）+ memory 沉淀 | 🔧 → 💬 | `scripts/clawhub_publish.sh`（已登录免 token）+ 沉淀文档 |
| 11. 腾讯 skillhub.cn 发版（可选） | 🔧 | `SKILLHUB_CN_TOKEN=skh_xxx scripts/skillhub_cn_publish.sh <fork>` |

> **一键前 6 步**：`scripts/run_all.sh <源skill名或绝对路径> [<new-slug>]` 会串联
> precheck→fork→strip_scan→license→scaffold→git_init（strip 命中仍需人工拍板；
> push / clawhub / skillhub.cn 因需 token + 确认不自动跑，脚本结束打印手动指引）。

### 跨 agent 通用性（v1.0.3）

本 skill 可移植到非 OpenClaw 的 agent（Claude Code / Cursor 等）：

- **源 skill 定位**：`fork.sh` 支持传 skill 绝对路径，或按名在多目录探测
  （`$SKILLS_DIR` → `~/.claude/skills` → `~/.cursor/skills` → `./skills` → `~/.openclaw/workspace/skills`）
- **输出目录**：`OPENSOURCE_OUT_DIR` 覆盖（默认 `./opensourceskills`）
- **独立 git repo**：`git_init.sh` 只认 fork 自己的 `.git`，即使 fork 位于某个已是 git repo 的
  工作区内也不会误提交到父仓库（v1.0.3 修复，附二次校验）
- **内网关键词表**：`OSG_STRIP_KEYWORDS` env 或 `strip_keywords.txt` 文件自定义（换公司内网词）

## Dependencies

### System commands

- **bash** (≥ 4.0)
- **git** (任意现代版本，新建 repo 推荐 ≥ 2.28 支持 `-b main`，老 git 有 `symbolic-ref` 兜底)
- **python3** (≥ 3.8，仅 `scripts/check_frontmatter.py` 使用，零外部包依赖)
- **curl** (用于 Step 9 GitHub repo 存在性预探测 + push 后 sha 验真 + skillhub.cn 发布，可选/按需)
- **rsync** (用于 `fork.sh` 排除 node_modules 复制，缺失时自动回退 `cp -r`)
- **node + npm** (用于安装 `clawhub` CLI；只在 Step 0 预检和 Step 10 clawhub publish 时需要)
- **clawhub** CLI (`npm install -g clawhub`，只在用 clawhub 渠道时需要)

### macOS 兼容

- `base64` 已做兜底（`-w0` BSD 不支持 → 回退 `base64 | tr -d '\n'`）
- 其它命令（`find` / `grep` / `sed` / `awk`）使用 POSIX 子集，跨平台兼容

---

## Step 0: slug 冲突预检（必须第一步）

**默认 slug 沿用源 skill 名**（即 `<source-skill-name>`），先用源 skill 名查重，命中再进入 rename 子流程。

```bash
scripts/precheck.sh <source-skill-name>
# 实际执行:clawhub inspect <source-skill-name>
```

| 命中情况 | 处理 |
|---|---|
| 未注册 | ✅ 安全继续，slug = source-skill-name |
| 同 owner 同名 | 升版本号直接 publish 即可（不需开源新流程） |
| **别人 owner 同名** | **必须换 slug**（加品牌前缀 `claw-` / `openclaw-` / 自定义）— 让用户拍板新 slug，重跑 precheck 直到通过 |
| 名字不同但概念高度雷同 | 让用户读对方 SKILL.md 决定差异化定位 |

**Why**：clawhub 不支持 slug rename，一旦 publish 就锁死。`agent-memory-manager` 真撞过 georges91560 已注册同名，预检省 80+ 分钟返工。

**退出码**：
- `0` = 未注册可继续
- `3` = 已注册需用户决策
- `4` = 网络异常（重跑）

---

## Step 1: 决策框架（开源前 4 问，对话拍板）

向用户确认：

1. **这个 skill 该不该开源**：内网耦合多 ≠ 不能开源，可以走"重制版"思路
2. **走"原 skill 直接演进"还是"副本剥离"**：内网仍有用户 → 副本；只有少量内网细节 → 演进
3. **副本起点**：已发版稳定版（推荐，更可控），不要拿 dirty WIP 当起点
4. **重制版要不要扩范围**：可以加，但只在副本里加，内网版按原节奏走

**默认选副本**（本 skill 整套流程围绕"副本"设计）。

---

## Step 2: 副本化

```bash
scripts/fork.sh <source-skill-name> [<new-slug>]
# 默认:cp -r skills/<source> opensourceskills/<source>
# 若 slug 改名:opensourceskills/<new-slug>
# 自动删:sign.key、.install-source.json、__pycache__/、*.pyc、.skill-data/、skill_meta.json、*.json.md
```

**强约束**：副本和内网版**独立 commit、独立版本号、独立 sign.key**。绝不原地改原 skill。

---

## Step 3: 11 条剔除清单（扫描 + 报告）

```bash
scripts/strip_scan.sh <fork-path>
# 跑两轮:
#  ① 文件层:列必删项当前状态（sign.key / __pycache__ / USAGE.md 重复等）
#  ② 字面层:grep 内网关键词（公司内网域名 / 平台代号 / sso_token 等，见 strip_keywords 配置）
# 输出:零命中 / 命中位置清单
```

完整 11 条清单和替换映射见 `references/strip_checklist.md`。**复杂或大量字面替换的细节场景**，可参考 `references/opensource_playbook.md` 第 3 节做深度处理（progressive disclosure）。

**报告输出后必须对话**：grep 命中的每一处由用户拍板「保留 / 删除 / 改写」，AI 不自决。

---

## Step 4: SKILL.md frontmatter 规范化

**frontmatter 跨 agent 兼容硬约束 3 条**（hello-env v1.0.0→v1.0.2 实证）：

1. `description` 用 `>` folded scalar（避免引号转义）
2. `description` ≤ 1024 字节（Anthropic 上限）
3. frontmatter **只留 `name` + `description`**——`version` / `metadata` / `author` / `tags` 都搬到 Markdown body

**Markdown body 顶部 4 行（必加）**：

```markdown
- **Version**: 1.0.0
- **License**: MIT
- **Author**: <real name> · [github.com/<handle>](https://github.com/<handle>)
- **Repository**: https://github.com/<handle>/<repo-name>
```

⚠️ clawhub 卡片**只解析 SKILL.md 顶部**，README 写得再漂亮都不算。

校验工具：`scripts/check_frontmatter.py <skill-path>`（4 项校验，0 ERR 才放行）。

---

## Step 5: LICENSE 拍板 + 生成

**必须问用户拍板**，AI 不自填：

- **MIT**（推荐，最宽松，clawhub 强制 MIT-0 也兼容；脚本生成的是完整法律文本）
- **Apache 2.0**（带专利条款，适合有专利防护需求；⚠️ 脚本生成的是**缩略版引用文本**，商用场景请从 https://www.apache.org/licenses/LICENSE-2.0.txt 替换完整文本）
- **GPL-3.0**（强 copyleft，谨慎使用；⚠️ 同样是缩略版，完整文本见 https://www.gnu.org/licenses/gpl-3.0.txt）

```bash
scripts/gen_license.sh <fork-path> <MIT|Apache-2.0|GPL-3.0> "<real name>" <year>
```

⚠️ 对外署名规则：用对外身份（如 `Jane Doe`）+ 公网邮箱（`*@gmail.com` 等），**不用内网邮箱**。
⚠️ 脚本会自动清洗作者名中的换行/反引号/分号等危险字符。

---

## Step 6: README.md + CHANGELOG.md + .gitignore 生成

```bash
scripts/scaffold.sh <fork-path>
# 生成:
#   README.md    ← 模板含 Quick Start / Features / Install / License / Author；Changelog 段只留指针
#   CHANGELOG.md ← 独立版本历史（Keep a Changelog 惯例），初始含 v1.0.0 条目
#   .gitignore   ← 通用安全规则（id_rsa / *.p12 / *.keystore / certs/*.key / .env / node_modules / __pycache__ 等）
```

**Changelog 惯例（强约束）**：版本历史一律放独立 `CHANGELOG.md`——
- ❌ 不放 SKILL.md：agent 每次触发都读 SKILL.md，历史记录纯属上下文浪费
- ❌ 不堆 README：版本多了喧宾夺主
- ✅ SKILL.md / README 各留一行指针 `See [CHANGELOG.md](./CHANGELOG.md)`
- strip_scan.sh 会检测 SKILL.md 内嵌 changelog（≥2 条版本记录即 WARN）

README 模板见 `references/readme_template.md`。

---

## Step 7: 本地 git init + 身份配置

```bash
scripts/git_init.sh <fork-path> "<user.name>" "<user.email>"
# 执行:
#   git init -b main
#   git symbolic-ref HEAD refs/heads/main  ← 老 git 兜底
#   git config user.name / user.email      ← 必须，容器 git 没有默认
#   git add . && git commit -m "Initial commit: v1.0.0"
```

**Why**：容器/PVC 环境 git 没有默认 user.name/email，commit 直接报"不允许空的姓名"（glic-check 首发踩过）。

---

## Step 8: UGLIC 自审（可选但强烈推荐）

调用 **`glic-check`** skill 跑 UGLIC 5 维（U/G/L/I/C）：

- **0 ERR** 才放行；WARN 全修或文字说明保留理由
- audit/check 类 skill 额外做「自审 + 三档样本」

```bash
# 引用 glic-check skill 跑
# 不在本 skill 内重复实现
```

完整规则见本 skill `references/uglic_quickref.md` 或直接读 glic-check skill。

---

## Step 9: GitHub repo 创建 + push

> ⚠️ **mono-repo 安全护栏（2026-08-02 新增）**：`github_push.sh` 推送前会检测目标 repo 根目录是否含 `skills/` 目录。若检测到（说明是 mono-repo），脚本会 **exit 8 拒绝推送**，并给出「子目录模式」手动发布指引。这是因为本流程把单个 skill 当 repo 根目录推到 main，会 force-overwrite 掉 mono-repo 里 `skills/` 下的所有其它 skill（`better-office-work-flow` 仓库 08-02 被这样冲掉过：4 skill → 1 skill）。对 mono-repo **必须**改用子目录模式（clone 目标 repo → 放进 `skills/<slug>/` → commit → push），绝不能直接推 fork 的 main。如确需清空 repo 只留这一个 skill，设 `OSG_ALLOW_MONOREPO_OVERWRITE=1`。**对 mono-repo 的正确做法见 §9.4。**

### 9.1 用户操作（必须用户做，AI 不能自动）

1. 浏览器登录 GitHub → 新建 repo `<repo-name>`（**勾 main 分支**，不勾 README/LICENSE/gitignore）
2. token 可用已配置来源（推荐 `OSG_GITHUB_TOKEN_CMD` / `gh auth token`）；若没有配置，再生成 Personal Access Token（PAT）并只通过环境变量传一次

### 9.2 Token 配置与卫生（铁律）

⚠️ **用户贴 token 时第一条回复必须**：
> "我收到了，会用环境变量传一次不落盘，跑完请去 GitHub Settings → Tokens 撤销这个 PAT。"

推荐长期配置：

```bash
# profile.env 里配置 token 读取命令，避免每次发布重新粘贴
OSG_GITHUB_TOKEN_CMD="gh auth token"
```

也支持：

```bash
GITHUB_TOKEN=ghp_xxx scripts/github_push.sh <fork-path> <github-handle>/<repo-name>
OSG_GITHUB_TOKEN=ghp_xxx scripts/github_push.sh <fork-path> <github-handle>/<repo-name>
```

`OSG_GITHUB_TOKEN` 可写进 profile，但这是明文 token，只在用户明确要求时使用；默认推荐 `OSG_GITHUB_TOKEN_CMD` 接 GitHub CLI 或 macOS Keychain。

### 9.3 推送（带 Basic Auth 重试，适配受限网络）

```bash
scripts/github_push.sh <fork-path> <github-handle>/<repo-name>
# 实际执行:
#   发布前自动清理派生缓存（_lib_exclude.sh: __pycache__/*.pyc/.DS_Store 等）
#   token 来源: GITHUB_TOKEN → OSG_GITHUB_TOKEN → OSG_GITHUB_TOKEN_CMD → gh auth token
#   AUTH_B64=$(printf "x-access-token:%s" "$RESOLVED_TOKEN" | base64 -w0)
#   git remote add origin https://github.com/<handle>/<repo>.git
#   for i in 1..5: timeout 60 git -c http.extraHeader="Authorization: Basic $AUTH_B64" push origin main && break
```

**Why Basic Auth header**：某些受限网络环境 push GitHub 时 bearer 已不认，必须用 Basic Auth header 注入；token 不进 remote URL。

push 完成后：如果本次用了临时 PAT，再次提醒用户 **去 GitHub Settings 撤销 PAT**；如果用的是 GitHub CLI / Keychain 长期配置，不要求每次撤销。

### 9.4 mono-repo 子目录增量发版（实际更常用）

**何时走这条**：目标 repo 是 **mono-repo**——根目录有 `skills/`，一个 repo 装多个 skill（本 skill 自己的家 `build-better-skills` 就是）。此时**不要**跑 `github_push.sh`（护栏会 exit 8 拦住，见 Step 9 开头的告警），改用子目录增量发版。

**「增量」的含义**：只动 `skills/<slug>/` 这一棵子树，其它成员一个字节都不碰。**首发新成员**和**给已有成员发新版**是同一条路径，只差 commit message。

**用常驻克隆，不要每次 clone 到 /tmp**：本机 `~/skills/<repo>/` 通常已有该 repo 的常驻克隆，直接复用它——省一次全量拉取，也避免 `/tmp` 副本和常驻克隆互相混淆。

```bash
SLUG=<skill-slug>
SRC=~/.workbuddy/skills/$SLUG/          # 源 skill（唯一真实维护点）
REPO=~/skills/<repo-name>               # 目标 mono-repo 的常驻克隆

# 1. 同步 源 → repo 子目录（末尾斜杠：把内容同步进去）
rsync -a --delete "$SRC" "$REPO/skills/$SLUG/"

# 2. 确认只动了这一个成员（其它成员零 diff）
cd "$REPO" && git status --short

# 3. 提交 + 推送
git add "skills/$SLUG" && git commit -m "$SLUG v<x.y.z>: <一句话>"
git push origin main                    # 受限网络见下「两个网络坑」
```

**Why `--delete`**：增量发版最容易出的错是「新增的文件进得去、删掉的文件出不来」，一轮轮攒下来 repo 里留着源目录早已没有的旧文件。`--delete` 让子目录与源严格一致，也让 `git status` 的第 2 步判别可信。

**两个网络坑（2026-10-06 实测，中国大陆网络环境）**：

| 症状 | 真因 | 解法 |
|---|---|---|
| `git push` 长时间挂起或报连接失败 | `github.com:443` 被墙，但 **`api.github.com` 通** ⚠️ 容易误判成"网没问题" | 走本机代理：`git -c http.proxy=http://127.0.0.1:<port> -c https.proxy=http://127.0.0.1:<port> push origin main`（端口看你本地代理软件） |
| `raw.githubusercontent.com` 取不到内容 | 该域名被墙 | **验真改走 GitHub API**，别用 raw |

**推送后必须验真**（raw 不通，用 API）：

```bash
API=https://api.github.com/repos/<owner>/<repo>/contents/skills/<slug>
# ① 远端版本号（取 SKILL.md 正文 base64 解码后再正则）
curl -s "$API/SKILL.md?ref=main" | python3 -c "
import sys,json,base64,re
c=base64.b64decode(json.load(sys.stdin)['content']).decode()
print('远端 Version:', re.search(r'\*\*Version\*\*:\s*([\d.]+)', c).group(1))"
# ② 新增文件是否真进包（光看本地 commit 不算数）
curl -s "$API/scripts?ref=main" | python3 -c "
import sys,json; [print(' ', x['name'], x['size'], 'bytes') for x in json.load(sys.stdin)]"
```

**万一推错（把 repo 根当 main 推上去，冲掉了成员）**：内容通常还能捞回来——`git reflog` 找覆盖前的 commit，或到 GitHub 上找那次 force-push 留下的**孤立提交**（`better-office-work-flow` 2026-08-02 就是这么从孤立提交 `63ae4858` 恢复的）。**第一反应是停手**，不要再推第二个版本，否则孤立提交会被覆盖掉、就真找不回了。

---

## Step 10: clawhub 发版（可选）+ memory 沉淀

### 10.1 clawhub publish（可选）

```bash
CLAWHUB_TOKEN=clh_xxx scripts/clawhub_publish.sh <fork-abs-path>
# 注意:
#   - 发布前自动清理派生缓存（_lib_exclude.sh: __pycache__/*.pyc/.DS_Store 等）
#   - 必须用绝对路径（相对路径偶发 SKILL.md required 报错）
#   - clawhub 强制 LICENSE 为 MIT-0（本地 LICENSE 文件被忽略，平台特性不是 bug）
#   - clawhub 没有 visibility 参数，用 hide/unhide 控制
#   - rate limit 11999/12000 → sleep 30s 重试
```

⚠️ **CLAWHUB_TOKEN 与 GitHub token 完全独立**；临时 token 分别撤销，长期配置分别管理。

### 10.2 受限发布环境的 visibility（部分内网 hub 特有）

某些内网 hub 会把特定用户/部门标记为「受限」，禁止公开可见（常表现为静默降级为 private）。

- ⛔ 该类 hub publish 不能设为 public（会强制软降级 private）
- ✅ **禁止**自作主张加 `--visibility private` 救场——降级后 PUT edit 也可能改不回来
- ✅ 正确做法：去掉 `--visibility` 参数让发版工具取 Hub 当前值回填
- ✅ **clawhub / GitHub / skills.sh 不受此限制**，可正常公开
- ✅ 调 publish/edit 后**禁止信 response 字段汇报**，必须 detail + PUT edit 空 body 双查真实落库值

### 10.3 memory 沉淀

提示用户创建 `memory/project_<slug>_opensource_fork.md`，记录：
- 决策：为什么开源、为什么走副本、首版号怎么定
- 改造：CLI 设计、env 变量命名、跨平台兜底
- 经验：用户拍板的设计问题清单
- 关联：指向上一个开源 skill 的 memory（链式继承）

通用经验沉淀到 `feedback_*.md`。

> ⚠️ **沉淀内容红线**：memory 笔记只记「决策与经验」，**严禁写入任何 token / secret / 明文凭证，也不要抄录内部路径、内网域名、平台代号等敏感上下文**。这与 §8「token 绝不落盘到 git/remote/memory」的硬规则一致——发布后的复盘笔记同样受此约束。

---

## 常见反模式（一定要避开）

| ❌ 反模式 | ✅ 正确做法 |
|---|---|
| 副本里改的同时改原 skill | 原 skill 不动，只动副本 |
| 副本目录名带 `-os` / `-opensource` 后缀 | 用 `opensourceskills/<原名>/`，slug 跟原名一致 |
| 用 `v0.1` / `v0.x` 试探发版 | 直接 `v1.0.0`（clawhub 期望"成熟" first release） |
| GitHub repo 用 `dev` / `master` 默认分支 | 必须 `main`（老 git `git symbolic-ref HEAD refs/heads/main` 兜底） |
| LICENSE 自填假名字 / 占位贡献者 | 必须问用户拍板 + 真名署名 |
| 把内网 grep 结果直接贴 chat | 任何内网 grep 输出先脱敏再贴 |
| frontmatter 塞 version / metadata / tags | 只留 name + description |
| changelog 塞进 SKILL.md / 堆在 README | 独立 CHANGELOG.md，SKILL.md/README 留指针 |
| 凭 response 字段判定 visibility 发版成功 | 必须 detail 接口二次 GET 验真 |
| AI 自动加 `--force` / `--yes` / `--i-am-sure` | 必须用户文字确认 |
| token 写入 git remote / memory / 日志 | token 只进环境变量或 `OSG_GITHUB_TOKEN_CMD`；profile 明文 token 仅在用户明确要求时使用 |

---

## 进一步参考

- `references/strip_checklist.md` — 11 条剔除清单 + 字面替换映射
- `references/readme_template.md` — README.md 模板
- `references/uglic_quickref.md` — UGLIC 5 维速查
- `references/precedents.md` — 11 个已开源 skill 先例 + 教学价值
- 完整开源方法论：`references/opensource_playbook.md`（16 节全流程 + 快速 checklist）
- 字面剔除深度场景：`references/opensource_playbook.md` 第 3 节 + `references/strip_checklist.md`

---

## 版本

当前 **v1.0.19**。完整版本历史见 [CHANGELOG.md](./CHANGELOG.md)。
