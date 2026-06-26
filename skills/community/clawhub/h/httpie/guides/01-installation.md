# 安装指南

**适用场景**: 首次使用 HTTPie，需要在本地环境中完成安装和配置

---

## 一、安装前准备

### 目标

确保系统具备运行 HTTPie 的基础环境，选择最适合的安装方式

### 前置条件

- 操作系统：macOS、Linux（Ubuntu/Debian/Fedora/Arch）、Windows 10+
- 网络连接（下载安装包）
- （pip 方式）Python 3.7 或更高版本

### 检查现有环境

**AI 执行说明**: AI 将自动检查当前系统环境，判断最佳安装路径

```bash
# 检查是否已安装 httpie
http --version

# 检查 Python 版本（如使用 pip 安装）
python3 --version

# 检查 pip
pip3 --version
```

**期望结果**:
- 若 `http --version` 有输出，说明已安装，无需重复安装
- Python 3.7+ 可用 pip 安装方式
- pip 3.x 可正常使用

---

## 二、安装方式选择

HTTPie 提供多种安装方式，根据你的系统和偏好选择：

| 安装方式 | 适用系统 | 优点 |
|--------|--------|-----|
| Homebrew | macOS / Linux | 最简单，自动管理依赖 |
| pip | 全平台（需要 Python） | 版本最新，适合 Python 开发者 |
| pipx | 全平台（需要 Python） | 隔离安装，推荐方式 |
| apt/yum/pacman | Linux | 系统包管理，稳定 |
| 独立二进制 | macOS / Linux | 无需 Python 依赖 |
| Windows Installer | Windows | 官方安装包，最方便 |

---

## 三、各平台安装步骤

### 方法 1: macOS 使用 Homebrew（推荐）

**AI 执行说明**: AI 可以直接执行 Homebrew 安装命令

```bash
# 安装 HTTPie
brew install httpie

# 验证安装
http --version
```

**期望输出**:
```
HTTPie 3.x.x
```

如果未安装 Homebrew，先执行：

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

---

### 方法 2: 使用 pip 安装（全平台）

**AI 执行说明**: AI 可以直接执行 pip 安装命令

```bash
# 使用 pip 安装（推荐使用 pip3）
pip3 install httpie

# 验证安装
http --version

# 如果 pip3 不可用，尝试 pip
pip install httpie
```

**注意**: 部分系统中 `http` 命令可能与系统命令冲突，可以使用完整路径：

```bash
# 查找安装路径
which http
python3 -m httpie --version
```

---

### 方法 3: 使用 pipx 安装（推荐，隔离环境）

pipx 会将 HTTPie 安装在独立的虚拟环境中，避免依赖冲突：

```bash
# 先安装 pipx（如未安装）
pip3 install pipx
pipx ensurepath

# 安装 HTTPie
pipx install httpie

# 验证安装
http --version
```

---

### 方法 4: Linux 系统包管理器

**Ubuntu / Debian**:

```bash
sudo apt update
sudo apt install httpie

http --version
```

**Fedora / RHEL / CentOS**:

```bash
sudo dnf install httpie

# 或者使用 yum（旧版系统）
sudo yum install httpie
```

**Arch Linux**:

```bash
sudo pacman -S httpie
```

**Alpine Linux**:

```bash
apk add httpie
```

---

### 方法 5: Windows 安装

**方式 A - pip（推荐）**:

```powershell
# 在 PowerShell 或 CMD 中执行
pip install httpie

# 验证
http --version
```

**方式 B - Chocolatey**:

```powershell
choco install httpie
```

**方式 C - Scoop**:

```powershell
scoop install httpie
```

---

### 方法 6: 独立二进制安装（无需 Python）

HTTPie 提供预编译的独立二进制文件，无需 Python 环境：

```bash
# macOS (Apple Silicon)
curl -SsL https://packages.httpie.io/mac/http.latest.arm64 -o /usr/local/bin/http
chmod +x /usr/local/bin/http

# macOS (Intel)
curl -SsL https://packages.httpie.io/mac/http.latest.x86_64 -o /usr/local/bin/http
chmod +x /usr/local/bin/http

# Linux (x86_64)
curl -SsL https://packages.httpie.io/linux/http.latest.x86_64 -o /usr/local/bin/http
chmod +x /usr/local/bin/http
```

---

## 四、验证安装

**AI 执行说明**: AI 将验证安装是否成功并进行简单测试

```bash
# 检查版本
http --version

# 发送一个测试请求（HTTPie 官方测试端点）
http GET https://httpie.io/hello
```

**期望输出（版本检查）**:
```
HTTPie 3.x.x
```

**期望输出（测试请求）**:
```
HTTP/1.1 200 OK
Content-Type: application/json
...

{
    "ahoy": [
        "Hello, World! 👋"
    ],
    ...
}
```

**成功标志**:
- HTTPie 版本信息正确显示
- 测试请求返回 200 状态码
- 响应体 JSON 格式化输出（有缩进和高亮）

---

## 五、升级 HTTPie

```bash
# pip 升级
pip3 install --upgrade httpie

# Homebrew 升级
brew upgrade httpie

# pipx 升级
pipx upgrade httpie

# 查看当前版本
http --version
```

---

## 六、卸载 HTTPie

```bash
# pip 卸载
pip3 uninstall httpie

# Homebrew 卸载
brew uninstall httpie

# pipx 卸载
pipx uninstall httpie
```

---

## 七、常见安装问题

### 问题 1: `http` 命令找不到

**症状**: 安装后执行 `http` 提示 `command not found`

**解决方案**:

```bash
# 检查 pip 安装位置
python3 -m site --user-base

# 将用户 bin 目录加入 PATH（添加到 ~/.zshrc 或 ~/.bashrc）
export PATH="$HOME/.local/bin:$PATH"

# 立即生效
source ~/.zshrc
```

### 问题 2: 权限不足

**症状**: 安装时报 `Permission denied` 错误

**解决方案**:

```bash
# 使用用户级安装（不需要 sudo）
pip3 install --user httpie

# 或使用 pipx（推荐）
pip3 install pipx
pipx install httpie
```

### 问题 3: pip 网络超时

**症状**: pip install 时网络连接失败或超时

**解决方案**:

```bash
# 使用国内镜像
pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple httpie

# 或使用阿里云镜像
pip3 install -i https://mirrors.aliyun.com/pypi/simple/ httpie
```

---

## 完成确认

### 检查清单

- [ ] HTTPie 已成功安装并可运行
- [ ] `http --version` 显示正确版本号
- [ ] 测试请求 `http GET https://httpie.io/hello` 返回 200
- [ ] 响应体 JSON 已正确格式化和高亮显示

### 下一步

继续阅读 [快速开始](02-quickstart.md) 学习 HTTPie 的基本用法
