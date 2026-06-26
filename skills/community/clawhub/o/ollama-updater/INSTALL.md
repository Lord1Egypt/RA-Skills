# 📦 Ollama Updater 安装指南

**版本**: 1.0.0  
**最后更新**: 2026-02-20

---

## 🚀 快速安装

### 方法 1: 使用 OpenClaw（推荐）

```bash
# 安装技能
openclaw skills install ollama-updater

# 验证安装
ollama-updater --help

# 运行安装
ollama-updater
```

### 方法 2: 使用 ClawHub

```bash
# 登录 ClawHub（首次使用）
clawhub login

# 安装技能
clawhub install ollama-updater

# 验证安装
ollama-updater --version

# 运行安装
ollama-updater
```

### 方法 3: 手动安装

```bash
# 1. 下载脚本
cd /tmp
curl -fsSL https://raw.githubusercontent.com/openclaw/skills/main/ollama-updater/ollama-install.sh -o ollama-install.sh

# 2. 添加执行权限
chmod +x ollama-install.sh

# 3. 运行安装
sudo ./ollama-install.sh
```

### 方法 4: Git 克隆

```bash
# 1. 克隆仓库
git clone https://github.com/openclaw/skills.git
cd skills/ollama-updater

# 2. 运行安装
sudo ./ollama-install.sh
```

---

## ✅ 验证安装

### 检查 Ollama 是否安装成功

```bash
# 检查版本
ollama --version

# 检查服务状态
ollama serve &

# 测试 API
curl http://localhost:11434/api/version
```

### 检查断点续传功能

```bash
# 查看脚本是否包含 -C - 参数
grep -n "curl.*-C -" /path/to/ollama-install.sh

# 应该输出类似：
# 123:        curl --fail --show-error --location --progress-bar -C - -o "$output" "$url"
```

---

## 🔧 配置

### 指定 Ollama 版本

```bash
# 安装特定版本
OLLAMA_VERSION=0.5.7 ollama-updater

# 或
export OLLAMA_VERSION=0.5.7
ollama-updater
```

### 自定义安装路径

默认安装到 `/usr/local/lib/ollama`

如需自定义，请修改脚本中的：
```bash
OLLAMA_INSTALL_DIR="/your/custom/path"
```

---

## 🧪 测试

### 测试断点续传

1. **开始安装**:
   ```bash
   ollama-updater
   ```

2. **模拟网络中断**（在下载过程中）:
   ```bash
   # 断开网络连接
   nmcli networking off
   ```

3. **等待错误**:
   ```
   curl: (92) HTTP/2 stream 1 was not closed cleanly
   ```

4. **恢复网络**:
   ```bash
   nmcli networking on
   ```

5. **重新运行**:
   ```bash
   ollama-updater
   ```

6. **验证续传**:
   ```
   >>> Downloading (attempt 2/3)...
   ###################### 31.1% → 100.0%  # ✅ 从断点继续
   ```

---

## 🐛 故障排查

### 问题 1: 命令不存在

**症状**:
```bash
bash: ollama-updater: command not found
```

**解决**:
```bash
# 检查技能是否安装
clawhub list | grep ollama-updater

# 重新安装
clawhub install ollama-updater

# 或添加到 PATH
export PATH="$PATH:~/.openclaw/workspace/skills/ollama-updater"
```

### 问题 2: 权限错误

**症状**:
```bash
sudo: a terminal is required to read the password
```

**解决**:
```bash
# 先验证 sudo 权限
sudo -v

# 然后运行
sudo ollama-updater
```

### 问题 3: zstd 错误

**症状**:
```bash
This version requires zstd for extraction. Please install zstd
```

**解决**:
```bash
# Debian/Ubuntu
sudo apt-get install zstd

# RHEL/CentOS/Fedora
sudo dnf install zstd

# Arch
sudo pacman -S zstd
```

### 问题 4: 下载速度慢

**解决**:
1. 使用有线网络
2. 避开网络高峰期
3. 检查 DNS 设置
4. 使用国内镜像（如有）

---

## 📋 系统要求

### 最低要求

- **操作系统**: Linux (x86_64, aarch64) 或 macOS
- **内存**: 2GB RAM (运行 Ollama)
- **磁盘**: 1GB 可用空间
- **工具**: curl, sudo

### 推荐配置

- **操作系统**: Ubuntu 24.04 LTS 或 macOS 12+
- **内存**: 8GB RAM
- **磁盘**: 10GB 可用空间
- **网络**: 稳定的宽带连接

### 可选工具

- **zstd**: 新版 Ollama 解压需要
- **systemd**: 自动启动服务需要
- **nvidia-smi**: NVIDIA GPU 检测需要

---

## 🔄 更新

### 更新技能

```bash
# 使用 ClawHub
clawhub update ollama-updater

# 或使用 OpenClaw
openclaw skills update ollama-updater
```

### 更新 Ollama

```bash
# 运行脚本会自动更新到最新版本
ollama-updater

# 或指定版本
OLLAMA_VERSION=0.5.7 ollama-updater
```

---

## 🗑️ 卸载

### 卸载 Ollama

```bash
# 停止服务
sudo systemctl stop ollama

# 禁用服务
sudo systemctl disable ollama

# 删除文件
sudo rm -rf /usr/local/lib/ollama
sudo rm /usr/local/bin/ollama
sudo rm /etc/systemd/system/ollama.service

# 删除用户
sudo userdel -r ollama
```

### 卸载技能

```bash
# 使用 ClawHub
clawhub remove ollama-updater
```

---

## 📞 获取帮助

### 文档

- **README.md**: 完整使用说明
- **SKILL.md**: 技能功能介绍
- **TEST-REPORT.md**: 测试报告

### 支持渠道

- **GitHub Issues**: https://github.com/openclaw/skills/issues
- **ClawHub 页面**: https://clawhub.com/skills/ollama-updater
- **Discord**: https://discord.com/invite/clawd

---

## 📝 版本历史

### v1.0.0 (2026-02-20)

- ✅ 初始版本
- ✅ 断点续传功能
- ✅ 自动重试机制
- ✅ 完整文档

---

**祝你安装顺利！🦙**
