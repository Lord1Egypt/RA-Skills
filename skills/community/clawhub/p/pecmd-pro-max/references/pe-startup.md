# PECMD 在 WinPE 启动中的应用

## 启动流程

WinPE 的启动链有两条真实入口，PECMD 通常替换其中一条：

```
UEFI/BIOS → bootmgr/bootmgfw.efi → winload.exe/efi → ntoskrnl.exe
    → smss.exe → winlogon.exe
        → winpeshl.exe
            → 读取 %SystemRoot%\System32\winpeshl.ini 的 [LaunchApp] AppPath=...
            → 或回退到 cmd.exe /k startnet.cmd
```

- **入口 A（改 Setup\CmdLine）**：PE 默认 `HKLM\SYSTEM\Setup\CmdLine` 为 `winpeshl.exe`；制作者常把它改为
  `PECMD.EXE MAIN %WinDir%\System32\PECMD.INI`。
- **入口 B（改 winpeshl.ini）**：保留 `Setup\CmdLine=winpeshl.exe`，把 `winpeshl.ini` 的
  `AppPath` 指向 `PECMD.EXE` 或 `wpeinit.exe`。

> 部分现有 PE 走入口 A，但在 `PECMD.INI` 首行用 `EXEC Winpeshl` 补做原生初始化；若 PECMD 已由
> `winpeshl.ini` 启动，不要再调用 `Winpeshl`，避免同一初始化链重入。

`winpeshl.ini` 的实际形态：

```ini
[LaunchApp]
AppPath=X:\Windows\System32\wpeinit.exe
```

> `Control\MiniNT` 键只用于标识 WinPE；不存在名为 WinPEShell 的注册表值。
> `SetupComplete.cmd` 不是 WinPE 启动脚本。

### WinXShell 集成

WinXShell 提供类 Explorer 桌面（任务栏、文件管理器、托盘），通常由 PECMD 启动：

```wcs
// 作为桌面 Shell 启动（路径按实际安装位置）
SHEL %ProgramFiles%\WinXShell\WinXShell.exe -winpe
// 或作为普通程序启动
EXEC %ProgramFiles%\WinXShell\WinXShell.exe -winpe -wallpaper -desktop
```

配置是 `WinXShell.jcfg`（JSON）与 `WinXShell.lua`，没有 XML 配置文件；常见安装位置是
`%ProgramFiles%\WinXShell\`，不是 `System32`。

## PECMD.INI — 标准入口点

`MAIN` 加载配置文件**并**启动 Windows 消息循环，执行完仍会驻留内存：

```wcs
PECMD.EXE MAIN X:\Windows\System32\PECMD.INI
```

典型启动顺序（按实际 PE 调整）：

```wcs
// 1. 启动画面
LOGO %CurDir%\splash.jpg
TEXT 系统正在初始化，请稍候...#0xFFFFFF L20T20 $20

// 2. 运行时初始化（U=等待移动设备就绪）
INIT IU,3000

// 3. 显示/驱动/服务
TEAM DISP W1024H768B32| EXEC !%SystemRoot%\System32\orderdrv.cmd
DEVI %CurDir%\Drivers\*.inf
EXEC !%SystemRoot%\System32\wpeinit.exe

// 4. 外置与快捷方式
LOAD %CurDir%\Tools\Network.ini
LINK %Desktop%\命令提示符,%SystemRoot%\System32\cmd.exe

// 5. 全局热键（PE 中用 HOTK，不是 HKEY）
HOTK Ctrl+Alt+#0x44,EXEC %SystemRoot%\System32\cmd.exe

// 6. Shell 必须最后
SHEL %SystemRoot%\explorer.exe

// 7. 关闭启动画面（脚本结束前）
LOGO
```

`MAIN` 自身驻留，**不需要**在末尾写 `WAIT -1`；`WAIT -1` 会让脚本永久挂起，反而阻止后续逻辑。

## 关键启动命令

### INIT — 初始化 PECMD 运行时

```wcs
INIT [选项列表],[等待时间],[USB起始盘符]
```

`INIT IU,3000`：I=安装托盘菜单功能，U=检测 USB 移动硬盘并分配盘符；`3000` 是**等待设备就绪**的时间，不是超时。
`INIT IU,3000,U:` 表示 USB 盘符从 U: 开始。

`INIT CIK`：C=把 CDROM 盘符写入环境变量，I=托盘菜单，K=安装低级键盘钩子。
> 公开发行的 WinPE 不建议带 `K`（help.txt 原文），低级键盘钩子可能与输入法/安全软件冲突。

### SHEL — 设置 Windows Shell

```wcs
SHEL [-user|-sys] [-shel:"自动命令"] <文件名|命令>[,密码BASE字符串][,重试次数]
```

- `-user` 配合 `MAIN --user`（旧文档写作 `MAIN -user`）；`-sys` 强制系统 Shell
- Shell 被杀时自动重载
- 若使用 `HOTK`/`HIDE`，`SHEL` 必须在其**之后**

```wcs
SHEL %SystemRoot%\explorer.exe
SHEL PECMD.EXE LOAD %CurDir%\MyShell.ini
```

### LOGO / TEXT

```wcs
LOGO %CurDir%\logo.jpg              // BMP/JPG/PNG/GIF
LOGO %CurDir%\splash.jpg,0xFF00FF   // 指定透明色
LOGO                                // 关闭（渐隐）
TEXT 正在初始化...#0x00FF00 L100T200 R600B400 $18:Microsoft YaHei
```

### DEVI — 安装驱动

```wcs
DEVI $%CurDir%\Drivers\NetCard.cab      // CAB 标准安装
DEVI $$%CurDir%\Drivers\NetCard.inf     // INF 标准安装
DEVI %CurDir%\Drivers\*.inf             // 批量 INF
```

### LINK / HOTK

```wcs
LINK %Desktop%\我的工具,%CurDir%\mytool.exe
HOTK #112,PECMD.EXE                     // F1 打开 PECMD 帮助
HOTK Ctrl+Alt+#0x44,EXEC cmd.exe        // PE 全局热键用 HOTK
```

## 常用模式

### 等待可移动驱动器后加载工具

```wcs
_SUB WaitForUSB
    LOOP #1=1,
    {
        FDRV &盘符=*:
        FORX * &盘符,&&drv,
        {
            FORM -raw &type=%&drv%        // 返回字符串名，如 DRIVE_REMOVABLE
            FIND $DRIVE_REMOVABLE=%&type%,
            {
                IFEX %&drv%\PETOOLS\LOAD.INI, TEAM LOAD %&drv%\PETOOLS\LOAD.INI| EXIT _SUB
            }
        }
        WAIT 2000
    }
_END
```

### 自动分配盘符

```wcs
SHOW -1:-1                           // 显示所有隐藏/无盘符分区
DISK ,,,1,U:                         // 按序号整理盘符，U 盘从 U: 起
```

### 设置虚拟内存

```wcs
PAGE C:\pagefile.sys 256 512         // 初始 256MB，最大 512MB
```

### 挂载 WIM 外置

```wcs
MOUN %CurDir%\Tools.wim,%SystemDrive%\Tools,1       // 只读挂载映像 1
MOUN %CurDir%\Tools.wim,%SystemDrive%\Tools,1,*     // 读写（第 4 参 tempDir）
IFEX %SystemDrive%\Tools\Setup.cmd, EXEC =!"%SystemDrive%\Tools\Setup.cmd"
```

### 按标记文件定位启动盘

```wcs
FORX \MyPETools.tag,&&usbDrv,1       // 不要写 @：@ 只搜索目录
IFEX %&usbDrv%\MyPETools.tag, SET &Base=%&usbDrv%
```

## 最小 PECMD.INI

SDK 官方“最精简”示例（GBK，无 `#code`，无 `WAIT -1`）：

```wcs
FBWF P40  L60  H96
INIT I
HOTK #112,PECMD.EXE
SHEL %SystemRoot%\EXPLORER.EXE
```

需要 USB 盘符与托盘时再升级为 `INIT IU,3000`。

## 重要注意事项

1. `MAIN` 自身驻留，不需要 `WAIT -1`；`WAIT -1` 只用于确实要永久挂起脚本的场景。
2. `SHEL` 放在 `INIT` 之后、`HOTK`/`HIDE` 之后。
3. `REGI .` 的 `.` 是“任意类型”，不是离线；离线注册表用 `HIVE 子项,文件`。
4. `%SystemDrive%` 通常是 `X:`（RAM 磁盘）。
5. PE 缺少运行库，优先静态链接工具，并用 `IFEX` 防护。
6. `%CurDir%` 是 PECMD.INI 所在目录，适合相对路径。
7. 调试用 `LOGS * X:\pecmd.log`，不要写到只读介质。
8. 编码声明与文件字节一致：PE 生态默认 `#code=936`；UTF-8 文件用 `#code=65001`。

## PE 环境限制

### 1. 缺少运行时库
未安装 VC++ 运行库和 .NET；使用静态链接工具，或把依赖打包进 PE。

### 2. 只读介质与 RAM 磁盘
`X:\` 是 RAM 磁盘，可写但重启丢失；启动介质本身可能只读。临时文件放 `%TEMP%` 或可写分区。

### 3. 默认无网络
网络适配器/协议栈未初始化。先运行 `wpeinit.exe`、`startnet.cmd` 或 `net start`，**再**用 `PCIP` 配置地址；
`PCIP` 本身不加载网卡驱动。WiFi 用 `ADSL-wlan`，PPPoE 用 `ADSL`。

### 4. 注册表在 RAM 中
SYSTEM/SOFTWARE 通过 FBWF 写时复制，**可写**，但重启后更改丢失；不是只读叠加层。
持久修改用离线 `HIVE`，或写入外置配置文件。

### 5. SYSTEM 账户
无传统用户配置文件，默认无 HKCU。需要时设置 `ENVI $USERPROFILE=X:\Users\Default` 并创建目录。

### 6. 缺少驱动
基础镜像可能不含存储/网卡/芯片组驱动；启动介质所需驱动必须提前注入 WIM。

### 7. 盘符不确定
用标记文件定位：`FORX \MyPETools.tag,&&usbDrv,1`（`@` 只搜目录，不能用于文件标记）。

### 8. 需要可写 USERPROFILE
Explorer 和部分 API 需要有效 `%USERPROFILE%`；在 `INIT`/`SHEL` 前设置并创建目录。

## PE 版本差异

| 特性 | WinPE 3.x | WinPE 5.x | WinPE 10.x |
|------|-----------|-----------|------------|
| 内核 | NT 6.1 | NT 6.3 | NT 10.0 |
| WIM 挂载 | wimgapi.dll | wimgapi + 可选 wimmount.sys | wimmount.sys（默认） |
| DPI 缩放 | 无 | 基础（`-scale`） | 完整（`-scale[:DPI]`、`-scalef`） |
| USB 3.0 | 需驱动注入 | 原生 | 原生 |
| NVMe | 不支持 | 有限 | 原生 |
| UEFI Secure Boot | 不可靠 | 可用 | 完全支持 |
| exFAT 启动 | 否 | 否 | 是 |

### 版本备注

- WinPE 3.x：`INIT U` 对 USB 很关键；现代存储驱动常需 `DEVI` 注入。
- WinPE 5.x：DISM 更快，原生 USB 3.0；`PART -super -up` 可改 GPT 分区类型。
- WinPE 10.x：NVMe/exFAT 原生，`INIT` 自动识别多数硬件；WiFi 可用 `ADSL-wlan` 或 `netsh wlan`。
