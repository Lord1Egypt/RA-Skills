---
name: hatsune-miku-monitor
description: 初音未来监控器 - 可爱的桌面系统监控工具（GIF动画 + 贴边隐藏 + 一键加速）
version: 1.0.1
author: gsp
---

# 初音未来监控器

一个可爱的桌面系统监控工具，使用初音未来 GIF 动画形象。

## 功能特性

- 🎤 **GIF 动画** — 流畅的初音未来动画
- 📊 **系统监控** — 实时显示 CPU、内存、磁盘、温度
- 🖱️ **点击交互** — 点击初音切换状态面板
- 📍 **贴边隐藏** — 拖到屏幕边缘自动隐藏
- ⚡ **一键加速** — 清理内存和系统缓存
- 🎨 **透明度调节** — 滑条实时调整透明度
- ↔️ **自由拖动** — 随意移动位置

## 快速开始

### 1. 从 ClawHub 安装

```bash
clawhub install hatsune-miku-monitor
```

### 2. 准备初音 GIF 图片

将你的初音 GIF 图片放到 `/tmp/chuyin.gif`：

```bash
# 如果你有 chuyin.gif
cp /path/to/your/chuyin.gif /tmp/chuyin.gif

# 或者创建 assets 目录
mkdir -p ~/.openclaw/workspace/skills/hatsune-miku-monitor/assets
cp /path/to/your/hatsune.gif ~/.openclaw/workspace/skills/hatsune-miku-monitor/assets/
```

### 3. 安装依赖

```bash
# Ubuntu/Debian
sudo apt install python3-gi python3-gi-cairo gir1.2-gtk-3.0

# 安装 Python 包
pip3 install psutil pillow

# 或使用安装脚本
cd ~/.openclaw/workspace/skills/hatsune-miku-monitor
bash scripts/install-deps.sh
```

### 4. 启动监控器

```bash
cd ~/.openclaw/workspace/skills/hatsune-miku-monitor
python3 scripts/hatsune-ball.py

# 或后台运行
python3 scripts/hatsune-ball.py &
```

## 使用说明

**操作方式：**
- **点击初音** → 切换状态面板（显示/隐藏）
- **拖动** → 移动位置
- **拖到边缘** → 自动隐藏成细条
- **点击"⚡ 一键加速"** → 清理内存和缓存
- **调节透明度** → 打开面板，拖动滑条
- **关闭** → 点击面板里的"✕ 关闭"

**显示内容：**
- CPU 使用率
- 内存使用率
- 磁盘使用率
- CPU 温度

## 一键加速功能

点击"⚡ 一键加速"按钮会：
- Python 垃圾回收（3次）
- 清理系统缓存（PageCache/dentries/inodes）
- Swap 刷新
- 清理用户缓存目录（thumbnails/pip/mesa）
- 清理 journalctl 日志（保留1天）

**增强效果（可选）：**

如果想让清理效果更明显，允许无密码执行：

```bash
sudo visudo
```

添加（替换 `your_username`）：
```
your_username ALL=(ALL) NOPASSWD: /usr/bin/sh -c echo * > /proc/sys/vm/drop_caches
your_username ALL=(ALL) NOPASSWD: /usr/sbin/swapoff
your_username ALL=(ALL) NOPASSWD: /usr/sbin/swapon
your_username ALL=(ALL) NOPASSWD: /usr/bin/journalctl
```

## 自定义图片

脚本会自动查找以下位置的 GIF 图片：
1. `~/.openclaw/workspace/skills/hatsune-miku-monitor/assets/hatsune.gif`
2. `~/.openclaw/workspace/skills/hatsune-miku-monitor/assets/chuyin.gif`
3. `/tmp/chuyin.gif`
4. `/tmp/hatsune.gif`

支持格式：GIF（推荐）、PNG、JPG

## 开机自启

### Linux (Systemd)

创建：`~/.config/systemd/user/hatsune-monitor.service`

```ini
[Unit]
Description=Hatsune Miku Monitor

[Service]
ExecStart=/usr/bin/python3 %h/.openclaw/workspace/skills/hatsune-miku-monitor/scripts/hatsune-ball.py
Restart=always

[Install]
WantedBy=default.target
```

启用：
```bash
systemctl --user enable hatsune-monitor
systemctl --user start hatsune-monitor
```

## 故障排除

### 问题：ModuleNotFoundError: No module named 'gi'

**解决：**
```bash
sudo apt install python3-gi python3-gi-cairo gir1.2-gtk-3.0
```

### 问题：在 conda 环境中无法运行

**解决：** 退出 conda 环境，使用系统 Python
```bash
conda deactivate
python3 scripts/hatsune-ball.py
```

### 问题：GIF 不显示

**解决：** 确保 GIF 在正确位置
```bash
# 检查文件
ls -la /tmp/chuyin.gif
# 或
ls -la ~/.openclaw/workspace/skills/hatsune-miku-monitor/assets/

# 安装 Pillow
pip3 install pillow
```

### 问题：只显示笑脸图标

**解决：** 未找到 GIF 图片，请将初音 GIF 放到上述路径之一

## 许可证

MIT License
