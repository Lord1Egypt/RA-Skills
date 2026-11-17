---
name: md-to-office
description: Markdown 转 Word/PPT/PDF，Pandoc 驱动的专业文档生成，支持模板和批量转换
source:
  type: derived
  url: https://skills.sh/claude-office-skills/skills/md-to-office
  repo: skills-repo/office-master
  path: skills/md-to-office/SKILL.md
  version: "1.0"
  updated: "2026-07-28"
metadata:
  category: 格式转换
  platform: 通用
  difficulty: 入门
---

# Markdown 转 Office 文档

> 将 Markdown 文件转换为 Word、PowerPoint、PDF 等 Office 格式，支持自定义模板和样式。

## 能力

- Markdown 转 Word (.docx)，支持目录生成和参考模板
- Markdown 转 PowerPoint (.pptx)，按标题分页、支持备注
- Markdown 转 PDF，支持 LaTeX 和 HTML 渲染引擎
- Markdown 转 EPUB 电子书
- YAML 前置元数据设置文档属性
- 批量转换和 Python 脚本集成

## 使用方式

在 Claude Code 中使用 `/md-to-office` 调用。

```
/md-to-office 把 README.md 转成专业的 Word 文档
/md-to-office 将笔记转成 PowerPoint 演示文稿
/md-to-office 生成带自定义样式的 PDF
/md-to-office 用公司模板生成 Word 报告
```

## 工作流

1. 确认 Markdown 源文件和目标格式
2. 安装 Pandoc：`brew install pandoc`（macOS）
3. （可选）准备参考模板文件（.docx/.pptx）
4. 运行转换：`pandoc input.md -o output.docx --reference-doc=template.docx`
5. 打开输出文件检查格式，微调 YAML 元数据后重新生成

## 适用场景

- 技术文档生成 Word/PDF 交付件
- 演讲笔记快速转为幻灯片
- API 文档生成多格式分发
- Markdown 写作后输出电子书（EPUB）
- 批量生成标准化报告（配合 Python 脚本）

## 限制

- 复杂 Word 排版可能不完全还原
- PDF 转换需安装 LaTeX（高质量）或 wkhtmltopdf（轻量）
- PowerPoint 不支持动画效果
- 高级表格和图片定位需手动调整

## 相关参考（Playbook）

- 源真相方向、模板策略、批量与目录级转换 → [references/office-md-roundtrip.md](../../references/office-md-roundtrip.md)
- 转换前的结构门禁（先卡再转，省返工）→ [references/doc-style-quality-gates.md](../../references/doc-style-quality-gates.md) + [scripts/check_doc_style.py](../../scripts/check_doc_style.py)
- 生成 .pptx 后的版式与品牌设计 → [references/presentation-design-system.md](../../references/presentation-design-system.md)
- 品牌色板 / `--reference-doc` 模板的跨会话复用 → [skills/office-context/SKILL.md](../office-context/SKILL.md)

> 本技能只负责**怎么转**（Pandoc 命令与参数）；转换方向、模板选择、门禁位置在上述 `references/` 中决策。
