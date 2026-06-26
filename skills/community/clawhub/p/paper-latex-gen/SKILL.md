---
name: paper-latex-gen
description: [已整合] LaTeX 生成功能已整合到 paper 统一入口技能
argument-hint: "[会议名] [主题]"
---

# ⚠️ 已整合 - 请使用 paper 统一入口

> **本技能保留用于向后兼容，功能已整合到 `paper` 统一入口技能**
>
> **推荐使用：** `paper latex [会议名] [主题]` 或直接使用本技能（自动转发）

---

# Paper LaTeX Generator（兼容层）

专业级学术论文 LaTeX 生成技能，提供会议模板和结构化生成。

## 迁移指南

**新用法：**
```
paper latex neurips 2025 深度学习
paper latex icml 强化学习
paper latex ieee 振动控制
```

**旧用法（仍然可用）：**
```
latex neurips 2025 深度学习
```

## 支持的会议模板
| 会议 | 年份 | 特点 |
|------|------|------|
| NeurIPS | 2024, 2025 | 机器学习顶会，双栏格式 |
| ICML | 2025, 2026 | 机器学习顶会，单栏格式 |
| ICLR | 2025, 2026 | 深度学习顶会，开放评审 |

## 输出格式
- paper.tex - 主 LaTeX 文件
- references.bib - BibTeX 引用文件
- figures/ - 图表目录
- 会议模板文件
