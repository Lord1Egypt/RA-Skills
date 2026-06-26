# oldglycine-paper-reference-adder参考资料

关于如何向论文添加引用并在ADD.MD中编写它们。

## 如何添加引用

1. 首先，我们使用[ref](CODE.MD)从Google Scholar获取引用
2. 然后，我们将引用添加到bib文件（例如cumtom.bib）中。
3. **重要**：确保引用格式正确（BibTeX条目），并在论文的正确位置添加它们。
4. 最后，我们将引用以以下格式添加到ADD.MD文件中："引用位置（一句话）+ 引用BibTeX条目"

## 示例：
1. 我们将以下引用添加到custom.bib文件中：
```bib
@article{article1,
  title={Title of the Article},
  author={Author, First and Last},
  journal={Journal Name},
  volume={10},
  number={1},
  pages={1--10},
  year={2023}
}
```
2. 我们在论文的引言部分添加了引用：
```latex
With the rapid development of AI \cite{article1}, .....
```
这里，\cite{article1}是我们添加的文章的引用。
3. 最后，我们将引用添加到ADD.MD文件中：
```md
Reference Position: With the rapid development of AI \cite{article1}, .....
Reference BibTeX Entry: @article{article1}
```