# 高级用法

**适用场景**: 掌握基础操作后，学习配置自定义命令、远程 Docker 管理、集成 Docker Compose 工作流等高级功能

---

## 一、配置文件详解

### 配置文件位置

lazydocker 使用 YAML 格式的配置文件，默认路径为：

- **macOS/Linux**: `~/.config/jesseduffield/lazydocker/config.yml`
- **Windows**: `%APPDATA%\jesseduffield\lazydocker\config.yml`

**AI执行说明**: AI 可以帮助生成和修改配置文件

```bash
# 创建配置目录
mkdir -p ~/.config/jesseduffield/lazydocker

# 创建或编辑配置文件
$EDITOR ~/.config/jesseduffield/lazydocker/config.yml
```

### 基础配置示例

```yaml
# ~/.config/jesseduffield/lazydocker/config.yml

gui:
  # 是否显示所有容器（包括已停止的）
  showAllContainers: false
  # 日志刷新频率（毫秒）
  scrollHeight: 2
  # 语言（目前仅支持英文）
  language: "auto"
  # 边框样式（single/double/rounded）
  border: "single"

logs:
  # 默认显示最后多少行日志
  tail: 200
  # 时间戳格式
  timestamps: false
  # 日志颜色
  since: "60m"

stats:
  # 统计数据展示时间范围（秒）
  maxDuration: 96

commandTemplates:
  # 进入容器的命令模板（可修改）
  dockerCompose: "docker-compose"
  restartService: "docker-compose restart {{ .Service.Name }}"

oS:
  # 终端编辑器（用于查看配置文件）
  editCommand: ""
  editCommandTemplate: "{{.EditCommand}} {{.Filename}}"
  openCommand: "open {{.Filename}}"
```

---

## 二、自定义命令

lazydocker 支持在配置文件中为容器、服务、镜像、卷定义自定义命令。

### 为容器添加自定义命令

**AI执行说明**: AI 可以帮助编写和验证自定义命令配置

```yaml
# 在 config.yml 中添加
customCommands:
  containers:
    - name: bash
      attach: true
      command: docker exec -it {{ .Container.ID }} bash

    - name: sh
      attach: true
      command: docker exec -it {{ .Container.ID }} sh

    - name: 查看环境变量
      attach: false
      command: docker inspect {{ .Container.ID }} --format "{{range .Config.Env}}{{println .}}{{end}}"

    - name: 导出容器
      attach: false
      command: docker export {{ .Container.ID }} > {{ .Container.Name }}.tar

    - name: 查看端口映射
      attach: false
      command: docker port {{ .Container.ID }}
```

### 为镜像添加自定义命令

```yaml
customCommands:
  images:
    - name: 推送镜像到 Registry
      attach: false
      command: docker push {{ .Image.ID }}

    - name: 查看镜像历史
      attach: false
      command: docker history {{ .Image.ID }}

    - name: 以此镜像运行临时容器
      attach: true
      command: docker run --rm -it {{ .Image.ID }} sh
```

### 为服务添加自定义命令

```yaml
customCommands:
  services:
    - name: 查看服务 CPU 占用
      attach: false
      command: docker stats --no-stream $(docker-compose ps -q {{ .Service.Name }})

    - name: 进入服务容器
      attach: true
      command: docker-compose exec {{ .Service.Name }} sh
```

---

## 三、管理远程 Docker

### 通过 TCP 连接远程 Docker

**AI执行说明**: AI 可以帮助配置远程 Docker 连接

```bash
# 方式1：设置环境变量
DOCKER_HOST=tcp://remote-server:2375 lazydocker

# 方式2：使用 TLS 加密连接（推荐生产环境）
DOCKER_HOST=tcp://remote-server:2376 \
DOCKER_TLS_VERIFY=1 \
DOCKER_CERT_PATH=~/.docker/certs \
lazydocker
```

### 通过 SSH 连接远程 Docker（推荐）

```bash
# Docker 23.0+ 支持 SSH 直接连接
DOCKER_HOST=ssh://user@remote-server lazydocker

# 或使用 docker context
docker context create remote --docker "host=ssh://user@remote-server"
docker context use remote
lazydocker
```

### 连接 Docker Desktop（macOS/Windows）

Docker Desktop 通常自动配置，lazydocker 直接启动即可识别。若遇到问题：

```bash
# macOS：指定 socket 路径
DOCKER_HOST=unix:///Users/$(whoami)/.docker/run/docker.sock lazydocker

# 或 colima 用户
DOCKER_HOST=unix:///Users/$(whoami)/.colima/default/docker.sock lazydocker
```

---

## 四、与 Docker Compose 深度集成

### 完整的 Compose 项目工作流

**AI执行说明**: AI 可以在 Compose 目录中执行完整的服务生命周期管理

```bash
# 进入项目目录
cd /path/to/project

# 启动 lazydocker（自动识别 docker-compose.yml 或 compose.yml）
lazydocker
```

### Compose 服务操作

在 **Services** 面板中可以执行的操作：

| 按键 | 功能 | 说明 |
|------|------|------|
| `u` | 拉取并启动服务 | 等同于 `docker-compose pull && docker-compose up -d` |
| `s` | 停止服务 | 等同于 `docker-compose stop <service>` |
| `r` | 重启服务 | 等同于 `docker-compose restart <service>` |
| `d` | 删除服务容器 | 等同于 `docker-compose rm -f <service>` |
| `l` | 查看服务日志 | 流式跟踪服务输出 |
| `e` | 编辑 compose 文件 | 在配置的编辑器中打开 |
| `x` | 显示命令菜单 | 查看所有可用操作 |

### 指定 Compose 文件路径

```yaml
# 在 config.yml 中指定
commandTemplates:
  dockerCompose: "docker-compose -f /path/to/docker-compose.yml"
```

---

## 五、日志高级操作

### 日志筛选与搜索

在日志面板中：
- 按 `/` 进入搜索模式，输入关键词高亮匹配行
- 按 `n` 跳转到下一个匹配
- 按 `N` 跳转到上一个匹配
- 按 `Esc` 退出搜索模式

### 配置日志行为

```yaml
logs:
  # 默认显示最后 N 行
  tail: 200
  # 显示时间戳
  timestamps: true
  # 显示最近多少时间内的日志（空字符串表示全部）
  since: "60m"
```

### 保存日志到文件

**AI执行说明**: AI 可以帮助提取和保存容器日志

```bash
# 在终端（非 lazydocker 中）保存日志
docker logs <container-name> > container.log 2>&1

# 保存最近 1000 行
docker logs --tail 1000 <container-name> > container.log 2>&1

# 保存特定时间段的日志
docker logs --since "2024-01-01T00:00:00" --until "2024-01-02T00:00:00" <container-name> > container.log
```

---

## 六、批量清理操作

### 清理无用资源

**AI执行说明**: AI 可以帮助识别并清理占用空间的无用 Docker 资源

在 lazydocker 中，可通过 `x` 键菜单执行系统清理：

- 删除所有已停止容器：在容器列表中按 `x`，选择 prune 选项
- 删除未使用的镜像：在镜像列表中按 `x`，选择 prune
- 删除未使用的卷：在卷列表中按 `x`，选择 prune

或在终端中执行：

```bash
# 清理所有未使用资源（容器、镜像、网络、构建缓存）
docker system prune

# 同时清理未使用的卷
docker system prune --volumes

# 查看磁盘使用情况
docker system df
```

---

## 七、主题与外观定制

### 颜色主题配置

```yaml
gui:
  theme:
    # 活跃边框颜色
    activeBorderColor:
      - white
      - bold
    # 非活跃边框颜色
    inactiveBorderColor:
      - cyan
    # 已选项目颜色
    selectedLineBgColor:
      - blue
    # 运行中容器颜色
    activeBackgroundColor:
      - bold
```

### 边框样式

```yaml
gui:
  # 边框样式：single / double / rounded / hidden
  border: "rounded"
```

---

## 八、键盘快捷键完整参考

在任意面板按 `?` 可查看当前上下文的快捷键帮助。

### 全局快捷键

| 按键 | 功能 |
|------|------|
| `q` | 退出 lazydocker |
| `?` | 显示帮助 |
| `x` | 显示当前面板的命令菜单 |
| `1` ~ `5` | 跳转到对应面板 |
| `[` / `]` | 切换面板标签 |
| `ctrl+c` | 退出 lazydocker |

### 容器面板快捷键

| 按键 | 功能 |
|------|------|
| `enter` | 进入容器（exec -it bash/sh） |
| `s` | 停止容器 |
| `r` | 重启容器 |
| `d` | 删除容器 |
| `a` | 附加到容器（attach） |
| `m` | 查看容器挂载信息 |
| `e` | 打开 env 文件 |
| `l` | 查看日志 |
| `f` | 开关日志跟随模式 |

### 镜像面板快捷键

| 按键 | 功能 |
|------|------|
| `d` | 删除镜像 |
| `x` | 显示命令菜单（prune 等） |

---

## 完成确认

### 检查清单
- [ ] 了解配置文件位置和基本结构
- [ ] 能够添加自定义命令
- [ ] 能够连接远程 Docker
- [ ] 掌握 Compose 服务完整管理流程
- [ ] 能够使用日志搜索功能
- [ ] 了解批量清理操作

### 下一步
如遇到问题，查看 [常见问题](../troubleshooting.md)
