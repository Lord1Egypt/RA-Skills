# 安装指南

**适用场景**: 首次使用 Glances，需要安装和配置环境

---

## 一、安装前准备

### 目标

确保系统具备运行 Glances 的基础环境

### 前置条件

- Python 3.8 或更高版本
- pip 包管理器
- 网络连接（下载依赖包）

### 检查系统环境

**AI执行说明**: AI 将自动检查你的系统环境，确认满足安装要求

```bash
# 检查 Python 版本（需要 3.8+）
python3 --version

# 检查 pip
pip3 --version

# 检查当前已安装的 glances（是否已有旧版本）
pip3 show glances
```

**期望结果**:
- Python 3.8+ 已安装 ✅
- pip3 可用 ✅

---

## 二、安装 Glances

### 方法1: 使用 pip 安装（推荐，跨平台通用）

**AI执行说明**: AI 可以直接执行安装命令

```bash
# 标准安装（基础功能）
pip3 install glances

# 安装带全部可选依赖（推荐，包含 Web UI 和更多导出插件）
pip3 install 'glances[all]'

# 验证安装
glances --version
```

**期望结果**:
```
Glances v4.x.x with Python 3.x.x
```

### 方法2: 使用 Homebrew 安装（macOS）

```bash
# 使用 Homebrew 安装
brew install glances

# 验证安装
glances --version
```

### 方法3: 使用系统包管理器（Linux）

**Ubuntu / Debian**:
```bash
# 安装系统包（版本可能较旧）
sudo apt update
sudo apt install glances

# 验证版本
glances --version
```

**Fedora / RHEL / CentOS**:
```bash
sudo dnf install glances
```

**Arch Linux**:
```bash
sudo pacman -S glances
```

**注意**: 系统包管理器提供的版本通常比 pip 滞后，建议生产环境使用 pip 安装最新版本。

### 方法4: 使用 Docker 安装（隔离环境）

**AI执行说明**: AI 可以帮助配置 Docker 运行命令

```bash
# 拉取最新镜像
docker pull nicolargo/glances:latest

# 以终端模式运行（显示本机系统信息）
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock:ro \
    -v /run/user/1000/podman/podman.sock:/run/user/1000/podman/podman.sock:ro \
    --pid host --network host \
    -it nicolargo/glances:latest

# 以 Web 服务器模式运行（端口 61208）
docker run -d --restart="always" \
    -p 61208-61209:61208-61209 \
    -e GLANCES_OPT="-w" \
    -v /var/run/docker.sock:/var/run/docker.sock:ro \
    --pid host \
    nicolargo/glances:latest
```

### 方法5: 使用 pipx 安装（推荐隔离安装）

```bash
# 安装 pipx（如未安装）
pip3 install pipx
pipx ensurepath

# 使用 pipx 安装 glances
pipx install glances

# 注入可选依赖
pipx inject glances bottle
```

---

## 三、安装可选依赖

Glances 通过额外依赖扩展功能，按需安装：

### Web UI 支持（浏览器访问）

**AI执行说明**: AI 会根据你的需求安装相应依赖

```bash
# 安装 Web UI 依赖（bottle 框架）
pip3 install 'glances[web]'

# 或单独安装
pip3 install bottle
```

### Docker 监控支持

```bash
pip3 install 'glances[docker]'
# 等同于：pip3 install docker
```

### 数据导出依赖

```bash
# 导出到 InfluxDB v1
pip3 install influxdb

# 导出到 InfluxDB v2
pip3 install influxdb-client

# 导出到 Prometheus
pip3 install prometheus_client

# 导出到 Elasticsearch
pip3 install elasticsearch

# 导出到 MQTT
pip3 install paho-mqtt

# CSV 导出（内置，无需额外安装）
# 一次性安装所有导出依赖
pip3 install 'glances[all]'
```

### 传感器和 SMART 支持

```bash
# 硬盘健康状态监控
pip3 install pySMART.smartx

# GPU 监控（NVIDIA）
pip3 install nvidia-ml-py3
```

---

## 四、配置文件初始化

### 创建配置文件目录

```bash
# Linux / macOS
mkdir -p ~/.config/glances

# 查看默认配置（Glances 自带示例配置）
glances --config /etc/glances/glances.conf 2>/dev/null || echo "使用默认配置"
```

### 生成默认配置文件

Glances 首次运行时会自动使用内置默认值。如需自定义配置：

```bash
# Linux / macOS 配置文件路径
# ~/.config/glances/glances.conf

# 查看配置文件搜索路径
glances --help | grep config
```

---

## 五、验证完整安装

**AI执行说明**: AI 将运行验证命令，确认所有功能正常工作

```bash
# 查看版本信息
glances --version

# 查看已加载的插件列表
glances --list-plugins

# 快速测试（运行 3 秒后退出）
glances --stdout cpu.total --time 3

# 检查 Web UI 依赖是否可用
python3 -c "import bottle; print('Web UI 依赖: OK')" 2>/dev/null || echo "Web UI 依赖未安装"

# 检查 Docker 监控依赖
python3 -c "import docker; print('Docker 监控依赖: OK')" 2>/dev/null || echo "Docker 监控依赖未安装"
```

**成功标志**:
- Glances 版本信息显示 ✅
- 插件列表正常输出 ✅
- `cpu.total` 输出数字值 ✅

---

## 六、升级 Glances

```bash
# 使用 pip 升级
pip3 install --upgrade glances

# 升级并包含所有依赖
pip3 install --upgrade 'glances[all]'

# 如果使用 Docker，拉取最新镜像
docker pull nicolargo/glances:latest
```

---

## 七、常见安装问题

### 问题1: pip3 命令找不到

**解决方案**:
```bash
# 尝试使用 pip（不带数字）
pip install glances

# 或通过 Python 模块调用
python3 -m pip install glances
```

### 问题2: 权限错误（Permission denied）

**解决方案**:
```bash
# 使用用户安装（推荐，避免污染系统环境）
pip3 install --user glances

# 或使用 sudo（不推荐）
sudo pip3 install glances
```

### 问题3: 国内网络超时

**解决方案**:
```bash
# 使用清华镜像源
pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple glances

# 使用阿里云镜像源
pip3 install -i https://mirrors.aliyun.com/pypi/simple/ glances
```

---

## 完成确认

### 检查清单

- [ ] Python 3.8+ 已安装
- [ ] Glances 已安装并显示版本号
- [ ] 插件列表可以正常输出
- [ ] （可选）Web UI 依赖已安装
- [ ] （可选）Docker 监控依赖已安装

### 下一步

继续阅读 [快速开始](02-quickstart.md) 学习如何启动和使用 Glances
