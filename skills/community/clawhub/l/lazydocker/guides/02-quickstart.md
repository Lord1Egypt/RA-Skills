# 快速开始

**适用场景**: 已安装 lazydocker，需要快速掌握基本操作——查看容器状态、查看日志、管理镜像

---

## 一、启动 lazydocker

### 基本启动

**AI执行说明**: AI 会先确认 Docker 守护进程状态，再启动 lazydocker

```bash
# 确认 Docker 正在运行
docker ps

# 启动 lazydocker
lazydocker
```

成功启动后，你将看到一个三列布局的 TUI 界面：
- 顶部：面板标签栏（Containers / Services / Images / Volumes / Networks）
- 左侧：当前面板的项目列表
- 右侧：选中项目的详细信息（Logs / Stats / Config / Env / Exec 等子标签）
- 底部：状态栏（当前按键提示和状态信息）

### 在 Docker Compose 项目中启动

```bash
# 进入包含 docker-compose.yml 的目录
cd /path/to/your/project

# 启动 lazydocker（自动识别 Compose 服务）
lazydocker
```

此时 **Services** 面板将展示 Compose 定义的所有服务。

---

## 二、界面导航基础

### 面板切换

| 按键 | 功能 |
|------|------|
| `[` | 切换到左侧的面板标签 |
| `]` | 切换到右侧的面板标签 |
| `1` | 跳转到 Containers 面板 |
| `2` | 跳转到 Services 面板 |
| `3` | 跳转到 Images 面板 |
| `4` | 跳转到 Volumes 面板 |
| `5` | 跳转到 Networks 面板 |

### 列表导航

| 按键 | 功能 |
|------|------|
| `↑` / `k` | 向上移动 |
| `↓` / `j` | 向下移动 |
| `PgUp` | 向上翻页 |
| `PgDn` | 向下翻页 |
| `Home` / `g` | 跳转到列表顶部 |
| `End` / `G` | 跳转到列表底部 |

### 右侧详情面板切换

| 按键 | 功能 |
|------|------|
| `←` / `h` | 切换到左侧详情标签 |
| `→` / `l` | 切换到右侧详情标签 |

---

## 三、容器管理基本操作

### 查看所有容器

启动 lazydocker 后默认进入 **Containers** 面板，显示所有容器（包括已停止的）：

```
容器列表示例：
  NAME           STATUS    IMAGE              PORTS
  web-app        running   nginx:latest       0.0.0.0:80->80/tcp
  db             running   postgres:15        5432/tcp
  redis-cache    exited    redis:7.0
```

状态颜色：
- 绿色：运行中（running）
- 红色：已停止（exited）
- 黄色：正在启动/停止（starting/stopping）

### 查看容器日志

**AI执行说明**: AI 可以帮助解读日志内容

1. 在 Containers 面板选中目标容器（`↑`/`↓` 导航）
2. 右侧面板默认显示日志（Logs 标签）
3. 或按 `→` 切换到 Logs 标签

日志面板内的操作：
- 日志自动跟随最新输出（tail 模式）
- 按 `f` 可以切换跟随/暂停
- 按 `/` 可以在日志中搜索
- 按 `ctrl+c` 可以停止日志流

### 停止容器

```
1. 在 Containers 面板选中运行中的容器
2. 按 s 键
3. 确认停止操作
```

### 重启容器

```
1. 在 Containers 面板选中容器
2. 按 r 键
3. 容器将重启，状态从 exited → running
```

### 删除容器

```
1. 在 Containers 面板选中已停止的容器
2. 按 d 键
3. 确认删除
```

**注意**: 删除运行中的容器需要先停止，或强制删除（会提示）。

---

## 四、查看容器统计信息

**AI执行说明**: AI 可以帮助分析资源使用情况

1. 在 Containers 面板选中运行中的容器
2. 按 `→` 切换右侧面板到 **Stats** 标签
3. 实时查看资源占用：

```
CPU 使用率:  0.35%
内存使用量:  128.5 MiB / 3.84 GiB (3.27%)
网络 I/O:   In: 1.2 kB  Out: 3.4 kB
块 I/O:     Read: 0 B   Write: 12.3 MB
进程数:      5
```

---

## 五、进入容器终端

**AI执行说明**: AI 可以帮助在容器中执行命令

1. 在 Containers 面板选中运行中的容器
2. 按 `enter` 键进入容器终端（自动尝试 bash，失败则回退到 sh）
3. 执行你需要的命令
4. 按 `exit` 或 `ctrl+d` 退出容器终端，返回 lazydocker

---

## 六、镜像管理基本操作

### 查看本地镜像

1. 按 `]` 或 `3` 切换到 **Images** 面板
2. 查看所有本地镜像列表：

```
镜像列表示例：
  REPOSITORY      TAG       IMAGE ID       CREATED        SIZE
  nginx           latest    abc123def456   2 days ago     188MB
  postgres        15        def456ghi789   1 week ago     412MB
  redis           7.0       ghi789jkl012   3 weeks ago    117MB
```

### 删除镜像

```
1. 在 Images 面板选中要删除的镜像
2. 按 d 键
3. 确认删除（如有容器使用该镜像，会提示强制删除）
```

---

## 七、卷管理基本操作

### 查看 Docker 卷

1. 按 `]` 或 `4` 切换到 **Volumes** 面板
2. 查看所有卷：

```
卷列表示例：
  NAME                        DRIVER    SIZE
  postgres_data               local     256MB
  redis_data                  local     12MB
  myapp_uploads               local     1.2GB
```

### 删除未使用的卷

```
1. 在 Volumes 面板选中要删除的卷
2. 按 d 键
3. 确认删除（注意：卷数据将永久丢失）
```

---

## 八、Docker Compose 服务管理

**AI执行说明**: 需在包含 docker-compose.yml 的目录中启动 lazydocker

### 查看服务状态

1. 按 `]` 或 `2` 切换到 **Services** 面板
2. 查看所有 Compose 服务状态

### 管理 Compose 服务

| 按键 | 功能 |
|------|------|
| `u` | 拉取最新镜像并重新创建服务（up） |
| `s` | 停止服务（stop） |
| `r` | 重启服务（restart） |
| `d` | 删除服务容器（down） |
| `l` | 查看服务日志 |
| `x` | 显示所有可用命令 |

---

## 九、常用操作速查

| 场景 | 操作 |
|------|------|
| 查看所有容器 | 启动 lazydocker，默认进入容器面板 |
| 查看容器日志 | 选中容器 → 右侧 Logs 标签 |
| 实时查看资源 | 选中容器 → 右侧 Stats 标签 |
| 进入容器 shell | 选中运行中容器 → 按 `enter` |
| 重启容器 | 选中容器 → 按 `r` |
| 停止容器 | 选中容器 → 按 `s` |
| 删除容器/镜像/卷 | 选中对象 → 按 `d` |
| 查看帮助 | 按 `?` |
| 退出 | 按 `q` |

---

## 完成确认

### 检查清单
- [ ] 成功启动 lazydocker 界面
- [ ] 能够在不同面板之间切换
- [ ] 能够查看容器日志
- [ ] 能够查看容器资源统计
- [ ] 能够执行停止/重启/删除操作

### 下一步
继续阅读 [高级用法](03-advanced-usage.md) 学习自定义命令、配置文件等高级特性
