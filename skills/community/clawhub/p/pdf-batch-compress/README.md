# PDF 批量压缩技能

## 快速开始

```bash
# 一键压缩目录下所有超过 50MB 的 PDF
bash ~/Desktop/pdf-batch-compress-skill/scripts/batch_compress.sh "/path/to/pdf/directory"

# 自定义阈值（如 30MB）
bash ~/Desktop/pdf-batch-compress-skill/scripts/batch_compress.sh "/path/to/pdf/directory" 30

# 自定义并行数（如 4 进程）
bash ~/Desktop/pdf-batch-compress-skill/scripts/batch_compress.sh "/path/to/pdf/directory" 50 4
```

## 环境依赖

```bash
# 1. 安装 Ghostscript
brew install ghostscript

# 2. 安装 Python PDF 库
/Users/weidong/.workbuddy/binaries/python/versions/3.13.12/bin/python3 -m venv /Users/weidong/.workbuddy/binaries/python/envs/default
/Users/weidong/.workbuddy/binaries/python/envs/default/bin/pip install pymupdf pikepdf
```

## 压缩策略

**Ghostscript 优先 → PyMuPDF 兜底**

1. 先用 Ghostscript 快速压缩（保留文本可搜索，速度最快）
2. GS 失败的文件用 PyMuPDF 渲染为图片 PDF（处理结构有缺陷的 PDF）
3. 多级 DPI 降级直到达标

## 文件结构

```
pdf-batch-compress-skill/
├── SKILL.md                      # 完整文档
├── README.md                     # 快速指南（本文件）
└── scripts/
    ├── batch_compress.sh         # 一键编排脚本
    ├── compress_single_gs.py     # GS 单文件压缩
    ├── compress_fast.py          # PyMuPDF 渲染压缩（优化版）
    ├── compress_single.py        # PyMuPDF 完整版（含 pikepdf）
    └── report.sh                 # 报告生成脚本
```

## 实测数据

基于 1430 个超过 50MB 的扫描版 PDF：
- 成功率：99.5%
- 总节省空间：76 GB
- 总耗时：约 2.5 小时
