# HubStudio ADB Connection Skill

This guide standardizes ADB connection workflows for HubStudio cloud phones.

## Scope

- Android 12 / Android 15: direct ADB connection
- Android 13 / Android 14 / Android 15A: SSH tunnel + local ADB connection

## Preconditions

- HubStudio local API is reachable (`http://127.0.0.1:6873`)
- Cloud phone is powered on
- ADB access is enabled
- Local `adb` command is installed and available in PATH

### If ADB is not installed

macOS (Homebrew):

```bash
brew install android-platform-tools
adb version
```

Windows (winget):

```powershell
winget install Google.PlatformTools
adb version
```

Manual install (all platforms):

- Download Android SDK Platform Tools from Google
- Add `platform-tools` directory to PATH
- Re-open terminal and run `adb version`

## Step 0: Enable ADB and Query Connection Info

1) Enable ADB:

```bash
node hubstudio.js adbEnable <mobileId>
```

2) Query ADB info:

```bash
node hubstudio.js adbInfo <mobileId>
```

Expected fields from response:
- `adbIp`
- `adbPort`
- `adbPassword` (connection code)
- For some versions/platforms, tunnel command fields may also be returned

## Workflow A: Android 12 / Android 15

### A1. Connect directly to cloud phone

```bash
adb connect <adbIp>:<adbPort>
```

### A2. Authenticate with connection code

```bash
adb shell <adbPassword>
```

or:

```bash
adb -s <adbIp>:<adbPort> shell <adbPassword>
```

### A3. Verify connection

```bash
adb devices
```

## Workflow B: Android 13 / Android 14 / Android 15A

### B1. Create SSH tunnel (first terminal)

```bash
ssh -oHostKeyAlgorithms=+ssh-rsa <sshUser>@<sshHost> -p <sshPort> -L <localPort>:adb-proxy:<remoteAdbPort> -Nf
```

When prompted, input the SSH password from platform response.

### B2. Connect local forwarded ADB port (second terminal)

```bash
adb connect localhost:<localPort>
```

### B3. Verify connection

```bash
adb devices
```

Expected output:

```text
List of devices attached
localhost:<localPort>    device
```

## Complete Operation Checklist

- [ ] Cloud phone is powered on
- [ ] `enableAdb=true` applied successfully
- [ ] `list-adb` returns non-null ADB fields
- [ ] Chosen proper workflow by Android version
- [ ] `adb devices` shows connected device

## Common Commands

```bash
adb devices
adb shell
adb shell pm list packages
adb install app.apk
adb uninstall <package.name>
adb reboot
```

## Troubleshooting

### `adb connect` timeout or refused

- Confirm cloud phone status is running
- Confirm ADB is enabled
- Re-query `list-adb` to ensure `adbIp/adbPort` is valid
- Check local firewall/network policy

### SSH tunnel mode cannot connect

- Verify tunnel process is alive
- Confirm `<localPort>` is not occupied
- Rebuild SSH tunnel and retry `adb connect localhost:<localPort>`

### Connected but shell auth fails

- Recheck `adbPassword` from latest `list-adb` response
- Retry on specific device with `adb -s ... shell <code>`
