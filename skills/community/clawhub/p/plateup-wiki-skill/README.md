# PlateUp Wiki Skill

PlateUp Wiki Skill 是面向 **PlateUp!（速速上菜）** 的 OpenClaw 知识技能，覆盖食谱、设备、自动化、卡牌、成就、顾客规则和游戏术语。

[English README](README.en.md)

## 功能

- 支持中文和英文问题
- 查询食谱、变体、配料和制作步骤
- 查询设备属性、升级树和自动化交互
- 查询卡牌效果、前置条件和成就条件
- 查询顾客阶段、耐心规则和队列机制
- 提供双语术语表和缺失中文译名建议
- 保留来源和游戏版本信息

## 语言规则

- 英文问题只显示英文游戏名称。
- 中文问题优先使用词表中的通用中文译名。
- 没有译名或只有建议译名时，显示 `建议译名：中文（English Name）`。
- 建议译名不会被当作官方本地化。

## 目录结构

```text
plateup-wiki-skill/
├── SKILL.md                  # 技能指令
├── agents/openai.yaml         # 可选界面元数据
└── references/
    ├── index.md               # 查询索引
    ├── recipes.yaml           # 食谱与变体
    ├── recipe-steps.yaml      # 制作步骤索引
    ├── appliances.yaml        # 设备与自动化
    ├── ingredients.yaml       # 食材映射
    ├── cards.yaml             # 卡牌
    ├── achievements.yaml      # 成就
    ├── customers.yaml         # 顾客阶段
    ├── terms.yaml             # 双语词表
    └── data-schema.md         # 数据规范
```

## OpenClaw 安装

将本目录复制或链接到 OpenClaw skill 目录：

```bash
cp -R plateup-wiki-skill ~/.openclaw/skills/plateup-wiki-skill
```

安装后可以使用 `$plateup-wiki-skill` 显式调用，也可以让 OpenClaw 在相关问题中自动选择该技能。

## 发布到 ClawHub

本仓库根目录已经适合作为 ClawHub skill 发布。发布时请保留根目录下的 `SKILL.md`，并一并包含 `references/` 目录。

## 数据来源

- [PlateUp! Official Wiki](https://wiki.plateupgame.com/)
- [PlateUp! Official Updates](https://www.plateupgame.com/updates/)
- [Bilibili 术语参考](https://www.bilibili.com/opus/709028087756488743)
- [Steam 社区成就指南](https://steamcommunity.com/sharedfiles/filedetails/?id=3267294764)

官方 Wiki 和更新说明优先用于游戏机制；社区来源主要用于译名、成就攻略和实用策略，并会标明来源性质。

## 数据规范

- 英文名称和稳定 ID 是规范标识。
- `null` 表示尚未采集到已核实的数据。
- 未知字段不会凭经验猜测。
- 食谱原始步骤文本会保留，便于追溯。
- `name_only` 表示仅收录设备名称，尚未结构化其机制。

## 状态

这是社区维护的参考技能，与 PlateUp! 或其开发团队没有官方关联或背书。
