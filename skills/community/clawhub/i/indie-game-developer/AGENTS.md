# AGENTS.md — indie-game-developer 入口文件

> indie-game-developer 仓库的 Agent 入口文件，定义独立游戏技能库的使用规则与 superpower 目录加载顺序。

## 架构与加载顺序（superpower）

本仓库按 skills-repo 的 **superpower 架构**组织，Agent 加载顺序如下：

1. **先读 `SKILL.md`（L1 路由层）** — 只做能力索引，不要在此找方法论正文。
2. **按需读 `references/`（L2）** — 引擎选型、资源管线、Steam 发行、QA 性能等完整 playbook，按任务类型加载，不全量读。
3. **落地具体能力时读 `skills/<name>/SKILL.md`（L3）** — Three.js / 设计 / 像素美术 / Steam 发行的细粒度能力。
4. **确定性任务用 `scripts/`（L4）** — 资源引用完整性、Steam 元数据校验，产物可复现。
5. **模板套用看 `assets/`（L5）** — 商店元数据模板、资源清单示例、示例场景。

渐进式加载原则：先路由、后深度；不凭记忆猜引擎 API 与商店规范。

## 仓库性质

这是一个 **AI Agent 技能库**，不是软件项目。所有内容为 Markdown 格式的技能定义文件，外加可复用模板与确定性脚本。

## 目录约定

```
indie-game-developer/
├── SKILL.md               # L1 路由层
├── README.md              # 项目介绍和使用指南
├── AGENTS.md              # AI 助手使用指引（本文件）
├── references/            # L2 深层 playbook
├── skills/                # L3 细粒度子技能
│   ├── <skill-name>/
│   │   └── SKILL.md
│   └── ...
├── scripts/               # L4 确定性脚本
└── assets/                # L5 可复用模板
```

## SKILL.md 格式

每个子技能文件遵循 `rules/skill-format.md`：含 `name` / `description` / `source`（来源追踪）/ `metadata`，正文写能力、使用方式、工作流、适用场景与限制。

## 工作约定

- 所有技能内容使用中文编写
- 技能聚焦单一环节，不贪大求全
- 每个技能需明确"能做什么"和"不能做什么"
- 优先覆盖独立开发者（单人/小团队）场景
- 面向 Steam / itch.io / App Store 等买断制平台
- 选型类问题先读 [references/decision-engine-tech.md](references/decision-engine-tech.md) 用决策树论证，再落地
- 资源/发行/QA 类问题先读对应 `references/` playbook，再调子技能

## 技能添加流程

1. 在 `skills/` 下创建以技能名命名的目录
2. 编写 `SKILL.md`（保留 `source` 字段）
3. 确保 `metadata` 字段完整
4. 更新 `README.md` 中的技能清单表与 `SKILL.md` 路由表

## 不做什么

- 不创建需要服务器/账号体系的产品技能
- 不创建面向大团队协作的技能
- 不创建免费+IAP/广告变现模式的技能（专注买断制）
