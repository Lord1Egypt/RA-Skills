# 🖱️ 浏览器扩展自动点击技能

自动点击浏览器扩展图标（如 OpenClaw Browser Relay），绕过浏览器安全限制。

## 📦 安装

### 1. 安装依赖

```bash
pip install pyautogui Pillow
```

### 2. 授权屏幕访问（macOS）

如果是 macOS 系统，需要在系统设置中授权：
- 系统设置 → 隐私与安全性 → 屏幕录制 → 添加终端/Python

## 🚀 使用方式

### 基础用法

```bash
# 点击 OpenClaw 插件图标（默认位置）
python click_extension.py

# 测试模式（只显示位置，不实际点击）
python click_extension.py --dry-run
```

### 常用参数

| 参数 | 说明 | 示例 |
|------|------|------|
| `--extension` | 扩展名称 | `--extension openclaw` |
| `--x` / `--y` | 自定义坐标 | `--x 1850 --y 50` |
| `--delay` | 点击前延迟（秒） | `--delay 2` |
| `--screenshot` | 点击前截图 | `--screenshot` |
| `--dry-run` | 测试模式 | `--dry-run` |
| `--calibrate` | 校准模式 | `--calibrate` |

### 完整示例

```bash
# 1. 先测试位置（不点击）
python click_extension.py --dry-run --screenshot

# 2. 校准模式（手动指定位置）
python click_extension.py --calibrate
# 5 秒内将鼠标移到图标位置

# 3. 实际点击
python click_extension.py --extension openclaw --delay 1
```

## 📍 图标位置参考

### 默认位置（基于分辨率）

| 分辨率 | OpenClaw 位置 |
|--------|--------------|
| 1920x1080 | (1850, 50) |
| 2560x1440 | (2450, 60) |
| 3840x2160 | (3700, 80) |

### 如何找到正确的坐标

**方法 1：校准模式（推荐）**

```bash
python click_extension.py --calibrate
```
然后在 5 秒内将鼠标移到图标位置。

**方法 2：查看截图**

```bash
python click_extension.py --screenshot --dry-run
```
查看生成的截图，用图片编辑器查看图标坐标。

## ⚠️ 注意事项

1. **首次使用请先测试**：使用 `--dry-run` 确认位置正确
2. **关闭其他窗口**：确保浏览器窗口在最前面
3. **权限问题**：macOS 需要授权屏幕录制权限
4. **分辨率变化**：如果更换显示器，需要重新校准

## 🔧 集成到 OpenClaw

在 OpenClaw 中调用此技能：

```python
# 在对话中请求
"点击浏览器上的 OpenClaw 插件图标"

# 或直接调用脚本
exec: python skills/browser-extension-clicker/click_extension.py
```

## 📁 文件结构

```
browser-extension-clicker/
├── SKILL.md              # 技能定义
├── click_extension.py    # 主脚本
├── README.md            # 使用说明
└── templates/           # 图标模板图片（可选）
    └── openclaw.png
```

## 🐛 故障排除

### 问题：点击位置不对

**解决**：使用校准模式重新定位
```bash
python click_extension.py --calibrate
```

### 问题：pyautogui 无法导入

**解决**：重新安装依赖
```bash
pip install --upgrade pyautogui Pillow
```

### 问题：macOS 提示权限不足

**解决**：在系统设置中授权
- 系统设置 → 隐私与安全性 → 屏幕录制 → 添加终端

## 📝 更新日志

- **v1.0.0** (2026-03-13)
  - 初始版本
  - 支持 OpenClaw 插件自动点击
  - 支持自定义坐标和校准模式
