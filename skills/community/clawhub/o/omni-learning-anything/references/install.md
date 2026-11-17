# Install / 安装

## A. 通用快捷安装 / Install through chat

把下面的指令发送到 Agent 对话框：

```text
请安装 omni-learning-anything：
https://github.com/ShawnRen57/omni-learning-anything
请优先下载 Releases 最新的轻量 Skill ZIP，按当前 Agent 的原生技能安装方式安装，
保留 SKILL.md、scripts、references、agents。检查完整性和当前客户端的原生技能清单，确认已启用；保留现有课程和连接，不覆盖本地修改。安装后告诉我如何用一句话开始。
```

The agent should obtain the latest skill ZIP, use its host's native skill installation mechanism and verify discovery. Read `platforms.md` for host scheduling only after a learning plan is approved. If installation requires a user-operated upload dialog, provide the downloaded ZIP and the precise steps below. Do not replace installation with pasting SKILL.md into an ordinary conversation.

## B. 手动安装 / Manual installation

先从 [Releases](https://github.com/ShawnRen57/omni-learning-anything/releases/latest) 下载 Skill ZIP。解压后的顶层目录为 `omni-learning-anything/`。需要文件夹安装时，复制整个文件夹；需要上传时，选择原 ZIP。以下按 2026-10-09 官方文档或官方客户端界面核对。

### Codex

将解压后的文件夹放入 `~/.agents/skills/omni-learning-anything/`，或项目的 `.agents/skills/omni-learning-anything/`。确认该目录中直接存在 SKILL.md，并以客户端实际技能清单和启用状态为准。未出现时刷新或重启；使用清单显示的调用名，或直接说“用 Omni Learning Anything 带我学习”。

Copy the extracted folder into the user or project `.agents/skills` directory. Verify native inventory/enabled state and use the invocation name reported by the host, or ask in ordinary language to use Omni Learning Anything.

依据：[官方 Skills 文档](https://learn.chatgpt.com/docs/build-skills)，其中也支持通过 `$skill-installer` 从 GitHub 安装。

### WorkBuddy

左侧 **专家 · 技能 · 连接器 → 技能 → 添加技能 → 上传技能**，拖入 ZIP 或点 **选择文件**。导入完成后在已安装列表启用。

Open **Experts / Skills / Connectors → Skills → Add skill → Upload skill**, select the ZIP and enable the imported skill.

依据：[官方技能说明](https://www.codebuddy.cn/docs/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Skills-Market)，并在官方桌面端 5.7.6 核对了“添加技能 → 上传技能”和包格式要求。

### DeepSeek Harness

解压 ZIP，把整个文件夹复制到 `~/.dsh/skills/omni-learning-anything/`，或项目 `.dsh/skills/omni-learning-anything/`。自定义 DSH_HOME 时使用其 `skills/` 子目录。确认技能目录出现 `omni-learning-anything`。

Copy the bundle into the configured user/project DSH skill root. The filesystem provider discovers a folder with SKILL.md one level below that root.

**插件 → 添加插件**安装的是有 package.json 和组合包 patch 的 DSH 插件；当前包按原生文件系统 Skill 方式安装，不能把 Skill ZIP 当作插件组合包填入该对话框。

依据：[官方文件系统 Skill provider](https://github.com/deepseek-ai/deepseek-harness/blob/master/packages/skill/skill-filesystem/README.md)、[官方插件安装说明](https://github.com/deepseek-ai/deepseek-harness/blob/master/packages/client/ui-plugin-manager/README.zh.md)。

### OpenClaw

解压后，在终端运行（替换文件夹路径）：

```sh
openclaw skills install /path/to/omni-learning-anything --global
openclaw skills list
```

也可把完整文件夹放到 `~/.openclaw/skills/omni-learning-anything/`；仅当前工作区使用时放到工作区 `skills/` 中。

Install the local extracted folder with the native `openclaw skills install` command, then check the inventory. Use `--global` for all local agents.

依据：[官方 Skills 文档](https://docs.openclaw.ai/tools/skills)、[官方 CLI 说明](https://docs.openclaw.ai/cli/skills)。Git 仓库安装要求源根目录有 SKILL.md；本仓库的技能在 skills 子目录，因此这里采用已解压的技能文件夹。

### 豆包 / Doubao desktop work mode

左侧 **插件 · 技能 · 伙伴 → 技能 → 添加 → 上传技能**，选择 **选择文件**上传 ZIP，或 **选择文件夹**选择解压后的技能目录。导入后在技能页查看并选用。

Open **Plugins / Skills / Partners → Skills → Add → Upload skill**; choose the ZIP or extracted folder.

依据：[豆包官方客户端](https://www.doubao.com/)。2026-10-09 在官方 macOS 桌面端 2.31.4 的工作界面核对了上述入口及上传弹窗：包或文件夹须包含 SKILL.md，且其 YAML 元数据须包含技能名称和描述。该条依据是官方产品界面，不是第三方教程；普通聊天页没有该入口时，先切换到提供技能功能的工作界面。

## 安装后 / After installation

用一句学习主题开始，例如“用 omni-learning-anything 带我学习西方建筑史”。Agent 检查生成文档所需的环境并收集学习偏好；Python/XeLaTeX 设置见 `setup.md`。安装 Skill 与开始学习是两个步骤，计划确认前不创建每日任务。

## C. One command / npx 安装

Requires Node.js meeting the current skills CLI requirement (tested skills 1.7.4 with Node 24; that CLI requires Node >=22.20). Node is for this installer only; Python is still used by the Skill. Users without Node can use chat/native installation or the ZIP.

```sh
npx skills@latest add ShawnRen57/omni-learning-anything --skill omni-learning-anything -g
```

Select the Agent you actually use. For a project installation, omit `-g`. Agent-operated unattended installation must explicitly select the requested host, for example `-a codex -y` or `-a claude-code -y`; do not install to every host silently. `skills` is the community installer, not this project's npm package. It discovers the complete folder under `skills/omni-learning-anything` in GitHub. Validate against the latest release after installation; repository installs follow main and may include unreleased changes.

```sh
npx skills@latest list -g
npx skills@latest update omni-learning-anything -g
```

Use the same scope for install/list/update. For project installs use list in that project and update with `-p`. The current CLI also accepts `check` as an update alias, so do not recommend it as a read-only update check. A network/proxy or old-Node failure is an installation blocker; keep the selected host and offer the native/ZIP route rather than claiming installation succeeded.

Upstream command and update semantics: [skills CLI](https://github.com/vercel-labs/skills/blob/main/docs/commands.md).

## D. Native Claude Code plugin / 原生插件

In Claude Code (2.1.275+):

```text
/plugin install omni-learning-anything --marketplace ShawnRen57/omni-learning-anything
```

Older versions can add the marketplace, then install:

```text
/plugin marketplace add ShawnRen57/omni-learning-anything
/plugin install omni-learning-anything@omni-learning-anything
```

From the shell the one-step form requires Claude Code 2.1.292+:

```sh
claude plugin install omni-learning-anything --marketplace ShawnRen57/omni-learning-anything
claude plugin details omni-learning-anything@omni-learning-anything
claude plugin marketplace update omni-learning-anything
claude plugin update omni-learning-anything@omni-learning-anything
```

Choose the intended user/project scope; ensure it is enabled for the actual course workspace. The native component inventory must contain the learning Skill. Use the command name shown by the host (plugins may namespace it), or ask in ordinary language to use Omni Learning Anything. A successful clone alone is not invocation or authorization.

The repository includes a versioned plugin manifest plus marketplace. This is a Claude Code distribution wrapper around the same Skill, not an npm dependency or an account connection. [Official plugin documentation](https://code.claude.com/docs/en/discover-plugins).

## E. Installation acceptance and safe updates / 安装验收与更新

The agent runs these steps; learners do not need to manipulate JSON or tokens.

1. Resolve the installed folder, then run `python /installed/omni-learning-anything/scripts/omni_learning.py installation inspect`. It checks bundled entry points, local module dependencies, the course catalog and linked references. `complete` is file completeness; `integrity_verified` additionally requires a matching managed-ZIP receipt. Neither establishes native discovery. Read-only unmanaged inspection recognizes the bounded public `_meta.json` shape used by registries and its matching-version `LICENSE.txt` alias. This is reported as normalization, not authenticity. Keep the metadata and use the original registry updater; ZIP adoption and updates remain strict.
2. Confirm the selected host's native skill/component inventory and enabled state, and use its actual discovered invocation name. Modern Codex may namespace a name; do not guess a fixed `$` command. The official Codex `$skill-installer` accepts the repository plus exact `skills/omni-learning-anything` path and optional release tag. It prints its resolved destination; use that, not an assumed global path. For manual/project installs `.agents/skills/omni-learning-anything` is supported. Reopen/restart only when the host has not reloaded new files. Confirm user/project scope before making a duplicate install.
3. Keep courses, virtual environments and saved connection profiles **outside** every installed Skill/cache folder. Do not write `config.json`, learning records or credentials into the bundle. New course initialization enforces this separation. If an older install already contains courses/local edits, preserve them and agree an external archive location before using an upstream updater.
4. Update only this Skill through its original native manager, and recheck inventory/completeness. Native installers may replace the whole skill directory; this is why course separation is required. Do not use `skills update` without a name (it can update unrelated skills), erase private profiles or reset an existing course. The existing renderer accepts older course schemas and preserves approval hashes; updating Skill files does not approve, retarget or schedule a course.

### Managed ZIP replacement

For a host without an updater, the agent downloads the release Skill ZIP plus SHA256SUMS, verifies the matching entry and obtains the intended standalone Skill destination. Use the updater from the newly downloaded bundle so it understands the new catalog and can validate the previous installed bundle. Never run ZIP replacement against a native plugin cache or a manager-owned symlink.

```sh
python /downloaded/omni-learning-anything/scripts/omni_learning.py installation install --archive /downloaded/skill.zip --destination /host/skills/omni-learning-anything --sha256 VERIFIED_SHA256
python /downloaded/omni-learning-anything/scripts/omni_learning.py installation update --archive /downloaded/new.zip --destination /host/skills/omni-learning-anything --sha256 VERIFIED_NEW_SHA256
```

Placeholders above are replaced by actual verified paths/hash, not sent to the learner to edit. Fresh installation refuses an existing folder. Updates require a matching managed receipt, reject missing/edited/unknown files and symlinks, stage the complete replacement, keep the old directory as a sibling backup and restore it if the swap fails. Report the backup path. No course or profile paths are read or migrated.

An older standalone ZIP/manual copy without a receipt can be enrolled with `installation adopt --archive /downloaded/old-release.zip --destination /host/skills/omni-learning-anything --sha256 VERIFIED_OLD_SHA256`, only when **every** installed file matches that exact trusted historical release. Otherwise retain it and use a fresh destination; never guess or discard local changes. The official Codex installer refuses overwriting an existing destination, so do not repeatedly rerun it as an update. For its unmanaged standalone copy use this verified historical-release enrollment plus managed ZIP update, or preserve it and stage a new copy. Do not adopt an installation managed by the community skills CLI or a native plugin manager.

Host upload/update dialogs (WorkBuddy, Doubao, etc.) remain host-controlled. Choose their update/replace action when available; avoid duplicate installs and recheck discovery. Their historical UI instructions above are not a fresh UI acceptance for every client release.

## F. First course / 首次使用的四个检查点

- **Discovered and callable:** complete files plus actual native inventory/enabled state; show how to start with one sentence. Do not call a file check a successful model invocation.
- **Only necessary setup:** ask/reuse the intended output first. Agent runs `setup-check --platform html` (or the actual selected platform/mode), which returns only that route's missing dependencies and official CLI steps. Python must be 3.10+; install missing packages in an external isolated environment and rerun there. HTML/Markdown/Obsidian need no document libraries; when the OS lacks IANA timezone data, the recipe adds tzdata (common on Windows). Text-PDF input adds pypdf. `doctor --config /private/staging/config.json` then verifies the selected actual settings and host evidence. No output destination is chosen silently.
- **Only necessary connection questions:** reuse a named connection; otherwise ask for the course parent/folder/Vault and guide official login/grants. Browser login is not API authorization. Check identity/location, create and read back the real approved plan through the selected official route and inspect it before claiming delivery. Expired login resumes that step; app setup and location stay remembered. See [onboarding](onboarding.md).
- **Learning continues after updates:** read the original external config/plan/state/learning and receipts; keep named connections outside the bundle. Continue the existing archive instead of reinitializing, overwriting old history, reauthorizing without reason or creating duplicate schedules. Unknown/missing access is surfaced as one concrete recovery action.

On a hard process termination/power loss, inspect the sibling backup and `.omni-learning-anything.install-lock`; confirm no installer is active before restoring the intact backup to an absent target and clearing the stale lock. Do not delete either copy or force-install over an uncertain state. Ordinary replacement errors and Ctrl-C restore an absent old target automatically; uncatchable termination is a recovery case.
