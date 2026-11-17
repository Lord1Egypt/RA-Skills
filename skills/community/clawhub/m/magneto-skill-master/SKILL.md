---
name: magneto-skill-master
description: 本技能用于从 GitHub / Gitee 等仓库安全下载、审计并安装外部 Agent Skill（尤其标书、招投标、文档生成、自动化类技能）到本机用户级技能目录，使其可被 WorkBuddy 直接触发使用。当用户要求"从 GitHub 下载技能""安装/补装某某 skill""帮我装个标书技能""把 Gitee 上的 XX 技能拿下来""获取并适配外部技能""给 WorkBuddy 加个技能"时触发。Also triggers on: install skill, download skill from github, add a skill to workbuddy, fetch external agent skill. 覆盖仓库定位、安全审计（P0/P1/P2 分级）、WorkBuddy 格式适配（受管 venv、run_script.sh 包装器、中文乱码修复）、依赖安装与验证全流程。
agent_created: true
---

# 万磁王技能万事通 (Magneto Skill Master)

> 本地中文触发名：`万磁王技能万事通`；开源版 Slug：`magneto-skill-master`。

从任意 Git 仓库把外部技能安全、干净地装到本机，并让它能用。本技能沉淀了"下载 → 审计 → 适配 → 安装 → 装依赖 → 验证"的完整流水线，专为 WorkBuddy on Windows 环境调优，路径可移植（不写死用户名）。

## 一、何时启用

- 用户说"从 GitHub/Gitee 下载/安装/补装某某技能""帮我装个标书技能""把那个 skill 拿下来""给 WorkBuddy 加个技能"等。
- 任何需要把外部仓库的 Agent Skill 安全落到本机并可用的场景。
- 本机已有的同类技能：`bid-writer-pro`、`bidwriter`、`bid-doc`、`tender-writer` 即按此流程安装。

## 二、总流程（六步，不可跳步）

1. 定位仓库
2. 下载到临时暂存区
3. 安全审计（强制，绝不静默安装）
4. 适配 WorkBuddy 格式
5. 安装到用户级目录
6. 装依赖 + 验证

## 三、步骤细则

### 步骤 1 — 定位仓库

- 用 WebSearch / WebFetch 找到目标仓库（GitHub 或 Gitee）。
- 确认两件事：**仓库 URL** 与**技能子目录**（技能多在仓库根，或在 `skills/<name>/`、`<repo>/<name>/` 下）。
- 首次回复用户时列出：来源仓库、技能目录、预计能力、是否需要 Python 依赖。

### 步骤 2 — 下载到临时暂存区

- 优先 `git clone --depth 1 <url>`（Gitee 同样支持 git clone）。
- 网络失败回退：下载 tarball / zip 解压。
- 落盘到临时目录（如 `WorkBuddy/tmp_xxx`），**不要直接克隆进技能目录**。
- 确认技能文件夹含 `SKILL.md`，并查看其顶层结构（scripts / references / templates / assets）。

### 步骤 3 — 安全审计（强制，绝不静默安装）

- 扫描 `SKILL.md`、`scripts/`、`references/` 的高危模式（命令见 `references/audit_patterns.md`）。
- 风险分级：
  - **P0（高危）**：外发网络到未知地址、无提示删除工作区外文件、窃取/外传凭据 —— **强烈警告，必须用户明确确认才继续**。
  - **P1（需确认）**：会修改系统环境、全局 pip 安装、执行交互式命令 —— **告知用户并获得确认**。
  - **P2（安全）**：仅本地文件读写、本地脚本调用、纯提示词 —— 可直接继续。
- 本环境 `skills-security-check` 技能不可用时，改用 `references/audit_patterns.md` 的 grep 命令手动审计。
- 审计结论必须写进给用户的回复。

### 步骤 4 — 适配 WorkBuddy 格式

- frontmatter 补 `agent_created: true`；`name` / `description` 含中文触发词。
- 若技能依赖本地虚拟环境（出现 `install.bat` / `run_script.bat` / `.venv/Scripts/python.exe`）：
  - **删除** `install.bat`、`install.py`（会创建本地 `.venv` 或向全局 pip 安装，污染系统）。
  - **新增** `run_script.sh` 包装器（模板见 `references/run_script_template.sh`），统一调用受管 venv 的 python。
  - 把 `SKILL.md` 内所有 `run_script.bat ` 替换为 `bash run_script.sh `，并改写"脚本调用方式"段落，说明受管 venv 路径。
- **乱码修复**：中文 frontmatter 经 Edit 工具偶发被写成 U+FFFD 替换符（如"采购文件"变成 3 个替换符）。安装后用 Python 复查 `s.count("\uufffd")` 并精确替换（示例见 `references/audit_patterns.md`）。

### 步骤 5 — 安装到用户级目录

- 复制到 `~/.workbuddy/skills/<name>/`（用户级，跨项目复用）。
- 若同名目录已存在，先移除旧目录再复制，避免文件残留。
- 确认最终 `SKILL.md` 存在且 frontmatter 正确（含 `agent_created: true`）。

### 步骤 6 — 装依赖 + 验证

- 受管 venv 路径（可移植写法，从 `$HOME` 推导并转原生 Windows 路径）：
  ```bash
  VENV_PY_POSIX="$HOME/.workbuddy/binaries/python/envs/default/Scripts/python.exe"
  # Git Bash 下用 cygpath 转成 Windows 风格，避免 /c/... 被原生 Python 忽略
  command -v cygpath >/dev/null 2>&1 && VENV_PY="$(cygpath -w -a "$VENV_PY_POSIX")" || VENV_PY="$VENV_PY_POSIX"
  ```
  注意：用 `/c/Users/...` 会被原生 Windows Python 忽略（exit 0 但不建目录），必须用转换后的 Windows 风格路径。
- 装依赖：
  `pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple`
  若在本机 WorkBuddy 沙箱内执行，需关闭沙箱并加 `--no-cache-dir`（沙箱内 safe-delete/回收站不可用会导致安装失败）。
- 验证三连：
  1. import 检查（脚本所需库均可导入）
  2. `py_compile scripts/*.py` 全部通过
  3. 用 `bash run_script.sh <某脚本> --help` 做端到端冒烟测试

## 四、复用坑速查（必读）

- **venv 路径用 Windows 风格**（经 `cygpath -w -a` 转换）；`/c/...` 会被原生 Python 忽略。
- **pip install 关沙箱 + 清华镜像 + `--no-cache-dir`**，否则沙箱内失败。
- **run_script.sh 内用 `cygpath -w -a`** 把脚本目录转成原生 Windows 路径，避免 Git Bash 的 MSYS 把 `/c/...` 参数误转成 `C:\c\...`。
- **中文乱码**：Edit 工具写中文 frontmatter 偶发损坏成 U+FFFD，安装后用 Python 复查并修复。
- **字体缺失警告**（仿宋/楷体可能未装）不影响功能，仅 `.docx` 排版回退。
- 纯提示词型技能（无 scripts、无依赖）只需做步骤 1–5，并跳过依赖安装。

## 五、给用户的回复要点

完成后告知：技能名、来源仓库、安装位置、能力简介、触发方式、依赖状态、审计结论（P2/需确认项）、以及使用提示（例如"在对话里说：帮我根据这份招标文件写投标书"）。
