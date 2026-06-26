---
name: printer-control
description: Control local and network printers from your computer. Use when you need to: (1) List available printers, (2) Print text files or documents, (3) Print raw text to a specific printer, (4) Check printer status, (5) Set default printer. Supports Windows with win32print or PowerShell fallback. Now with partial name matching for easier printer selection.
---

# Printer Control Skill

This skill enables agent-controlled printing on Windows systems.

## ⚠️ Security & Permissions

**Requires explicit user authorization** before any print operation. Printing consumes physical resources and can be disruptive.

Always confirm:
- Which printer to use
- What to print
- Number of copies

## Quick Start

### List Available Printers

```bash
python scripts/list_printers.py
```

Or with PowerShell:
```powershell
powershell -Command "Get-Printer | Select-Object Name, Type, Shared, PortName"
```

### Print a Text File

```bash
python scripts/print_file.py --printer "Printer Name" --file "C:\path\to\file.txt"
```

### Print Raw Text

```bash
python scripts/print_text.py --printer "Printer Name" --text "Hello, World!"
```

### Set Default Printer

```bash
python scripts/set_default.py --printer "Printer Name"
```

## Scripts

| Script | Purpose |
|--------|---------|
| `list_printers.py` | List all available printers |
| `print_file.py` | Print a file to a specified printer |
| `print_text.py` | Print raw text string |
| `set_default.py` | Set default printer |
| `printer_status.py` | Check printer status (online, paper, toner) |

## Dependencies

### Option 1: pywin32 (Recommended for Windows)

```bash
pip install pywin32
```

### Option 2: PowerShell (Built-in, no install needed)

The scripts automatically fall back to PowerShell if pywin32 is not available.

## Usage Examples

**Example 1: List printers and pick one**
```bash
python scripts/list_printers.py
# Output shows available printers, pick one by name
```

**Example 2: Print a document**
```bash
python scripts/print_file.py --printer "HP LaserJet Pro" --file "report.pdf" --copies 2
```

**Example 3: Print a quick note**
```bash
python scripts/print_text.py --text "Meeting at 3pm" --printer "Office Printer"
```

## Troubleshooting

### "Printer not found"
- Run `list_printers.py` to verify the exact printer name
- Printer names are case-sensitive

### "Access denied"
- Some network printers require authentication
- Check printer permissions

### "pywin32 not available"
- Scripts will auto-fallback to PowerShell
- For best results, install pywin32: `pip install pywin32`

### Print job stuck in queue
```powershell
powershell -Command "Restart-Service -Name Spooler"
```

## API Reference

See `references/printer-api.md` for detailed API documentation and Windows print subsystem details.
