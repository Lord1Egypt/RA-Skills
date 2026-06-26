---
name: printer-ai
description: "Cross-platform local printer CLI - Manage and print to local printers (Windows/macOS/Linux) via the printer-ai CLI. Use when the user needs to print files, query printer status, or manage print jobs. NOT for: cloud/remote printers."
metadata: {"openclaw":{"emoji":"🖨️","requires":{"bins":["printer-ai"]},"install":[{"id":"uv","kind":"uv","package":"git+https://github.com/NullYing/printer-ai-skills.git","bins":["printer-ai"],"label":"Install printer-ai (uv)"}]}}
---

# Cross-Platform Local Printer Skill

Operate local printers via the `printer-ai` CLI. Supports Windows, macOS, and Linux.

## When to Use

✅ **USE this skill when:**

- User wants to print local files (PDF, images, Office documents, etc.)
- Query local printer list and status (查询本地打印机列表和状态)
- Manage print jobs: check status, cancel jobs (管理打印任务)
- Get detailed printer attributes / capabilities (获取打印机属性/能力)

## When NOT to Use

❌ **DON'T use this skill when:**

- Operating cloud / remote print boxes (use `lianke-print-box` skill instead)
- The printer is not locally connected

## Setup

```bash
# Install
uv tool install git+https://github.com/NullYing/printer-ai-skills.git

# Verify
printer-ai printers
```

## Printing Workflow

### 1. List Printers

```bash
# Human-friendly format
printer-ai printers

# JSON format (recommended for parsing)
printer-ai printers --json
```

Get the printer `index` from output (needed for subsequent commands). ⭐ marks the default printer.

### 2. Check Printer Status

```bash
printer-ai status INDEX
# Or JSON format
printer-ai status INDEX --json
```

Status meanings:
- 🟢 `idle` = Ready (空闲可用)
- 🟡 `processing` = Busy (处理中)
- 🔴 `stopped` = Stopped (已停止)

### 3. Get Printer Attributes (optional, to discover capabilities)

```bash
printer-ai attrs INDEX
```

Returns all supported options (paper size, color mode, duplex, etc.).

### 4. Print a File

```bash
# Print with default printer
printer-ai print /path/to/file.pdf

# Specify printer by index
printer-ai print /path/to/file.pdf --index 2

# With print options — macOS/Linux (CUPS/IPP format)
printer-ai print /path/to/file.pdf --options '{"copies":"2","media":"A4","orientation_requested":"3","print_color_mode":"color"}'

# With print options — Windows (DEVMODE format)
printer-ai print /path/to/file.pdf --options '{"dmCopies":2,"dmPaperSize":9,"dmOrientation":1,"dmColor":2}'
```

### 5. Query Job Status

```bash
printer-ai job-status JOB_ID
```

### 6. List All Jobs

```bash
printer-ai jobs
printer-ai jobs --printer "Printer Name"
printer-ai jobs --json
```

### 7. Cancel a Job

```bash
printer-ai cancel-job JOB_ID
```

## Print Options Quick Reference

### macOS / Linux (CUPS/IPP format)

| Option | Example Value | Description |
|--------|--------------|-------------|
| `copies` | `"2"` | Number of copies (打印份数) |
| `media` | `"A4"`, `"Letter"` | Paper size (纸张大小) |
| `orientation_requested` | `"3"`=portrait, `"4"`=landscape | Orientation (方向) |
| `print_color_mode` | `"monochrome"`, `"color"` | Color mode (颜色模式) |
| `sides` | `"one-sided"`, `"two-sided-long-edge"` | Duplex (双面打印) |
| `print_quality` | `"3"`=draft, `"4"`=normal, `"5"`=high | Quality (质量) |
| `page_ranges` | `"1-5,10-15"` | Page range (页面范围) |
| `number_up` | `"2"`, `"4"` | Pages per sheet (每页合并页数) |

### Windows (DEVMODE format)

| Option | Example Value | Description |
|--------|--------------|-------------|
| `dmCopies` | `2` | Number of copies (打印份数) |
| `dmPaperSize` | `9`=A4, `1`=Letter | Paper size (纸张大小) |
| `dmOrientation` | `1`=portrait, `2`=landscape | Orientation (方向) |
| `dmColor` | `1`=mono, `2`=color | Color mode (颜色模式) |
| `dmDuplex` | `1`=simplex, `2`=long-edge, `3`=short-edge | Duplex (双面打印) |
| `dmPrintQuality` | `-4`=default | Quality (质量) |

## Notes

- Check printer status with `printer-ai status` before printing to confirm it is online
- Print option formats differ by platform: macOS/Linux uses CUPS/IPP string format, Windows uses DEVMODE integer format
- Use `printer-ai attrs` to discover actual supported options for a specific printer
- The `--json` flag returns pure JSON output for easy programmatic parsing
