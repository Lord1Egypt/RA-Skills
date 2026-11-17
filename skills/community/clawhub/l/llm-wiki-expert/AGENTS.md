# AGENTS.md — llm-wiki-expert

本仓库是一个采用 superpower 架构的 AI Agent 技能库，用于创建和运营 LLM Wiki。它不是某个具体 Wiki 的内容仓库；`assets/` 与 `scripts/` 用来生成目标 Wiki。

## 目录约定

```text
llm-wiki-expert/
├── SKILL.md          # L1 唯一入口与路由
├── references/       # L2 方法论与决策树
├── skills/           # L3 独立可安装能力
├── scripts/          # L4 stdlib-only 确定性工具
├── assets/           # L5 契约和页面模板
├── tests/            # 脚本好/坏样本测试
├── AGENTS.md
├── README.md
└── LICENSE
```

## 加载顺序

1. 始终先读根 `SKILL.md` 的能力索引。
2. 方法论决策只加载一个最相关的 `references/*.md`。
3. 落地动作调用 `skills/<name>/SKILL.md`；确定性检查优先跑 `scripts/`。
4. 创建目标 Wiki 时复用 `assets/`，不得在各项目重造相互漂移的模板。

## SKILL.md 约定

- 根 `SKILL.md` 只做路由，必须 ≤150 行、无 TODO，frontmatter 声明 `architecture: superpower`。
- 子技能目录名必须与 frontmatter `name` 一致，并含完整 `source` 追踪。
- 子技能正文必须包含：能力、使用方式、工作流、适用场景、限制。
- 正文使用中文，Effect、RAG、frontmatter 等技术术语保留英文。

## Wiki 领域约定

- `raw/` 是不可变证据层：只追加，不把 Agent 改写后的文本伪装成原文。
- `wiki/` 是可重编译知识层：允许合并、拆分、过期和归档，但变更需进日志。
- 精确事实必须可定位到来源；冲突不能静默覆盖。
- 检索方案由查询评测决定，禁止为了“高级”默认引入向量数据库。
- 脚本默认不联网、不修改目标 Wiki；`scaffold_wiki.py` 只新增缺失文件且不覆盖。

## 添加能力流程

1. 用 `skills-repo-admin/skills/skill-radar` 搜索社区来源并记录证据。
2. 新建 `skills/<name>/SKILL.md`，填写 `source`。
3. 若引入新的决策方法，新增 `references/`；若是确定性重复任务，新增脚本和测试。
4. 在根路由表和 README 清单同时登记，避免孤儿能力。
5. 运行 `python3 -m unittest discover -s tests -v`。
6. 运行 skills-repo-admin 的结构门禁与 README 内容门禁。

## 不做什么

- 不把 LLM Wiki 宣称为 RAG 的通用替代；两者解决的粒度不同。
- 不自动裁决互相矛盾的来源，也不删除被否决的人类反馈。
- 不在缺乏授权时抓取私有数据、受限内容或覆盖目标仓库既有文件。
- 不用脚本判断内容是否“正确”；脚本只提供可复现的结构与证据问题。
