# 初音未来监控器

一个可爱的桌面系统监控工具，使用初音未来 GIF 动画形象。

## 功能特性

- 🎤 **GIF 动画** — 流畅的初音未来动画
- 📊 **系统监控** — 实时显示 CPU、内存、磁盘、温度
- 🖱️ **点击交互** — 点击初音切换状态面板
- 📍 **贴边隐藏** — 拖到屏幕边缘自动隐藏
- ⚡ **一键加速** — 清理内存和系统缓存
- 🎨 **透明度调节** — 滑条实时调整透明度

## 快速开始

### 安装

```bash
clawhub install hatsune-miku-monitor
```

### 准备 GIF

将初音 GIF 放到 `/tmp/chuyin.gif` 或创建 assets 目录：

```bash
mkdir -p ~/.openclaw/workspace/skills/hatsune-miku-monitor/assets
cp your_hatsune.gif ~/.openclaw/workspace/skills/hatsune-miku-monitor/assets/chuyin.gif
```

### 安装依赖

```bash
sudo apt install python3-gi python3-gi-cairo gir1.2-gtk-3.0
pip3 install psutil pillow
```

### 启动

```bash
cd ~/.openclaw/workspace/skills/hatsune-miku-monitor
python3 scripts/hatsune-ball.py
```

## 使用说明

- **点击初音** → 显示/隐藏状态面板
- **拖动** → 移动位置
- **拖到边缘** → 自动隐藏
- **⚡ 一键加速** → 清理内存
- **透明度滑条** → 调整透明度
- **✕ 关闭** → 退出程序

## 开机自启

创建 systemd 服务：

```bash
mkdir -p ~/.config/systemd/user
cat > ~/.config/systemd/user/hatsune-monitor.service << 'EOF'
[Unit]
Description=Hatsune Miku Monitor

[Service]
ExecStart=/usr/bin/python3 %h/.openclaw/workspace/skills/hatsune-miku-monitor/scripts/hatsune-ball.py
Restart=always

[Install]
WantedBy=default.target
EOF

systemctl --user enable hatsune-monitor
systemctl --user start hatsune-monitor
```

## 故障排除

- **缺少 gi 模块** → `sudo apt install python3-gi`
- **conda 环境** → `conda deactivate`
- **GIF 不显示** → 检查 `/tmp/chuyin.gif` 是否存在
- **只显示笑脸** → 未找到 GIF，请放置图片

## 许可证

MIT License
