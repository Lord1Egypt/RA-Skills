# MCPorter 安装与配置

## 目的

这份文档只负责 `mcporter` 这一层：

- 使用 `../scripts/setup.sh` 检查当前状态
- 让脚本把 `pixcake-mcp` 路径写进配置
- 缺失时给出 `mcporter` 与路径定位的处理动作

这份文档不负责：

- 启动 PixCake 客户端
- 单独启动 `pixcake-mcp`
- 通过手动拉起二进制来验证进程生命周期

## 前提

读这份文档前，必须已经满足以下条件：

- `SKILL.md` 已经先完成 Access Check
- 当前环境通过 `mcporter` 接入 PixCake
- 已经知道如何定位 `pixcake` 与 `pixcake-mcp`

如果还处在“客户端是否启动”“二进制路径在哪里”这些问题上，不继续读这份文档，回到上层接入检查处理。启动 PixCake 后会自动带起 `pixcake-mcp`，不需要单独启动它。

## 常用落点

下面这些位置只用于 Access Check 阶段缩小排查范围，不是可以直接抄进配置的猜测值。

- macOS：`PixCake` 客户端包体常见在 `/Applications/PixCake*.app` 或 `~/Applications/PixCake*.app`
- macOS：真正的客户端可执行文件和 `pixcake-mcp` 常在对应 `.app` 包内的 `Contents/MacOS/` 下同级，例如 `/Applications/pixcake.app/Contents/MacOS/`
- Windows：`PixCake` 安装目录常见在 `C:\Program Files\PixCake\`、`C:\Program Files (x86)\PixCake\`，也可能在 `D:\PixCake\` 或 `E:\PixCake\`
- Windows：`pixcake-mcp` 通常与客户端同目录，文件名为 `pixcake-mcp.exe`

## 常用查找命令

建议顺序：先查进程，再查常见安装目录，最后再用系统搜索补充定位。

macOS：

```bash
pgrep -af 'pixcake|pixcake-mcp'
find /Applications ~/Applications -maxdepth 3 \( -iname '*pixcake*.app' -o -iname 'pixcake-mcp' \) 2>/dev/null
mdfind 'pixcake'
mdfind 'pixcake-mcp'
```

如果已经定位到 `.app` 包体，可继续查看包内可执行文件：

```bash
ls /Applications/pixcake.app/Contents/MacOS
```

Windows PowerShell：

```powershell
Get-Process | Where-Object { $_.Path -match 'pixcake' } | Select-Object Name, Path
Get-ChildItem 'C:\Program Files','C:\Program Files (x86)','D:\','E:\' -Filter 'pixcake-mcp.exe' -Recurse -ErrorAction SilentlyContinue
reg query HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall /s /f PixCake
reg query HKLM\SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall /s /f PixCake
```

## 检查顺序

按以下顺序检查，不要跳步：

1. Windows 如果当前文件名是 `scripts\setup.ps1.txt`，必须先重命名为 `setup.ps1`，否则后续命令无法执行：

```powershell
Rename-Item .\scripts\setup.ps1.txt setup.ps1
```

2. 先运行状态检查脚本：

```bash
# macOS
./scripts/setup.sh --check-only

# Windows PowerShell
.\scripts\setup.ps1 -CheckOnly
```

3. 如果脚本没找到 `pixcake` 或 `pixcake-mcp`，继续定位真实路径；必要时显式传路径：

```bash
# macOS
./scripts/setup.sh --pixcake-app "/Applications/pixcake.app/Contents/MacOS/pixcake" --pixcake-mcp "/Applications/pixcake.app/Contents/MacOS/pixcake-mcp"

# Windows PowerShell
.\scripts\setup.ps1 -PixcakeApp "C:\Program Files\PixCake\pixcake.exe" -PixcakeMcp "C:\Program Files\PixCake\pixcake-mcp.exe"
```

4. 如果脚本显示配置缺失，运行自动设置：

```bash
# macOS
./scripts/setup.sh

# Windows PowerShell
.\scripts\setup.ps1
```

5. 如果脚本显示 `mcporter` 缺失，直接运行自动设置；脚本会尝试通过 npm 安装 `mcporter`

6. 配置完成后，再验证 `pixcake` server 是否能被 `mcporter` 枚举：

```bash
mcporter --config ~/.openclaw/workspace/config/mcporter.json list pixcake --json
```

## 安装与配置

优先使用 `./scripts/setup.sh`（macOS）或 `.\scripts\setup.ps1`（Windows；如果当前文件名还是 `setup.ps1.txt`，先重命名）自动写配置。脚本会：

- 自动定位 `pixcake` 与 `pixcake-mcp`
- 在缺少 `mcporter` 时自动执行 `npm install -g mcporter`
- 在 `~/.openclaw/workspace/config/mcporter.json` 中写入 `pixcake`
- 如果本机已存在 `mcporter`，顺手做一次验证

脚本不会：

- 自动启动 PixCake 客户端
- 单独启动 `pixcake-mcp`

安装后验证命令可用：

```bash
command -v mcporter
mcporter --version
```

脚本写完后，可直接检查配置文件：

```bash
cat ~/.openclaw/workspace/config/mcporter.json
```

如果还没有 `pixcake`，把 `pixcake` 这一项补进 `mcpServers`。不要覆盖掉其他已经存在的 server。

macOS 最小示例：

```json
{
  "mcpServers": {
    "pixcake": {
      "transport": "stdio",
      "command": "/Applications/pixcake.app/Contents/MacOS/pixcake-mcp"
    }
  }
}
```

`command` 必须写成已经确认过的 `pixcake-mcp` 真实绝对路径。

这里的要求只是“路径明确并可用于配置”，不是在这份文档里手动启动它。

## 验证

完成配置后，先验证 server 能被枚举：

```bash
mcporter --config ~/.openclaw/workspace/config/mcporter.json list pixcake --json
```

需要参数文档时：

```bash
mcporter --config ~/.openclaw/workspace/config/mcporter.json list pixcake --schema --json
```

真实调用时：

```bash
mcporter --config ~/.openclaw/workspace/config/mcporter.json call pixcake.<tool_name> key=value
```

## Windows 说明

- `mcporter` 不会自动扫描 `D:` / `E:` 盘去找 PixCake
- Windows 下不要直接把 `pixcake-mcp.exe` 写进 `command`
- 目前实测可运行的写法是：`command` 用 `cmd`，`args` 传 `["/c", "<pixcake-mcp.exe绝对路径>"]`，并显式设置 `cwd`
- 也就是说，要先拿到实际安装路径和所在目录，再谈配置与连接

Windows 示例：

```json
{
  "mcpServers": {
    "pixcake": {
      "transport": "stdio",
      "command": "cmd",
      "args": [
        "/c",
        "C:\\Program Files\\PixCake\\pixcake-mcp.exe"
      ],
      "cwd": "C:\\Program Files\\PixCake"
    }
  }
}
```

## Guardrails

- 这份文档只处理 `mcporter` 安装、配置和验证
- 优先通过 `./scripts/setup.sh` 做配置写入
- 不在这里启动 PixCake 客户端
- 不在这里要求单独启动 `pixcake-mcp`
- 不猜 `pixcake-mcp` 的安装位置
- 不假设 `mcporter` 能自动发现 PixCake
- 不在没有 `list` 结果时猜工具名
- 不用连续重试代替配置检查
