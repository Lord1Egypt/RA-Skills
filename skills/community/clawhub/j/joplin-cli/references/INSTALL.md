# Joplin 终端版安装指南

> 来源：https://joplinapp.org/help/apps/terminal/#installation

## 安装方法

### 方法一：NPM（推荐）

```bash
# 安装 Node.js 12+（如果未安装）
# Ubuntu/Debian:
sudo apt install nodejs npm

# 安装 Joplin 终端版
NPM_CONFIG_PREFIX=~/.joplin-bin npm install --loglevel=error -g joplin

# 创建软链接
sudo ln -s ~/.joplin-bin/bin/joplin /usr/local/bin/joplin
```

### 方法二：Arch Linux（AUR）

```bash
yay -S joplin
```
同时提供 CLI 工具（`joplin`）和桌面应用（`joplin-desktop`）。

---

## 验证安装

```bash
joplin version
```

---

## CLI 配置同步

通过命令行配置同步目标，无需进入 TUI 界面。

### 查看当前同步配置

```bash
joplin config sync.target
```

同步目标类型：
- `0` - 无
- `2` - 本地文件系统
- `3` - OneDrive
- `5` - Nextcloud
- `6` - WebDAV
- `7` - Dropbox
- `8` - S3
- `9` - Joplin Server
- `10` - Joplin Cloud

### Dropbox

```bash
joplin config sync.target 7
joplin sync    # 首次会提示授权链接
```

### OneDrive

```bash
joplin config sync.target 3
joplin sync    # 首次会提示授权链接
```

### Nextcloud

```bash
joplin config sync.target 5
joplin config sync.5.path "https://example.com/nextcloud/remote.php/webdav/Joplin"
joplin config sync.5.username "你的用户名"
joplin config sync.5.password "你的密码"
joplin sync
```

### WebDAV

```bash
joplin config sync.target 6
joplin config sync.6.path "https://webdav.example.com/Joplin"
joplin config sync.6.username "用户名"
joplin config sync.6.password "密码"
joplin sync
```

### 本地文件系统

```bash
joplin config sync.target 2
joplin config sync.2.path "/path/to/sync/directory"
joplin sync
```

### Joplin Cloud

```bash
joplin config sync.target 10
joplin config sync.10.username "你的邮箱"
joplin config sync.10.password "你的密码"
joplin sync
```

---

## ⚠️ 重要：任务后同步

**如果配置了远程同步，每次完成任务后必须执行 `joplin sync`**，确保：

1. 本地修改同步到远程
2. 多设备间数据一致
3. 数据备份

示例工作流：

```bash
# 创建笔记
joplin mknote "会议记录"

# 写入内容
joplin set "会议记录" body "## 议程\n\n1. ...\n2. ..."

# ✅ 完成后同步
joplin sync
```

自动化脚本示例：

```bash
#!/bin/bash
# 每次操作后自动同步
joplin mknote "日记 - $(date +%Y-%m-%d)"
joplin sync
```

---

## 配置文件位置

- 配置目录：`~/.config/joplin/`
- 数据目录：`~/.config/joplin/`
- 快捷键配置：`~/.config/joplin/keymap.json`

---

## 卸载

```bash
npm uninstall -g joplin
sudo rm /usr/local/bin/joplin
rm -rf ~/.joplin-bin
rm -rf ~/.config/joplin   # 同时删除数据
```