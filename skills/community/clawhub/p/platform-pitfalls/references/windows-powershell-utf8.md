# Windows PowerShell 5.1 中文乱码：三层修复

## Why it happens

Windows PowerShell 5.1（大多数 Windows 安装的默认版本）在 `.ps1` 文件
**没有 UTF-8 BOM** 时，用系统 ANSI 代码页解码脚本源文件。中文 Windows
上就是 GBK / CP936——脚本里的中文字面量在**解析阶段**就被错误解码，
你的代码一行都没跑就已经烂了。运行时再设
`[Console]::OutputEncoding = UTF8` 救不回来：内存里的字符串已经损坏。

PowerShell 7+ 默认 UTF-8 解析源文件，没这个问题——但你不能假设用户装了。

## Steps（三层全上，不可省）

### 1. `.ps1` 存成 UTF-8 with BOM

PowerShell 5.1 只有看到文件头 BOM（`EF BB BF`）才按 UTF-8 解析。

跨平台加 BOM（开发机上跑）：

```bash
python3 -c '
p = "install.ps1"
with open(p, "rb") as f: data = f.read()
if not data.startswith(b"\xef\xbb\xbf"):
    with open(p, "r+b") as f:
        f.seek(0)
        f.write(b"\xef\xbb\xbf" + data)
    print("BOM added")
else:
    print("BOM already present")
'
# 验证：
head -c 4 install.ps1 | xxd   # 期望：efbb bf<首字节>
```

Windows 本机方式：

```powershell
$content = Get-Content -Raw install.ps1
[System.IO.File]::WriteAllText("$PWD\install.ps1", $content, (New-Object System.Text.UTF8Encoding $true))
```

`UTF8Encoding $true` 才写 BOM。`Out-File -Encoding utf8` 在 PS 5.1 写
BOM、PS 7+ **不写**——行为不一致，用显式构造器。

### 2. 脚本内尽早设编码 + chcp

放注释头之后：

```powershell
# UTF-8 output (otherwise non-ASCII gets garbled on PS 5.1)
# NOTE: this file is saved as UTF-8 with BOM so PS 5.1 parses literals correctly.
$OutputEncoding              = [System.Text.Encoding]::UTF8
[Console]::OutputEncoding    = [System.Text.Encoding]::UTF8
try { chcp 65001 > $null } catch {}
```

`chcp 65001` 把控制台代码页切到 UTF-8，覆盖终端还在等 ANSI 的场景。
`try/catch` 必须有——legacy `cmd.exe` 控制台上 chcp 可能静默失败。

### 3. 关键字符串从 UTF-8 字节构造

兜底层。如果某一行**必须**显示正确（成功横幅、下一步提示），即使
第 1 层被人重存文件弄丢 BOM 也要活：

```powershell
$utf8 = [System.Text.Encoding]::UTF8
# "请复制以下内容发给你的AI" 的 UTF-8 字节：
$msg = $utf8.GetString([byte[]](0xE8,0xAF,0xB7,0xE5,0xA4,0x8D,0xE5,0x88,0xB6,
                                 0xE4,0xBB,0xA5,0xE4,0xB8,0x8B,0xE5,0x86,0x85,
                                 0xE5,0xAE,0xB9,0xE5,0x8F,0x91,0xE7,0xBB,0x99,
                                 0xE4,0xBD,0xA0,0xE7,0x9A,0x84,0x41,0x49))
Write-Host $msg
```

完全绕过解析器。生成字节数组：

```bash
python3 -c 'import sys; print(",".join(f"0x{b:02X}" for b in "请复制以下内容发给你的AI".encode("utf-8")))'
```

只对用户真正看到的 1-2 行用；整脚本字节数组化不可维护。

## Pitfalls

- **不要因为有第 3 层就跳过第 1 层**。PS 5.1 解析整个脚本（含 CJK
  变量名、中文字符串比较、带正则的注释），没 BOM 照样烂。
- `Set-Content -Encoding UTF8`：PS 5.1 写 BOM，PS 7+ 不写。
- `Out-File` 在 PS 5.1 默认 UTF-16 LE——**永远带** `-Encoding`。
- PowerShell ISE 有自己的 console host，无视 chcp——让用户用
  `powershell.exe` 或 Windows Terminal。
- 脚本自身源码编码（第 1 层）和脚本写其他文件的编码
  （`Set-Content -Encoding UTF8`）是两个独立问题。

## Verification

```powershell
# 1. BOM 在？
Format-Hex -Path .\install.ps1 -Count 4
# 期望: 00000000  EF BB BF <next byte>

# 2. 跑起来肉眼看中文
.\install.ps1
```

仍有乱码时问三件事：Windows 版本、PowerShell 版本
（`$PSVersionTable.PSVersion`）、console host（Windows Terminal /
经典控制台 / ISE）。第 3 层全覆盖；若第 3 层也挂，是字体问题——
推荐 Windows Terminal + Cascadia Code + 系统 CJK fallback。

---

# 姊妹问题：Python 脚本在 Windows 控制台

同一个家族的坑：Python 脚本 `print()` 中文/emoji，`sys.stdout` 默认
活动代码页（中文 Windows cp936、英文 Windows cp1252）——
`UnicodeEncodeError: 'gbk' codec can't encode character...`。

## 修复：入口 reconfigure stdout/stderr

**每个 Python 入口脚本**（`python script.py` 跑的，不是库模块）在
docstring 后、其他 import 前加：

```python
# ── Windows console safety: force UTF-8 on stdout/stderr so Chinese / emoji
#    don't blow up under the default cp936 codec on Windows PowerShell / cmd.
#    No-op on POSIX terminals that are already UTF-8.
import sys as _sys
try:
    _sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    _sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass
```

- `reconfigure` 自 Python 3.7 可用，是最干净的重编码已打开文本流的方式
- 这里 `errors="replace"` 合理：单条怪字符不该崩掉整个 CLI；
  **构建工具链/管线入口用 strict**（见 chinese-utf8-pipeline.md 第 1 层），
  展示型 CLI 用 replace——按失败代价选
- `try/except` 兜 <3.7 和非 tty stdout

## 放哪

- **库/共享模块：不要加**。从库里 reconfigure stdout 是全局副作用。
- **每个 CLI 入口：加**。

## 相关但独立的 Python-on-Windows 坑

- `open()` 在 Windows 默认系统 ANSI——读写 JSON/Markdown/配置**永远显式**
  `encoding="utf-8"`
- `Path.home()` 跨平台安全（Windows 用 USERPROFILE）
- `shutil.move()` 跨盘符退化为 copy+remove，非原子——要原子就先
  staging 到目标盘临时目录
- `os.symlink()` 在 Windows 要开发者模式或管理员——安装器用
  copy/junction 或检测后警告
- `os.listdir()` 的 Unicode 文件名在 Python 3 原生支持
