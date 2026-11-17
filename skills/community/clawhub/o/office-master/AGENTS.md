# Office Master — Agent 入口

> 本仓库是 skills-repo 组织下的办公效率技能库。Agent 在处理 office-master 相关任务时加载本文件。采用 superpower 架构。

## 目录约定（superpower）

| 层 | 目录 | 职责 | Agent 何时读 |
|----|------|------|--------------|
| L1 | `SKILL.md` | 路由层，能力索引 | 始终先读 |
| L2 | `references/` | 深层 playbook（往返/设计/门禁） | 按路由表按需加载 |
| L3 | `skills/` | 四个细粒度子技能 | 落地具体动作时调用 |
| L4 | `scripts/` | 确定性文档检查脚本 | 需核查样式/大纲时运行 |
| L5 | `assets/` | 样式规则、brief 模板 | 被 scripts 读取执行 |

## 加载顺序

1. 读 `SKILL.md` 路由表，判断任务属于哪一类。
2. 做方法论决策（转换方向、品牌风格、样式门禁）→ 读对应 `references/`。
3. 要落地具体动作（转格式、做设计、跑 python-pptx）→ 调 `skills/` 子技能。
4. 需确定性检查（标题层级、大纲结构）→ 跑 `scripts/`，规则来自 `assets/`。

## 技能清单

| 技能 | 文件 | 用途 |
|------|------|------|
| office-to-md | [skills/office-to-md/SKILL.md](skills/office-to-md/SKILL.md) | Office 文档转 Markdown |
| md-to-office | [skills/md-to-office/SKILL.md](skills/md-to-office/SKILL.md) | Markdown 转 Office 文档 |
| presentation-designer | [skills/presentation-designer/SKILL.md](skills/presentation-designer/SKILL.md) | 专业演示文稿设计 |
| ppt-automation | [skills/ppt-automation/SKILL.md](skills/ppt-automation/SKILL.md) | PowerPoint 自动化操作 |

## 适用场景

- 独立开发者需要将文档在不同格式间转换
- 需要制作专业级演示文稿但缺乏设计能力
- 批量处理 Office 文档

## 技能来源

所有技能改编自 skills.sh 社区的成熟技能（安装量 ≥1K），详情见各 SKILL.md 的 source 字段。
