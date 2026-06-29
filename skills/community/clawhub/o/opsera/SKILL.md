---
name: opsera
description: Use the bundled Opsera executable as the Xshell replacement for VPN-launched sessions. Use when an agent needs to run commands or upload/download files through a current VPN-created .xsh local SSH tunnel. The bundled exe works as both GUI and CLI.
---

# Opsera

Opsera is self-contained in this skill directory.

Source and downloads:

- GitHub: https://github.com/tao-vin/opsera
- Releases / latest exe: https://github.com/tao-vin/opsera/releases

Executable:

```powershell
$opsera = Join-Path $env:CODEX_HOME "skills\opsera\bin\opsera.exe"
```

If `CODEX_HOME` is not set, resolve this skill directory first, then use `bin\opsera.exe` under it.

## Modes

- No args opens the GUI.
- `command` and `file` args run CLI mode for agents.
- CLI mode writes events to `%LOCALAPPDATA%\Opsera\events`; GUI shows those command/upload/download events.

## Command

```powershell
& $opsera command run --xsh "<path.xsh>" "hostname && whoami"
```

## Upload

```powershell
& $opsera file upload --xsh "<path.xsh>" "D:\local\file.txt" "/root/file.txt"
```

## Large Upload

Use this for large files. It uploads resumable chunks, keeps SSH alive, merges remotely, and verifies sha256.

```powershell
& $opsera file upload-large --xsh "<path.xsh>" --chunk-mb 512 "D:\local\big.dat" "/root/big.dat"
```

## Download

```powershell
& $opsera file download --xsh "<path.xsh>" "/root/file.txt" "D:\local\file.txt"
```

## Rules

- Use the bundled `bin\opsera.exe`; do not depend on external install directories.
- Use CLI mode, not HTTP, for agent operations.
- Do not call Xshell directly.
- Use `.xsh` fields `Host`, `Port`, `UserName`, and encrypted session password as parsed by Opsera.
- If the `.xsh` tunnel port is closed, ask the user to launch the VPN entry again and rerun immediately.
- Do not expose passwords.
