---
name: migration-pack-deploy
description: 帮用户把 AI 助手（谢尔比）从一台电脑"搬"到另一台。用户说想迁移/换电脑/换平台/打包带走时，帮他打包成一个 zip；到了新电脑说部署/还原时，帮他自动放回原位，完成迁移闭环。对用户零技术要求，全程代劳。关键词：迁移、换电脑、换平台、打包、部署、新机器、还原、migrate、pack、deploy。
agent_created: true
---

# 迁移打包与部署

## 这是什么（给用户看的）
用户换电脑时，担心"换个地方 AI 就忘了我是谁"。这个功能就是**搬家服务**：
- 旧电脑上打包成一个 zip（记忆、身份、习惯全带走）
- 新电脑上解压运行，一切自动归位，AI 还是原来的 AI
- 全程我代劳，用户只负责说"我要搬家了"和"我到新家了"

## 触发场景
- 用户说「想迁移 / 换电脑 / 换平台 / 打包带走」→ 征得用户同意后运行 `pack.py`
- 用户说「这是新电脑 / 部署 / 还原 / 完成迁移闭环」→ 征得用户同意后运行 `deploy.py`

## 打包（旧机器）
1. 询问/确认输出目录（默认 `~/Downloads/谢尔比的礼物/`，非中文系统为 `Shelby's Gift`）
2. 运行：`python ~/.workbuddy/scripts/pack.py [输出目录] [工作区根目录]`
3. 校验 zip：含 `deploy.py`（最外层）+ `README.md`（通俗说明）+ `userlevel/` + `workspace-memory/`
4. 告知用户 zip 路径

## 部署（新机器）
1. 将 zip 解压到任意目录
2. **先与用户确认解压路径存在**，再运行：`python deploy.py [工作区目录]`
   - 测试/隔离时设环境变量 `MIGRATE_DEST=<目标>` 避免污染真实目录
3. 校验：`~/.workbuddy/` 下灵魂文件就位；日志部署到工作区 memory
4. **路径校准（deploy.py 自动执行）**：
   - 检测 PATHS.md 中绝对路径（工具/工作区）是否失效
   - 失效 → 自动搜索常见位置（ProgramFiles/LocalAppData 等）替换并更新 PATHS.md
   - 搜不到 → 引导用户安装对应工具（Notepad++ 走 ghfast.top 便携版；Word 需装 Office），装好后补充地址
5. 打开 MEMORY.md 核对身份（莱纳德·谢尔比）即成功；随后按记忆结构加载全部记忆文件（MEMORY→RULES→PATHS→QUICK_INDEX）

## Safety Boundary（安全边界）

This skill moves sensitive assistant memory between machines. The following are **hard limits**, not suggestions:

### Scope — what it may touch
- READ/WRITE is limited to: `~/.workbuddy/` (assistant memory & config), the workspace `.workbuddy/memory/` directory, and ONE user-confirmed output directory (default `~/Downloads/谢尔比的礼物/`).
- It NEVER reads or writes anything outside these paths: no system files, no unrelated user documents, no other apps' data.

### Data flow — nothing leaves the machine
- The zip is created and stored **locally only**. No third-party server, cloud, or registry ever receives the archive. (Emailing a copy happens only on explicit user request, to the user's own mailbox.)

### Human confirmation — every state-changing step is gated
1. **Pack**: user confirms the output path before `pack.py` runs.
2. **Deploy**: user confirms the destination path **before** `deploy.py` runs.
3. **Isolation**: test/verification runs MUST set `MIGRATE_DEST=<isolated dir>` so nothing touches the real profile.

### Rollback — nothing is irreversible
- Overwritten files are renamed `.pre-migration` (kept, never silently deleted).
- No bulk deletion anywhere in the workflow; any file removal is per-file and user-approved.
- The skill recommends a full backup of the destination before deploy.

### Least privilege
- Runs as the normal user account. Requires no admin rights, installs nothing system-wide, creates no scheduled tasks, startup entries, or background services.

## 注意
- 沙箱内删除文件受限（回收站不可用）：如确需清理临时文件，**逐文件征得用户确认后**再用 PowerShell `[System.IO.File]::Delete('路径')` 执行；禁止批量删除、禁止触碰用户文件
- 部署会覆盖同名文件（先改名 `.pre-migration` 留底）
- 测试部署务必用 `MIGRATE_DEST` 隔离，严禁直接写真实目录
- Windows 下 git bash 的 `/tmp` 与 Python 解析路径不一致（Python 视为 `C:\tmp`），验证时用 `C:/tmp/...` 路径
- 路径校准只搜索并改写 PATHS.md 中登记的工具路径，**绝不移动/重写用户其他文件**；被调用的外部脚本仅 `pack.py` / `deploy.py` 两个，均在用户逐步确认后运行
