# 船货盘本地库（SQLite）· 零基础说明（与 `SKILL.md`「首次写入 SQLite 前」对应）

路由 A 会把解析好的船盘/货盘存到本机**一个文件**里，文件名一般为 **`charter_facts.sqlite3`**。  
用户**不需要**会写代码、**不需要**自己敲 SQL、**不需要**安装 MySQL / PostgreSQL 这类「数据库服务器」。

助手在**第一次**需要写入或查询该文件、或用户主动问「数据库 / SQLite / 船货盘库」时，**必须先**走本节；**禁止**未说明就要求用户去下复杂软件。

---

## A. 用大白话告诉用户「这是什么」（约 4～6 句，可复述）

```text
您的船货盘查询结果，除了当场回答，还会自动保存在本机一个文件里（charter_facts.sqlite3），
方便以后问「上海出发的船」「某条 IMO」时更快找到，不用每次都重新读全部邮件。

这个文件用的是 SQLite——可以理解为「存在您电脑上的一个记事本式数据库文件」，
不是要在公司机房再装一套数据库。

正常情况下您不用自己安装 SQLite，也不用打开任何数据库软件；
我会通过 HiFleet 技能自带的工具自动创建和读写这个文件。
```

---

## B. 先检查环境（由助手代做，勿让用户猜）

在需要 **2.4.1 写入** 或 **`charter_facts_tool.py`** 之前，助手应在受信环境中**静默检查**（用户无代码基础时**不要**把下面命令原样丢给用户，除非检查失败需配合安装）：

1. **Python 是否可用**：`python3 --version` 或 `python --version`（本 Skill 宿主通常已带 Python，见 `SKILL.md` metadata）。  
2. **SQLite 模块是否可用**：`python3 -c "import sqlite3; print(sqlite3.sqlite_version)"`（或 `python -c ...`）。  
3. **技能目录是否可写**：确认 `hifleet-mytonnages/`（或 `HIFLEET_MYTONNAGES_DIR` 指向的目录）可创建 `charter_facts.sqlite3`。

**三项均通过** → 直接进入 **Workflow 2** 的 **2.4.1**，**无需**让用户安装任何东西。  
**任一项失败** → 进入 **C** 或 **D**（按失败类型）。

---

## C. 多数情况：无需单独安装 SQLite

满足以下**全部**条件时，向用户说明「**已就绪，无需您操作**」即可：

- 宿主环境（OpenClaw / Codex 等）已安装 **Python 3**；  
- `import sqlite3` 成功（Python **自带** SQLite，与「再下一个 SQLite 安装包」不是一回事）；  
- 技能目录有写入权限。

**禁止**对零基础用户说「请安装 SQLite 数据库服务」「请建库建表」「请用 Navicat / DBeaver 连接」等。

---

## D. 仅当检查失败：征求同意后再引导（opt-in）

必须使用户能**拒绝**。示例话术：

```text
您电脑上的 Python 暂时还不能使用内置的 SQLite 功能（或技能目录无法写入），
船货盘暂时无法保存到本地文件，以后按港口/IMO 查询可能会变慢。

是否同意我带您用最简单的方式装好？一般只需安装/修复 Python，不用学编程。
回复「同意」继续；回复「不同意」则暂不启用本地船货盘库（仍可用邮件检索，但可能更费时间）。
```

- **同意** → 按 **E** 分系统引导（一次只给 1～2 步，等用户反馈再继续）。  
- **拒绝** → 说明：仍可走邮件向量检索，但 **2.3 SQLite 结构化查询** 可能不可用；**不得**反复催促。

---

## E. 安装/修复指引（零基础 · 分步）

> **原则**：优先 **安装/修复 Python 3**（自带 SQLite）；**不要**让用户单独下载「SQLite 命令行」除非 Python 路径已排除仍失败。  
> 全程由助手在用户**明确同意**后代执行命令，或给出**带截图说明的官方链接**；**禁止**要求用户理解 PATH、pip、虚拟环境等术语。

### E.1 Windows

1. 打开浏览器，访问 **https://www.python.org/downloads/** ，下载 **Python 3.11 或更高** 的安装包。  
2. 运行安装程序时，**勾选** 「**Add python.exe to PATH**」（添加到 PATH）→ 再点「Install Now」。  
3. 安装完成后**关闭并重新打开** OpenClaw / Codex（或整个电脑重启一次更稳妥）。  
4. 回到对话告诉助手「装好了」，由助手再次执行 **B** 中的检查。  

若仍提示没有 `sqlite3`：请用户卸载后重装 Python，并确认未使用「精简版 / 嵌入版」Python；必要时联系 HiFleet 客服。

### E.2 macOS

1. 若从未装过 Python：可从 **https://www.python.org/downloads/macos/** 安装官方 Python 3，或按宿主文档使用系统推荐方式。  
2. 安装后重启 OpenClaw / Codex，由助手再次检查 **B**。  

（多数 Mac 上 OpenClaw 自带 Python 已足够，**先**走 **B**，不要一上来就让用户装 Homebrew。）

### E.3 仍失败时的兜底（少见）

仅在 **Python 已正常且 `import sqlite3` 仍失败** 时：

- 说明可能是 Python 发行版裁剪过组件，建议**换用官方 python.org 安装包**重装；  
- **不要**要求用户配置 `pysqlite`、编译源码或改注册表。  

**不建议**零基础用户单独安装「SQLite 官网命令行工具」；该工具不能替代 Python 内置模块。

---

## F. 文件位置（用户问「数据存在哪」时）

用口语说明即可，例如：

```text
船货盘数据在您本机技能文件夹里的 charter_facts.sqlite3 这一个文件。
换电脑或删了这个文件，本地历史船货盘记录会没有，但您的邮箱里的邮件还在。
```

默认路径示例（以实际安装为准，助手按环境回答，勿让用户记路径）：

- OpenClaw：`~/.openclaw/workspace/skills/hifleet-mytonnages/charter_facts.sqlite3`  
- Codex：`$CODEX_HOME/skills/hifleet-skills/hifleet-mytonnages/charter_facts.sqlite3`  

可通过环境变量 **`HIFLEET_CHARTER_DB_PATH`** 改存盘位置（由部署方或助手配置，**勿**让零基础用户手改）。

---

## G. 助手禁止事项（硬性）

- **禁止**要求用户执行 `CREATE TABLE`、手写 SQL、安装 MySQL/PostgreSQL。  
- **禁止**把 `charter_facts.sqlite3` 上传到公网或发给他人（含完整对话粘贴）。  
- **禁止**在未获同意时删除用户的 `charter_facts.sqlite3`；若用户要求「清空本地船货盘」，须再次确认后由助手删除或重建。  
- **禁止**因 SQLite 未就绪就**伪造**结构化查询结果。

---

## H. 与 Workflow 的衔接

| 阶段 | 说明 |
|------|------|
| 路由 A · 首次写入前 | 完成 **B**；失败则 **D→E**，成功再 **2.4.1** |
| **2.3** 检索 | 库文件存在则优先 SQLite；不存在且未修复则降级向量检索并说明 |
| 路由 B | **不使用** 本文件；班轮船期走 **`SCHEDULE_API.md`** |
