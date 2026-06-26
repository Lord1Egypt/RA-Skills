# openclaw-skills-setup-cn

面向中文用户的 ClawHub 安装与使用技能（Skill），覆盖安装、镜像配置、**找技能**（发现/推荐）以及技能管理。

## 技能结构（标准 Skill 布局）

```
openclaw-skills-setup-cn/
├── SKILL.md    # 技能说明与触发条件（必选）
├── README.md   # 本文件
└── .gitignore
```

## 功能

- ClawHub 安装与初始化
- 镜像配置（支持阿里云镜像）
- **找技能**：根据需求发现、推荐并安装技能
- 技能的安装、更新、启用/禁用

## 安装

```bash
clawhub install openclaw-skills-setup-cn
```

## 触发场景

当在 OpenClaw 中使用时，以下关键词或场景会激活本技能：

- **ClawHub 本身**：`clawhub`、`安装 clawhub`、`clawhub 怎么用`
- **找技能**：`找技能` / `找 skill`、`有什么技能可以` / `有什么 skill 可以`、`找一个技能` / `找一个 skill`、`搜索技能` / `搜索 skill`
- **技能管理**：`安装技能` / `安装 skill`、`更新技能` / `更新 skill`、`管理技能` / `管理 skill`
- **CLI 命令**：`clawhub init`、`clawhub install`、`clawhub search`、`clawhub update`、`openclaw skills`

## 许可证

MIT
