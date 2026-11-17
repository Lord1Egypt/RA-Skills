# 大项目组织技能包（project-organization）

> 🔍 **不知道这是干什么的？** 装好后直接问 AI「这个是做什么的」，AI 会给你介绍，不用读文档。

把「一个会长期演进的项目」从**第一天就组织好**的 AI 技能包：分层目录 + 归属判断 + 缓冲区 + 软删除 + 结构自检。

很多任务开始时很小，但会长成庞然大物——文件越堆越乱、不知道放哪、删错了没法恢复。本技能把「大项目怎么组织」固化成**方法论 + 可执行脚手架**。

## 它解决什么

| 痛点 | 本技能的答案 |
|---|---|
| 项目文件越堆越乱、不知道放哪 | **大项目制 + 按主题分层**（`projects/ shared/ archive/`），AI 自动判断归属 |
| 人类与 AI 互相传文件靠"甩到桌面/下载目录" | **`buffer/` 缓冲区**（扁平、2 天 TTL）——把文件丢进去，对 AI 说「读取 buffer」即按语义归位 |
| 删错了没法恢复 | **`.trash/` 软删除**（可还原、可压缩、可审计）；硬删只有一条路且需确认 |
| 结构悄悄漂移、没人发现 | **`audit_project.py`** 一键自检（缺 README / 顶层散落 / 缓冲区超期 / 归档无索引…）|
| 操作没有痕迹 | `.tools/journal.jsonl` + 派生 `_log.md`（append-only）|

## 它是什么

**一套约定 + 一组脚本**：

```
<大项目根>/
├── .bigproject.json          # 根标记（脚本据此定位）
├── README.md                 # 大项目概览
├── AGENTS.md / INDEX.md / MEMORY.md / TODO.md
├── projects/<子项目>/         # 每个子项目：README + scripts/ data/ results/ output/
├── shared/                    # 跨项目共享（只读引用）
├── buffer/                    # ★ 人类 ⇄ AI 交换区（扁平 + 2 天 TTL）
├── archive/                   # 已结束项目
├── .tools/                    # 操作日志
└── .trash/                    # ★ 软删除暂存（可还原）
```

**两条硬规则**：① **buffer 只做中转**（超期强制清理）；② **buffer 里每一项都必须在 `projects/`（或 `shared/`/`archive/`）有归宿**，禁止当唯一副本。

## 安装

- **ClawHub**：`clawhub install project-organization`
- **手动**：把本目录放进 OpenCode / OpenClaw 的 `skills/` 下即可（脚本全部参数化、零硬编码）。

## 脚本

| 脚本 | 作用 |
|---|---|
| `new_big_project.py` | 新建合规的大项目根骨架 |
| `new_subproject.py` | 新建子项目（含 README/STATE/目录），支持挂外部代码仓 |
| `audit_project.py` | 结构自检（stdout JSON） |
| `buffer.py` | 缓冲区：`list / take / deliver / add / purge / discard` |
| `trash.py` | 软删除：`put / list / restore / purge / compress / status` |
| `journal.py` | 操作日志 |
| `git_setup.py` | 大项目根 git 初始化（含 .gitignore 与首次提交）|
| `oc_project_link.py` | 处理 OpenCode「同目录多条 project 记录」（会话列表变空）|

所有脚本：**CLI 参数化、stdout JSON、即跑即退、无阻塞**。

## 缓存与凭据

本技能**不含任何凭据**，也不会写入你的私密数据；`runtime/`、`__pycache__/`、`tmp/`、`output/` 均已 `.gitignore`。

## 开源与发布

本技能包**完全开源**；**最新版以下面两处为准**：

| 渠道 | 地址 | 查看 / 获取 |
|---|---|---|
| **GitHub**（源码） | **https://github.com/TOMUIV/project-organization-skill** | 看完整代码、Fork、提 Issue、跟版本 |
| **ClawHub**（技能市场） | slug **`project-organization`** | `clawhub install project-organization`（或搜索 `project-organization`）|

> 想确认「最新版是多少 / 改了什么」——去上面任一渠道看即可；本仓库与 ClawHub 同源同版本。

## 许可

MIT-0（No Attribution，见 `LICENSE`）。欢迎通过 GitHub Issue 反馈 bug 与建议。
