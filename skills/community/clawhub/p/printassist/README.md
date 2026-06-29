# PrintAssist 🖨️

Print any file with a plain-language instruction. No more fighting with print dialogs.

```
"Print this PDF double-sided, A4, black and white."
"Drucke das zweimal nebeneinander auf ein Querformat-Blatt."
"Merge these three PDFs and print pages 2–5, 2 copies."
"Remove the background from this photo and print it on A4."
```

Works with **PDF**, **Word/Excel/PowerPoint**, and **photos**. Integrates with **Adobe Creative Cloud** for photo editing (exposure, crop, background removal, presets) before printing.

> Built for [Claude Code](https://claude.ai/code) and [OpenClaw](https://openclaw.ai/) on Windows.

---

## Prerequisites

| Tool | Purpose | Install |
|---|---|---|
| Python 3.11+ | Runs all scripts | [python.org](https://www.python.org) |
| SumatraPDF | PDF printing via CLI | auto via `setup.ps1` |
| LibreOffice | Office → PDF conversion | auto via `setup.ps1` |
| winget | Package manager | built into Windows 11 |

Optional: Adobe Creative Cloud subscription for photo editing via the Adobe MCP connector.

---

## Installation

```powershell
git clone https://github.com/nilsgollub/PrintAssist.git
cd PrintAssist
powershell -ExecutionPolicy Bypass -File setup.ps1
```

`setup.ps1` will:
1. Install SumatraPDF and LibreOffice via winget (if not already installed)
2. Run `pip install -r requirements.txt`
3. Detect your printers and generate `config/printers.yaml` automatically

---

## Configuration

### Printers (`config/printers.yaml`)

Generated automatically by `setup.ps1`. To edit manually:

```yaml
default:
  printer_name: "Your Printer Name"   # fallback for any device

hosts:
  YOUR-PC-HOSTNAME:
    printer_name: "Printer on PC"
  YOUR-LAPTOP-HOSTNAME:
    printer_name: "Printer on Laptop"
```

Find your printer names: `wmic printer get name`  
Find your hostname: `$env:COMPUTERNAME`

### Adobe CC (optional)

Open Claude Code and run `/mcp`, then authenticate with `adobe-creativity`. Required only for photo editing features (background removal, exposure, presets, etc.).

---

## Usage with Claude Code

Drop a file into the chat and describe what you want:

```
# Print
"Print this — A4, duplex, black and white"
"2 Kopien, Querformat, Seiten 3-7"

# PDF manipulation
"Merge these PDFs"
"Split into one file per page"
"Rotate all pages 90 degrees"
"Add a watermark"
"Extract pages 2, 5 and 7"
"Compress this PDF"

# Office editing
"Replace all occurrences of 'Draft' with 'Final'"
"Set cell B3 in sheet 'Sales' to 42"
"Add a slide with title 'Q3 Results'"

# Photos (requires Adobe CC)
"Remove the background"
"Fix the exposure and print on A4"
"Apply a cinematic preset and print"
"Crop to 10×15 cm"

# Preview
"Show me a preview before printing"
```

---

## Usage with OpenClaw

Install the skill from [ClawHub](https://clawhub.sh):

```bash
clawhub install printassist --workdir "$env:USERPROFILE\.openclaw" --dir plugin-skills
```

Then talk to OpenClaw naturally on any connected channel (Telegram, WhatsApp, etc.).

---

## Project structure

```
PrintAssist/
├── SKILL.md                  # OpenClaw / ClawHub skill definition
├── CLAUDE.md                 # Claude Code project memory & routing rules
├── setup.ps1                 # One-command setup for any Windows device
├── requirements.txt
├── config/
│   ├── printers.example.yaml # Template — copy to printers.yaml
│   └── printers.yaml         # Your config (gitignored)
└── scripts/
    ├── print.py              # Print dispatcher (PDF / Office / image)
    ├── pdf_tools.py          # Merge, split, rotate, watermark, encrypt…
    └── office_tools.py       # Word, Excel, PowerPoint editing
```

---

## Limitations

- **PDF text editing** is not possible with these tools — use Adobe Acrobat
- **Windows only** (SumatraPDF + win32print)
- **Wake-on-LAN over WiFi** is unreliable — remote printing requires the PC to be on

---

## License

MIT-0 — do whatever you want with it.
