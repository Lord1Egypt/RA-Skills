# Traefik 配置过程总结

## 初始状态
- 用户请求安装 Traefik 反向代理
- 系统上已运行多个 Docker 容器服务

## 配置步骤

### 1. 创建基础配置

创建 `docker-compose.yml`:
```yaml
- Traefik v3.0 镜像
- 暴露 80 和 443 端口
- 挂载 Docker socket
- 启用 Docker provider 和 File provider
- 启用访问日志和 Prometheus 指标
```

### 2. 创建动态路由配置

创建 `traefik-dynamic.yml`:
- 定义路由规则
- 配置中间件（路径剥离）
- 定义服务后端

### 3. 连接容器到网络

关键步骤：所有需要代理的容器必须连接到 Traefik 的网络
```bash
docker network connect compose_default <container-name>
```

### 4. 路由方案选择

**方案 A: 路径前缀路由**
- 访问方式：`http://192.168.9.192/<service>`
- 优点：单一 IP，易记忆
- 缺点：所有服务共享同一域名

**方案 B: 主机名路由 (.nip.io)**
- 访问方式：`http://<service>.192.168.9.192.nip.io`
- 优点：每个服务独立域名
- 缺点：需要理解 .nip.io 机制

**方案 C: Docker Labels**
- 配置方式：直接在 docker-compose.yml 中添加 labels
- 优点：统一管理，无需额外配置文件
- 适用场景：Traefik Dashboard 等简单路由

### 5. 启用功能特性

启用的功能:
- ✅ API Dashboard - 管理面板
- ✅ Docker Provider - 容器自动发现
- ✅ File Provider - 动态配置文件
- ✅ Access Log - JSON 格式访问日志
- ✅ Traefik Log - DEBUG 级别日志
- ✅ Prometheus Metrics - 监控指标
- ✅ HTTP/HTTPS - 双端口支持

### 6. 最终配置

最终采用方案：
- Traefik Dashboard: Docker Labels + .nip.io
- 其他服务：关闭转发，使用原端口访问

## 常见问题解决

### 问题 1: 404 错误
**原因**: 容器不在同一 Docker 网络
**解决**: `docker network connect compose_default <container>`

### 问题 2: 配置不生效
**原因**: YAML 语法错误或 Traefik 未重载
**解决**: 检查语法，重启 Traefik

### 问题 3: 插件配置错误
**原因**: Traefik v3 不支持命令行插件加载
**解决**: 移除 `--plugins.*` 参数

## 最终状态

Traefik 运行状态:
- 容器名：traefik
- 网络：compose_default
- Dashboard: http://traefik.192.168.9.192.nip.io
- 配置方式：Docker Labels
- 功能：Dashboard, Logging, Metrics 全部启用

其他服务:
- 保持原有端口访问
- 不再通过 Traefik 代理
- 可随时添加 Traefik 路由

## 配置文件位置

- docker-compose.yml: `~/.docker/compose/docker-compose.yml`
- traefik-dynamic.yml: `~/.docker/compose/traefik-dynamic.yml`

## 常用命令

```bash
# 查看 Traefik 日志
docker logs traefik

# 查看已配置路由
docker exec traefik wget -q -O - http://localhost:8080/api/http/routers

# 重启 Traefik
docker restart traefik

# 连接容器到网络
docker network connect compose_default <container-name>

# 断开容器从网络
docker network disconnect compose_default <container-name>
```
