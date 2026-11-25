# Windows 配置

## 前置条件

- Windows 10/11，Python 3.9 或更高版本。
- 推荐官方 Python，安装时勾选 `Add python.exe to PATH`。
- 直链下载需要 `curl`；现代 Windows 通常自带，缺失时安装 curl。
- 可选：`rclone`、`aria2c`、AList、OpenSSH Client。

## 路径

技能自动使用 Windows 标准目录：

| 内容 | 默认路径 |
|---|---|
| 配置 | `%APPDATA%\pan-downloader\config.json` |
| 日志 | `%LOCALAPPDATA%\pan-downloader\logs\pan-downloader.log` |
| 默认下载 | `%USERPROFILE%\Downloads\网盘下载` |

也可以用环境变量覆盖：`PAN_CONFIG`、`PAN_LOG`、`PAN_STATE_DIR`、`PAN_PLATFORM`。

## 快速开始

在 PowerShell 中运行：

```powershell
cd "<技能目录>\scripts"
.\pan.ps1 init
.\pan.ps1 doctor
.\pan.ps1 detect "https://pan.quark.cn/s/xxxx"
.\pan.ps1 get "https://example.com/a.zip" --dry-run
```

在 CMD 中运行：

```bat
cd /d "<技能目录>\scripts"
pan.cmd init
pan.cmd doctor
pan.cmd get "https://example.com/a.zip" --dry-run
```

`pan.cmd` 和 `pan.ps1` 只是启动包装器，实际入口仍是 `scripts\pan.py`。技能目录中不要放 `config.json`、Cookie、Token 或密码。

## 系统凭据库

Windows 使用 Credential Manager（凭据管理器）保存密码。配置只保存 `credential:名称` 引用，不保存明文。交互输入：

```powershell
.\pan.ps1 secret set engine.webdav
```

脚本/agent 从 stdin 保存：

```powershell
$env:WEBDAV_PASSWORD | .\pan.ps1 secret set engine.webdav --stdin
```

不要把密码直接写进 PowerShell 命令、批处理文件或聊天。使用 `secret check` 只检查存在性，不打印密码。

## 远程设备

Windows 既可以把文件下载到本机，也可以作为远程 NAS 的控制端：

```powershell
.\pan.ps1 remote add nas --kind ssh --host 192.168.1.10 --user lis --root /volume1
.\pan.ps1 remote check nas --probe
.\pan.ps1 remote deploy nas
.\pan.ps1 remote get nas "https://pan.baidu.com/s/xxxx" --pwd 1234
```

SMB 盘建议先映射为盘符，再登记为 `mount`：

```powershell
.\pan.ps1 remote add zdisk --kind mount --root "Z:\网盘下载"
.\pan.ps1 get "https://example.com/a.zip" --remote zdisk
```

更完整的品牌、协议和故障排查见 `references/21-远程NAS与私有存储.md`。

## 安全与兼容

- 不把密码放进命令行参数；优先 `secret set` 交互输入。
- 旧配置中的 `keychain:` 引用仍可读取；新引用统一使用 `credential:`，Windows 会落到 Credential Manager。
- 路径含空格时使用引号，例如 `--to "D:\我的下载\资料"`。
- 远程 SSH 优先使用 Windows OpenSSH 的密钥/agent，不使用 `sshpass` 或明文密码。
- 会员只影响本地并发调度，不承诺不限速，也不绕过平台验证码和风控。
