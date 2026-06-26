# 安装指南

**适用场景**: 首次使用 lazydocker，需要在系统上安装并配置运行环境

---

## 一、安装前准备

### 目标

确保系统具备运行 lazydocker 的基础环境（Docker 已安装并运行）

### 前置条件

- Docker Engine 或 Docker Desktop 已安装
- 对于 macOS 用户，推荐使用 Homebrew
- 对于 Linux 用户，推荐使用安装脚本
- 对于 Windows 用户，需要 WSL2 环境

### 检查 Docker 环境

**AI执行说明**: AI 将自动检查你的 Docker 安装状态

```bash
# 检查 Docker 版本
docker --version

# 检查 Docker 守护进程是否运行
docker info

# 验证可以列出容器
docker ps
```

**期望结果**:
- Docker 已安装并显示版本号 ✅
- Docker 守护进程运行中（`docker info` 无错误） ✅
- `docker ps` 命令返回容器列表（可以为空） ✅

---

## 二、安装 lazydocker

### 方法1: 使用 Homebrew 安装（macOS/Linux，推荐）

**AI执行说明**: AI 可以直接执行安装命令

```bash
# 添加 tap（如果尚未添加）
brew install jesseduffield/lazydocker/lazydocker
```

**验证安装**:
```bash
lazydocker --version
```

**期望结果**:
```
commit=<hash>, build date=<date>, build source=homebrew, version=0.23.x, os=darwin, arch=arm64/amd64
```

---

### 方法2: 使用官方安装脚本（Linux，推荐）

**AI执行说明**: AI 可以执行安装脚本

```bash
# 下载并运行官方安装脚本
curl https://raw.githubusercontent.com/jesseduffield/lazydocker/master/scripts/install_update_linux.sh | bash
```

此脚本将自动：
1. 检测系统架构（amd64/arm64）
2. 下载对应的二进制文件
3. 安装到 `~/.local/bin/` 目录
4. 设置可执行权限

**验证安装**:
```bash
lazydocker --version
```

---

### 方法3: 使用 go install 安装（需要 Go 环境）

**AI执行说明**: 如果已有 Go 环境，AI 可以使用此方法

```bash
# 需要 Go 1.19 或更高版本
go install github.com/jesseduffield/lazydocker@latest
```

安装完成后，确保 `$GOPATH/bin` 在 PATH 中：
```bash
# 添加到 ~/.bashrc 或 ~/.zshrc
export PATH=$PATH:$(go env GOPATH)/bin
```

---

### 方法4: 手动下载二进制文件（所有平台）

**AI执行说明**: AI 可以帮助下载对应平台的二进制文件

访问 GitHub Releases 页面，根据系统选择合适的版本：
```
https://github.com/jesseduffield/lazydocker/releases
```

**macOS (Apple Silicon)**:
```bash
# 下载 darwin_arm64 版本
curl -Lo lazydocker.tar.gz "https://github.com/jesseduffield/lazydocker/releases/latest/download/lazydocker_Darwin_arm64.tar.gz"
tar -xzf lazydocker.tar.gz lazydocker
sudo mv lazydocker /usr/local/bin/
```

**macOS (Intel)**:
```bash
curl -Lo lazydocker.tar.gz "https://github.com/jesseduffield/lazydocker/releases/latest/download/lazydocker_Darwin_x86_64.tar.gz"
tar -xzf lazydocker.tar.gz lazydocker
sudo mv lazydocker /usr/local/bin/
```

**Linux (amd64)**:
```bash
curl -Lo lazydocker.tar.gz "https://github.com/jesseduffield/lazydocker/releases/latest/download/lazydocker_Linux_x86_64.tar.gz"
tar -xzf lazydocker.tar.gz lazydocker
sudo mv lazydocker /usr/local/bin/
```

**Linux (arm64)**:
```bash
curl -Lo lazydocker.tar.gz "https://github.com/jesseduffield/lazydocker/releases/latest/download/lazydocker_Linux_arm64.tar.gz"
tar -xzf lazydocker.tar.gz lazydocker
sudo mv lazydocker /usr/local/bin/
```

---

### 方法5: 使用 Scoop 安装（Windows）

**AI执行说明**: Windows 用户推荐在 PowerShell 中执行

```powershell
scoop install lazydocker
```

或在 WSL2 中使用 Linux 安装方式。

---

### 方法6: 使用 Docker 运行（无需安装）

**AI执行说明**: 适合临时使用，无需在系统安装二进制

```bash
# 使用 Docker 运行 lazydocker（挂载 Docker socket）
docker run --rm -it \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v ~/.config/lazydocker:/.config/jesseduffield/lazydocker \
  lazyteam/lazydocker
```

---

## 三、配置 PATH（如需）

如果使用脚本安装或手动下载，需要确保 lazydocker 在 PATH 中：

```bash
# 检查 lazydocker 是否可被找到
which lazydocker

# 如果未找到，手动添加到 PATH（以 ~/.local/bin 为例）
echo 'export PATH=$PATH:$HOME/.local/bin' >> ~/.bashrc
source ~/.bashrc

# zsh 用户
echo 'export PATH=$PATH:$HOME/.local/bin' >> ~/.zshrc
source ~/.zshrc
```

---

## 四、验证安装

**AI执行说明**: AI 将验证 lazydocker 是否正确安装

```bash
# 检查版本
lazydocker --version

# 测试启动（确保 Docker 正在运行）
docker ps && lazydocker
```

**成功标志**:
- lazydocker 版本信息正常显示 ✅
- lazydocker TUI 界面成功启动 ✅
- 容器列表（或空状态）正常显示 ✅

---

## 五、升级 lazydocker

### Homebrew 升级

```bash
brew upgrade jesseduffield/lazydocker/lazydocker
```

### 脚本升级（Linux）

```bash
# 同安装脚本，可重复运行以升级
curl https://raw.githubusercontent.com/jesseduffield/lazydocker/master/scripts/install_update_linux.sh | bash
```

### go install 升级

```bash
go install github.com/jesseduffield/lazydocker@latest
```

---

## 六、卸载 lazydocker

```bash
# Homebrew 卸载
brew uninstall lazydocker

# 手动安装的卸载
sudo rm /usr/local/bin/lazydocker

# 删除配置文件（可选）
rm -rf ~/.config/jesseduffield/lazydocker
```

---

## 完成确认

### 检查清单
- [ ] Docker 已安装并运行
- [ ] lazydocker 已安装
- [ ] `lazydocker --version` 正常输出版本信息
- [ ] lazydocker TUI 界面可以正常启动

### 下一步
继续阅读 [快速开始](02-quickstart.md) 学习如何使用 lazydocker 管理容器
