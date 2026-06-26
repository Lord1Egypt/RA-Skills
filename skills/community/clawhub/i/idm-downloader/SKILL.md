---
name: idm-downloader
description: Download large files using IDM (Internet Download Manager) on Windows. Use when user wants to download files via URL and prefers IDM, or explicitly requests IDM downloading. Ideal for large files (hundreds of MB to several GB). Triggers on requests like "download this file with IDM", "use IDM to download", "IDM下载", "用IDM下载文件".
---

# IDM Downloader

Use IDM (Internet Download Manager) to download large files via COM interface or command line on Windows. Recommended for large files such as datasets, videos, disk images, and archives where download resumption and acceleration are beneficial.

## Quick Usage

```bash
# Download a file to specified directory
python scripts/download_idm.py <url> [output_directory] [filename]

# Download to current directory
python scripts/download_idm.py <url>

# Download with custom filename
python scripts/download_idm.py <url> <output_directory> <custom_filename>
```

## Features

1. **COM Interface (Primary)**: Uses IDM's COM automation (`IDMan.CIDWMControl.1`) for reliable downloads
2. **Command Line Fallback**: Uses `IDMan.exe` with `/n` flag for immediate download
3. **Registry Search**: Finds IDM installation from Windows Registry if not at default paths
4. **Auto Filename**: Extracts filename from URL if not specified

## IDM Command Line

IDMan.exe parameters:
- `/d <URL>` - URL to download
- `/p <path>` - Local directory to save file
- `/f <filename>` - Filename to save as
- `/n` - Start download immediately (no prompt)

## Requirements

### System Requirements
- **OS**: Windows (IDM is a Windows-only application)
- **IDM**: Internet Download Manager installed on the system

### Python Dependencies

| Dependency | Purpose | Install Command |
|------------|---------|-----------------|
| Python 3.x | Runtime | - |
| pywin32 | COM interface & registry access | `pip install pywin32` |
| win32com.client | IDM COM automation | (included in pywin32) |
| pythoncom | COM initialization | (included in pywin32) |
| winreg | Windows Registry access | (built-in, Windows only) |

> **Note**: `pywin32` is optional but recommended for better compatibility and COM interface support. The script will fall back to command-line mode if not installed.

## Notes

- IDM must be installed on the system
- If COM fails, automatically falls back to command line
- Downloads start immediately with `/n` flag
