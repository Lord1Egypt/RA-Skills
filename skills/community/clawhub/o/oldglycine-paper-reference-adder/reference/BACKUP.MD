# oldglycine-paper-reference-adder备份文件

关于如何备份文件，以及决定哪些文件应该备份、哪些文件应该修改。

## 如何备份
- 备份用户的论文目录：
```
Workspace/
    ├── 用户的论文目录/             # 在此处编辑custom.bib和tex文件以添加引用。
        ├── custom.bib
        ├── main.tex
        ├── sections/
            ├── Introduction.tex
            ├── RelatedWork.tex
            ├── Method.tex
            ...
    ├── 用户的论文目录_backup/      # 项目目录的备份。请勿编辑！
        ├── custom.bib
        ├── main.tex
        ├── sections/
            ├── Introduction.tex
            ├── RelatedWork.tex
            ├── Method.tex
            ...
    ├── ADD.MD
    ├── 其他文件...                      # 忽略它们。
```