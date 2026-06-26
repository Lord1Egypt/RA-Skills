---
name: browser-extension-clicker
description: |
  自动点击浏览器扩展图标（如 OpenClaw Browser Relay）。
  使用系统级 GUI 自动化，绕过浏览器安全限制。
  当需要操作浏览器工具栏、扩展图标、系统菜单时使用。
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - python3
        - pip
    emoji: "🖱️"
    install:
      - id: python
        kind: python
        packages:
          - pyautogui
          - Pillow
        label: "安装 GUI 自动化依赖"
---

# 浏览器扩展自动点击技能

使用系统级 GUI 自动化点击浏览器扩展图标。

## 使用场景

- 自动点击 OpenClaw Browser Relay 插件图标
- 自动点击其他浏览器扩展图标
- 自动操作浏览器工具栏菜单

## 命令

```bash
# 点击 OpenClaw 插件图标（默认位置）
python click_extension.py --extension openclaw

# 指定浏览器
python click_extension.py --extension openclaw --browser chrome

# 自定义图标位置
python click_extension.py --x 1800 --y 50

# 截图确认位置
python click_extension.py --screenshot
```

## 参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--extension` | 扩展名称 (openclaw/other) | openclaw |
| `--browser` | 浏览器类型 (chrome/edge/firefox) | chrome |
| `--x` | 图标 X 坐标（可选） | 自动检测 |
| `--y` | 图标 Y 坐标（可选） | 自动检测 |
| `--screenshot` | 截图确认位置 | False |
| `--delay` | 点击前延迟（秒） | 1.0 |

## 图标位置参考

### Chrome/Edge 默认位置

| 扩展 | X 坐标 | Y 坐标 | 说明 |
|------|--------|--------|------|
| OpenClaw | 屏幕右上角 | 工具栏区域 | 拼图图标右侧 |
| 一般扩展 | 1750-1900 | 30-80 | 取决于屏幕分辨率 |

### 1920x1080 分辨率参考

```
OpenClaw 图标：x=1850, y=50
```

### 2560x1440 分辨率参考

```
OpenClaw 图标：x=2450, y=60
```

## 自动检测逻辑

1. 截取屏幕顶部右侧区域
2. 使用模板匹配查找红色小龙虾图标
3. 返回图标中心坐标

## 依赖安装

```bash
pip install pyautogui Pillow
```

## 注意事项

- 需要屏幕访问权限（macOS 需在系统设置中授权）
- 点击前会等待 1 秒确保浏览器已加载
- 建议先使用 `--screenshot` 确认图标位置
