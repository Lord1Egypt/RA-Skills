---
name: merge-travel-pdfs
description: Automatically merge reimbursement folders into one PDF. Supports recursive folder scanning, PDF merging, two invoices per A4 page, phone screenshots/images placed as A4 half-page slots, and Excel workbooks with multiple sheets converted to PDF before merging.
---

# Merge Travel PDFs

## 中文说明

这个 skill 用来自动整理报销材料文件夹，把 PDF、图片和 Excel 合并成一个适合提交报销或打印归档的 PDF。

功能 1：递归扫描文件夹并合并材料

- 自动递归查找指定文件夹下的 PDF、图片和 Excel 文件
- 将普通证明材料、行程单、截图、发票等整理合并到一个 PDF
- 支持按子文件夹分别生成多个合并结果

功能 2：发票两张合并到一张 A4

- 自动识别发票类 PDF
- 将发票按 A5 区域排版
- 默认两张发票合成一张 A4 页面，方便打印和报销提交

功能 3：手机截图和图片按 A4 半页排版

- 支持手机截图、照片、图片附件
- 默认把图片放入 A4 半页区域
- 两张图片合成一页 A4，避免一张截图占满一整页

功能 4：Excel 多 sheet 转 PDF 后合并

- 支持 Excel 工作簿里的多个可见 sheet
- 转换前尽量设置为 A4 纵向、宽度适配一页
- 转成 PDF 后再和其他报销材料一起合并

## Overview

Use the bundled script to merge a reimbursement folder into one checked PDF:

- Function 1: recursively scan a reimbursement folder and merge supported PDF, image, and Excel materials into one output PDF
- Function 2: detect invoice PDFs and place two invoice pages on one A4 page for compact printing or reimbursement submission
- Function 3: place phone screenshots and other image attachments into A4 half-page slots, two images per A4 page by default
- Function 4: convert Excel workbooks, including multiple visible sheets, to PDF before merging with the rest of the materials
- all A4/full-page materials are appended first: normal PDFs and converted Excel workbooks
- invoice PDFs that are already A4/full-page are kept as A4 and placed with the front full-page section
- before converting Excel, each visible sheet is kept A4 portrait and fit to 1 page wide with unlimited pages tall
- `航旅纵横` / `行程校验单` PDFs are appended after A4/full-page materials and before A5 invoice merged sheets
- all A5 merged sheets are appended last: normal images first, then invoice pages
- invoice PDFs are detected from extracted text and filename signals
- invoice pages and image attachments are placed two per A4 page
- image attachments are rotated 90 degrees by default before fitting into the A5 slot
- a JSON report records classification, counts, warnings, and verification results
- Excel report entries include visible sheet names; confirm converted page count covers all visible sheets

## Quick Start

Run the script from this skill. Excel conversion requires `soffice`/LibreOffice on the machine:

```bash
python3 scripts/merge_travel_pdfs.py "/path/to/folder" \
  --output "/path/to/folder/merged-reimbursement.pdf" \
  --report "/path/to/folder/merge-report.json" \
  --render-check "/path/to/folder/合并检查缩略图" \
  --image-rotate 90 \
  --overwrite
```

## Dependencies

The script is designed for macOS and Windows, with Linux best-effort support.

- Python packages are auto-installed with the current interpreter's `pip` when missing: `PyMuPDF`, `Pillow`, `openpyxl`.
- Excel conversion requires LibreOffice/`soffice`.
- If LibreOffice is missing, the script attempts automatic installation:
  - macOS: Homebrew `brew install --cask libreoffice`
  - Windows: `winget install TheDocumentFoundation.LibreOffice` first, then Chocolatey if available
  - Linux: `apt-get`, `dnf`, or `yum` when available
- Use `--no-auto-install` or environment variable `MERGE_TRAVEL_PDFS_NO_AUTO_INSTALL=1` to disable automatic installation.

If no supported package manager exists, install LibreOffice manually and rerun.

```bash
python3 scripts/merge_travel_pdfs.py "/path/to/folder" --no-auto-install
```

To create one output per immediate child folder:

```bash
python3 scripts/merge_travel_pdfs.py "/path/to/parent-folder" \
  --split-subfolders \
  --image-rotate 90 \
  --overwrite
```

## Workflow

1. Inspect the source folder with `find` or `rg --files` and confirm output files will not be included as inputs.
2. Decide folder scope:
   - If the user does not specify separate outputs, process the requested folder recursively as one PDF.
   - If the user asks for separate copies or mentions multiple subfolders, run the script once per immediate subfolder and produce one PDF/report per subfolder.
   - If the wording is ambiguous, ask whether they want one recursive PDF or separate PDFs per subfolder.
3. Run the script once with `--dry-run` if classification looks risky.
4. Run the full merge with `--report` and `--render-check`.
5. Read the final summary and, if needed, inspect the JSON report's `items` list for each file's classification reason.
6. If a file is misclassified, rerun with manual overrides:

```bash
--force-invoice "relative/path/or/name-fragment"
--force-normal "relative/path/or/name-fragment"
```

Both override flags can be repeated.

## Invoice Detection

The script treats a PDF as an invoice when the extracted text and filename pass a weighted keyword score. Strong signals include `发票号码`, `发票代码`, `开票日期`, `价税合计`, `购买方`, `销售方`, `纳税人识别号`, `增值税`, `电子发票`, `全电发票`, `数电票`, `校验码`, and `国家税务总局`.

Do not rely only on the word `报销`; itinerary sheets and reimbursement summaries often contain it but are not invoices. Images are included as normal A5 attachments unless manually overridden. Excel files are always treated as normal supporting material and converted to PDF.

## Verification

Always check the script summary:

- `expected_output_pages` must equal `actual_output_pages`
- `normal_pdf_pages + a4_invoice_pages + spreadsheet_pages + hanglv_pages + normal_image_sheets + invoice_sheets` should match the output page count
- `warnings` should be empty or understood
- render-check PNGs should show at least the first, last, and representative invoice pages

If verification fails, do not deliver the PDF as complete. Fix the cause, rerun, and re-check.
