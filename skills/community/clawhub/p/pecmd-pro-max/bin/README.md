# 内置 PECMD 解释器

随技能分发的 PECMD2012 **1.88.05.94** 完整版二进制，用于本地语法/行为验证，使示例与文档不依赖外部 SDK 目录。

| 文件 | 架构 | 子系统 | 大小 | 来源（SDK 1.88.05.94） |
|---|---|---|---|---|
| `PECMD32.exe` | x86 (PE32) | GUI | 1,660,928 | `PECMD原始.EXE` |
| `PECMD32-cli.exe` | x86 (PE32) | Console | 1,660,928 | `PECMD原始_cli.EXE` |
| `PECMD64.exe` | x64 (PE32+) | GUI | 1,243,648 | `X64/PECMD.EXE` |
| `PECMD64-cli.exe` | x64 (PE32+) | Console | 2,017,792 | `X64/PECMD原始_cli.EXE` |

- 文件版本：`201201.88.05.94`；产品版本：`201201.88.05.94`。
- 完整性：`SHA256SUMS.txt`（`sha256sum -c SHA256SUMS.txt`）。
- 许可：PECMD2012 为 NonCopyRight，可自由使用与分发（见官方帮助 `help.txt` 前言）。
- 本仓库未执行这些二进制；仅校验了 PE 架构、版本资源与哈希。

## 用法

```bat
REM 加载脚本（窗口程序，脚本内 CALL @ 才创建窗口）
bin\PECMD64.exe LOAD examples\gui\tabl-table.wcs

REM WinPE 入口（执行 INI 并进入消息循环）
bin\PECMD64.exe MAIN X:\Windows\System32\PECMD.INI

REM 需要 stdin/stdout 时用 CLI 变体（脚本内容为 READ -,line,&v 与 WRIT -,$+0,%&v%）
bin\PECMD64-cli.exe LOAD test.wcs
```

选择建议：

- 32 位 WinPE 用 `PECMD32.exe`；64 位 WinPE 用 `PECMD64.exe`。
- 调试管道/控制台输出用 `*-cli.exe`（Console 子系统）；GUI 子系统版本没有标准输出。
- `PECMD64.exe` 为官方打包版；x86 完整版 SDK 只提供未打包的 `PECMD原始.EXE`，故 `PECMD32.exe` 体积较大，属正常。
