# Make-to-Markdown 快速上手指南

> **文档摘要**
> 本文档「快速上手指南」，涵盖 6 个章节。5 分钟从零到产出第一份 RAG 就绪的 Markdown 物料。

---

## 1. 前置准备（一次性）

确保系统已安装 `uv`（用于运行 markitdown）：

```bash
# Windows (PowerShell)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# 验证
uv --version
```

Python 3.8+ 已内置在绝大多数系统中，无需额外安装。

## 2. 单文件转换（最常用）

```bash
# 进入 skill 目录
cd path/to/Make-to-Markdown

# 转换一份文档（自动安装依赖 → 转换 → 清洗）
python scripts/convert.py 你的文件.docx -o 输出.md
```

**支持的文件格式**：`.pdf` `.docx` `.doc` `.pptx` `.ppt` `.xlsx` `.xls` `.epub` `.html` `.csv` `.json` `.xml` `.png` `.jpg` `.mp3` `.zip` 等 20+ 种。

## 3. 批量转换一整个文件夹

```bash
python scripts/batch_convert.py ./源目录/ ./输出目录/
```

自动递归遍历所有子目录，保持原始目录结构。失败文件会记录到 `输出目录/_conversion_errors.log`。

## 4. 常用参数速查

### convert.py

| 参数 | 作用 |
|------|------|
| `-o output.md` | 指定输出路径 |
| `--no-summary` | 不注入文档摘要 |
| `-q` / `--quiet` | 静默模式 |

### batch_convert.py

| 参数 | 作用 |
|------|------|
| `--ext .pdf .docx` | 仅处理指定格式 |
| `--clean` | 转换后额外执行独立清洗 |

### post_clean.py

| 参数 | 作用 |
|------|------|
| `-o cleaned.md` | 输出到新文件 |
| `--summary` | 注入文档级摘要 |
| `--check-only` | 仅检查结构，不修改文件 |
| `--no-breadcrumbs` | 禁用上下文面包屑 |
| `--quality-report` | 输出 JSON 质量报告 |

## 5. 典型工作流

### 场景一：论文 / 报告入库

```bash
# 一次调用搞定
python scripts/convert.py paper.pdf -o paper.md
```

输出：已清洗的 Markdown，含摘要、标题层级修复、表格完整。

### 场景二：Office 旧格式预处理

```bash
# .doc / .ppt 自动通过 Office COM 转为 .docx / .pptx 后转换
python scripts/convert.py 旧文档.doc -o 旧文档.md
```

若无 Microsoft Office，自动尝试 LibreOffice CLI。

### 场景三：知识库批量建设

```bash
# 递归转换整个资料库
python scripts/batch_convert.py ./knowledge-base/ ./kb-md/

# 转换后检查质量
python scripts/post_clean.py ./kb-md/某文件.md --check-only
```

## 6. 常见问题

**Q: 提示 markitdown 依赖缺失？**
A: convert.py 会自动通过 `uv tool install markitdown --with=...` 安装全部可选依赖，通常不需要手动干预。

**Q: .doc 文件转换失败？**
A: 需要安装 Microsoft Office（含 Word）或 LibreOffice。二选一即可。

**Q: 转换结果标题层级混乱？**
A: v2.6 已内置标题层级修复（多 H1 降级、越级补过渡），自动处理。

**Q: 想单独清洗一份已有的 Markdown？**
A: 使用 `python scripts/post_clean.py 文件.md --summary -o 清洗后.md`。

**Q: 输出文件在哪里？**
A: 查看命令输出的最后一行，格式为 `输出: E:\绝对路径\文件.md`。
*（内容由AI生成，仅供参考）*
