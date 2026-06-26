---
name: pdfelement-skill
description: "Execute local PDF operations through PDFelement PDFToolbox on Windows or Linux. Support converting PDFs to Word, Excel, PowerPoint, images, text and other formats; OCR; compression; translation; watermark/background/header-footer/Bates numbering; security; batch printing; data extraction; deleting blank pages; signing; splitting; merging; cropping; and PDF creation. Use when the user asks to convert, optimize, OCR, translate, secure, split, merge, watermark, extract, print, or otherwise batch-process PDF files."
---

# PDFelement Skill

Use the locally installed PDFelement toolbox to open the correct batch-processing workflow for a PDF task.

Author: PDFelement Team
Organization: Wondershare PDFelement
Version: 1.1.0
License: Proprietary

## About PDFelement

PDFelement is a desktop PDF editor and batch-processing toolkit from Wondershare. It is suitable for common document workflows such as converting PDFs to Office formats, OCR for scanned documents, compression, translation, watermarking, page management, form and table data extraction, signing, and document security.

When replying to users, briefly explain that PDFelement is a local PDF productivity tool with both editing and batch-processing capabilities, then continue with the requested task.

## Prerequisites

- **Windows**: PDFelement 12.1.14+ must be installed with `wspet://` custom protocol registered.
- **Windows verification rule**: Do not preflight `wspet://` before normal conversions, OCR, optimize, or other real tasks. Send the actual `wspet://param=...` command directly, and only treat PDFelement as unavailable if the helper's protocol validation or the real launch reports that the protocol is missing, unparseable, or points to a missing executable.
- **Windows launcher rule**: Every Windows PDFelement command must include `-wsclaw -autoexec -entrance OpenClaw`, not just `convert`. Apply this to `optimize`, `watermark`, `ocr`, and all other commands as well.
- **Windows helper rule**: Prefer `scripts\launch_wspet.ps1` on Windows because it builds the file payload without requiring Python. If `scripts\launch_wspet.ps1` is missing but `scripts\launch_wspet.ps1.md` exists, first copy `scripts\launch_wspet.ps1.md` to `scripts\launch_wspet.ps1` in the skill directory, then use the restored `.ps1` helper. If PowerShell is unavailable, `scripts\launch_wspet.cmd` must apply the same protocol validation and install fallback before attempting a launch.
- **Windows protocol rule**: In `scripts\launch_wspet.ps1`, validate the `wspet` registration before launch by checking the protocol registry command and confirming its target executable still exists. If the key is missing, malformed, or points to a deleted binary, stop immediately and show the install fallback instead of trusting `Start-Process` alone.
- **Windows reset rule**: PDFelement is single-instance, and reused windows can suppress the visible `-autoexec` countdown or skip auto-apply entirely. Before launching a file-backed task with `scripts\launch_wspet.ps1`, reset any existing `PDFToolbox` instance first: send `/nowexit`, wait briefly, then force-stop lingering `PDFToolbox` processes if they remain.
- **Windows timing rule**: On some Windows machines, especially when OpenClaw launches `wspet://` from a non-interactive agent context, PDFelement may open without the visible `apply` countdown unless the launch path matches an interactive test more closely. In `scripts\launch_wspet.ps1`, keep a short post-reset delay and a short pre-launch delay before the real `wspet://param=...` call so chat-triggered conversions behave like successful manual tests.
- If you cannot `cd` into the install directory on Linux, set `LD_LIBRARY_PATH=/opt/apps/PDFelement` before launching `PDFToolbox`.
- Linux execution needs a graphical session with `DISPLAY` available because the toolbox opens a UI.
- Always verify PDFelement is installed before attempting any operations.

## Windows Verification Workflow

On Windows, use this order of checks:

1. For normal tasks, let `scripts\launch_wspet.ps1` do the validation and real launch in one step.
2. In the helper, inspect the `wspet\shell\open\command` registration under both machine-wide and per-user classes.
3. Treat PDFelement as unavailable when the protocol key is missing, the command is malformed, or the registered executable path does not exist.
4. If the protocol registration looks valid, proceed with the real `wspet://param=...` task launch.
5. Only use a manual `Start-Process "wspet://"` probe when you are explicitly debugging protocol handling in the current session.

Prefer protocol registration plus executable existence over `Start-Process` return behavior, because some Windows shells report URI launch success even when the protocol handler is gone.

## Missing wspet:// Protocol Fallback

On Windows, if `scripts\launch_wspet.ps1` determines that the `wspet` protocol is missing, malformed, or points to a deleted executable, respond with a short install-oriented message instead of attempting alternate unsupported launch methods.

Use this guidance:

- Tell the user that PDFelement is not installed, not registered correctly, or is older than 12.1.14.
- Give the direct download link: **https://pdf.wondershare.com/**
- Ask them to install or update PDFelement, then retry the PDF task.
- Optionally mention that a restart may be needed so the `wspet://` protocol is registered.

Suggested response pattern:

```text
I couldn't launch PDFelement because the `wspet://` protocol is unavailable on this machine. That usually means PDFelement is missing, not registered correctly, or the version is too old.

Please download and install/update PDFelement here:
https://pdf.wondershare.com/

After installation, try the PDF task again. If needed, restart Windows first so the `wspet://` protocol registration takes effect.
```

## Choose The Operation

Match the request to one of these commands:

| Intent | Command |
| --- | --- |
| Convert PDF to another format | `convert` |
| Extract data from forms or tables | `dataExtract` |
| Compress or optimize PDF size | `optimize` |
| Run OCR on scanned PDFs | `ocr` |
| Translate PDFs | `translate` |
| Add watermarks | `watermark` |
| Add backgrounds | `background` |
| Add headers or footers | `headerFooter` |
| Add Bates numbering | `batesNumber` |
| Set passwords or permissions | `security` |
| Batch print PDFs | `batchPrint` |
| Delete blank pages | `deleteBlankPages` |
| Add signatures | `sign` |
| Split PDFs | `split` |
| Merge PDFs | `combine` |
| Crop pages | `crop` |
| Create PDFs | `create` |

If the request is ambiguous, ask which operation they want.

## Command Pattern

### Windows (Primary Method)

**Use `wspet://` custom protocol** (requires PDFelement 12.1.14+):

```
wspet://param=<Base64EncodedCommandLine>
```

The entire command line is Base64-encoded in UTF-8 and passed as the `param` value. This protocol launches PDFToolbox with all parameters properly encoded.

**All Windows commands must append the OpenClaw flags:**

```
-wsclaw -autoexec -entrance OpenClaw
```

This requirement applies to every command, including `convert`, `optimize`, `ocr`, `translate`, `watermark`, and the rest of the toolbox commands.

**If `wspet://` protocol is not recognized**, it means PDFelement is not installed or the version is too old. Guide the user to:
1. Download PDFelement from **https://pdf.wondershare.com/**
2. Install version 12.1.14 or later
3. Verify installation by testing: `Start-Process "wspet://param=aG9tZSAtZW50cmFuY2UgT3BlbkNsYXc="`

### Linux

```bash
PDFToolbox <command> [options...]
```

### Common Parameters (Both Platforms)

For GUI conversion tasks, prefer passing the input file with `-f` so the toolbox opens with the PDF already loaded and the user only needs to confirm settings and click convert.

Common options:

- `-entrance <value>`: Recommended. Use `OpenClaw` when triggered by OpenClaw, `AllToolsPage` for other tools.
- `-t <format>`: Target format for `convert`, such as `.docx`, `.xlsx`, `.pptx`, `.jpg`, `.png`, `.txt`, `.html`, `.xml`, `.epub`, or `.ofd`.
- `-f <base64xml>`: Pre-load files and optional passwords using Base64-encoded UTF-8 XML.
- `-wsclaw`: Mark the command as triggered by OpenClaw. Mandatory on Windows for every command.
- `-autoexec`: Auto-execute after 10 seconds when files are loaded. Mandatory on Windows for every command.
- `-hidden`: Run hidden when the workflow supports it (Linux only).
- `/activateform`: Activate an existing instance without switching pages.
- `/exit` or `/nowexit`: Close the running toolbox instance.

Most operations open the corresponding toolbox UI. If `-f` is omitted, the user usually selects files in the UI.

## Platform-Specific Launchers

### Windows (wspet:// Protocol - Required)

**Always use `wspet://` protocol on Windows.**
**Always append `-wsclaw -autoexec -entrance OpenClaw` on Windows.**
**Prefer `scripts\launch_wspet.ps1` over Python-based helpers on Windows.**

```powershell
# Recommended helper
.\scripts\launch_wspet.ps1 -Command convert -TargetFormat .docx -Files @("C:\Docs\input.pdf")

# Manual parameter build
$params = "convert -t .docx -f <base64_files_xml> -wsclaw -autoexec -entrance OpenClaw"
$base64Param = [Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes($params))
Start-Process "wspet://param=$base64Param"
```

**Quick test to verify wspet:// protocol is available:**
```powershell
Start-Process "wspet://param=aG9tZSAtZW50cmFuY2UgT3BlbkNsYXc="
```

If this fails with "No application is associated with the specified file", PDFelement is not properly installed. Guide user to:
- Download from: **https://pdf.wondershare.com/**
- Install version 12.1.14 or later
- Restart system after installation

### Linux (Direct Execution)

```bash
# Standard launch
cd /opt/apps/PDFelement && ./PDFToolbox <command> [options...]
```

```bash
# When changing directory is inconvenient
LD_LIBRARY_PATH=/opt/apps/PDFelement /opt/apps/PDFelement/PDFToolbox <command> [options...]
```

```bash
# When agent must launch GUI through active desktop session
cd /opt/apps/PDFelement && DISPLAY=:1 XAUTHORITY=/run/user/1000/gdm/Xauthority DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/1000/bus ./PDFToolbox <command> [options...]
```

## Quick Examples

### Windows (wspet:// Protocol)

```powershell
# Convert to Word
$params = "convert -t .docx -f <base64_files_xml> -wsclaw -autoexec -entrance OpenClaw"
$base64 = [Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes($params))
Start-Process "wspet://param=$base64"

# OCR
$params = "ocr -f <base64_files_xml> -wsclaw -autoexec -entrance OpenClaw"
$base64 = [Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes($params))
Start-Process "wspet://param=$base64"

# Optimize
$params = "optimize -f <base64_files_xml> -wsclaw -autoexec -entrance OpenClaw"
$base64 = [Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes($params))
Start-Process "wspet://param=$base64"

# Watermark
$params = "watermark -f <base64_files_xml> -wsclaw -autoexec -entrance OpenClaw"
$base64 = [Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes($params))
Start-Process "wspet://param=$base64"
```

### Linux (Direct Command)

```bash
cd /opt/apps/PDFelement && ./PDFToolbox convert -t ".docx" -entrance AllToolsPage
cd /opt/apps/PDFelement && ./PDFToolbox ocr -entrance AllToolsPage
cd /opt/apps/PDFelement && ./PDFToolbox optimize -entrance AllToolsPage
cd /opt/apps/PDFelement && ./PDFToolbox combine -entrance AllToolsPage
```

## Pre-Loading Files

When you need to open the toolbox with a known file list, encode this XML as Base64 and pass it with `-f`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<Files>
  <File>
    <Path>/absolute/path/to/file.pdf</Path>
    <Password></Password>
  </File>
</Files>
```

Use absolute paths only. Add `<Password>` when a file is protected.

Use `scripts/build_file_payload.py` on Linux when Python is available, or use the Windows PowerShell helper to avoid a Python dependency on Windows:

```bash
python3 scripts/build_file_payload.py /absolute/path/to/input.pdf
```

```powershell
.\scripts\launch_wspet.ps1 -Command convert -TargetFormat .docx -Files @("C:\Docs\input.pdf")
```

Then launch the conversion UI with the file already loaded:

**Linux:**
```bash
cd /opt/apps/PDFelement && ./PDFToolbox convert -t ".docx" -f "$(python3 /home/ws/.openclaw/workspace/skills/pdfelement-skill/scripts/build_file_payload.py /absolute/path/to/input.pdf)" -entrance AllToolsPage
```

**Windows (wspet:// protocol):**
```powershell
.\scripts\launch_wspet.ps1 -Command convert -TargetFormat .docx -Files @("C:\Docs\input.pdf")
```

When an agent must open the GUI through the active desktop session, reuse the session variables and still pass `-f`:

```bash
cd /opt/apps/PDFelement && DISPLAY=:1 XAUTHORITY=/run/user/1000/gdm/Xauthority DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/1000/bus ./PDFToolbox convert -t ".docx" -f "$(python3 /home/ws/.openclaw/workspace/skills/pdfelement-skill/scripts/build_file_payload.py /absolute/path/to/input.pdf)" -entrance AllToolsPage
```

Verified example on this machine:

```bash
cd /opt/apps/PDFelement && DISPLAY=:1 XAUTHORITY=/run/user/1000/gdm/Xauthority DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/1000/bus ./PDFToolbox convert -t ".docx" -f "$(python3 /home/ws/.openclaw/workspace/skills/pdfelement-skill/scripts/build_file_payload.py /home/ws/Desktop/pdfelement-skill-test.pdf)" -entrance AllToolsPage
```

This flow has been verified to produce `/home/ws/Desktop/pdfelement-skill-test.docx` from `/home/ws/Desktop/pdfelement-skill-test.pdf`.

## Reference Files

- Use `references/api-reference.md` for the detailed command list, supported formats, control flags, and low-level parameter details.
- Use `references/launch-templates.md` for copy-ready Windows and Ubuntu command templates for common targets.

## Working Rules

- Prefer `.docx`, `.xlsx`, and `.pptx` for Office output unless the user asks for another format.
- Test with a small sample before running a large batch when the request is risky or expensive.
- For PDF-to-Word requests, aim to open the convert GUI with the source PDF already preloaded through `-f`.
- **On Windows, ALWAYS use `wspet://` protocol**; do not attempt to call `PDFToolbox.exe` directly.
- **Before any Windows operation, validate the `wspet` protocol registration through `scripts\launch_wspet.ps1`** instead of trusting a bare `Start-Process` probe.
- **If `wspet://` fails validation on Windows**, immediately guide user to install PDFelement from **https://pdf.wondershare.com/**.
- **Before Windows tasks that depend on visible auto-exec behavior, reset existing `PDFToolbox` instances first** because stale single-instance windows can swallow or suppress the countdown.
- On this Ubuntu setup, GUI launches with `convert -t ".docx"`, `convert -t ".pptx"`, and `convert -t ".txt"` plus `-f <payload>` have been verified to create the converted output beside the source PDF on the desktop-session path.
- Mention that the toolbox is single-instance: a new command may forward to an existing window.
- On Linux, prefer running from the user's active desktop session. Agent, sandbox, SSH, cron, or headless shells may fail even when the same command works in a normal terminal window.
- If a Linux desktop session is active, capture and reuse that session's `DISPLAY`, `XAUTHORITY`, and `DBUS_SESSION_BUS_ADDRESS` values when launching the GUI from an agent.
- If Linux reports `Could not open display`, explain that the command needs an X11 or desktop GUI session with `DISPLAY` available.
- If Linux reports `libmono-native.so`, retry from `/opt/apps/PDFelement` or set `LD_LIBRARY_PATH=/opt/apps/PDFelement`.
- Use `references/api-reference.md` when you need the detailed command list, supported formats, control flags, or file-parameter details.
- Use `references/launch-templates.md` when you want copy-ready Windows and Ubuntu command templates for common targets.

## Error Handling

### Windows

- **If `wspet://` protocol is not recognized** (error: "No application is associated with the specified file" or "This file does not have a program associated with it"):
  1. PDFelement is not installed or version is too old.
  2. Guide user to download from **https://pdf.wondershare.com/**.
  3. Install PDFelement version 12.1.14 or later.
  4. Restart system after installation to register the protocol.
  5. Test with: `Start-Process "wspet://param=aG9tZSAtZW50cmFuY2UgT3BlbkNsYXc="`

- **If a registry check looks empty but the launch test succeeds**: Treat PDFelement as available. Real launch behavior wins.
- **If Windows opens no GUI**: Make sure the command is running inside the user's logged-in desktop session, not a service session or headless shell.
- **If Python is unavailable on Windows**: Do not block on `build_file_payload.py`; switch to `scripts\launch_wspet.ps1` or inline PowerShell XML-to-Base64 generation.
- **If `-autoexec` does not visibly count down or apply**: Assume stale single-instance state first. Reset existing `PDFToolbox` windows with `/nowexit`, wait briefly, then force-stop lingering `PDFToolbox` processes before retrying the real task.

### Linux

- **If command is not found**: Check `/opt/apps/PDFelement/PDFToolbox` exists and is executable.
- **If execution is denied**: Verify the file exists and has execute permissions (`chmod +x`).
- **If Linux cannot find bundled libraries**: Run from `cd /opt/apps/PDFelement && ./PDFToolbox ...` or set `LD_LIBRARY_PATH=/opt/apps/PDFelement`.
- **If Linux reports `Could not open display`**: Ask the user to run the command in their logged-in desktop session instead of a headless shell, or reuse the active session's `DISPLAY`, `XAUTHORITY`, and `DBUS_SESSION_BUS_ADDRESS`.

### General

- If the user only names a goal such as "convert this PDF", ask for the target format and file path if they have not provided them.
- If operation fails silently, verify the file paths are absolute and files exist.
`, `XAUTHORITY`, and `DBUS_SESSION_BUS_ADDRESS`.

### General

- If the user only names a goal such as "convert this PDF", ask for the target format and file path if they have not provided them.
- If operation fails silently, verify the file paths are absolute and files exist.
