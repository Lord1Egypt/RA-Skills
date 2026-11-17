# Chinese / non-ASCII encoding: the five-layer defense

中文编码坑的标准防线。每条规则都来自真实事故，不是理论。核心原则：

> **任何一层默认编码都不可信。每个边界显式声明 UTF-8，并用真实
> Windows CI 验收——本机 macOS/Linux 全绿不算数。**

## 五层防线（按数据流方向）

### 1. Python 入口自身

```python
def main(argv=None):
    for stream in (sys.stdout, sys.stderr):
        # StringIO/embedding hosts may not expose reconfigure()
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="strict")
```

- `errors="strict"`：坏编码要炸出来，不许 `replace` 静默吞掉。
  只有面向用户展示层才允许 `replace`（见 PowerShell 章姊妹节）。
- 入口脚本在 docstring 后立即执行；**库模块绝不碰全局流**。

### 2. Python 子进程

```python
child_env = dict(env, PYTHONIOENCODING="utf-8", VSLANG="1033")
subprocess.run(command, env=child_env, check=True)
```

- `PYTHONIOENCODING=utf-8`：Python 孙进程与重定向日志同协议
- `VSLANG=1033`：MSVC 诊断强制英文，避免本地化 legacy code page 解码歧义
- **native 子进程输出保持原字节**（不 decode、不 `errors=replace`）
- Windows 控制台：命令生命周期内 `SetConsoleOutputCP(65001)`，
  **失败也恢复**原 code page（try/finally）：

```python
@contextmanager
def utf8_console():
    if os.name != "nt":
        yield
        return
    kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
    previous = kernel32.GetConsoleOutputCP()
    active = bool(previous)
    if active:
        kernel32.SetConsoleOutputCP(65001)
    try:
        yield
    finally:
        if active:
            kernel32.SetConsoleOutputCP(previous)
```

### 3. Python 文件 IO（最高频事故点）

```python
# 错。write_text 不带 encoding 用 locale 默认编码：
# Windows runner 是 cp1252，中文内容直接 UnicodeEncodeError
path.write_text('中文内容')

# 对。任何非 ASCII 内容必须显式：
path.write_text('中文内容', encoding='utf-8')
path.read_text(encoding='utf-8')
```

- 路径名非 ASCII 不炸（文件系统层）；**内容**非 ASCII 才炸
- macOS 本地全绿（默认 UTF-8 locale）**完全掩盖**此坑，
  只有 Windows CI 才暴露——写完非 ASCII IO 必须推 CI 验证
- git 子进程输出：`capture_output=True` 拿 bytes + `os.fsdecode`，
  `git ls-files -z` 必须按 bytes 的 `b'\0'` 分割

### 4. CMake

```cmake
execute_process(COMMAND ... RESULT_VARIABLE r OUTPUT_VARIABLE o
                 ERROR_VARIABLE e ENCODING UTF-8)
```

- `execute_process` **不显式 `ENCODING UTF-8`** 时，Windows 上按
  活动代码页（GBK）解码子进程输出 → 中文测试名乱码/丢字节
- 经典事故：doctest 2.5.3 `doctestAddTests.cmake` 两处
  execute_process（测试名发现 + suite 标签发现），修复是给两处都加
  `ENCODING UTF-8`
- CMake 只在 Windows 应用 ENCODING；跨平台工具输出 UTF-8 时
  所有平台都要能消费
- 多配置生成器（Visual Studio）把可执行文件放 `bin/<CONFIG>/`，
  单配置放 `bin/`——运行时库（DLL）staging 目标目录要用
  `if(CMAKE_CONFIGURATION_TYPES) ... $<CONFIG>` 区分，否则
  POST_BUILD 自检/发现进程起不来
- `file(READ)` 文本文件注意编码假设；`file(WRITE)` 默认按字节写

### 5. MSVC 编译器

- `/utf-8` 同时设源码字符集和执行字符集——**只影响 MSVC 自身**，
  不保证任何工具（cmake/python/git）输出是 UTF-8
- 代码里出现中文注释/字符串字面量：源文件存 UTF-8（无 BOM）+
  `/utf-8` flag；否则 MSVC 按 GBK 读 UTF-8 源文件
- MSVC 的英文诊断靠 `VSLANG=1033`（见第 2 层）

## 验收标准（写完必做，缺一不可）

1. **真实 Windows CI**（MSVC 或 MinGW）跑过含中文内容的路径
2. **中文路径 + 中文文件内容**的失败诊断：故意用中文文件名触发
   错误，验证报错信息里中文可读（不是问号/乱码）
3. **重定向日志**：`PYTHONIOENCODING=cp1252` 的父进程下运行入口，
   输出到文件的中文不炸不乱
4. **doctest/CTest 发现 roundtrip**：用真实上游 discovery 模块 +
   中文测试名 + 中文 suite 标签，生成的 CTest 用例名逐字相等。
   不能只看终端显示正常（终端 code page 会伪装成功）
5. 断言内部调用次数（如 CMake execute_process 次数）不可靠
   （随版本策略变化），断言**每个被抓到的调用都带 ENCODING UTF-8**
   + 最终 roundtrip 效果

## 已知误区

| 误区 | 事实 |
|---|---|
| "我本机跑通了" | macOS/Linux 默认 UTF-8 locale 掩盖一切，Windows 才是考场 |
| "加了 /utf-8 就安全了" | 只管 MSVC 编译器，不管 cmake/python/git 输出 |
| "errors='replace' 兜底" | 静默吞坏字节，把事故变成更晚更难的排查 |
| "控制台显示正常" | code page 伪装；必须验文件字节和 CTest 生成物 |
| "PATH 有 msys64 = MinGW 污染" | 目录子串≠工具链污染；比较真实工具目录（ucrt64/bin vs usr/bin） |
| "MSYS2 == MinGW" | 反了：MinGW 是 MSYS2 发行版里的子环境；usr/ 是 POSIX 层产物不能发布 |

## 事故模式档案（匿名化，可直接对照）

1. **doctest 中文测试名乱码**：CMake discovery 的两处
   `execute_process` 缺 `ENCODING UTF-8`，Windows 上按 GBK 解码。
   修复 + 用真实上游模块做中文用例名 roundtrip 回归。
2. **`UnicodeEncodeError: 'charmap' codec can't encode '\u975e'`**：
   测试写中文内容 `write_text` 无 encoding（Windows cp1252 炸）。
   macOS 本地全绿，CI 才暴露。
3. **重定向日志中文乱码**：父链路没设 `PYTHONIOENCODING`，
   孙进程输出按 locale 编码进文件。入口 reconfigure 严格模式 +
   子进程环境统一 UTF-8。
4. **多配置生成器下 DLL 与 exe 不同目录**：测试可执行文件在
   `bin/Release/`，运行时库拷到了 `bin/`，构建期测试发现进程
   起不来报 "Error running test executable"。
5. **MinGW 程序缺编译器运行时 DLL**：链接后自检/发现进程启动失败。
   MinGW 构建要把 `libgcc/libstdc++/winpthread` DLL 与产物同目录
   staging（`gcc -print-file-name=<dll>` 定位）。
