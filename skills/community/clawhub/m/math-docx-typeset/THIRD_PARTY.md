# 第三方依赖与许可证声明（THIRD_PARTY）

本 skill 的全部自有代码（`SKILL.md`、`README.md`、`references/*`、`scripts/latex2docx.py`）均为原创，采用与本项目一致的宽松许可，可自由使用、修改、分发。

本 skill **不打包任何第三方库的源代码**，所有依赖均由使用者通过 `pip install` 安装，各依赖包自带的 LICENSE 随 PyPI 分发。以下列出运行所必需的第三方依赖及其许可证，以满足上游项目的 attribution 要求（均为宽松许可证，无 GPL 类传染性义务）：

| 依赖 | 版本 | 作者 | 许可证 | 项目地址 |
|---|---|---|---|---|
| latex2mathml | 3.x | Ronie Martinez | MIT | https://github.com/roniemartinez/latex2mathml |
| mathml2omml | 0.0.2 | amedama (Copyright 2019) | MIT | https://github.com/amedama41/mathml2omml |
| python-docx | 1.x | Steve Canny | MIT | https://github.com/python-openxml/python-docx |
| matplotlib | 3.x | Matplotlib Development Team | Matplotlib License（BSD 风格） | https://github.com/matplotlib/matplotlib |

## 许可证原文要点

### MIT License（latex2mathml / mathml2omml / python-docx）

> Copyright (c) 各自作者（Ronie Martinez / amedama 2019 / Steve Canny）
>
> Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction... subject to the following conditions:
>
> **The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.**

即：若在任何分发物中包含上述库的源代码副本，需保留其版权与许可声明。本 skill 以 `pip` 依赖方式使用，**未将源码打包进本仓库**，故不构成"分发副本"；此处列出仅为透明与合规留痕。

### Matplotlib License（BSD 风格）

Matplotlib 采用经修改的 BSD 许可证（PSF 风格）。若基于 matplotlib 准备衍生作品，应在作品中包含版权声明的简要摘要。本 skill 仅在「图片对照版」（`--image-variant`）功能中调用 matplotlib 进行公式渲染，且通过 `pip` 依赖使用，未直接分发其代码。

## 上游项目思路说明（非代码复制）

- **`XiaoMaColtAI/math-modeling-skill`**：仅在本 skill 设计初期作为「学术 LaTeX 排版工具」的调研参考对象，提供「环境诊断 + 编译校验」的方向启发。本 skill 的实际实现路线（LaTeX→MathML→OMML 生成 Word 原生可编辑公式、Python 库串联、降级预案、图片对照附件、引号修正）与其编译路线（`latexmk`/`XeLaTeX`）完全不同，**未复制其任何源代码**。
- 本 skill 的直接重建规范来源是使用者提供的《学术论文 LaTeX‑docx 公式排版 Skill 开发指南》附件，以及自有设计。

---
最后更新：math-docx-typeset v1.2
