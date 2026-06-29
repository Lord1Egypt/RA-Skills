# PDF Engine Comparison

Three viable options for generating Chinese-language PDFs on macOS. Picked
the best for research reports; the others are kept as fallbacks.

## Decision Matrix

| 维度 | **weasyprint** ⭐ | reportlab | pandoc + LaTeX |
|------|------------------|-----------|---------------|
| **输出代码复杂度** | 低（HTML+CSS） | 中（Python 风格 API） | 极低（纯 MD） |
| **中文支持** | ✅ 完美 | ✅ 完美 | ✅ 完美（需 ttf 字体配置） |
| **安装难度** | 中（需 brew pango） | 易（pip only） | 难（需 MacTeX ~5GB） |
| **输出文件大小** | 2-3MB/页（全字体嵌入） | 0.3MB/页（系统字体引用） | 1-2MB/页 |
| **样式灵活性** | ⭐⭐⭐⭐⭐（CSS） | ⭐⭐⭐（Python 样式） | ⭐⭐⭐⭐（LaTeX 主题） |
| **学习曲线** | 低 | 中 | 高 |
| **数据源** | Markdown → HTML → PDF | 直接编程（无 MD 中间层） | Markdown → LaTeX → PDF |
| **调试便利性** | ⭐⭐⭐⭐⭐（`--keep-html` 留中间产物） | ⭐⭐ | ⭐⭐⭐ |

## When to Use Each

### weasyprint (default for research reports)
- **Use when:** 调研报告、fact-check、方案、对比分析
- **Code path:** Markdown → Python-Markdown → HTML+CSS → weasyprint → PDF
- **Pros:** MD 单一事实源，CSS 易调整，自动嵌入字体（接收方无字体也能看）
- **Cons:** 文件大（字体嵌入）；首次需要 brew pango + DYLD env var

### reportlab
- **Use when:** 程序化生成（无 MD 源）、极致文件大小控制、复杂表格/图表
- **Code path:** Python data structures → reportlab Paragraph/Table → PDF
- **Pros:** 完全控制输出，文件最小（300KB/页），无系统依赖
- **Cons:** 不读 MD，代码冗长；HTML 标签在表格里需要 Paragraph 包裹

### pandoc + LaTeX (tectonic)
- **Use when:** 需要学术级排版、纯 MD 输入、与 RMarkdown/Quarto 生态集成
- **Code path:** MD → pandoc → LaTeX → tectonic/xelatex → PDF
- **Pros:** 输出最优雅，公式/参考文献支持强
- **Cons:** tectonic ~200MB 下载；LaTeX 模板调试痛苦

## Migration Path (this project)

We tested all three on the same Mike Lynch / Bayesian report:

| Engine | 7页PDF大小 | 生成时间 | 中文渲染 | MD 源维护 |
|--------|------------|----------|----------|----------|
| reportlab | 316 KB | < 1s | ✅ | ❌ 重写 |
| weasyprint | 2.4 MB | 0.7s | ✅ | ✅ |
| pandoc+tectonic | (未测) | — | — | ✅ |

**结论：** weasyprint 是研究类报告的最佳平衡点。MD 源可编辑，PDF 自动生成，文件大小可接受（飞书/Telegram 直发 2-3MB 都无压力）。

## Optimization Notes (when file size matters)

If a 10+ page report starts pushing 20MB+, consider:

1. **Font subsetting** — embed only the glyphs used in the document:
   ```bash
   pip install fonttools brotli
   pyftsubset STXIHEI.ttf \
     --text="$(cat report.md)" \
     --output-file=STXIHEI.subset.ttf \
     --flavor=woff2
   ```
   Typically reduces font from 15MB → 50-200KB.

2. **Reduce font count** — only embed STXIHEI (body). Use CSS font-weight
   variations instead of separate font files.

3. **Compress images** — weasyprint doesn't recompress by default; pre-compress
   with `pillow` or `imagemagick`.

For research reports under 15 pages, the unoptimized 2-3MB output is fine.
