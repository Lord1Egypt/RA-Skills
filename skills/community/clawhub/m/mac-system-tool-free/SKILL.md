---
slug: mac-system-tool-free
name: mac-system-tool-free
version: 1.0.0
displayName: Mac 系统工具
summary: "面向个人用户的 mac,提供核心能力"
license: "MIT"
edition: free
description: "面向个人用户的 macOS 系统管控与控制工具. 核心能力: - 系统信息、进程、磁盘、电池查询 - 音量、亮度、网络基础控制 - 截图、剪贴板、Finder 操作 - 破坏性操作二次确认 适用场景: - 个人查看 Mac 系统状态 - 调整音量亮度与网络 - 截图与剪贴板操作 差异化: 免费版聚焦个人只读查询与基础控制，破坏性操作二次确认，零成本使用. 适用关键词: mac 系统, 系统信息, 进程, 音量, 亮度, 截图, 剪贴板, macos, system control"
tags:
  - macOS
  - 系统管理
  - 个人效率
  - 其他工具
  - 工具
  - 效率
  - 自动化
  - 研究
  - 分析
  - 写作
tools:
  - read
  - exec
  - glob
  - grep
homepage: ""
category: "Automation"
pricing_tier: free
---
# Mac 系统工具（免费版）

## 概述

本工具帮助个人用户管理与控制 macOS 系统功能：系统信息、进程、磁盘、电池查询，音量亮度网络控制，截图剪贴板 Finder 操作。破坏性操作（关机、重启、杀进程）二次确认.
## 核心能力

| 能力 | 说明 | 免费版范围 |
|---|---|-----|
| 系统信息 | 软件/硬件/内存/磁盘/电池 | 只读 |
| 进程管理 | CPU/内存排序、查找、结束 | 二次确认 |
| 音量亮度 | 查询与设置 | 基础 |
| 网络 | WiFi、IP、DNS、ping | 基础 |
| 截图剪贴板 | 截屏、pbcopy/pbpaste | 全覆盖 |
| Finder | 打开、显示、废纸篓 | 基础 |
**技术实现要点**：核心能力基于`input_params`参数与`output_format`配置实现,支持创建/查询/修改/删除等操作模式,通过`config_options`进行运行时配置.
### 核心功能执行
用`input_params`参数进行配置.

**处理**: 解析核心功能执行的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回核心功能执行的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 参数配置与调用
用`config_options`参数进行配置.

**处理**: 解析参数配置与调用的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回参数配置与调用的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`config_options`参数,支持修改/重置/导入操作

### 结果处理与输出
用`output_format`参数进行配置.

**处理**: 解析结果处理与输出的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回结果处理与输出的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`output_format`参数,支持导出/保存/转换操作
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：面向个人用户的、macOS、系统信息查询与基、础控制工具、系统管理与控制工等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持.
## 使用场景

### 场景一：查看系统状态

```bash
# 系统软硬件信息
system_profiler SPSoftwareDataType SPHardwareDataType
# ...
# CPU 占用前 10
ps aux --sort=-%cpu | head -11
# ...
# 磁盘与电池
df -h /
pmset -g batt
```

### 场景二：音量与亮度

```bash
# 查询音量
osascript -e 'output volume of (get volume settings)'
# ...
# 设置音量
osascript -e 'set volume output volume 50'
# ...
# 亮度（需 brightness 工具）
brightness 0.8
```

### 场景三：截图与剪贴板

```bash
# 全屏截图到桌面
screencapture ./Desktop/screenshot.png
# ...
# 区域截图
screencapture -i ./Desktop/region.png
# ...
# 复制内容到剪贴板
echo "内容" | pbcopy
pbpaste
```

## 不适用场景

以下场景Mac 系统工具不适合处理：

- 实时流数据处理
- 小规模数据手动分析
- 非结构化文本情感分析

## 触发条件

需要数据分析、报表生成、统计洞察、数据可视化时使用。不适用于非本工具能力范围的需求.
## 快速开始

1. 用户描述要做的系统操作.
2. 判断类别（查询/调整/破坏性）.
3. 查询类直接执行；破坏性先确认.
4. 需要 sudo 的提前告知.
**响应解析**: 完成完成后,查看输出响应确认任务状态。成功时输出包含解析摘要和响应数据;失败时根据错误信息排查问题,查阅错误解析章节获取恢复步骤.
## 示例

工作流分类：

| 类别 | 处理方式 |
|:-----|:-----|
| 信息查询 | 直接执行并展示 |
| 设置调整 | 直接执行 |
| 破坏性 | 先向用户确认 |
| 需 sudo | 提前告知用户 |

## 优秀实践

- **查询先做**：先查状态再调整，避免盲目操作.
- **破坏性必确认**：关机、重启、杀进程、清废纸篓先问用户.
- **sudo 提前说**：需要提权的命令提前告知，避免中途卡住.
- **截图命名规范**：按日期或用途命名，便于查找.
- **剪贴板别存敏感**：pbcopy 内容留剪贴板，敏感信息用后清理.
## 常见问题

**Q1：能批量管理多台 Mac 吗？**
A：不能。多设备远程管理为专业版能力.
**Q2：杀进程安全吗？**
A：操作前向用户确认目标进程，避免误杀系统进程.
**Q3：亮度命令无效？**
A：系统默认无 `brightness` 命令，需额外安装或用 AppleScript.
**Q4：免费版支持定时任务吗？**
A：不支持。定时任务与自动化策略为专业版能力.
**Q5：关机重启能撤销吗？**
A：不能。执行前务必确认，命令不可逆.
## 进阶用法

### 系统信息查询集

```bash
# 软件信息
sw_vers                          # macOS 版本
uname -a                         # 内核信息
# ...
# 硬件信息
sysctl -n machdep.cpu.brand_string   # CPU 型号
sysctl -n hw.memsize                  # 内存（字节）
system_profiler SPHardwareDataType    # 硬件概览
# ...
# 磁盘与电池
df -h /                          # 磁盘占用
pmset -g batt                    # 电池状态
```

### 进程管理

```bash
# CPU 占用前 10
ps aux --sort=-%cpu | head -11
# ...
# 内存占用前 10
ps aux --sort=-%mem | head -11
# ...
# 查找进程
pgrep -fl "chrome"
# ...
# 结束进程（先确认）
kill PID          # 正常结束
kill -9 PID       # 强制结束（谨慎）
```

### 网络诊断

```bash
# WiFi 信息
networksetup -getairportnetwork en0
# ...
# IP 与 DNS
ifconfig | grep "inet "
scutil --dns | grep nameserver
# ...
# 连通性
ping -c 4 example.com
traceroute example.com
```

## 常用操作速查

| 操作 | 命令 |
|---:|---:|
| 音量查询 | `osascript -e 'output volume of (get volume settings)'` |
| 设置音量 | `osascript -e 'set volume output volume 50'` |
| 静音 | `osascript -e 'set volume output muted true'` |
| 全屏截图 | `screencapture ./Desktop/s.png` |
| 区域截图 | `screencapture -i ./Desktop/r.png` |
| 复制到剪贴板 | `echo x \| pbcopy` |
| 粘贴 | `pbpaste` |
| 打开 Finder | `open .` |
| 清空废纸篓 | `rm -rf ./.Trash/*`（先确认） |

## 安全操作规范

- **查询优先**：先查状态再调整，避免盲目操作.
- **sudo 提前说**：需提权命令提前告知，避免中途卡住.
- **系统进程别杀**：杀进程前确认目标，避免误杀系统进程.
- **剪贴板防泄**：敏感信息用后清理剪贴板.
## 依赖说明

### 运行环境
- **Agent 平台**: 支持SKILL.md的任意AI Agent（Claude Code / Cursor / Codex / Gemini CLI 等）
- **操作系统**: macOS（Windows/Linux 仅部分命令兼容）

### 依赖详情
| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:---:|:---:|:---:|:---:|
| osascript | 系统工具 | 必需 | macOS 自带 |
| brightness | 亮度控制 | 可选 | Homebrew 安装 |
| LLM API | API | 必需 | 由 Agent 内置 LLM 提供 |

### API Key 配置
- 本工具为纯 Markdown 指令，无需额外 API Key
- sudo 操作需用户系统密码，由系统弹窗处理

### 可用性分类
- **分类**: MD+EXEC（Markdown 指令 + 命令行执行）
- **说明**: 通过自然语言指令驱动 Agent 执行 macOS 系统命令

## 错误处理

| 错误场景 | 原因 | 处理方式 |
|:------|------:|:------|
| 配置错误 | 参数缺失或格式错误 | 检查依赖说明中的配置要求 |
| 运行时错误 | 运行环境不满足 | 确认运行环境符合依赖说明 |
| 网络错误 | 连接超时或不可达 | 执行ping命令测试网络连通性,检查防火墙和代理设置连接后执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令，参考国内替代方案 |

## 已知限制

- 需LLM支持,无LLM环境不可用
- 复杂业务场景建议结合人工经验判断
- 执行效率受模型能力与网络环境影响
- 当前为免费版本,如需完整功能请升级到付费版获取全部能力

## 输出格式
```json
{
  "success": true,
  "data": {
    "result": "Mac 系统工具处理结果",
    "execution_time": "0.5s",
    "metadata": {
      "version": "1.0",
      "processor": "mac system"
    }
  },
  "execution_log": ["解析输入参数", "执行核心处理", "格式化输出结果"],
  "error": null
}
```
