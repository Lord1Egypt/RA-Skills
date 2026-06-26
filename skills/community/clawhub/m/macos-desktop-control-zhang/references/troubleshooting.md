# 故障排除指南

---

## 🔧 常见问题

### 1. 截屏失败

**错误**: `❌ 错误：截屏失败`

**可能原因**:
- 屏幕录制权限未授予
- 输出目录不存在

**解决方案**:
```bash
# 1. 检查权限
bash scripts/check_permissions.sh

# 2. 打开设置
open "x-apple.systempreferences:com.apple.preference.security?Privacy_ScreenCapture"

# 3. 确保输出目录存在
mkdir -p ~/Desktop/OpenClaw-Screenshots
```

---

### 2. 无法控制应用

**错误**: `Application can't be controlled by scripts`

**可能原因**:
- 自动化权限未授予
- 应用不支持 AppleScript

**解决方案**:
```bash
# 1. 检查自动化权限
bash scripts/check_permissions.sh

# 2. 打开设置
open "x-apple.systempreferences:com.apple.preference.security?Privacy_Automation"

# 3. 对于不支持 AppleScript 的应用，使用 open 命令
open -a "应用名"
```

---

### 3. pyautogui 导入失败

**错误**: `ModuleNotFoundError: No module named 'pyautogui'`

**解决方案**:
```bash
# 安装依赖
pip3 install --user pyautogui pyscreeze pillow psutil

# 或使用虚拟环境
python3 -m venv .venv
source .venv/bin/activate
pip install pyautogui pyscreeze pillow psutil
```

---

### 4. 脚本无执行权限

**错误**: `Permission denied`

**解决方案**:
```bash
chmod +x scripts/*.sh
chmod +x scripts/*.py
```

---

### 5. 中文路径问题

**错误**: 路径包含中文时失败

**解决方案**:
```bash
# 设置正确的编码
export LANG=zh_CN.UTF-8
export LC_ALL=zh_CN.UTF-8

# 或在 ~/.zshrc 中添加
echo 'export LANG=zh_CN.UTF-8' >> ~/.zshrc
echo 'export LC_ALL=zh_CN.UTF-8' >> ~/.zshrc
source ~/.zshrc
```

---

### 6. 鼠标控制不精确

**原因**: Retina 屏幕坐标系统

**解决方案**:
```python
# 使用相对移动而非绝对坐标
pyautogui.moveRel(100, 0, duration=0.5)

# 或调整坐标
# Retina 屏幕：逻辑坐标 x2 = 实际像素
```

---

### 7. 中文输入乱码

**原因**: 输入法干扰

**解决方案**:
```python
# 使用剪贴板方式输入中文
import subprocess
subprocess.run(['pbcopy'], input="中文文字".encode('utf-8'))
pyautogui.hotkey('command', 'v')
```

---

### 8. 安全模式触发

**错误**: `PyAutoGUI fail-safe triggered`

**原因**: 鼠标移到屏幕角落

**解决方案**:
```python
# 方案 1: 禁用安全模式（谨慎）
pyautogui.FAILSAFE = False

# 方案 2: 告知用户
print("⚠️  安全模式已启用：鼠标移到角落可紧急停止")
```

---

## 🛠️ 调试技巧

### 启用详细输出

```bash
# 在脚本开头添加
set -x  # 显示执行的命令
```

### 检查 Python 路径

```python
import sys
print(f"Python 路径：{sys.executable}")
print(f"Python 版本：{sys.version}")
print(f"已安装包：{sys.path}")
```

### 检查权限状态

```bash
# 列出所有权限
tccutil list

# 检查特定权限
tccutil list Accessibility
tccutil list AppleEvents
tccutil list ScreenCapture
```

---

## 📞 获取帮助

如果以上方法都无法解决问题：

1. 查看 SKILL.md 文档
2. 检查权限配置指南
3. 运行权限检测脚本
4. 查看错误日志

---

**最后更新**: 2026-03-31
