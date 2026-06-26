# HanSphere 知识库参考

本文件存放 HanSphere-specific 配置，供 `knowledge-base` skill 在 HanSphere 环境下加载。

## 根目录

- 本地根目录：`D:\HanSphere`
- 仓库名称：`HanSphere`
- 笔记格式：Markdown (.md)
- 默认编辑器：VS Code
- 正文语言：中文
- 目录命名：英文

## 知识库路径

```
D:\HanSphere/
├── README.md              # 仓库总览
└── Notes/
    ├── 00-Inbox/          # 收集箱 (临时)
    ├── 01-Daily/          # 日报 (按月分子目录)
    ├── 02-Sources/        # 外部来源 (文章/资料)
    │   └── Fulltext/      # 全文存档
    ├── 03-Concepts/       # 通用概念 (按领域分子目录)
    ├── 04-Issues/         # 问题模型
    ├── 05-Projects/       # 所有项目 (个人+公司)
    ├── 06-Architecture/   # 架构设计
    ├── 07-Patterns/       # 工作方法 (SOP)
    ├── 08-Reviews/        # 复盘总结 (周报/月报)
    ├── 09-Indexes/        # 索引导航
    ├── 10-Operations/     # 操作日志+体检报告
    ├── 98-Templates/      # 模板库
    └── 99-Archive/        # 归档区
```

## 命名规范

| 类型 | 格式 | 示例 |
| --- | --- | --- |
| Inbox | `INBOX-YYYYMMDD-Title.md` | `INBOX-20260422-MeetingNotes.md` |
| Daily | `DAILY-YYYY-MM-DD.md` | `DAILY-2026-04-22.md` |
| Source | `SRC-Topic-YYYY-MM-DD.md` | `SRC-Harness-Engineering-Implementation-2026-04-22.md` |
| Source Fulltext | `SRC-Topic-Fulltext-YYYY-MM-DD.md` | `SRC-xxx-Fulltext-2026-04-22.md` |
| Concept | `CONCEPT-Domain-Topic.md` | `CONCEPT-JVM-GC.md` |
| Issue | `ISSUE-System-Problem.md` | `ISSUE-MySQL-ConnectionTimeout.md` |
| Project | `PRJ-Project-Name/` | `PRJ-WeaveHan-Blog/` |
| Architecture | `ARCH-Topic.md` | `ARCH-Microservices-Decomposition.md` |
| Pattern | `PATTERN-Scenario.md` | `PATTERN-RetryWithBackoff.md` |
| Review | `YYYY-Www-WeeklyReview-MMDD-MMDD.md` / `YYYY-MM-MonthlyReview.md` | `2026-W14-WeeklyReview-0331-0406.md` |
| Index | `INDEX-Domain.md` | `INDEX-Overview.md` |
| Ops-Log | `ops-YYYY-MM-DD.md` | `ops-2026-04-22.md` |
| Lint-Report | `LINT-YYYY-MM-DD-NNN.md` | `LINT-2026-04-22-001.md` |

## 操作日志路径

- `D:\HanSphere\Notes\10-Operations\logs\ops\ops-YYYY-MM-DD.md`
- `D:\HanSphere\Notes\10-Operations\logs\wiki-health\lint-YYYY-MM-DD.log`
- `D:\HanSphere\Notes\10-Operations\reports\wiki-health\LINT-YYYY-MM-DD-NNN.md`

## 操作日志模板

```markdown
# 操作日志 - YYYY-MM-DD

- **日期：** YYYY-MM-DD
- **操作人：** <AI 名称>
- **触发：** 用户请求/主动执行/其他

## 操作记录

### HH:MM - 操作简述

- **新建：** [路径](路径) - 说明
- **修改：** [路径](路径) - 说明
```

## 体检脚本

```powershell
node D:\HanSphere\Notes\10-Operations\tools\wiki-lint.js
```

可通过环境变量 `NOTES_DIR` 指定扫描目录。

## 项目目录结构

```
PRJ-Project-Name/
├── 00-Index/
│   └── INDEX.md              # 项目唯一入口（不创建 README.md）
├── 01-Overview/
│   └── Project-Overview.md
├── 02-Requirements/           # 需求文档（可选）
├── 03-Architecture/           # 架构设计（可选，含 Database/ 子目录）
├── 04-Modules/                # 模块结构（可选）
├── 05-Source-Materials/       # 原始资料（可选）
├── 06-Interfaces/             # 接口文档（可选）
├── 07-Data/                   # 数据样例、字段映射、导入导出（可选）
├── 08-Environments/           # 环境配置（可选）
├── 11-Issues/                 # 项目问题（可选）
├── 12-Change-Logs/            # 变更记录
├── 13-Todos/                  # 待办（可选）
├── 14-Decisions/              # 决策记录（可选）
└── 15-Reviews/                # 项目级复盘（可选）
```

## 图表规范

使用 Mermaid 图表时：
- 主题：`%%{init: {'theme': 'neutral'}}%%`
- 节点标签避免 `|` `/` `\` `→` 字符
- 菱形节点 `{}` 不放在 `subgraph` 内部

## Git 提交规范

```bash
cd D:\HanSphere
git add .
git commit -m "docs: 简要描述变更"
git push
```

提交信息前缀：`docs:` 文档/笔记更新，`feat:` 新增内容模块，`fix:` 修正错误，`refactor:` 结构调整。

## 字段默认值映射

### 正文语言

- 默认：中文

### 各类型 status 值

| 语义类型 | 创建时建议值 | 成熟文档常见值 |
| --- | --- | --- |
| 来源资料 (Source) | `captured` | `processed` |
| 概念知识 (Concept) | `draft` | `stable` |
| 问题排查 (Issue) | `open` | `verified` |
| 方法流程 (Pattern) | `draft` | `stable` |
| 项目资料 (Project) | `active` | `active` |

### 各类型 review_cycle

| 类型 | 默认周期 |
| --- | --- |
| 来源资料 (Source) | 30d |
| 概念知识 (Concept) | 60d |
| 问题排查 (Issue) | 30d |
| 方法流程 (Pattern) | 60d |
| 项目资料 (Project) | 90d（可选） |
| 时序记录 (Daily) | 不需要 |

### 语义类型 → HanSphere 实现映射

| 语义角色 | HanSphere 目录 | HanSphere 文件前缀 |
| --- | --- | --- |
| 时序记录 | `01-Daily/` | `DAILY-` |
| 临时收集 | `00-Inbox/` | `INBOX-` |
| 来源资料 | `02-Sources/` | `SRC-` |
| 概念知识 | `03-Concepts/` | `CONCEPT-` |
| 问题排查 | `04-Issues/` | `ISSUE-` |
| 项目资料 | `05-Projects/` | `PRJ-` |
| 决策设计 | `06-Architecture/` | `ARCH-` |
| 方法流程 | `07-Patterns/` | `PATTERN-` |
| 复盘总结 | `08-Reviews/` | `YYYY-Www-` / `YYYY-MM-` |
| 导航索引 | `09-Indexes/` | `INDEX-` |
