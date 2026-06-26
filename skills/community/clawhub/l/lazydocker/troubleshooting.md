# 常见问题与解决方案

---

## 问题分类说明

**简单问题（1-2步排查）**: 环境配置、权限问题等  
**中等问题（3-5步排查）**: 连接失败、界面异常等  
**复杂问题（5-10步排查）**: 远程连接、Docker Compose 集成等

---

## 安装问题

### 1. lazydocker 命令未找到【简单问题】

**问题描述**: 安装后运行 `lazydocker` 提示 `command not found`

**排查步骤**:
```bash
# 检查安装位置
which lazydocker
ls ~/.local/bin/lazydocker
ls /usr/local/bin/lazydocker

# 检查 PATH 变量
echo $PATH
```

**常见原因**:
- 安装目录不在 PATH 中（50%）
- 安装未成功（30%）
- 使用了错误的 shell（20%）

**解决方案**:

**方案A（推荐）**: 添加安装目录到 PATH
```bash
# 如果安装在 ~/.local/bin
echo 'export PATH=$PATH:$HOME/.local/bin' >> ~/.bashrc
source ~/.bashrc

# zsh 用户
echo 'export PATH=$PATH:$HOME/.local/bin' >> ~/.zshrc
source ~/.zshrc
```

**方案B**: 重新安装（Homebrew）
```bash
brew install jesseduffield/lazydocker/lazydocker
```

**方案C**: 创建符号链接
```bash
sudo ln -s ~/.local/bin/lazydocker /usr/local/bin/lazydocker
```

---

### 2. Homebrew 安装失败【简单问题】

**问题描述**: `brew install` 命令报错

**排查步骤**:
```bash
# 检查 Homebrew 版本
brew --version

# 更新 Homebrew
brew update

# 检查 tap 是否存在
brew tap | grep jesseduffield
```

**常见原因**:
- Homebrew 版本过旧（40%）
- 网络连接问题（40%）
- tap 重复添加（20%）

**解决方案**:

**方案A（更新 Homebrew）**:
```bash
brew update && brew upgrade
brew install jesseduffield/lazydocker/lazydocker
```

**方案B（使用安装脚本代替）**:
```bash
curl https://raw.githubusercontent.com/jesseduffield/lazydocker/master/scripts/install_update_linux.sh | bash
```

**方案C（手动下载二进制）**:
访问 https://github.com/jesseduffield/lazydocker/releases 下载对应版本

---

## 启动问题

### 3. 启动时提示"Cannot connect to the Docker daemon"【中等问题】

**问题描述**: 运行 `lazydocker` 后报错 `Cannot connect to the Docker daemon at unix:///var/run/docker.sock`

**排查步骤**:
```bash
# 1. 检查 Docker 守护进程状态
docker info

# 2. 检查 Docker socket 是否存在
ls -la /var/run/docker.sock

# 3. 检查当前用户权限
groups $(whoami)

# 4. 尝试用 sudo 启动
sudo docker info
```

**常见原因**:
- Docker Desktop 未启动（45%）
- 当前用户不在 docker 组（30%）
- Docker 守护进程崩溃（15%）
- socket 路径不正确（10%）

**解决方案**:

**方案A（启动 Docker Desktop）**:
- macOS: 点击 Docker Desktop 图标启动
- Linux: `sudo systemctl start docker`

**方案B（添加用户到 docker 组，Linux）**:
```bash
sudo usermod -aG docker $USER
# 重新登录或执行以下命令使权限立即生效
newgrp docker

# 验证
docker ps
```

**方案C（macOS Docker Desktop socket 路径问题）**:
```bash
# Docker Desktop 可能使用不同的 socket 路径
DOCKER_HOST=unix:///Users/$(whoami)/.docker/run/docker.sock lazydocker
```

**方案D（colima 用户）**:
```bash
DOCKER_HOST=unix:///Users/$(whoami)/.colima/default/docker.sock lazydocker
```

---

### 4. 界面显示乱码或字符错误【简单问题】

**问题描述**: lazydocker 界面显示方框、问号或其他乱码字符

**排查步骤**:
```bash
# 检查终端编码
echo $LANG
echo $LC_ALL

# 检查终端类型
echo $TERM
```

**常见原因**:
- 终端编码非 UTF-8（60%）
- 终端不支持 Unicode（30%）
- 字体缺少字符（10%）

**解决方案**:

**方案A（设置 UTF-8 编码）**:
```bash
export LANG=en_US.UTF-8
export LC_ALL=en_US.UTF-8
lazydocker
```

**方案B（持久化设置）**:
```bash
# 添加到 ~/.bashrc 或 ~/.zshrc
echo 'export LANG=en_US.UTF-8' >> ~/.bashrc
echo 'export LC_ALL=en_US.UTF-8' >> ~/.bashrc
```

**方案C**: 切换到支持 Unicode 的终端模拟器（iTerm2、Alacritty、Windows Terminal）

---

### 5. 界面颜色显示异常（全是黑白）【简单问题】

**问题描述**: lazydocker 界面没有颜色高亮，全部显示为黑白

**排查步骤**:
```bash
# 检查终端颜色支持
echo $TERM
tput colors
```

**常见原因**:
- TERM 变量未正确设置（60%）
- 终端不支持 256 色（30%）
- SSH 会话颜色传递问题（10%）

**解决方案**:

**方案A（设置 TERM 变量）**:
```bash
export TERM=xterm-256color
lazydocker
```

**方案B（SSH 会话）**:
```bash
# 在 SSH 连接时传递颜色支持
ssh -t user@server "TERM=xterm-256color lazydocker"
```

**方案C**: 在 `~/.config/jesseduffield/lazydocker/config.yml` 中调整主题颜色配置

---

## 功能问题

### 6. 按 `enter` 进入容器失败【中等问题】

**问题描述**: 按 `enter` 尝试进入容器时报错或无响应

**排查步骤**:
```bash
# 1. 确认容器正在运行
docker ps | grep <container-name>

# 2. 手动测试 exec
docker exec -it <container-id> bash

# 3. 尝试 sh（如容器没有 bash）
docker exec -it <container-id> sh
```

**常见原因**:
- 容器没有 bash（仅有 sh）（40%）
- 容器已停止（30%）
- 终端类型不兼容（20%）
- 容器权限限制（10%）

**解决方案**:

**方案A（容器只有 sh）**: 
lazydocker 会自动回退到 sh，但如果失败，可通过自定义命令配置：
```yaml
# 在 config.yml 中添加
customCommands:
  containers:
    - name: sh
      attach: true
      command: docker exec -it {{ .Container.ID }} sh
```

**方案B（容器已停止）**:
先按 `r` 重启容器，确认 status 变为 running 后再按 `enter`

---

### 7. Services 面板为空，无法管理 Compose 服务【中等问题】

**问题描述**: 切换到 Services 面板时为空，或提示"No services found"

**排查步骤**:
```bash
# 1. 确认当前目录包含 Compose 文件
ls docker-compose.yml docker-compose.yaml compose.yml compose.yaml 2>/dev/null

# 2. 验证 Compose 文件格式正确
docker-compose config

# 3. 检查 docker-compose 命令是否可用
docker-compose --version
```

**常见原因**:
- 未在 Compose 项目目录启动 lazydocker（55%）
- Compose 文件命名不标准（25%）
- docker-compose 未安装（20%）

**解决方案**:

**方案A（在正确目录启动）**:
```bash
cd /path/to/your/compose/project
lazydocker
```

**方案B（指定 Compose 文件）**:
```yaml
# 在 config.yml 中指定
commandTemplates:
  dockerCompose: "docker-compose -f /absolute/path/to/docker-compose.yml"
```

**方案C（安装 docker-compose）**:
```bash
# 作为 Docker 插件（推荐）
docker compose version

# 或独立安装
pip install docker-compose
```

---

### 8. 容器日志显示不完整或无法加载【中等问题】

**问题描述**: 日志面板空白，或只显示极少量日志

**排查步骤**:
```bash
# 1. 在终端直接查看日志确认问题
docker logs <container-name>

# 2. 检查配置中的 tail 设置
cat ~/.config/jesseduffield/lazydocker/config.yml | grep tail

# 3. 检查容器日志驱动
docker inspect <container-name> --format '{{.HostConfig.LogConfig.Type}}'
```

**常见原因**:
- 容器使用了非默认日志驱动（如 journald、syslog）（40%）
- tail 配置值过小（30%）
- 容器刚启动无日志（20%）
- 日志文件权限问题（10%）

**解决方案**:

**方案A（调整 tail 配置）**:
```yaml
# 在 config.yml 中修改
logs:
  tail: 500
  since: "24h"
```

**方案B（日志驱动问题）**:
使用非 `json-file` 驱动时，lazydocker 可能无法正常获取日志。
建议将容器日志驱动改回默认：
```yaml
# 在 docker-compose.yml 中
services:
  myapp:
    logging:
      driver: json-file
      options:
        max-size: "10m"
        max-file: "3"
```

---

## 远程连接问题

### 9. 无法连接远程 Docker 主机【复杂问题】

**问题描述**: 设置 `DOCKER_HOST` 后仍无法连接远程 Docker

**排查步骤**:
```bash
# 1. 验证网络连通性
ping remote-server
nc -zv remote-server 2375

# 2. 测试 Docker 远程连接
DOCKER_HOST=tcp://remote-server:2375 docker info

# 3. 检查远程 Docker 是否开启 TCP 监听
ssh user@remote-server "sudo ss -tlnp | grep dockerd"

# 4. 检查防火墙
ssh user@remote-server "sudo ufw status"

# 5. 查看 Docker 守护进程配置
ssh user@remote-server "cat /etc/docker/daemon.json"
```

**常见原因**:
- 远程 Docker 未开启 TCP 监听（40%）
- 防火墙阻挡 2375/2376 端口（30%）
- TLS 证书配置错误（20%）
- 网络连接问题（10%）

**解决方案**:

**方案A（使用 SSH 方式连接，最安全推荐）**:
```bash
# 不需要开启 Docker TCP 端口，通过 SSH 隧道
DOCKER_HOST=ssh://user@remote-server lazydocker
```

**方案B（开启远程 Docker TCP，仅限受信任网络）**:
在远程服务器的 `/etc/docker/daemon.json` 中添加：
```json
{
  "hosts": ["unix:///var/run/docker.sock", "tcp://0.0.0.0:2375"]
}
```
然后重启 Docker: `sudo systemctl restart docker`

**方案C（使用 Docker Context）**:
```bash
docker context create remote --docker "host=ssh://user@remote-server"
docker context use remote
lazydocker
```

---

### 10. lazydocker 内存占用过高【中等问题】

**问题描述**: lazydocker 运行后系统内存占用明显增加，或界面卡顿

**排查步骤**:
```bash
# 检查 lazydocker 进程资源占用
ps aux | grep lazydocker

# 检查容器数量
docker ps -a | wc -l

# 检查日志配置
cat ~/.config/jesseduffield/lazydocker/config.yml
```

**常见原因**:
- 日志 tail 配置值过大（40%）
- 容器数量过多（30%）
- 统计刷新频率过高（20%）
- 日志内容本身体积过大（10%）

**解决方案**:

**方案A（减小日志缓存）**:
```yaml
logs:
  tail: 100
  since: "30m"
```

**方案B（隐藏已停止容器）**:
```yaml
gui:
  showAllContainers: false
```

**方案C（降低统计精度）**:
```yaml
stats:
  maxDuration: 60
```

---

## 获取帮助

### 诊断信息收集

**AI执行说明**: AI 可以帮助收集诊断信息并分析问题

```bash
# 收集环境信息
echo "=== lazydocker 版本 ===" && lazydocker --version
echo "=== Docker 版本 ===" && docker --version
echo "=== Docker 状态 ===" && docker info 2>&1 | head -20
echo "=== 操作系统 ===" && uname -a
echo "=== TERM 设置 ===" && echo "TERM=$TERM, LANG=$LANG"
echo "=== 配置文件 ===" && cat ~/.config/jesseduffield/lazydocker/config.yml 2>/dev/null || echo "(未找到配置文件)"
```

### 参考资源

- GitHub Issues: https://github.com/jesseduffield/lazydocker/issues
- GitHub Discussions: https://github.com/jesseduffield/lazydocker/discussions
- 配置文档: https://github.com/jesseduffield/lazydocker/blob/master/docs/Config.md
- 项目 Wiki: https://github.com/jesseduffield/lazydocker/wiki

---

**提示**: 如遇到本文档未涵盖的问题，请到 GitHub Issues 中搜索或提问，附上诊断信息可获得更快的帮助。
