# 🦐 macOS Desktop Control

> macOS 原生桌面控制工具 - 截屏、进程管理、系统信息、剪贴板、应用控制

**版本**: 1.0.0  
**平台**: macOS only  
**作者**: 张长沙

---

## ⚡ 快速开始

### 安装
```bash
cd skills/macos-desktop-control
bash scripts/install.sh
```

### 基础使用
```bash
# 截屏
bash scripts/screenshot.sh

# 进程列表
bash scripts/processes.sh

# 系统信息
bash scripts/system_info.sh

# 剪贴板
bash scripts/clipboard.sh get
bash scripts/clipboard.sh set "文字"
```

---

## 📋 功能清单

### ✅ 无需依赖（核心功能）

| 功能 | 脚本 | 说明 |
|------|------|------|
| 📸 截屏 | `screenshot.sh` | 全屏/选择区域/窗口截图 |
| 📋 进程管理 | `processes.sh` | 进程列表/搜索/CPU 占用 |
| 💻 系统信息 | `system_info.sh` | 硬件/软件/磁盘/内存/网络/电池 |
| 📋 剪贴板 | `clipboard.sh` | 读取/写入/复制文件 |
| 🖥️ 应用控制 | `app_control.sh` | 打开/关闭/切换应用 |
| 🪟 窗口管理 | `window_manager.sh` | 窗口列表/关闭/最小化/最大化/移动/调整大小 |
| 🤖 自动化工作流 | `automation_workflows.sh` | 晨会/专注/清理/演示/诊断/批量截图 |

### ⭐ 需要 pyautogui（进阶功能）

| 功能 | 脚本 | 说明 |
|------|------|------|
| 🖱️ 鼠标控制 | `desktop_ctrl.py` | 位置/点击/移动/滚动 |
| ⌨️ 键盘控制 | `desktop_ctrl.py` | 输入/按键/快捷键 |
| 📸 Python 截屏 | `desktop_ctrl.py` | 程序化截图 |

---

## 🔐 权限配置

首次使用需要配置权限：

```bash
bash scripts/check_permissions.sh
```

或手动打开：
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

## 📖 文档

- **SKILL.md** - 技能说明文档
- **examples/basic_usage.md** - 使用示例
- **references/permissions_guide.md** - 权限配置指南
- **references/troubleshooting.md** - 故障排除

---

## 🛠️ 安装依赖

### 基础功能（无需额外依赖）
系统自带工具：screencapture, ps, osascript, pbcopy, pbpaste

### 进阶功能（可选）
```bash
pip3 install --user pyautogui pyscreeze pillow psutil
```

---

## 🎯 使用场景

### 场景 1: 远程协助
```bash
# 截屏分享
bash scripts/screenshot.sh -d 3

# 查看对方运行的应用
bash scripts/processes.sh -g
```

### 场景 2: 自动化测试
```bash
# 鼠标点击测试
python3 scripts/desktop_ctrl.py mouse click 100 100

# 键盘输入测试
python3 scripts/desktop_ctrl.py keyboard type "Test"
```

### 场景 3: 系统监控
```bash
# 查看 CPU 占用
bash scripts/processes.sh -t 10

# 系统信息报告
bash scripts/system_info.sh -a
```

### 场景 4: 批量操作
```bash
# 打开多个应用
bash scripts/app_control.sh open Safari
bash scripts/app_control.sh open "Google Chrome"
bash scripts/app_control.sh open "Visual Studio Code"
```

---

## ⚠️ 安全说明

1. **截屏隐私**: 截屏默认保存到 `~/Desktop/OpenClaw-Screenshots`
2. **键盘记录**: 本技能不会记录键盘输入，仅模拟输入
3. **权限最小化**: 仅申请必要的权限
4. **危险操作**: 结束进程等危险操作需要确认

---

## 🐛 常见问题

### Q: 截屏失败？
检查屏幕录制权限：
```bash
bash scripts/check_permissions.sh
```

### Q: 无法控制应用？
检查自动化权限：
```bash
bash scripts/check_permissions.sh
```

### Q: pyautogui 导入失败？
安装依赖：
```bash
pip3 install --user pyautogui pyscreeze pillow psutil
```

---

## 📚 相关资源

- [AppleScript 官方文档](https://developer.apple.com/library/archive/documentation/AppleScript/Conceptual/AppleScriptLangGuide/)
- [pyautogui 文档](https://pyautogui.readthedocs.io/)
- [macOS 隐私权限](https://support.apple.com/guide/mac-help/privacy-and-security-mh15209/mac)

---

## 📝 更新日志

### v1.0.0 (2026-03-31)
- ✅ 初始版本发布
- ✅ 基础功能：截屏、进程、系统信息、剪贴板
- ✅ 应用控制：AppleScript 集成
- ✅ 权限检测脚本
- ✅ 完整文档

---

**许可证**: MIT  
**问题反馈**: 提交到 OpenClaw 工作区
