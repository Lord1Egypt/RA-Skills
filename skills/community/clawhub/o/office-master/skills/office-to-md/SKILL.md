---
name: office-to-md
description: Office/PDF 文档转 Markdown，支持 Word/Excel/PPT/图片/音频，基于 markitdown 驱动
source:
  type: derived
  url: https://skills.sh/claude-office-skills/skills/office-to-md
  repo: skills-repo/office-master
  path: skills/office-to-md/SKILL.md
  version: "1.0"
  updated: "2026-07-28"
metadata:
  category: 格式转换
  platform: 通用
  difficulty: 入门
---

# Office 文档转 Markdown

> 将 Word、Excel、PowerPoint、PDF 等 Office 格式转换为 Markdown，让文档可搜索、可版本控制、AI 友好。

## 能力

- Word (.docx) 转 Markdown，保留标题、表格、列表、超链接
- Excel (.xlsx) 转 Markdown 表格，每个 Sheet 独立分节
- PowerPoint (.pptx) 转 Markdown，每页幻灯片一个章节
- PDF 文本提取为 Markdown
- 图片 OCR（需 Vision 模型）和音频转录
- 批量转换整个目录

## 使用方式

在 Claude Code 中使用 `/office-to-md` 调用。

```
/office-to-md 把这份 Word 文档转成 Markdown
/office-to-md 将这个 Excel 表格提取为 Markdown 格式
/office-to-md 批量转换 ./documents 目录下所有文件
```

## 工作流

1. 确认源文件格式和目标需求
2. 安装 markitdown：`pip install markitdown[all]`
3. 运行转换脚本：`markitdown input.docx -o output.md`
4. 检查输出质量，调整复杂表格和格式
5. 将 Markdown 纳入 Git 版本控制

## 适用场景

- 项目文档从 Word 迁移到 Markdown/Git 工作流
- Excel 数据转为可搜索的 Markdown 表格
- 会议 PPT 提取为文本纪要
- PDF 报告内容提取后做 AI 分析
- 构建 AI 训练用的文档语料库

## 限制

- 复杂排版（嵌套表格、文本框）可能丢失
- 图片不嵌入，仅通过 Vision 模型生成描述文本
- Word 修订痕迹和批注不会保留
- 部分表格结构转换后需手动调整

## 相关参考（Playbook）

- 该不该转、往哪转、往返失真与「何时不该转」的决策 → [references/office-md-roundtrip.md](../../references/office-md-roundtrip.md)
- 转出的 Markdown 是否结构合法（标题层级/单一 H1）→ [references/doc-style-quality-gates.md](../../references/doc-style-quality-gates.md) + [scripts/check_doc_style.py](../../scripts/check_doc_style.py)
- 抽取出的内容要做成演示 → [references/presentation-design-system.md](../../references/presentation-design-system.md)
- 兄弟子技能：反向生成 [skills/md-to-office](../md-to-office/SKILL.md)

> 本技能只负责**怎么转**（命令与参数）；转不转、失真容忍度、批量策略在上述 `references/` 中决策。
