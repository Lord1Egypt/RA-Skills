---
name: novelforge
description: "通用小说创作与叙事引擎系统。面向短篇、中篇与长篇连载等各类小说，通过故事筑基 SOP 驱动题材对齐、规模承载力评估、总纲与世界观立项；通过自动化流水线驱动原生 Markdown Wiki 构建、蓝图校验、上下文编译、正文起草、双独立审查与事实结算；支持从小说或文章语料中两阶段提炼与构建自定义叙事引擎。当用户输入包括「新书立项」「故事筑基」「设计世界观」「规划总纲」「规模评估」「题材对齐」「写小说」「写下一章」「写第X章」「改写」「补充伏笔/钩子」「规划大纲」「检查质量」「章节结算」「继续流水线」「暂停写作」，或要求「参考某小说/文章提炼引擎」「构建叙事引擎」等任意小说创作与引擎构建任务时触发。"
metadata:
  openclaw:
    emoji: "🖋️"
    version: "1.0.0"
    requires:
      bins: ["python3", "git"]
---

# NovelForge 创作 Skill

触发后，根据自然语言意图定位项目根目录与章节，通过标准作业程序 (SOP 流水线)
自动串联蓝图、上下文、正文、审查、结算与交付。用户无需记忆和执行底层分散指令；
流水线具备可中断与可恢复保障。

## 不可绕过的边界

Markdown 只解释方法；脚本决定状态转换是否有效。Agent 使用
`scripts/novelforgectl.py pipeline advance` 统一驱动项目初始化、蓝图校验、上下文编译、
审查、结算与交付。
正文修改必须使用带源哈希的 `scripts/apply_patch.py`，以便原子地使章节链失效。
手工编辑 `.novelforge/state` 不属于有效工作流。

## 故事模型与记忆

每章都有小而明确的显式依赖集合。编译器生成 Context Ticket，其中包含依赖哈希、蓝图哈希和
Engine Snapshot。写作后必须通过两类独立审查。Settlement 记录事实并增量沉淀至故事记忆。
任何输入变化都会使下游产物失效，不会静默复用过期上下文。

小说的直接设定、蓝图与正文统一以原生的 Markdown Wiki 格式直接存储在项目根目录（`blueprints/`, `chapters/`, `characters/` 等），并通过双向链接建立引用网络，不得双份投影；机器运行状态、依赖工单与审查凭证严格以 JSON/JSONL 保存在 `.novelforge/` 供脚本确定性处理。

## 内置引擎与扩展

`engines/jin-yong/` 是选择性复制、可独立运行的内置叙事引擎，包含可按阶段、场景类型和项目状态
激活的方法卡与研究切片。它不是全局语言或文风要求。用户可通过自然语言要求系统参考样本小说或文章
提炼生成新引擎（详见 [references/engine-distillation.md](references/engine-distillation.md)），
或通过 `novelforgectl` 安装启用任意第三方引擎；Core 只校验契约、路径安全和哈希，不评判文学趣味。

可选风格检测器默认以告警报告作者/作品信号。项目可以明确把指定检测器或规则提升为
`blocking`；该策略永远不会阻止安装新引擎。

## Agent 职责

| Agent | 职责 | 机器交接物 |
| --- | --- | --- |
| `story-builder` | 大纲、章节蓝图、场景和伏笔设计 | `blueprints/<chapter-id>.md` |
| `story-writer` | 起草正文和哈希校验的窄范围回修 | `chapters/<chapter-id>.md` |
| `quality-checker` | 文本诊断和结构化审查证据 | `.novelforge/reviews/<chapter-id>-text.json` |
| `hook-inspector` | 跨章连续性和引擎审查证据 | `.novelforge/reviews/<chapter-id>-engine.json` |

## 参考资料地图

- [novelforge.md](novelforge.md) — 可执行工作流与门禁顺序
- [references/story-genesis.md](references/story-genesis.md) — 故事筑基与规模承载力评估规范
- [references/engine-contract.md](references/engine-contract.md) — 引擎契约与启用规则
- [references/engine-distillation.md](references/engine-distillation.md) — 叙事引擎提炼与构建规范
- [references/project-profile-spec.md](references/project-profile-spec.md) — 项目自有选择
- [references/story-memory.md](references/story-memory.md) — 文件型记忆与 Context Ticket
- [references/state-machine.md](references/state-machine.md) — 章节状态机
- [references/character-design.md](references/character-design.md) — 角色档案、性格底色与压力累积模型
- [references/naming-methodology.md](references/naming-methodology.md) — 跨题材通用实体命名因果构词方法论
- [references/blueprint-template.md](references/blueprint-template.md) — 蓝图字段
- [references/quality-checklist.md](references/quality-checklist.md) — 结构与告警检查
- [references/settlement-spec.md](references/settlement-spec.md) — 结算规格与状态投影规范
- [references/project-override-spec.md](references/project-override-spec.md) — 可选项目策略

## 验证

```bash
python3 scripts/novelforgectl.py skill-audit
python3 -m unittest discover -s tests -p 'test_*.py'
```

审计只扫描 Core Markdown。可选检测器、用户引擎、测试和生成夹具属于扩展面，不会被视为
Core 源码污染。
