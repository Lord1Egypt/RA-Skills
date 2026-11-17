---
name: presentation-designer
description: 专业演示文稿设计：5 套品牌风格、排版体系、动画指南、一致性验证，产出 Apple/Microsoft/Google 级别幻灯片
source:
  type: derived
  url: https://skills.sh/willem4130/claude-code-skills/elite-powerpoint-designer
  repo: skills-repo/office-master
  path: skills/presentation-designer/SKILL.md
  version: "1.0"
  updated: "2026-07-28"
metadata:
  category: 演示设计
  platform: 通用
  difficulty: 进阶
---

# 专业演示文稿设计师

> 将内容转化为世界级演示文稿，达到 Apple 发布会、Microsoft 产品发布、Google I/O 的设计水准。

## 能力

- **5 套品牌风格**：科技Keynote、企业专业、创意大胆、金融精英、创业融资
- **智能模板匹配**：根据内容类型自动选择合适版式（标题页/章节页/对比/时间线/数据图表）
- **排版体系**：字体层级（24-96pt）、间距系统、色彩应用规范
- **专业动画**：入场淡入、数量递增、章节过渡，每页最多 3 个动画元素
- **一致性验证**：字体、颜色、间距、模板使用的自动检查

## 使用方式

在 Claude Code 中使用 `/presentation-designer` 调用。

```
/presentation-designer 为我的创业项目做一份融资路演 PPT
/presentation-designer 把这份 Markdown 转为科技 Keynote 风格演示
/presentation-designer 将季度报告做成企业专业风格的幻灯片
```

## 工作流

1. 分析内容类型和受众，推荐品牌风格
2. 解析 Markdown 结构，自动匹配幻灯片版式
3. 应用设计系统（字体层级、间距、色彩）
4. 添加专业过渡和动画效果
5. 运行一致性验证，输出 .pptx 文件

## 适用场景

- 融资路演和创业 Pitch Deck
- 产品发布和发布会演示
- 季度/年度业务报告
- 技术分享和会议演讲
- 销售提案和客户演示

## 限制

- 需要 Office-PowerPoint-MCP-Server 或 python-pptx 环境
- 动画效果在不同平台兼容性不一（建议预览确认）
- 复杂数据图表建议先单独制作再嵌入
- 最终效果依赖于 python-pptx 对动画和渐变的支持程度

## 相关参考（Playbook）

- 选哪套品牌风格、每页用哪种版式、排版硬规则与一致性验证 → [references/presentation-design-system.md](../../references/presentation-design-system.md)
- 演示大纲结构门禁（页数/标题长度/重复）→ [scripts/check_ppt_brief.py](../../scripts/check_ppt_brief.py) + [assets/presentation-brief-template.md](../../assets/presentation-brief-template.md)
- 上游 Markdown 如何分页成 .pptx 骨架 → [references/office-md-roundtrip.md](../../references/office-md-roundtrip.md)
- 品牌五件套跨会话复用 → [skills/office-context/SKILL.md](../office-context/SKILL.md)

> 本技能只负责**怎么设计出来**；风格选型、版式矩阵、交付格式兼容性在上述 `references/` 中决策。
