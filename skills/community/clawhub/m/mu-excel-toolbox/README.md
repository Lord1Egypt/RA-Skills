<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/default-banner.png">
    <source media="(prefers-color-scheme: light)" srcset="assets/default-banner.png">
    <img alt="mu-excel-toolbox" src="assets/default-banner.png" width="100%">
  </picture>
</p>

# 📊 mu-excel-toolbox · Excel全能工具箱

> One skill for the entire Excel lifecycle — **read & write** · **merge & split** · **clean & validate** · **pivot & chart** · **template fill** · **encrypt & protect** — just describe what you need in natural language.

**English** | [中文](README_CN.md) | [🌐 Landing Page](https://muippt.github.io/mu-excel-toolbox/)

[![WeChat](https://img.shields.io/badge/muippt-07C160?logo=wechat&logoColor=white)](https://mp.weixin.qq.com/s/YLtXENt_7WzO2DgJCFUtPA)
[![Xiaohongshu](https://img.shields.io/badge/muippt-FF2442?logo=xiaohongshu&logoColor=white)](https://xhslink.com/m/ESxtgUNMdl)
[![Book](https://img.shields.io/badge/Book-Visual%20Team%20Management-BBDDE5?logo=bookstack&logoColor=white)](https://item.m.jd.com/product/14547345.html)
[![mu-skillhub](https://img.shields.io/badge/mu--skillhub-9E95B7?logo=refinedgithub&logoColor=white)](https://muippt.github.io/mu-skill-hub/)
[![License](https://img.shields.io/github/license/muippt/mu-excel-toolbox)](LICENSE)
[![Version](https://img.shields.io/github/v/release/muippt/mu-excel-toolbox)](https://github.com/muippt/mu-excel-toolbox/releases)
[![Stars](https://img.shields.io/github/stars/muippt/mu-excel-toolbox)](https://github.com/muippt/mu-excel-toolbox/stargazers)

## 💡 Usage Examples

- 📋 **Quick Preview**: "Show me how many sheets this Excel has, and what columns each sheet contains"
- 📎 **Merge Reports**: "Combine these 5 monthly sales reports into one annual summary"
- ✂️ **Split by Department**: "Split the roster by the 'Department' column — one Excel file per department"
- 🧹 **Data Cleaning**: "Remove empty rows, standardize phone numbers to 11 digits, unify dates to YYYY-MM-DD"
- 🔗 **VLOOKUP**: "Join the roster and attendance tables using employee ID"
- 📊 **Chart Generation**: "Create a bar + line combo chart from this sales data"
- 📈 **Pivot Table**: "Cross-tabulate sales by department and month"
- 📄 **Template Fill**: "Batch-generate offer letters from employee data"
- 🔍 **Diff Comparison**: "Compare two versions of the roster — who was added, removed, or changed"
- 🔒 **File Encryption**: "Password-protect the salary spreadsheet"

## ✨ Core Highlights

### 🛠️ 22 Features — Full Excel Lifecycle

From "let me take a look" to "encrypted delivery," every step of your Excel workflow has a matching tool — no need to switch between multiple software:

| Category | Features | Description |
|----------|----------|-------------|
| 📖 Read & Write | Smart Preview / Read / Write & Create | Auto-detect sheet structure, column names, data types |
| 🔄 Convert | Format Interconversion | xlsx ↔ csv ↔ json ↔ tsv, auto-encoding detection |
| 📎 Consolidate | Merge / Split / Split by Column | Multi-file merge, split by sheet or column value |
| 🔗 Relate | VLOOKUP / Dedup | Cross-table join, smart dedup keeping latest |
| 🧹 Clean | Data Cleaning / Validation | Empty row cleanup, format standardization, rule validation |
| 📄 Template | Template Fill | Batch-generate offer letters and standardized docs |
| 💅 Style | Conditional Format / Styling | Auto red/green highlighting, header beautification, auto column width |
| 📐 Calculate | Formulas / Pivot Tables | Auto-insert SUM/AVERAGE formulas, cross-tabulation |
| 📊 Visualize | Charts / Data Analysis | Bar, line, pie, combo charts, statistical summaries |
| 🔍 Compare | Diff / Image Insert | Row-by-row comparison, batch image insertion |
| 🔒 Secure | Password Protection | File-level encrypt/decrypt |

### ⚡ Large File Ready — 100K+ Rows Streaming

Not "load everything into memory first" — automatically detects file size and seamlessly switches to streaming mode for files exceeding 100,000 rows:

- **Read**: Auto-enables read_only mode, memory usage reduced by 90%+
- **Write**: Auto-enables write_only mode, generates and writes on-the-fly
- **Error Tolerance**: Skips bad rows/cells and continues, summarizes errors at the end

### 🧹 8 Data Cleaning Rules

The most common dirty data problems in HR and business scenarios, solved with one command:

1. Remove empty rows/columns
2. Trim leading/trailing whitespace
3. Standardize phone numbers to 11-digit format
4. Unify dates to YYYY-MM-DD
5. Standardize currency/amount formats
6. Validate ID card number format
7. Validate email format
8. Flag duplicate records

### 📐 5 Output Formats

All scripts uniformly support multi-format output for different downstream scenarios:

| Format | Use Case |
|--------|----------|
| json | API integration / programmatic access |
| csv | Lightweight exchange / import to other systems |
| markdown | Documentation embedding / quick reading |
| table | Terminal display |
| xlsx | Standard Excel output |

### 🔒 File-Level Encryption

Sensitive files like salary tables and performance data — one command to encrypt, one command to decrypt:

- Set / modify / remove passwords
- Based on msoffcrypto-tool with standard Office encryption
- Compatible with Microsoft Office / WPS / LibreOffice

## 📌 Comparison

### mu-excel-toolbox vs Manual Excel Operations

| Dimension | mu-excel-toolbox | Manual |
|-----------|------------------|--------|
| Merge 10 reports | 1 command, seconds | Copy-paste one by one, 10-30 min |
| Split by department | 1 command, auto-split | Filter → Copy → New → Paste, repeat N times |
| Data cleaning | 8 rules, one click | Manual find-and-replace, error-prone |
| VLOOKUP | Auto-match + export | Write formula → drag → debug, fragile |
| Diff comparison | Row-by-row + change report | Eyeball comparison, breaks at 100+ rows |
| Batch template fill | Data + template → batch generate | Edit one by one, repetitive labor |
| Large file handling | Streaming mode, no crash | Excel freezes on open |

### mu-excel-toolbox vs Writing Python Scripts Yourself

| Dimension | mu-excel-toolbox | DIY Scripts |
|-----------|------------------|-------------|
| Barrier to entry | Natural language, no code needed | Requires Python + openpyxl/pandas |
| Feature coverage | 22 tools out of the box | Write from scratch each time |
| Large file handling | Auto-streaming | Implement streaming logic yourself |
| Error handling | Built-in tolerance + error report | Debug each bug yourself |
| Encoding issues | Auto-detect UTF-8/GBK/GB2312 | Classic UnicodeDecodeError nightmare |
| Safety backup | Auto-backup before write | Overwrite and it's gone |
| Maintenance | Skill unified updates | Scattered scripts, unmaintained |

## 🚀 22 Features at a Glance

| # | Feature | One-liner | Trigger Example |
|---|---------|-----------|-----------------|
| 1 | 📋 Smart Preview | See sheets, columns, rows, data types | "Show me this Excel" |
| 2 | 📖 Read | Precise read by sheet/column/range | "Read columns A-D from Sheet2" |
| 3 | ✏️ Write & Create | Write data to a new Excel file | "Generate an Excel from this data" |
| 4 | 🔄 Format Convert | xlsx ↔ csv ↔ json ↔ tsv | "Convert CSV to xlsx" |
| 5 | 📎 Merge | Combine multiple files/sheets | "Merge these 5 monthly reports" |
| 6 | ✂️ Split | Split by sheet into separate files | "Split by sheet" |
| 7 | ✂️ Split by Column | Split by a column's values | "Split by department" |
| 8 | 🔗 VLOOKUP | Cross-table join | "Join by employee ID" |
| 9 | 🧹 Dedup | Deduplicate by specified columns | "Dedup by name + phone" |
| 10 | 🧽 Data Cleaning | Empty rows, format standardization | "Clean dirty data" |
| 11 | 📄 Template Fill | Batch generate from template | "Batch generate offer letters" |
| 12 | ✅ Validation | Email/ID/phone format check | "Check which emails are invalid" |
| 13 | 🎨 Conditional Format | Auto-color by rules | "Red below 60, green above 90" |
| 14 | 💅 Styling | Header beautification, auto width | "Bold header with background" |
| 15 | 📐 Formulas | Auto-insert Excel formulas | "Add SUM in column E" |
| 16 | 📊 Charts | Bar/line/pie/combo charts | "Generate a sales bar chart" |
| 17 | 📈 Pivot Table | Cross-tabulation analysis | "Summarize sales by dept and month" |
| 18 | 🔬 Data Analysis | Statistical summary: mean/median/distribution | "Give me a statistical summary" |
| 19 | 🔍 Diff | Row-by-row file comparison | "Compare two versions of the roster" |
| 20 | 🖼️ Image Insert | Batch insert images to rows | "Insert employee photos" |
| 21 | 🔒 Password Protect | File encrypt/decrypt | "Password-protect the salary table" |
| 22 | ⚡ Large File | 100K+ rows auto-streaming | Auto-triggered, no manual action |

## ⚙️ Technical Specs

| Item | Description |
|------|-------------|
| Runtime | Any AI agent framework that supports Skills/prompts (e.g. Claude Code, Cursor, Windsurf) |
| Python | 3.9+ |
| Core Dependencies | openpyxl / pandas / xlsxwriter / xlrd / msoffcrypto-tool |
| Input Formats | .xlsx / .xls / .csv / .tsv / .json |
| Output Formats | .xlsx / .csv / .json / .tsv / markdown / table |
| Large File Threshold | 100K rows auto-switch to streaming mode |
| Encoding Support | UTF-8 / GBK / GB2312 / Latin-1 auto-detect |
| Script Count | 20 independent Python scripts + 1 shared module |
| Lines of Code | 5,636 |

## 🛠️ Quick Start

**Step 1: Install**

```bash
# Unzip to your agent's skills directory
unzip mu-excel-toolbox.zip -d ./mu-excel-toolbox

# Dependencies auto-install on first run, or install manually
pip install -r ./mu-excel-toolbox/scripts/requirements.txt
```

**Step 2: Start Using**

Just tell your AI agent what you want to do — the skill auto-routes to the right tool:

```
# Preview a file
"Show me what's in sales.xlsx"

# Merge multiple reports
"Merge January.xlsx through December.xlsx into an annual summary"

# Clean + validate
"Clean this roster's dirty data, check phone and email formats"

# Generate a chart
"Create a monthly bar + line combo chart from the sales data"
```

> 💡 First run auto-installs dependencies (~30 seconds), then it's ready to go.

## 🔒 Security & Privacy

- All scripts execute locally — the Skill itself does not upload files to any third-party service
- When used via an AI Agent, conversation content is processed by the LLM provider — please be mindful of sensitive data
- No telemetry, no data collection, no usage tracking
- Write operations auto-backup original files to prevent data loss
- MIT License, free to modify and distribute

## ⭐ Star History

If this project helps you, please give it a ⭐!

[![Star History Chart](assets/star-history.png)](https://www.star-history.com/?repos=muippt%2Fmu-excel-toolbox&type=date)

> In one line: No code, no plugins — just tell your agent what you need and get Excel done.

## 👤 About the Author

🎓 Signatory Author of Tsinghua University Press / 2026 Dangdang Influential Author / AI & Large Model Business HR Specialist at a Leading Tech Company / National Level-1 HR Manager / Level-2 Psychological Counselor / Self-taught Designer

📚 Author of [*Visual Team Management*](https://item.m.jd.com/product/14547345.html). Clients include ByteDance, Tencent, Baidu, China Mobile, SMG, BOE…

💡 [WeChat Official Account](https://mp.weixin.qq.com/s/YLtXENt_7WzO2DgJCFUtPA) / [Xiaohongshu](https://xhslink.com/m/ESxtgUNMdl): muippt

## 📄 License & Acknowledgments

[MIT](LICENSE) © 2026 木先生iPPT

Thanks to [openpyxl](https://openpyxl.readthedocs.io/) · [pandas](https://pandas.pydata.org/) · [xlsxwriter](https://xlsxwriter.readthedocs.io/) · [xlrd](https://github.com/python-excel/xlrd) · [msoffcrypto-tool](https://github.com/nolze/msoffcrypto-tool) and other excellent open-source projects for providing the technical foundation.

> Note: Much of this project was co-created with AI assistance. If you believe your work has been used without proper attribution, please open an issue.
