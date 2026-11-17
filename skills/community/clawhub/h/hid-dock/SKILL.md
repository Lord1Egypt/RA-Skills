---
name: hid-dock
description: "Connect to and control the Acasis Flow HID dock hardware (VID=0x35e6 PID=0xa4ac, 64-byte reports). Use when: the user asks to connect, check, switch view/page, read from, or send to the HID dock / 扩展坞 / Flow View device. Switches the dock screen between 数据同步(dataSync) and 快捷操作(shortcuts), inspects connection, reads reports, and sends raw payloads. Windows only. NOT for: generic mouse/keyboard automation or other vendors' HID devices."
metadata:
  openclaw:
    emoji: "🔌"
    os: ["win32"]
    install:
      - id: hid-dock-win-x64
        kind: download
        os: ["win32"]
        url: "https://github.com/facaiHero/hid-dock/releases/download/v1.0.0/hid-dock-win-x64.zip"
        archive: zip
        extract: true
        targetDir: "."
        label: "Download hid-dock CLI (Windows x64, self-contained)"
---

# HID Dock Skill

Connect to and control the Acasis Flow HID dock (VID `0x35e6` / PID `0xa4ac`, 64-byte reports).

## ⚙️ First-run setup (run this ONCE before using the skill)

The `hid-dock.exe` CLI (self-contained, ~37MB, no .NET needed) is NOT bundled with the skill.
On first use, download and extract it with this PowerShell command (run via the exec tool):

```powershell
$exe = "$env:USERPROFILE\.openclaw\tools\hid-dock\hid-dock.exe"; if (-not (Test-Path $exe)) { New-Item -ItemType Directory -Force -SplitPath $exe | Out-Null; $z = "$env:TEMP\hid-dock-win-x64.zip"; Invoke-WebRequest "https://github.com/facaiHero/hid-dock/releases/download/v1.0.0/hid-dock-win-x64.zip" -OutFile $z; Expand-Archive $z -DestinationPath (Split-Path $exe) -Force; Remove-Item $z; "installed" } else { "already installed" }; & $exe info
```

This checks if the exe exists, downloads + extracts it if missing, then verifies with `info`.
Skip the download step if the exe already exists — just run the command directly (below).

## When to Use

✅ **USE this skill when:**

- "连一下我的 HID 扩展坞" / "connect the dock" / "连上设备" → run `info`
- "切换到数据同步" / "切到数据同步页" → run `view dataSync`
- "切换到快捷操作" / "切到快捷页" → run `view shortcuts`
- "切换到视频" → `view video` ; "切换到PC遥控" → `view pcRemote`
- "检查扩展坞连接状态" / "check connection" → run `info`
- "读扩展坞数据" → run `read`

## When NOT to Use

❌ **DON'T use this skill when:**

- Generic mouse/keyboard automation → use a desktop-control skill
- Other vendors' HID devices → VID/PID will not match
- Non-Windows hosts

## Commands

The CLI targets the fixed device VID=0x35e6 PID=0xa4ac. The exe lives at
`%USERPROFILE%\.openclaw\tools\hid-dock\hid-dock.exe`. Run with PowerShell `&`.

### Switch dock view (切页面)

```powershell
& "$env:USERPROFILE\.openclaw\tools\hid-dock\hid-dock.exe" view shortcuts
& "$env:USERPROFILE\.openclaw\tools\hid-dock\hid-dock.exe" view dataSync
```

Sends a 64-byte SET_DASHBOARD_VIEW packet (action=4, view byte at offset 6):
`dataSync`=数据同步(0), `shortcuts`=快捷操作(1), `video`=视频(2), `pcRemote`=PC遥控(3).
On success prints `SENT view='<name>' (viewByte=<n>). 64-byte packet: ...`.

### Verify connection

```powershell
& "$env:USERPROFILE\.openclaw\tools\hid-dock\hid-dock.exe" info
```

Opens the device; on success ends with `CONNECTED. Device is open and ready.`.
If `OpenDevice() failed`, another app holds the HID — tell the user to close AcasisFlowDeskAi and retry.

### List all HID devices

```powershell
& "$env:USERPROFILE\.openclaw\tools\hid-dock\hid-dock.exe" list
```

Marks the target with `<== TARGET`. Use if `info`/`view` say "not found" (check it's plugged/powered).

### Read input reports

```powershell
& "$env:USERPROFILE\.openclaw\tools\hid-dock\hid-dock.exe" read 1 2000
```

### Send raw payload

```powershell
& "$env:USERPROFILE\.openclaw\tools\hid-dock\hid-dock.exe" send 01020304
```

## Notes

- Device must be physically connected and powered. Run `list` first if `info`/`view` say "not found".
- HID is exclusive: only one program may hold the device open at a time. Close AcasisFlowDeskAi before using.
- Windows only (self-contained .NET 10 single-file exe).
- 64-byte protocol: [0]=action [1]widgetType [2]row [3]col [4]width [5]height [6-7]payload [8-63]name(UTF-8).
