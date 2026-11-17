# MathModel Toolkit

数学建模竞赛工具箱——提供 CUMCM 官方 LaTeX 论文模板（基于 cumcmthesis.cls v2.6）、常用建模算法代码库与数据预处理工具。

## 使用方式

当用户要求生成论文、编写建模代码或需要模板时，根据用户需求调用以下资源。

## References

- `references/cumcmthesis.cls` — CUMCM 国赛官方 LaTeX 文档类 v2.6（依赖 XeLaTeX 编译）
- `references/cumcm-latex-template.tex` — 简易 ctexart 模板（备选，无需额外 cls 文件）
- `references/common-algorithms.md` — 常用数学建模算法速查与 Python 实现
- `references/bib/gbt7714-numerical.bst` — GB/T 7714 数字编号参考文献样式（推荐）
- `references/bib/gbt7714-2005.bst` — GB/T 7714-2005 国标参考文献样式（备选）
- `references/bib/ref.bib` — BibTeX 参考文献数据库模板（Zotero 导出）
- `references/font/` — 模板所需中英文字体（YaHei.Consolas, MONACO, Fira Code）

## Templates

- `templates/template_数学建模国赛.tex` — 基于 cumcmthesis.cls 的完整 CUMCM 论文模板，包含封面、承诺书、编号页、8 章论文结构、BibTeX 参考文献管理、代码附录

## 模板编译方式

```
编译引擎: XeLaTeX（必须，不支持 pdfLaTeX）
编译流程: XeLaTeX → BibTeX → XeLaTeX → XeLaTeX
参考文献: \bibliographystyle{gbt7714-numerical}  + \bibliography{bib/ref}
```

模板默认选项：`withoutpreface`（去封面编号页，电子提交用）、`bwprint`（黑白打印），可根据需要修改。

## 工作流程

1. **确定需求**：用户需要论文模板还是算法代码？
2. **读取资源**：读取 references 或 templates 下的对应文件
3. **定制论文**：
   - 以 `templates/template_数学建模国赛.tex` 为基础
   - 填充题号(tihao)、报名号(baominghao)、学校、队员、指导教师、日期
   - 按 8 章结构填写：问题重述 → 问题分析 → 模型假设 → 符号说明 → 各问题模型 → 模型评价 → 参考文献 → 附录
   - 图片放 `figures/` 目录，代码放附录
   - 使用 `\upcite{}` 上标引用参考文献
4. **输出**：生成完整的 `.tex` 源码文件，确保可直接编译
