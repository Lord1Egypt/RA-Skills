# L4 Skill Forge

**帮你从零到一设计并交付生产级 Claude Code Skill 的 AI 顾问。**

不只是写一个能跑的 skill——而是交付一个**可验证、可维护、可演进、可安全上线**的完整技能包。

## 这是什么

Claude Code 支持自定义 Skill（技能），可以让 AI 按你定义的流程工作。但写出一个随手写的 skill 和写出一个生产级 skill，差距很大。

L4 Skill Forge 是一个 **AI 顾问型 skill**，它会带着你：

- 定义你的 skill 要解决什么问题
- 按 L4 标准设计结构（输入/输出契约、失败处理、安全门控）
- 生成完整的文件包（主文件 + 模板 + 检查表 + 评估用例）
- 做发布前的安全审查

## 快速开始

### 安装

```bash
clawhub install ReffWu/l4-skill-forge
```

### 使用

安装后，在 Claude Code 中直接说：

- "帮我做一个 skill"
- "把这个 skill 升级到生产级"
- "对这个 skill 做安全审查"

AI 会自动激活本技能，引导你完成整个流程。

## 适合谁用

- 想给自己或团队定制 Claude Code 工作流的人
- 已经写了一些 skill 但想提升质量的人
- 想了解 L4 生产级 skill 标准的人

**零经验也没关系**——内置新手引导模式，会一步步带你做。

## 交付物包含什么

每次运行后你会得到：

```
your-skill/
├── SKILL.md              # 主技能文件
├── references/           # 设计规范文档
├── assets/
│   ├── templates/        # 可复用模板
│   ├── checklists/       # 发布检查表
│   └── evals/            # 评估测试用例
└── scripts/              # 自动化脚本
```

## 文件说明

| 文件 | 说明 |
|------|------|
| `SKILL.md` | 主技能文件，Claude Code 读取的入口 |
| `references/l4-standard.md` | L4 生产级标准定义 |
| `references/onboarding-zero-to-one.md` | 新手引导流程 |
| `assets/templates/skill-blueprint.md` | Skill 设计蓝图模板 |
| `assets/checklists/release-checklist.md` | 上线前安全检查表 |
| `assets/evals/eval-cases.md` | 评估测试用例集 |
| `scripts/score-skill.js` | 自动打分脚本 |

## L4 是什么意思

技能成熟度分级：

| 级别 | 描述 |
|------|------|
| L1 | 一次性 prompt，用完即弃 |
| L2 | 有结构，但没有错误处理 |
| L3 | 有测试，有基本安全考虑 |
| **L4** | **生产级：可验证、可审计、可演进** |

## License

MIT
