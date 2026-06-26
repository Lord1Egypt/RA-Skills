# macOS GUI Automation

## ⚠️ 首次使用需要授权

### 1. 辅助功能权限

```bash
# 打开系统设置
open "x-apple.systempreferences:com.apple.preference.security?Privacy_Accessibility"
```

在 **系统设置 → 隐私与安全性 → 辅助功能** 中添加：
- Terminal / iTerm
- 你用来运行 OpenClaw 的终端应用

### 2. 屏幕录制权限（截图需要）

```bash
open "x-apple.systempreferences:com.apple.preference.security?Privacy_ScreenCapture"
```

## 快速测试

```bash
# 测试 cliclick（点击屏幕中心）
cliclick c:$(($(osascript -e 'tell app "Finder" to get bounds of window of desktop') | awk '{print ($3+$1)/2}')),$(($(osascript -e 'tell app "Finder" to get bounds of window of desktop') | awk '{print ($4+$2)/2}'))

# 测试截图 + OCR
screencapture /tmp/test.png
tesseract /tmp/test.png stdout
```

## 使用技能

在 OpenClaw 中调用：

```
使用 gui-automation 技能点击坐标 500,300
读取当前屏幕上的文字
在输入框中输入"hello world"
```

## 脚本位置

- 技能目录：`~/.openclaw/skills/macos-gui-automation/`
- 辅助脚本：`~/.openclaw/skills/macos-gui-automation/scripts/gui-automation.sh`

## 常用命令

```bash
# 点击
cliclick c:500,300

# 双击
cliclick dc:500,300

# 输入文字
cliclick t:"hello"

# 按回车
cliclick kp:enter

# 截图区域 (x,y,宽，高)
screencapture -R 100,100,800,600 /tmp/screen.png

# OCR 识别
tesseract /tmp/screen.png stdout
```
