---
name: platform-pitfalls
slug: platform-pitfalls
version: 1.0.0
author: dqsjqian
display_name: 平台疑难杂症速查手册
display_name_en: Platform Pitfalls Playbook
description: >
  Cross-platform engineering pitfalls playbook: Chinese/non-ASCII encoding
  defense (Python entrypoints, child processes, file IO, CMake
  execute_process ENCODING, MSVC /utf-8 vs VSLANG, Windows console code
  pages, doctest/CTest discovery), PowerShell 5.1 mojibake three-layer fix
  (UTF-8 BOM + chcp + byte arrays), and 11 C++20 coroutine pitfalls (lambda
  captures, catch co_await, mutex resume, handle lifetimes,
  container-overflow spans). Load when authoring or debugging cross-platform
  build tooling, CI, installers or async C++ — especially anything that must
  run on Chinese Windows (cp936/GBK) or Windows runners (cp1252). Triggers:
  中文乱码, mojibake, UnicodeEncodeError charmap, doctest CTest Chinese test
  names, PYTHONIOENCODING, VSLANG, code page 936, 璇峰鎻朵, coroutine UAF,
  ASan container-overflow.
description_zh: >
  跨平台工程疑难杂症速查：中文编码五层防线（Python 入口/子进程/文件 IO/CMake
  ENCODING/MSVC）、PowerShell 5.1 中文乱码三层修复（UTF-8 BOM + chcp +
  字节数组）、C++20 协程 11 个高频坑（lambda 捕获、catch co_await、mutex
  resume、handle 生命周期、span container-overflow）。写跨平台构建工具、
  CI、安装器或异步 C++ 时加载，尤其是要在中文 Windows（cp936/GBK）或
  Windows runner（cp1252）上运行的东西。
description_en: >
  Cross-platform pitfalls playbook: a five-layer Chinese/non-ASCII encoding
  defense, the PowerShell 5.1 mojibake three-layer fix, and 11 C++20
  coroutine pitfalls. Load when authoring cross-platform build tooling, CI,
  installers or async C++.
---

# Platform Pitfalls Playbook

疑难杂症不是玄学：每一条都是「本机全绿、目标平台爆炸」的事故换来的。
本手册把三类高频平台坑收敛成可执行的防御清单。

## When to use

遇到以下任一情况，读对应章节（`references/` 下）：

| 症状 | 读哪章 |
|---|---|
| Windows 上中文变 `璇峰•鎻•朵` / `UnicodeEncodeError: 'charmap'/'gbk' codec` | @references/chinese-utf8-pipeline.md |
| 跨平台脚本/构建工具要处理中文路径、中文测试名、重定向日志 | @references/chinese-utf8-pipeline.md |
| `.ps1` 脚本在中文 Windows PowerShell 5.1 上乱码 | @references/windows-powershell-utf8.md |
| Python CLI 在 Windows 控制台 print 中文/emoji 炸 | @references/windows-powershell-utf8.md |
| C++20 协程 `-O3` 悬空、mutex 内 resume 崩、ASan container-overflow | @references/cpp20-coroutines.md |

## 核心原则（全章通用）

1. **任何一层默认编码都不可信**。每个边界显式声明 UTF-8。
2. **本机 macOS/Linux 全绿不算数**——默认 UTF-8 locale 掩盖一切，
   中文 Windows 和 Windows runner 才是考场。
3. **写完必须推真实 Windows CI 验收**，含中文路径、中文内容、
   重定向日志与失败诊断的可读性。
4. **不静默吞错**。`errors='replace'`、空 `except`、降级跳过都是把
   事故变成更晚更难的排查。

## 沉淀新坑（本手册的维护方式）

踩到新平台坑并修复后，按「症状 → 原因 → 解法 → 验收命令」四段式追加进
对应章节；开新章节的标准：同类坑第二次出现、或独立成一个技术域。
不要记「某次会话里 AI 说了什么」，记可复现的工程事实。

## 章节索引

- `references/chinese-utf8-pipeline.md` — 中文编码五层防线
  （Python 入口 / 子进程 / 文件 IO / CMake / MSVC + 控制台）+ 验收
  标准 + 常见误区（含 MSYS2/MinGW 关系澄清）
- `references/windows-powershell-utf8.md` — PowerShell 5.1 三层修复
  （UTF-8 BOM + chcp 65001 + 关键字符串字节数组）+ Python 控制台姊妹问题
- `references/cpp20-coroutines.md` — C++20 协程 11 坑速查
  （症状→原因→解法）+ TaskScope/事件循环/TLS 异步集成验收补充
