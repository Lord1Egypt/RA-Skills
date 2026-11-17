---
name: pdf-batch-compress
description: 批量压缩超过指定大小的PDF文件，Ghostscript + PyMuPDF双引擎降级压缩，保留最佳画质
version: 1.0.0
title: "PDF 批量压缩技能"
summary: "批量压缩超过指定大小的 PDF 文件，支持 Ghostscript + PyMuPDF 双引擎降级压缩，保留最佳画质"
read_when:
  - 需要批量压缩 PDF 文件到指定大小以下
  - PDF 文件过大需要减小体积
  - 扫描版书籍 PDF 需要压缩
  - 需要替换原文件并保留原文件名
metadata:
  openclaw:
    requires:
      bins:
        - gs
        - python3
    os:
      - macos
      - linux
    emoji: 📦
    homepage: https://github.com/weidong/pdf-batch-compress
---

# PDF 批量压缩技能

将目录下所有超过指定大小（默认 50MB）的 PDF 文件压缩到阈值以下，压缩后替换原文件并保留原文件名。

## 核心策略：双引擎降级压缩

本技能采用 **Ghostscript 优先 + PyMuPDF 兜底** 的双引擎策略，确保最高压缩成功率：

### 引擎 1：Ghostscript（主力，速度快 4-6 倍）
- 保留文本可搜索（OCR 层不丢失）
- 速度极快：单文件约 5-15 秒
- 4 级降级：`ebook(150dpi)` → `screen(72dpi)` → `aggressive(72dpi+高压缩)` → `extreme(50dpi)`
- 对标准 PDF 成功率约 75%

### 引擎 2：PyMuPDF 渲染（兜底，处理 GS 失败的文件）
- 将每页渲染为 JPEG 图片后重建 PDF
- 能处理结构有缺陷的 PDF（如 Foxit PhantomPDF 生成的文件）
- 多级 DPI 降级：150→120→100→80→72→60→50 dpi
- 成功率接近 100%（仅极少数超大文件无法达标）

### 最佳努力机制
- 当所有降级方案仍无法达标时，选择压缩效果最好的版本替换原文件
- 前提是压缩后至少比原始文件小 30%，否则保留原文件

## 环境依赖

### 必需工具
```bash
# Ghostscript（主力引擎）
brew install ghostscript

# Python 3 + PDF 库（兜底引擎）
# 使用 WorkBuddy 管理的 Python 环境
/Users/weidong/.workbuddy/binaries/python/versions/3.13.12/bin/python3 -m venv /Users/weidong/.workbuddy/binaries/python/envs/default
/Users/weidong/.workbuddy/binaries/python/envs/default/bin/pip install pymupdf pikepdf
```

### 验证安装
```bash
which gs && gs --version
/Users/weidong/.workbuddy/binaries/python/envs/default/bin/python3 -c "import fitz; import pikepdf; print('OK')"
```

## 使用方法

### 一键执行（推荐）

```bash
# 压缩指定目录下所有超过 50MB 的 PDF
bash ~/Desktop/pdf-batch-compress-skill/scripts/batch_compress.sh "/path/to/pdf/directory"

# 自定义阈值（如压缩到 30MB 以下）
bash ~/Desktop/pdf-batch-compress-skill/scripts/batch_compress.sh "/path/to/pdf/directory" 30

# 自定义并行进程数（默认 8）
bash ~/Desktop/pdf-batch-compress-skill/scripts/batch_compress.sh "/path/to/pdf/directory" 50 4
```

### 分步执行

```bash
# 步骤 1：查找所有超过阈值的 PDF
find "/path/to/directory" -iname "*.pdf" -type f -size +50M > /tmp/large_pdfs.txt
wc -l /tmp/large_pdfs.txt

# 步骤 2：用 Ghostscript 批量压缩（8 进程并行）
tr '\n' '\0' < /tmp/large_pdfs.txt | xargs -0 -P 8 -I {} \
  /Users/weidong/.workbuddy/binaries/python/envs/default/bin/python3 \
  ~/Desktop/pdf-batch-compress-skill/scripts/compress_single_gs.py "{}" \
  2>&1 | tee /tmp/compress_log_gs.txt

# 步骤 3：用 PyMuPDF 处理 GS 失败的剩余文件
find "/path/to/directory" -iname "*.pdf" -type f -size +50M > /tmp/large_pdfs_remaining.txt
tr '\n' '\0' < /tmp/large_pdfs_remaining.txt | xargs -0 -P 8 -I {} \
  /Users/weidong/.workbuddy/binaries/python/envs/default/bin/python3 \
  ~/Desktop/pdf-batch-compress-skill/scripts/compress_fast.py "{}" \
  2>&1 | tee /tmp/compress_log_final.txt

# 步骤 4：生成报告
bash ~/Desktop/pdf-batch-compress-skill/scripts/report.sh
```

### 单文件压缩

```bash
# 用 Ghostscript 压缩单个文件
/Users/weidong/.workbuddy/binaries/python/envs/default/bin/python3 \
  ~/Desktop/pdf-batch-compress-skill/scripts/compress_single_gs.py "/path/to/file.pdf"

# 用 PyMuPDF 压缩单个文件（GS 失败时使用）
/Users/weidong/.workbuddy/binaries/python/envs/default/bin/python3 \
  ~/Desktop/pdf-batch-compress-skill/scripts/compress_fast.py "/path/to/file.pdf"
```

## 脚本说明

| 脚本 | 用途 | 特点 |
|------|------|------|
| `batch_compress.sh` | 一键编排脚本 | 自动完成查找→GS压缩→PyMuPDF兜底→报告 |
| `compress_single_gs.py` | GS 单文件压缩 | 保留文本可搜索，速度最快 |
| `compress_fast.py` | PyMuPDF 渲染压缩 | 处理 GS 失败的 PDF，直接从低 DPI 开始 |
| `compress_single.py` | PyMuPDF 完整版 | 包含 pikepdf 结构优化 + 渲染，最全面 |
| `report.sh` | 生成压缩报告 | 统计成功率、节省空间等 |

## 日志格式

每个脚本输出管道分隔的日志行，格式为：
```
状态|文件路径|原始大小MB|压缩后大小MB|压缩方法
```

状态值：
- `OK` — 成功压缩到阈值以下
- `PARTIAL` — 未达标但已大幅压缩（>30%），已替换原文件
- `FAIL` — 无法压缩，保留原文件
- `SKIP` — 文件已在阈值以下，跳过
- `ERROR` — 处理出错

## 性能参考

基于 1430 个超过 50MB 的扫描版投资书籍 PDF 的实测数据：

| 指标 | 数据 |
|------|------|
| 文件总数 | 1430 |
| 成功率 | 99.5% |
| 总节省空间 | 76 GB |
| 总耗时 | 约 2.5 小时 |
| GS 阶段速度 | 约 25 文件/分钟（8 进程） |
| PyMuPDF 阶段速度 | 约 7 文件/分钟（8 进程） |
| GS 成功率 | 约 75% |
| PyMuPDF 兜底成功率 | 约 98% |

## macOS 兼容性注意事项

- macOS 的 `xargs` 不支持 `-d` 参数，使用 `tr '\n' '\0' | xargs -0` 替代
- macOS 的 `pgrep` 不支持 `-c` 参数，使用 `pgrep -fl pattern | wc -l` 替代
- Python `multiprocessing.Pool` 在 macOS 上可能卡死（spawn 模式），改用 `xargs -P` 更可靠
- Ghostscript 二进制路径：`/opt/homebrew/bin/gs`（Apple Silicon）或 `/usr/local/bin/gs`（Intel）

## 参数调优指南

### 阈值大小
- 默认 50MB，可根据需要调整
- 阈值越小，需要的 DPI 越低，画质损失越大

### 并行进程数
- 默认 8 进程，建议等于 CPU 逻辑核心数
- 查看核心数：`sysctl -n hw.logicalcpu`
- 磁盘 I/O 是瓶颈时，增加进程数无益

### DPI 选择参考
| 原始大小 | 推荐起始 DPI | 预期压缩比 |
|----------|-------------|-----------|
| 50-75 MB | 150 dpi | ~0.6x |
| 75-100 MB | 120 dpi | ~0.5x |
| 100-150 MB | 100 dpi | ~0.45x |
| 150-200 MB | 80 dpi | ~0.4x |
| 200-300 MB | 72 dpi | ~0.35x |
| 300+ MB | 50 dpi | ~0.25x |

## 故障排除

### Ghostscript 安装失败
```bash
# 如果遇到 icu4c 依赖问题
brew install icu4c@78
brew link icu4c@78
brew install ghostscript
```

### GS 压缩失败（Foxit PDF）
Foxit PhantomPDF 生成的 PDF 结构有缺陷，GS 无法压缩其中的图片。这些文件会自动由 PyMuPDF 渲染方案处理。

### 磁盘断开
如果目标目录在外部磁盘上，压缩过程中断开会导致脚本失败。重新连接后重新运行即可——已压缩的文件会被跳过（因为已在阈值以下）。

### 内存不足
渲染大 PDF（300+ MB）时可能占用大量内存。降低并行进程数到 4 或 2 可缓解。

## 文件结构

```
pdf-batch-compress-skill/
├── SKILL.md                      # 本文档
└── scripts/
    ├── batch_compress.sh         # 一键编排脚本
    ├── compress_single_gs.py     # GS 单文件压缩
    ├── compress_fast.py          # PyMuPDF 渲染压缩（优化版）
    ├── compress_single.py        # PyMuPDF 完整版（含 pikepdf）
    └── report.sh                 # 报告生成脚本
```
