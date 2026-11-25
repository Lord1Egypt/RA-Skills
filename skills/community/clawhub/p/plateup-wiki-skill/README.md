# PlateUp Wiki Skill

PlateUp Wiki Skill 是面向 **PlateUp!（速速上菜）** 的知识技能，覆盖食谱、设备、自动化、卡牌、成就、顾客规则和游戏术语。

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

- 默认用提问的语言回答；用户明确要求其他语言、双语展示或翻译时，按其要求处理。
- 英文回答默认只显示英文游戏名称。
- 中文回答默认只显示词表已有的通用中文译名（`zh_status: community`）；词表未收录或仅有建议译名时，显示 `建议译名：中文（English Name）`。建议译名不是官方本地化。

## 目录结构

```text
plateup-wiki-skill/
├── SKILL.md                  # 技能指令
├── agents/openai.yaml         # 可选界面元数据
└── references/
    ├── index.md               # 查询索引
    ├── recipes.yaml           # 食谱、变体与制作步骤
    ├── appliances.yaml        # 设备与自动化
    ├── ingredients.yaml       # 食材反查补充
    ├── cards.yaml             # 卡牌
    ├── achievements.yaml      # 成就
    ├── customers.yaml         # 顾客阶段
    ├── terms.yaml             # 双语词表
    └── data-schema.md         # 数据规范
```

## OpenClaw 安装

从 GitHub 安装到 OpenClaw 当前工作区：

```bash
openclaw skills install git:syh31/plateup-wiki-skill@main
```

安装后可以在聊天中使用 `$plateup-wiki-skill` 显式调用，例如 `$plateup-wiki-skill 披萨怎么做？`。

## Hermes Agent 安装

在当前本地仓库根目录运行以下命令，将 `SKILL.md` 和 `references/` 复制到 Hermes 的默认技能目录：

```bash
mkdir -p ~/.hermes/skills/plateup-wiki-skill/references
cp SKILL.md ~/.hermes/skills/plateup-wiki-skill/
cp -R references/. ~/.hermes/skills/plateup-wiki-skill/references/
hermes skills list
```

在列表中看到该技能后，可在 Hermes 聊天中输入 `/plateup-wiki-skill 披萨怎么做？`。使用自定义配置目录时，请参照 [Hermes 技能文档](https://hermes-agent.nousresearch.com/docs/user-guide/features/skills) 调整路径。

## 发布到 ClawHub

通过 [ClawHub 的 GitHub 导入](https://github.com/openclaw/clawhub/blob/main/docs/skill-format.md#github-import) 发布时，请选择自己账号下的公开、非 Fork 仓库，在预览中确认根目录的 `SKILL.md` 和 `references/` 都包含在发布包内。

ClawHub 发布采用 [MIT-0](https://github.com/openclaw/clawhub/blob/main/docs/skill-format.md#license)。发布前请确认有权按该许可分发所包含的内容；列出 Wiki 或社区来源不等于取得再分发授权。

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
- [食谱与制作步骤](references/recipes.yaml)是食材反查的主表，[食材映射](references/ingredients.yaml)补充未列在主表中的对应关系。
- `name_only` 表示仅收录设备名称，尚未结构化其机制。

## 状态

这是社区维护的参考技能，与 PlateUp! 或其开发团队没有官方关联或背书。
