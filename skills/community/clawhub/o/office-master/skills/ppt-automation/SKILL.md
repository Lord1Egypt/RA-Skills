---
name: ppt-automation
description: PowerPoint 编程自动化：python-pptx 创建/修改/提取幻灯片，模板驱动，MCP 集成
source:
  type: derived
  url: https://skills.sh/practicalswan/agent-skills/powerpoint-ppt
  repo: skills-repo/office-master
  path: skills/ppt-automation/SKILL.md
  version: "1.0"
  updated: "2026-07-28"
metadata:
  category: 演示
  platform: 通用
  difficulty: 进阶
---

# PowerPoint 自动化操作

> 通过 python-pptx 编程操作 .pptx 文件：创建幻灯片、应用模板、插入图片、提取文本。

## 能力

- 从结构化数据创建幻灯片
- 应用模板、品牌配色和幻灯片布局
- 更新已有演示文稿中的文本、图片、图表
- 提取幻灯片文本用于审校或翻译
- MCP 不可用时的本地 python-pptx 回退方案

## 使用方式

在 Claude Code 中使用 `/ppt-automation` 调用。

```
/ppt-automation 从这份 Markdown 创建一套幻灯片
/ppt-automation 给这个 PPT 套上公司模板
/ppt-automation 提取这张幻灯片的所有文本
/ppt-automation 批量替换 PPT 中的图片
```

## 工作流

1. 确认 MCP 工具是否可用，不可用则走 python-pptx 回退
2. 解析输入内容和目标需求
3. 编写 python-pptx 脚本创建或修改 .pptx 文件
4. 打开/渲染输出文件进行视觉验证
5. 检查布局、字体、配色是否一致

## 适用场景

- 批量生成标准化幻灯片（如周报、月报模板）
- 为已有 PPT 更换模板和品牌配色
- 从 PPT 中提取文本用于翻译或审校
- 编程方式操作演示文稿，无需手动重复操作

## 限制

- 依赖于 python-pptx 库，部分高级动画和效果不支持
- 复杂图表的编程操作较繁琐
- MCP 可用性因客户端而异，需提前确认
- 图片质量依赖于源文件分辨率，建议 1920x1080 以上

## 相关参考（Playbook）

- 版式选择矩阵、排版硬规则、python-pptx 落地要点与「基线版 vs 手调」约定 → [references/presentation-design-system.md](../../references/presentation-design-system.md)
- 大纲结构先过门禁再编程生成 → [scripts/check_ppt_brief.py](../../scripts/check_ppt_brief.py) + [references/doc-style-quality-gates.md](../../references/doc-style-quality-gates.md)
- 从 Markdown 生成初始骨架（先生成再编程改）→ [skills/md-to-office/SKILL.md](../md-to-office/SKILL.md)
- 模板路径与品牌色板的跨会话复用 → [skills/office-context/SKILL.md](../office-context/SKILL.md)

> 本技能只负责**怎么用代码操作 .pptx**；用哪种版式、动画上限、是否该覆盖人工微调在上述 `references/` 中决策。
