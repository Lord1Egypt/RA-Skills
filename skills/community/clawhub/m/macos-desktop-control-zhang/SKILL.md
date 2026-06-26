---
name: macos-desktop-control
description: macOS 桌面控制工具。截屏、进程管理、系统信息、剪贴板、应用控制。macOS desktop control via native tools (screencapture, ps, AppleScript). 仅支持 macOS。
version: 1.5.3
author: 张长沙
platform: macOS only
metadata:
  requires:
    bins:
      - screencapture
      - ps
      - osascript
    permissions:
      - Accessibility
      - AppleEvents
      - ScreenCapture
---

# macOS Desktop Control

macOS 原生桌面控制工具，无需额外依赖即可使用核心功能。

## 🚀 快速开始

### 基础命令（无需依赖）

```bash
# 截屏
bash scripts/screenshot.sh

# 进程列表
bash scripts/processes.sh

# 系统信息
bash scripts/system_info.sh

# 剪贴板读取
bash scripts/clipboard.sh get

# 剪贴板写入
bash scripts/clipboard.sh set "要复制的文字"
```

### 进阶命令（需要 pyautogui）✅

```bash
# 安装依赖
pip3 install --user --break-system-packages pyautogui pyscreeze pillow psutil

# 鼠标位置
python3 scripts/desktop_ctrl.py mouse position

# 鼠标移动
python3 scripts/desktop_ctrl.py mouse move 500 300

# 鼠标点击
python3 scripts/desktop_ctrl.py mouse click 500 300

# 键盘输入
python3 scripts/desktop_ctrl.py keyboard type "Hello"

# 快捷键（Cmd+C）
python3 scripts/desktop_ctrl.py keyboard hotkey command c
```

**⚠️ 重要**: 需要授予辅助功能权限！
```bash
bash scripts/check_permissions.sh
```

---

## 📋 命令速查

| 命令 | 功能 | 依赖 | 权限 |
|------|------|------|------|
| `screenshot` | 截屏 | 无 | 屏幕录制 |
| `processes` | 进程列表 | 无 | 无 |
| `info` | 系统信息 | 无 | 无 |
| `clipboard get` | 读取剪贴板 | 无 | 无 |
| `clipboard set` | 写入剪贴板 | 无 | 无 |
| `app open` | 打开应用 | 无 | 自动化 |
| `app close` | 关闭应用 | 无 | 自动化 |
| `app front` | 前端应用 | 无 | 自动化 |
| `mouse position` | 鼠标位置 | pyautogui | 辅助功能 |
| `mouse click` | 鼠标点击 | pyautogui | 辅助功能 |
| `keyboard type` | 键盘输入 | pyautogui | 辅助功能 |

---

## 🔐 权限配置

### 首次使用必须配置

运行权限检测脚本：
```bash
bash scripts/check_permissions.sh
```

或手动打开设置：
```bash
# 辅助功能（鼠标键盘控制）
open "x-apple.systempreferences:com.apple.preference.security?Privacy_Accessibility"

# 自动化（应用控制）
open "x-apple.systempreferences:com.apple.preference.security?Privacy_Automation"

# 屏幕录制（截屏）
open "x-apple.systempreferences:com.apple.preference.security?Privacy_ScreenCapture"
```

**⚠️ 重要**: 授权后需要重启终端应用！

---

## 📖 使用示例

### 示例 1: 截屏
```
用户：帮我截个屏
小龙虾：✅ 已截取屏幕，保存到 ~/Desktop/screenshot_20260331_213700.png
```

### 示例 2: 查看进程
```
用户：看看现在运行着哪些应用
小龙虾：
当前运行的主要进程：
- Safari (PID: 1234)
- VS Code (PID: 2345)
- Terminal (PID: 3456)
- QQ (PID: 4567)
```

### 示例 3: 关闭应用
```
用户：把 Safari 关了
小龙虾：✅ 已关闭 Safari 应用
```

### 示例 4: 系统信息
```
用户：看看我的电脑配置
小龙虾：
📊 系统信息
- 型号：MacBook Air (M2, 2023)
- 系统：macOS 15.3.1
- 内存：16 GB
- 存储：512 GB SSD
```

### 示例 5: 剪贴板操作
```
用户：复制这段文字到剪贴板
小龙虾：✅ 已将文字复制到剪贴板
```

---

## 🛠️ 安装

### 一键安装
```bash
cd skills/macos-desktop-control
bash scripts/install.sh
```

### 手动安装
```bash
# 1. 设置脚本权限
chmod +x scripts/*.sh

# 2. 检查权限
bash scripts/check_permissions.sh

# 3. 安装 Python 依赖（可选，用于鼠标键盘控制）
pip3 install --user --break-system-packages pyautogui pyscreeze pillow psutil
```

---

## 🔖 命令别名（快捷方式）

| 完整命令 | 快捷方式 | 说明 |
|----------|---------|------|
| `bash scripts/screenshot.sh` | `mdc shot` | 截屏 |
| `bash scripts/processes.sh -g` | `mdc ps` | 进程列表 |
| `bash scripts/system_info.sh --short` | `mdc info` | 系统信息 |
| `bash scripts/app_control.sh front` | `mdc front` | 前端应用 |
| `python3 scripts/desktop_ctrl.py mouse position` | `mdc mouse` | 鼠标位置 |

**设置别名**（添加到 ~/.zshrc）:
```bash
echo 'alias mdc="cd ~/.openclaw/workspace/skills/macos-desktop-control && bash"' >> ~/.zshrc
source ~/.zshrc
```

---

## 🐛 故障排除

### 问题 1: 权限未授予
```bash
bash scripts/check_permissions.sh
```

### 问题 2: 脚本无执行权限
```bash
chmod +x scripts/*.sh
```

### 问题 3: pyautogui 导入失败
```bash
pip3 install --user pyautogui pyscreeze pillow psutil
```

### 问题 4: 截屏为空白
检查屏幕录制权限：
```bash
open "x-apple.systempreferences:com.apple.preference.security?Privacy_ScreenCapture"
```

---

## 📚 相关文档

- `references/permissions_guide.md` - 权限配置指南
- `references/applescript_cheatsheet.md` - AppleScript 速查表
- `references/troubleshooting.md` - 故障排除
- `examples/basic_usage.md` - 基础使用示例

---

## ⚠️ 安全说明

1. **截屏隐私**: 截屏默认保存到用户目录，请注意不要泄露敏感信息
2. **键盘记录**: 本技能不会记录键盘输入，仅模拟输入
3. **权限最小化**: 仅申请必要的权限
4. **危险操作**: 结束进程等危险操作需要确认

---

**版本**: 1.0.0  
**最后更新**: 2026-03-31  
**平台**: macOS only
