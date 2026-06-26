---
name: "openclaw-android"
description: "通过openclaw控制android手机，所有命令在手机内部执行，先su切换到root权限后执行后续命令，支持获取安装软件列表、打开和关闭app、操作app（点击、滑动、输入文本）以及截图app。当用户需要控制android设备或执行app操作时调用。"
---

# OpenClaw Android 控制器

## 功能说明

本技能通过OpenClaw工具控制Android手机，所有命令通过`shell.sh`脚本执行，脚本会自动处理`su`切换到root权限的操作，并记录执行日志用于调试，利用Android系统自带的命令如`am`、`pm`、`input`和`screencap`等，实现对Android设备的各种操作，包括：
- 获取安装软件列表（系统应用和第三方应用）
- 打开和关闭app
- 操作app（点击、滑动、输入文本、按键操作）
- 截图app

## 适用场景

- 自动化测试Android应用
- 远程控制Android设备
- 批量执行Android设备操作
- 监控Android设备状态
- 管理已安装的应用
- 对应用进行操作和截图

## 核心命令

### 1. 应用管理

#### 启动应用
```bash
# 启动指定包名的应用
sh "$(dirname "$0")/shell.sh" start com.example.app/.MainActivity

# 启动应用并传递参数
sh "$(dirname "$0")/shell.sh" start com.example.app/.MainActivity --es key value
```

#### 停止应用
```bash
# 停止指定包名的应用
sh "$(dirname "$0")/shell.sh" stop com.example.app
```

#### 清除应用数据
```bash
# 清除应用数据
sh "$(dirname "$0")/shell.sh" clear com.example.app
```

### 2. 包管理

#### 安装应用
```bash
# 安装APK文件（假设APK已在设备上）
sh "$(dirname "$0")/shell.sh" install /data/local/tmp/app.apk
```

#### 卸载应用
```bash
# 卸载应用
sh "$(dirname "$0")/shell.sh" uninstall com.example.app
```

#### 列出已安装应用
```bash
# 列出所有已安装应用
sh "$(dirname "$0")/shell.sh" list-packages

# 列出系统应用
sh "$(dirname "$0")/shell.sh" list-system

# 列出第三方应用
sh "$(dirname "$0")/shell.sh" list-third-party
```

### 3. 模拟输入

#### 点击屏幕
```bash
# 在指定坐标点击屏幕
sh "$(dirname "$0")/shell.sh" tap x y
```

#### 滑动屏幕
```bash
# 从(x1,y1)滑动到(x2,y2)
sh "$(dirname "$0")/shell.sh" swipe x1 y1 x2 y2

# 带延迟的滑动（毫秒）
sh "$(dirname "$0")/shell.sh" swipe x1 y1 x2 y2 duration
```

#### 输入文本
```bash
# 输入文本
sh "$(dirname "$0")/shell.sh" text "Hello World"
```

#### 按键操作
```bash
# 按下返回键
sh "$(dirname "$0")/shell.sh" keyevent 4

# 按下Home键
sh "$(dirname "$0")/shell.sh" keyevent 3

# 按下菜单键
sh "$(dirname "$0")/shell.sh" keyevent 82
```

### 4. 屏幕截图

#### 截取屏幕
```bash
# 截取屏幕并保存到指定路径
sh "$(dirname "$0")/shell.sh" screenshot /sdcard/screenshot.png

# 截取屏幕到默认路径
sh "$(dirname "$0")/shell.sh" screenshot
```

### 5. 文件操作

#### 查看文件列表
```bash
# 查看指定目录文件
sh "$(dirname "$0")/shell.sh" ls /sdcard/

# 查看当前目录
sh "$(dirname "$0")/shell.sh" ls
```

## 示例使用场景

### 场景1: 启动应用并点击按钮
```bash
# 启动应用
sh "$(dirname "$0")/shell.sh" start com.example.app/.MainActivity

# 等待应用加载
sleep 2

# 点击登录按钮（假设坐标为500,1000）
sh "$(dirname "$0")/shell.sh" tap 500 1000

# 输入用户名
sh "$(dirname "$0")/shell.sh" text "username"

# 点击密码输入框
sh "$(dirname "$0")/shell.sh" tap 500 1200

# 输入密码
sh "$(dirname "$0")/shell.sh" text "password"

# 点击登录按钮
sh "$(dirname "$0")/shell.sh" tap 500 1400
```

### 场景2: 截图
```bash
# 截取屏幕
sh "$(dirname "$0")/shell.sh" screenshot /sdcard/screenshot.png
```

### 场景3: 安装和测试应用
```bash
# 安装应用（假设APK已在设备上）
sh "$(dirname "$0")/shell.sh" install /data/local/tmp/app-debug.apk

# 启动应用
sh "$(dirname "$0")/shell.sh" start com.example.app/.MainActivity

# 执行测试操作...

# 卸载应用
sh "$(dirname "$0")/shell.sh" uninstall com.example.app
```

## 注意事项

1. 所有命令都在Android手机内部执行，不需要ADB连接
2. 所有命令通过`shell.sh`脚本执行，脚本会自动处理root权限切换
3. 坐标操作需要根据设备屏幕分辨率进行调整
4. 执行复杂操作时，建议添加适当的延迟以确保操作完成
5. 大批量操作可能会触发设备的安全机制，请注意操作频率
6. 每次执行命令都会在`/sdcard/`目录下生成日志文件，用于调试

## 故障排除

- **权限不足**: 确保设备已root，且su命令可用
- **命令失败**: 检查命令语法是否正确，确保包名和路径无误
- **截图失败**: 确保存储权限已授予，尝试使用不同的存储路径
- **应用启动失败**: 检查应用包名和Activity名称是否正确