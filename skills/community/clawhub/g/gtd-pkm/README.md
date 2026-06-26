# OpenClaw GTD PKM

一个面向 OpenClaw 的 GTD 个人知识管理 Skill，用来帮助用户审计、共创、分阶段落地并持续优化自己的 PKM 系统。

它不把“搭知识库”理解成一次性初始化任务，而是把自己当成一个长期协作的顾问和实施搭档：先看现状，再出蓝图，再选一个最值得先做的阶段，最后边运行边收敛。

## 适用场景

- 从零搭建基于 OpenClaw 的 GTD/PKM 知识库
- 重构已有的 Markdown / Obsidian / OpenClaw 知识库
- 审计目录、标签、命名、归档和迁移路径
- 设计 `AGENTS.md`、`HEARTBEAT.md`、`TODO/`、cron 等自动化协作机制
- 只想先解决某个局部问题，例如收集箱、日志、周回顾、标签收敛或知识输出闭环

## 核心特点

- 共创优先：先理解用户真实工作流，而不是直接套模板
- 分阶段落地：每次只推进一个清晰批次，降低改造风险
- 兼顾结构与运行：既设计目录和标签，也关注自动化和日常维护
- 尽量可迁移：参考资料和脚本都围绕可复用、可演进来设计

## 工作方式

这个 Skill 默认遵循下面的协作节奏：

1. 发现现状
2. 产出蓝图
3. 只落地一个清晰阶段
4. 陪用户运行和调优

默认不会一上来就大改目录、批量迁移或直接初始化。只有当用户明确要求“直接初始化”时，才会跳过共创步骤。

## 目录结构

```text
openclaw-gtd-pkm/
├── SKILL.md
├── README.md
├── agents/
│   └── openai.yaml
├── scripts/
│   ├── bootstrap_knowledge.py
│   └── knowledge_audit.py
└── references/
    ├── collaborative-design-playbook.md
    ├── gtd-knowledge-framework.md
    ├── openclaw-automation-recipes.md
    └── openclaw-portable-patterns.md
```

## 文件说明

- `SKILL.md`
  - Skill 的核心定义与模型执行说明
  - 包含触发条件、协作流程、脚本调用时机和安全边界
- `agents/openai.yaml`
  - 面向 UI 和分发的展示元数据
  - 包含 `display_name`、`short_description` 和 `default_prompt`
- `scripts/bootstrap_knowledge.py`
  - 在蓝图确认后快速生成第一版 GTD 知识库骨架
- `scripts/knowledge_audit.py`
  - 对现有知识库做结构审计，输出 GTD 对齐建议
- `references/*.md`
  - 按需加载的参考材料，用来支持设计、自动化和迁移判断

## 自带脚本

### 1. 审计现有知识库

适合先摸清现状，再决定是否重构。

```bash
python3 scripts/knowledge_audit.py --knowledge-root /path/to/knowledge-base
```

输出内容包括：

- 顶层目录覆盖情况
- Markdown 文件分布
- Frontmatter 标签统计
- 命名风险
- GTD 迁移建议

### 2. 初始化知识库骨架

适合在蓝图已确认后，快速落地第一版目录、规范和模板。

```bash
python3 scripts/bootstrap_knowledge.py --knowledge-root /path/to/knowledge-base --owner-name 用户
```

它会生成：

- GTD 顶层目录与基础子目录
- `README.md`
- 标签规范、命名规范、GTD 工作流规范
- 模板文件和待阅读队列

它不会默认生成 `AGENTS.md`、`HEARTBEAT.md` 或 `TODO/`，这些更适合在运行阶段结合用户实际工作流再设计。

## 示例调用

如果在支持 Skill 调用的环境里，可以这样使用：

```text
Use $openclaw-gtd-pkm to audit my current notes and plan a phased OpenClaw GTD PKM rollout.
```

也可以直接用自然语言提出需求，例如：

- 帮我审计这个知识库，先不要改文件
- 先给我一版 GTD 知识库蓝图，再决定第一阶段怎么落地
- 我已经有一套 Obsidian 笔记，帮我设计迁移到 OpenClaw 的方案
- 只帮我做收集箱、周回顾和知识输出闭环

## 发布前检查

当前版本已经补齐了适合发布到 ClawHub 的关键结构：

- `SKILL.md`
- `agents/openai.yaml`
- `scripts/`
- `references/`

如果你在本地继续迭代，发布前建议至少做这几步检查：

```bash
python3 /Users/zhaor/.codex/skills/.system/skill-creator/scripts/quick_validate.py .
python3 -m py_compile scripts/bootstrap_knowledge.py scripts/knowledge_audit.py
```

如果你修改了脚本逻辑，最好再用一个临时目录真实跑一遍初始化和审计。

## 设计原则

- 目录表达阶段和归属，标签表达主题和属性
- 自动化服务于习惯养成，而不是为了自动化而自动化
- 不把“标准答案”强压给用户，优先贴着已有习惯演进
- 大规模迁移前先做审计、确认和备份

## 说明

这份 `README.md` 面向人阅读，方便仓库展示、分享和维护。

真正决定 Skill 如何触发和执行的，仍然是 [`SKILL.md`](./SKILL.md)。
