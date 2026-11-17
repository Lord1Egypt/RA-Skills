# Platform Pitfalls Playbook

跨平台工程疑难杂症速查手册——每一条都是「本机全绿、目标平台爆炸」的事故换来的。

## 内容

| 章节 | 覆盖 |
|---|---|
| [中文编码五层防线](references/chinese-utf8-pipeline.md) | Python 入口 / 子进程 / 文件 IO / CMake `ENCODING` / MSVC `/utf-8` vs `VSLANG` / Windows 控制台 code page + 验收标准 |
| [PowerShell 5.1 三层修复](references/windows-powershell-utf8.md) | UTF-8 BOM + `chcp 65001` + 关键字符串字节数组；Python 控制台姊妹问题 |
| [C++20 协程 11 坑](references/cpp20-coroutines.md) | lambda 捕获、catch `co_await`、mutex resume、handle 生命周期、span container-overflow、TaskScope/事件循环/TLS 验收 |

## 核心原则

1. 任何一层默认编码都不可信，每个边界显式声明 UTF-8
2. 本机 macOS/Linux 全绿不算数——中文 Windows（cp936）和 Windows runner（cp1252）才是考场
3. 写完必须推真实 Windows CI 验收
4. 不静默吞错（`errors='replace'`、空 `except`、降级跳过都是把事故推迟）

## 使用

安装为 AI 助手的 skill（SKILL.md 是入口），或直接读 `references/` 下的章节。

## License

MIT
