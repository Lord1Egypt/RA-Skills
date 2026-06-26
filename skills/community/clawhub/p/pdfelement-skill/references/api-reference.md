# PDFToolbox.exe Command-Line API Reference

## Overview

This document provides the complete command-line API reference for `PDFToolbox.exe` (Windows) and `PDFToolbox` (Linux), the command-line interface for PDFelement batch operations.

**Version**: Based on source code analysis (2026)
**Platform**: Windows, Ubuntu/Linux
**Architecture**: Single-instance application with parameter forwarding

---

## Runtime Notes

### Windows

- **Primary Method: Use `wspet://` custom protocol** (requires PDFelement 12.1.14+)
- The `wspet://` protocol is the standard way to launch PDFToolbox on Windows
- Direct `PDFToolbox.exe` execution is deprecated; always use `wspet://` protocol
- **Protocol Verification:** Test with `Start-Process "wspet://param=aG9tZSAtZW50cmFuY2UgT3BlbkNsYXc="`
- **If protocol fails:** PDFelement is not installed or version is too old
  - Download from: **https://pdf.wondershare.com/**
  - Install PDFelement 12.1.14 or later
  - Restart system to register the protocol
- For conversion tasks, prefer including `-f <payload>` with `-wsclaw -autoexec` flags for OpenClaw integration
- Example with wspet protocol:

```powershell
$filesXml = @"
<?xml version="1.0" encoding="UTF-8"?>
<Files>
  <File>
    <Path>C:\Docs\input.pdf</Path>
    <Password></Password>
  </File>
</Files>
"@
$base64Files = [Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes($filesXml))
$params = "convert -t .docx -f $base64Files -wsclaw -autoexec -entrance OpenClaw"
$base64Param = [Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes($params))
Start-Process "wspet://param=$base64Param"
```

### Ubuntu/Linux

- Prefer launching from `/opt/apps/PDFelement` with `./PDFToolbox` so bundled libraries are resolved.
- If changing directory is inconvenient, set `LD_LIBRARY_PATH=/opt/apps/PDFelement` before launching.
- GUI launch requires an active desktop session. Headless shells, services, or SSH sessions may fail unless they reuse the active session's `DISPLAY`, `XAUTHORITY`, and `DBUS_SESSION_BUS_ADDRESS`.
- For conversion tasks, prefer `convert -t <format> -f <payload> -entrance AllToolsPage` so the GUI opens with the PDF already loaded.
- Verified on this machine: `convert` with `-t ".docx"`, `-t ".pptx"`, and `-t ".txt"` plus `-f <payload>` created output files beside the source PDF.
- Example with a preloaded file from an active desktop session:

```bash
cd /opt/apps/PDFelement && DISPLAY=:1 XAUTHORITY=/run/user/1000/gdm/Xauthority DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/1000/bus ./PDFToolbox convert -t ".docx" -f "$(python3 /home/ws/.openclaw/workspace/skills/pdfelement-skill/scripts/build_file_payload.py /absolute/path/to/input.pdf)" -entrance AllToolsPage
```

---

## Command Syntax

### Windows (Primary Method - wspet:// Protocol)

```
wspet://param=<Base64EncodedCommandLine>
```

**The `wspet://` protocol is the standard and recommended method for Windows.** The entire command line is Base64-encoded in UTF-8 and passed as the `param` value.

**Example:**
```powershell
$params = "convert -t .docx -entrance OpenClaw"
$base64 = [Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes($params))
Start-Process "wspet://param=$base64"
```

**Protocol Requirements:**
- PDFelement version 12.1.14 or later must be installed
- Protocol is automatically registered during PDFelement installation
- Verify availability: `Start-Process "wspet://param=aG9tZSAtZW50cmFuY2UgT3BlbkNsYXc="`

**If protocol is not recognized:**
- Download PDFelement from **https://pdf.wondershare.com/**
- Install version 12.1.14+
- Restart system after installation

### Windows (Legacy - Not Recommended)

```
PDFToolbox.exe <command> [options...]
```

⚠️ **Deprecated:** Direct execution is not recommended. Use `wspet://` protocol instead.

### Ubuntu/Linux

```bash
/opt/apps/PDFelement/PDFToolbox <command> [options...]
```

### Components

1. **`<command>`** — Required first parameter that determines the operation mode
2. **`[options]`** — Optional parameters for configuration and file pre-loading

---

## Commands

All commands are defined in `ToolboxParameter.SupportStartup` and are **case-sensitive**.

### Document Conversion

#### `convert`
Opens the batch conversion interface.

**Usage (Windows - wspet:// protocol):**
```powershell
$params = "convert -t .docx -entrance OpenClaw"
$base64 = [Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes($params))
Start-Process "wspet://param=$base64"
```

**Usage (Ubuntu/Linux):**
```bash
/opt/apps/PDFelement/PDFToolbox convert -t ".docx" -entrance AllToolsPage
```

**Additional Parameters:**
- `-t <format>` — Target format (e.g., `.docx`, `.xlsx`, `.pptx`, `.jpg`)
- `-f <base64xml>` — Pre-load files (see File Parameter Format)
- `-entrance <string>` — Entry point identifier

**Supported Formats:**
| Format | Description |
|--------|-------------|
| `.docx`, `.doc` | Microsoft Word |
| `.xlsx`, `.xls` | Microsoft Excel |
| `.pptx`, `.ppt` | Microsoft PowerPoint |
| `.txt` | Plain Text |
| `.rtf` | Rich Text Format |
| `.html`, `.xml` | Web formats |
| `.epub` | E-book format |
| `.jpg`, `.jpeg`, `.png`, `.bmp`, `.gif`, `.tiff` | Image formats |
| `.pdf` | PDF/A, PDF/X formats |
| `.hwp`, `.hwpx` | Hancom Office |
| `.ofd` | Open Fixed-layout Document |

---

### OCR (Optical Character Recognition)

#### `ocr`
Opens the batch OCR interface.

**Usage (Windows - wspet:// protocol):**
```powershell
$params = "ocr -entrance OpenClaw"
$base64 = [Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes($params))
Start-Process "wspet://param=$base64"
```

**Usage (Ubuntu/Linux):**
```bash
/opt/apps/PDFelement/PDFToolbox ocr -entrance AllToolsPage
```

**Purpose:** Convert scanned PDFs or images in PDFs to searchable text.

---

### Document Optimization

#### `optimize`
Opens the batch compression/optimization interface.

**Usage (Windows - wspet:// protocol):**
```powershell
$params = "optimize -entrance OpenClaw"
$base64 = [Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes($params))
Start-Process "wspet://param=$base64"
```

**Purpose:** Reduce PDF file size by optimizing images and removing unnecessary data.

---

### Translation

#### `translate`
Opens the batch translation interface.

**Usage (Windows - wspet:// protocol):**
```powershell
$params = "translate -entrance OpenClaw"
$base64 = [Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes($params))
Start-Process "wspet://param=$base64"
```

**Purpose:** Translate PDF documents between different languages.

---

### Watermarking

#### `watermark`
Opens the batch watermark interface.

**Usage (Windows - wspet:// protocol):**
```powershell
$params = "watermark -entrance OpenClaw"
$base64 = [Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes($params))
Start-Process "wspet://param=$base64"
```

**Purpose:** Add text or image watermarks to PDFs.

---

### Background

#### `background`
Opens the batch background interface.

**Usage:**
```powershell
PDFToolbox.exe background -entrance AllToolsPage
```

**Purpose:** Add background colors or images to PDF pages.

---

### Headers and Footers

#### `headerFooter`
Opens the batch header and footer interface.

**Usage:**
```powershell
PDFToolbox.exe headerFooter -entrance AllToolsPage
```

**Purpose:** Add headers and footers with page numbers, dates, etc.

---

### Bates Numbering

#### `batesNumber`
Opens the batch Bates numbering interface.

**Usage:**
```powershell
PDFToolbox.exe batesNumber -entrance AllToolsPage
```

**Purpose:** Add Bates numbers for legal document management.

---

### Security

#### `security`
Opens the batch security interface.

**Usage:**
```powershell
PDFToolbox.exe security -entrance AllToolsPage
```

**Purpose:** Set passwords, encryption, and permissions on PDFs.

---

### Batch Printing

#### `batchPrint`
Opens the batch printing interface.

**Usage:**
```powershell
PDFToolbox.exe batchPrint -entrance HotKey
```

**Purpose:** Print multiple PDF documents.

---

### Data Extraction

#### `dataExtract`
Opens the batch data extraction interface.

**Usage:**
```powershell
PDFToolbox.exe dataExtract -entrance AllToolsPage
```

**Purpose:** Extract data from PDF forms and tables.

---

### Delete Blank Pages

#### `deleteBlankPages`
Opens the delete blank pages interface.

**Usage:**
```powershell
PDFToolbox.exe deleteBlankPages -entrance AllToolsPage
```

**Purpose:** Automatically detect and remove blank pages from PDFs.

---

### Digital Signatures

#### `sign`
Opens the batch signature interface.

**Usage:**
```powershell
PDFToolbox.exe sign -entrance AllToolsPage
```

**Purpose:** Add digital signatures to PDFs.

---

### Split Documents

#### `split`
Opens the batch split interface.

**Usage:**
```powershell
PDFToolbox.exe split -entrance AllToolsPage
```

**Purpose:** Split PDF documents into multiple files.

---

### Combine Documents

#### `combine`
Opens the combine/merge interface.

**Usage:**
```powershell
PDFToolbox.exe combine -entrance AllToolsPage
```

**Purpose:** Merge multiple PDF files into one document.

**Note:** Currently defined but may behave similar to home page in some versions.

---

### Crop Pages

#### `crop`
Opens the batch crop interface.

**Usage:**
```powershell
PDFToolbox.exe crop -entrance AllToolsPage
```

**Purpose:** Crop PDF pages to remove margins or unwanted areas.

---

### Create PDFs

#### `create`
Opens the batch PDF creation interface.

**Usage:**
```powershell
PDFToolbox.exe create -entrance AllToolsPage
```

**Purpose:** Create PDF documents from various source files.

---

### Home Page

#### `home`
Opens the toolbox home page (tool list).

**Usage:**
```powershell
PDFToolbox.exe home -entrance Exe
```

**Purpose:** Display the main tool selection interface.

---

### Modal Mode

#### `modal`
Opens the first instance in modal dialog mode.

**Usage:**
```powershell
PDFToolbox.exe modal -entrance AllToolsPage
```

**Purpose:** Display toolbox as a modal dialog using `ShowDialog()`.

---

## Parameters

### Data Parameters

These parameters are parsed by `ParameterParser.ParseArguments()` starting from index 1.

#### `-f <base64xml>`
Pre-load file list with optional passwords.

**Format:** Base64-encoded UTF-8 XML

**XML Structure:**
```xml
<?xml version="1.0" encoding="UTF-8"?>
<Files>
  <File>
    <Path>C:\Documents\sample.pdf</Path>
    <Password>123456</Password>
  </File>
  <File>
    <Path>C:\Documents\another.pdf</Path>
    <Password></Password>
  </File>
</Files>
```

**PowerShell Example (Windows - wspet:// protocol):**
```powershell
$xml = @'
<?xml version="1.0" encoding="UTF-8"?>
<Files>
  <File>
    <Path>C:\Docs\A.pdf</Path>
    <Password>123456</Password>
  </File>
  <File>
    <Path>C:\Docs\B.pdf</Path>
    <Password></Password>
  </File>
</Files>
'@
$base64Files = [Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes($xml))
$params = "convert -t .docx -f $base64Files -wsclaw -autoexec -entrance OpenClaw"
$base64Param = [Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes($params))
Start-Process "wspet://param=$base64Param"
```

**Bash Example (Ubuntu/Linux):**
```bash
xml='<?xml version="1.0" encoding="UTF-8"?>
<Files>
  <File>
    <Path>/home/user/Documents/A.pdf</Path>
    <Password>123456</Password>
  </File>
  <File>
    <Path>/home/user/Documents/B.pdf</Path>
    <Password></Password>
  </File>
</Files>'
f=$(echo -n "$xml" | base64 -w 0)
/opt/apps/PDFelement/PDFToolbox convert -t ".docx" -f "$f" -entrance AllToolsPage
```

**Behavior:**
- `Path` element is used as unique key; duplicate paths are ignored
- `Password` can be empty string
- Files are automatically loaded into the operation's file list

**Scope:** All batch operation pages (via `BaseTaskPage.LoadArgs`)

---

#### `-t <format>`
Target format for conversion operations.

**Format:** File extension string (e.g., `.docx`, `.xlsx`, `.jpg`)

**Scope:** `convert` command only

**Example (Windows - wspet:// protocol):**
```powershell
$params = "convert -t .xlsx -entrance OpenClaw"
$base64 = [Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes($params))
Start-Process "wspet://param=$base64"
```

**Behavior:**
- Matched against `SupportFormats.FormatExtDic`
- Falls back to default format if not recognized (usually `.docx`)
- Case-sensitive

---

#### `-entrance <string>`
Entry point identifier for tracking and analytics.

**Format:** Any string value

**Common Values:**
- `AllToolsPage` — From main tools interface
- `HotKey` — From keyboard shortcut
- `DeviceBoot` — From system startup
- `Notify` — From notification/tray icon
- `OptimizeForm` — From optimize page
- `OCRSetting` — From OCR settings
- `TranslatePage` — From translate page
- `OpenClaw` — From OpenClaw AI assistant
- `API` — From programmatic call

**Scope:** All commands

**Example (Windows - wspet:// protocol):**
```powershell
$params = "convert -entrance OpenClaw"
$base64 = [Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes($params))
Start-Process "wspet://param=$base64"
```

**Note:** While `/entrance` is defined in code, use `-entrance` for compatibility.

---

#### `-wsclaw`
Mark the command as triggered by OpenClaw's `pdfelement-skill`.

**Version:** 12.1.14+

**Format:** Flag (no value)

**Scope:** All commands

**Purpose:** Used for tracking and analytics to identify commands launched from OpenClaw AI assistant.

**Example (Windows - wspet:// protocol):**
```powershell
$params = "convert -t .docx -wsclaw -entrance OpenClaw"
$base64 = [Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes($params))
Start-Process "wspet://param=$base64"
```

---

#### `-autoexec`
Auto-execute the operation after a 10-second countdown when files are loaded and the Apply button is available.

**Version:** 12.1.14+

**Format:** Flag (no value)

**Scope:** All batch operation commands

**Requirements:** Must be used together with `-wsclaw` to be effective.

**Behavior:**
- When files are loaded via `-f` and the operation is ready, a 10-second countdown starts
- User can cancel during the countdown
- After countdown, the operation executes automatically
- If `-wsclaw` is not present, this flag is ignored

**Example (Windows - wspet:// protocol):**
```powershell
$filesXml = @"
<?xml version="1.0" encoding="UTF-8"?>
<Files>
  <File>
    <Path>C:\Docs\sample.pdf</Path>
    <Password></Password>
  </File>
</Files>
"@
$base64Files = [Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes($filesXml))
$params = "convert -t .docx -f $base64Files -wsclaw -autoexec -entrance OpenClaw"
$base64Param = [Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes($params))
Start-Process "wspet://param=$base64Param"
```

---

#### `-m <handle>`
Owner window handle for window positioning and parent-child relationship.

**Format:** Integer (long) window handle

**Scope:** All commands

**Example:**
```powershell
PDFToolbox.exe convert -m 123456 -entrance API
```

**Purpose:** Used for centering new window over parent window.

---

### Control Parameters

These parameters are parsed by `CommandLineHelper.CheckSwitch()` and support both `-` and `/` prefixes.

#### `/exit` or `-exit`
Request to exit existing instance.

**Default:** `false`

**Example:**
```powershell
PDFToolbox.exe /exit
```

**Behavior:**
- If no existing instance: exits immediately
- If existing instance: sends exit request to it

---

#### `/nowexit` or `-nowexit`
Force immediate exit.

**Default:** `false`

**Example:**
```powershell
PDFToolbox.exe /nowexit
```

**Behavior:**
- Sets `IsExit=true` and terminates immediately
- More forceful than `/exit`

---

#### `-hidden`
Run in hidden mode without showing main window.

**Default:** `false`

**Example:**
```powershell
PDFToolbox.exe convert -hidden -entrance DeviceBoot
```

**Behavior:**
- Initializes in background
- Does not display main window
- Often combined with `-enablehidden`

---

#### `-enablehidden`
Allow hidden message loop operation.

**Default:** `false`

**Example:**
```powershell
PDFToolbox.exe -hidden -enablehidden -entrance DeviceBoot
```

**Purpose:** Combined with `-hidden` for background operations without visible window.

---

#### `/activateform` or `-activateform`
Activate existing window without switching pages.

**Default:** `false`

**Example:**
```powershell
PDFToolbox.exe /activateform -entrance Notify
```

**Behavior:**
- Brings existing window to foreground
- Does not change current page
- Useful for "wake up" operations

---

#### `-enablenotify <boolean>`
Control tray icon and notification features.

**Default:** `true`

**Accepted Values:** `0`, `1`, `true`, `false`

**Example:**
```powershell
PDFToolbox.exe home -enablenotify 0 -entrance DeviceBoot
```

**Behavior:**
- `false` or `0`: Disables tray icon logic
- `true` or `1`: Enables tray icon (default)

---

## Boolean Value Parsing

For control parameters, the following formats are accepted (case-insensitive):

| Format | Example | Result |
|--------|---------|--------|
| Flag only | `-hidden` | `true` |
| Space separator | `-hidden true` | `true` |
| Equals sign | `-hidden=1` | `true` |
| Colon | `-hidden:false` | `false` |
| Zero/One | `-hidden 0` | `false` |

**Parsed by:** `CommandLineHelper.ValueToBoolean()`

---

## Single Instance Behavior

PDFToolbox.exe uses a mutex + .NET Remoting architecture for single-instance enforcement:

### First Instance
1. Acquires mutex lock
2. Initializes remoting channel
3. Shows main window
4. Processes parameters locally

### Subsequent Instances
1. Detects existing instance via mutex
2. Forwards parameters via remoting to first instance
3. Terminates self

### Remote Execution Logic
When parameters are forwarded:

```
if (IsExit == true)
    → Call Exit() on existing instance
else if (IsHidden == false)
    → Show/Activate window
    → Process command (switch page if needed)
else if (IsHidden == true && IsRemoteCall)
    → Do nothing (background operation)
    → Return immediately
```

**Source References:**
- `Source/Product/PEToolbox/PEToolboxApp.cs:101` — Single instance check
- `Source/Product/PEToolbox/PEToolboxApp.cs:299` — Remote execution

---

## Command Line Parsing Flow

```
PDFToolbox.exe <command> -param1 value1 -param2 value2 /flag1 -flag2
                  ↓
          1. Extract control flags
             (CheckSwitch: /exit, -hidden, etc.)
                  ↓
          2. Extract first argument as <command>
             (convert, ocr, optimize, etc.)
                  ↓
          3. Parse remaining arguments as data parameters
             (ParseArguments from index 1: -f, -t, -entrance, -m)
                  ↓
          4. Route to appropriate page
             (ShowPage based on command)
                  ↓
          5. Apply parameters to page
             (LoadArgs: file list, target format, etc.)
```

**Key Source Files:**
- `Source/Product/PEToolbox/ParameterStart.cs:74` — Main parsing entry
- `Source/Product/StartupParameters/ParameterParser.cs:99` — Data parameter parsing
- `Source/Product/Utilities/Helpers/CommandLineHelper.cs:45` — Control flag parsing

---

## Parameter Prefix Rules

### Data Parameters (Dictionary-based)
- **Currently supported:** `-` prefix only
- **Examples:** `-f`, `-t`, `-entrance`, `-m`
- **Reason:** `IsArg` implementation only checks for `'-'` at index 0

### Control Parameters (Switch-based)
- **Supported:** Both `-` and `/` prefixes
- **Examples:** `-hidden`, `/exit`, `-activateform`, `/nowexit`
- **Case-insensitive**

### Important Notes

⚠️ **Current Limitation:**
While `/entrance` is defined in code constants, the current parameter parser only recognizes `-entrance` due to `IsArg` implementation. For maximum compatibility, always use `-entrance`.

---

## Error Handling

### Windows Errors

#### wspet:// Protocol Not Recognized

**Symptoms:**
- Error: "This file does not have a program associated with it"
- Error: "No application is associated with the specified file"
- Protocol handler not found

**Solution:**
1. PDFelement is not installed or version is outdated
2. Download from **https://pdf.wondershare.com/**
3. Install PDFelement version 12.1.14 or later
4. Restart system to register the `wspet://` protocol
5. Verify installation:
   ```powershell
   Start-Process "wspet://param=aG9tZSAtZW50cmFuY2UgT3BlbkNsYXc="
   ```

#### GUI Not Appearing

**Cause:** Command running in non-desktop session

**Solution:** Ensure command runs in user's logged-in desktop session

### Linux Errors

#### Unrecognized Commands
- Fallback behavior: Defaults to `home` command
- No error message displayed
- Source: `Source/Product/PEToolbox/ParameterStart.cs:145`

### General Errors

#### Invalid Parameters
- Silently ignored (dictionary check prevents duplicates)
- Invalid format values fall back to defaults
- No error messages to user

#### File Loading Errors
- Invalid Base64 or XML in `-f`: File list remains empty
- Invalid file paths: Skipped during loading
- Password-protected files without password: Prompt user during operation

---

## Usage Examples

### Example 1: Simple Conversion (Windows - wspet://)
```powershell
$params = "convert -t .docx -entrance OpenClaw"
$base64 = [Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes($params))
Start-Process "wspet://param=$base64"
```
Opens conversion interface with Word format pre-selected.

---

### Example 2: Conversion with Pre-loaded Files (Windows - wspet://)
```powershell
$xml = @'
<?xml version="1.0" encoding="UTF-8"?>
<Files>
  <File>
    <Path>C:\Work\report.pdf</Path>
    <Password></Password>
  </File>
  <File>
    <Path>C:\Work\invoice.pdf</Path>
    <Password>secret123</Password>
  </File>
</Files>
'@
$fileParam = [Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes($xml))
PDFToolbox.exe convert -t ".xlsx" -f $fileParam -entrance API
```
Converts two PDFs to Excel with one password-protected.

---

### Example 3: OCR with Auto-Execute (Windows - wspet://)
```powershell
$filesXml = @"
<?xml version="1.0" encoding="UTF-8"?>
<Files>
  <File>
    <Path>C:\Scans\document.pdf</Path>
    <Password></Password>
  </File>
</Files>
"@
$base64Files = [Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes($filesXml))
$params = "ocr -f $base64Files -wsclaw -autoexec -entrance OpenClaw"
$base64 = [Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes($params))
Start-Process "wspet://param=$base64"
```
Starts OCR with file pre-loaded and 10-second auto-execute countdown.

---

### Example 4: Optimize with Auto-Execute (Windows - wspet://)
```powershell
$filesXml = @"
<?xml version="1.0" encoding="UTF-8"?>
<Files>
  <File>
    <Path>C:\Docs\large.pdf</Path>
  </File>
</Files>
"@
$base64Files = [Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes($filesXml))
$params = "optimize -f $base64Files -wsclaw -autoexec -entrance OpenClaw"
$base64 = [Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes($params))
Start-Process "wspet://param=$base64"
```
Compresses PDF with auto-execute enabled.

---

### Example 5: Translate with Auto-Execute (Windows - wspet://)
```powershell
$params = "translate -f $base64Files -wsclaw -autoexec -entrance OpenClaw"
$base64 = [Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes($params))
Start-Process "wspet://param=$base64"
```
Translates PDF with pre-loaded files.

---

### Example 6: Multiple Files Conversion (Windows - wspet://)
```powershell
$filesXml = @"
<?xml version="1.0" encoding="UTF-8"?>
<Files>
  <File>
    <Path>D:\PDFs\Document1.pdf</Path>
    <Password></Password>
  </File>
  <File>
    <Path>D:\PDFs\Document2.pdf</Path>
    <Password></Password>
  </File>
  <File>
    <Path>D:\PDFs\Document3.pdf</Path>
    <Password></Password>
  </File>
</Files>
"@
$base64Files = [Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes($filesXml))
$params = "convert -t .pptx -f $base64Files -wsclaw -autoexec -entrance OpenClaw"
$base64Param = [Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes($params))
Start-Process "wspet://param=$base64Param"
```
Converts three PDFs to PowerPoint format with files pre-loaded and auto-execute.

---

### Example 7: Protocol Verification Test (Windows)
```powershell
# Test if wspet:// protocol is available
Start-Process "wspet://param=aG9tZSAtZW50cmFuY2UgT3BlbkNsYXc="
```
Opens PDFToolbox home page. If this fails, PDFelement is not properly installed.

---

### Example 8: Using wspet:// Protocol (Windows)

**Basic Protocol Usage (PowerShell):**
```powershell
$params = 'convert -t ".docx" -entrance AllToolsPage'
$base64Param = [Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes($params))
Start-Process "wspet://param=$base64Param"
```

**Basic Protocol Usage (CMD):**
```cmd
set "params=convert -t .docx -entrance AllToolsPage"
for /f "delims=" %%i in ('powershell -Command "[Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes('%params%'))]"') do set "base64Param=%%i"
start wspet://param=%base64Param%
```

---

### Example 9: wspet:// with File Pre-loading and Auto-Execute

**PowerShell:**
```powershell
# Build file list XML
$filesXml = @"
<?xml version="1.0" encoding="UTF-8"?>
<Files>
  <File>
    <Path>C:\Docs\sample.pdf</Path>
    <Password></Password>
  </File>
</Files>
"@
$base64FilesXml = [Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes($filesXml))

# Build command with OpenClaw markers
$params = "convert -t .docx -f $base64FilesXml -wsclaw -autoexec -entrance OpenClaw"
$base64Param = [Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes($params))
$escapedParam = [Uri]::EscapeDataString($base64Param)

# Launch
Start-Process "wspet://param=$escapedParam"
```

**CMD:**
```cmd
@echo off
setlocal enabledelayedexpansion

rem Build file list XML
set "filesXml=<?xml version="1.0" encoding="UTF-8"?><Files><File><Path>C:\Docs\sample.pdf</Path><Password></Password></File></Files>"

rem Encode files XML
for /f "delims=" %%i in ('powershell -Command "[Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes('%filesXml%'))]"') do set "base64FilesXml=%%i"

rem Build command
set "params=convert -t .docx -f !base64FilesXml! -wsclaw -autoexec -entrance OpenClaw"

rem Encode command
for /f "delims=" %%i in ('powershell -Command "[Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes('!params!'))]"') do set "base64Param=%%i"

rem Launch
start wspet://param=!base64Param!
```

---

### Example 10: wspet:// for Different Operations

**Optimize with auto-execute:**
```powershell
$filesXml = @"
<?xml version="1.0" encoding="UTF-8"?>
<Files>
  <File>
    <Path>C:\Docs\large.pdf</Path>
  </File>
</Files>
"@
$base64Files = [Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes($filesXml))
$params = "optimize -f $base64Files -wsclaw -autoexec -entrance OpenClaw"
$base64 = [Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes($params))
Start-Process "wspet://param=$base64"
```

**OCR with auto-execute:**
```powershell
$params = "ocr -f $base64Files -wsclaw -autoexec -entrance OpenClaw"
$base64 = [Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes($params))
Start-Process "wspet://param=$base64"
```

**Translate with auto-execute:**
```powershell
$params = "translate -f $base64Files -wsclaw -autoexec -entrance OpenClaw"
$base64 = [Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes($params))
Start-Process "wspet://param=$base64"
```

---

## Integration Points

PDFToolbox.exe is called from various points in PDFelement and external applications:

| Source | Entry Point | Typical Command |
|--------|-------------|-----------------|
| All Tools Interface | `IAllToolHandler.cs:101` | `convert -entrance AllToolsPage` |
| Keyboard Shortcuts | `AppHotKeyService.cs:146` | `<command> -entrance HotKey` |
| Toolbox Entry | `ToolboxEntry.cs:11` | Various commands |
| OCR Settings | `OcrSettingForm.cs:443` | `ocr -f <base64> -entrance OCRSetting` |
| Optimize Form | `OptimizeForm.cs:387` | `optimize -f <base64> -entrance OptimizeForm` |
| Translate Page | `PdfTranslatePage.cs:626` | `translate -f <base64> -entrance TranslatePage` |
| **OpenClaw AI (wspet://)** | **pdfelement-skill** | `wspet://param=<base64>` with `-wsclaw -autoexec -entrance OpenClaw` |

### OpenClaw Integration

When integrating with OpenClaw AI assistant through the `pdfelement-skill`:

1. **Use wspet:// protocol** for Windows compatibility
2. **Include `-wsclaw` flag** to mark OpenClaw as the trigger source
3. **Add `-autoexec` flag** to enable 10-second countdown auto-execution
4. **Set entrance to `OpenClaw`** for proper tracking
5. **Pre-load files via `-f`** for seamless user experience

**Typical OpenClaw Command Pattern:**
```
wspet://param=<Base64Encoded: "command -t format -f files -wsclaw -autoexec -entrance OpenClaw">
```

---

## Version Compatibility

This API reference is based on source code analysis and applies to:
- **PDFelement**: Current enterprise/professional versions
- **Platform**: Windows, Ubuntu/Linux
- **Windows Shell**: PowerShell 5.1+, Command Prompt
- **Linux Shell**: Bash, Zsh, or any POSIX-compatible shell
- **Linux Installation Path**: `/opt/apps/PDFelement/PDFToolbox`

---

## Security Considerations

1. **File Paths:** Always use absolute paths to prevent ambiguity
2. **Passwords:** Stored in plain text in XML; use secure channels
3. **Base64 Encoding:** Not encryption; only for transport encoding
4. **Single Instance:** Remoting channel uses default security settings

---

## Performance Notes

1. **Startup Time:** First instance takes longer (UI initialization)
2. **Parameter Forwarding:** Subsequent calls are fast (remoting)
3. **Large File Lists:** XML size affects parsing time
4. **Hidden Mode:** Slightly faster startup without UI rendering

---

## Debugging Tips

### Windows

1. **Verify wspet:// Protocol First**
   ```powershell
   # Test protocol availability
   Start-Process "wspet://param=aG9tZSAtZW50cmFuY2UgT3BlbkNsYXc="
   ```
   If this fails, PDFelement is not properly installed.

2. **Check PDFelement Installation**
   - Verify version is 12.1.14 or later
   - Download from: **https://pdf.wondershare.com/**
   - Restart system after installation

3. **Test Simple Commands First**
   - Start with basic commands before complex ones
   - Use `-entrance OpenClaw` for tracking

4. **Verify Base64 Encoding**
   ```powershell
   # Check if encoding is correct
   $params = "convert -t .docx -entrance OpenClaw"
   $base64 = [Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes($params))
   Write-Host "Encoded: $base64"
   ```

5. **Monitor Processes**
   - Check Task Manager for PDFToolbox.exe instances
   - Single instance architecture may forward commands

### Linux

1. **Verify Installation**
   - Check `/opt/apps/PDFelement/PDFToolbox` exists
   - Ensure execute permissions: `chmod +x /opt/apps/PDFelement/PDFToolbox`

2. **Check Desktop Session**
   - Use `ps aux | grep PDFToolbox` to check running processes
   - Verify `DISPLAY`, `XAUTHORITY`, `DBUS_SESSION_BUS_ADDRESS` are set

3. **Test Library Path**
   ```bash
   cd /opt/apps/PDFelement && ./PDFToolbox home -entrance Test
   ```

4. **Encoding Verification**
   - Use `base64 -w 0` for single-line encoding
   - Verify UTF-8 encoding for XML

### General

1. **Start Simple:** Test basic commands before adding complexity
2. **Check File Paths:** Always use absolute paths
3. **Verify Parameters:** Use `-entrance Test` to verify parameter passing
4. **Monitor Output:** Check for error messages or warnings

---

## Additional Resources

- **Main Documentation:** [SKILL.md](../SKILL.md)
- **Source Code References:** See inline comments in this document

---

© 2026 Wondershare PDFelement Team. All rights reserved.
