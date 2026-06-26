---
name: oldglycine-paper-reference-adder
description: 自动为研究论文添加相关学术引用。支持Overleaf项目目录，从TeX文件提取关键词，在Google Scholar搜索相关论文，将BibTeX条目添加到项目的bib文件，并在关键部分插入引用标记。
metadata:
  versions: 1.1.0
---
# oldglycine-paper-reference-adder

## 使用场景
- 当研究论文需要在特定部分（引言、相关工作、方法）添加额外引用时
- 当你想根据论文内容查找相关引用文献时
- 当你需要确保不添加重复引用时

## 工作原理
1. **备份**: 创建项目目录的备份以防止数据丢失
2. **内容分析**: 读取TeX文件并提取关键词和现有引用
3. **引用搜索**: 使用Google Scholar（通过scholarly库）查找相关论文
4. **BibTeX生成**: 为新引用生成BibTeX条目
5. **集成**: 将新引用添加到bib文件并在文章中插入引用标记
6. **报告**: 生成包含所有添加引用及其位置的ADD.MD文件

## 参考资料
- 代码参考 [ref](./reference/CODE.MD)
  - 代码并不是即插即用，你**必须**根据用户的论文结构以及文章内容调整代码。
- 如何备份 [ref](./reference/BACKUP.MD)
- 如何添加引用 [ref](./reference/REFERENCES.MD)

## 参数
- `project_dir`: Overleaf项目目录路径
- `num_references`: 要查找的引用数量（默认：10）
- `output_report`: ADD.MD报告的路径（默认：./ADD.MD）

## 依赖项
- scholarly（用于Google Scholar搜索）
- bibtexparser（用于BibTeX处理）
- pdflatex（可选，用于编译论文）

## 注意事项
- 处理现有引用以避免重复
- 重点在关键部分（引言、相关工作、方法）插入引用
- 生成所有添加引用的详细报告
- 兼容Overleaf项目结构
- 使用scholarly库作为Google Scholar API的替代方案
