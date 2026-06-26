# 容器管理参考文档

> 覆盖 Docker/Podman 容器生命周期、镜像构建、Docker Compose、容器网络/存储、安全加固、日志监控与故障排查。

---

## 目录

- [1. 容器基础](#1-容器基础)
- [2. 镜像管理](#2-镜像管理)
- [3. 容器生命周期](#3-容器生命周期)
- [4. Dockerfile 最佳实践](#4-dockerfile-最佳实践)
- [5. Docker Compose](#5-docker-compose)
- [6. 容器网络](#6-容器网络)
- [7. 容器存储](#7-容器存储)
- [8. 容器安全](#8-容器安全)
- [9. Podman](#9-podman)
- [10. 日志与监控](#10-日志与监控)
- [11. 容器编排基础](#11-容器编排基础)
- [12. 故障排查](#12-故障排查)

---

## 1. 容器基础

### 1.1 安装 Docker

```bash
# Ubuntu/Debian
curl -fsSL https://get.docker.com | bash
# 或手动安装
apt-get update
apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# RHEL/CentOS
dnf config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
dnf install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# 启动并设置开机自启
systemctl enable --now docker

# 非 root 用户使用 Docker
usermod -aG docker $USER
newgrp docker

# 验证
docker version
docker info
docker run hello-world
```

### 1.2 Docker 守护进程配置

```json
// /etc/docker/daemon.json
{
  "storage-driver": "overlay2",
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "50m",
    "max-file": "3"
  },
  "default-address-pools": [
    {"base": "172.17.0.0/12", "size": 24}
  ],
  "registry-mirrors": [
    "https://mirror.ccs.tencentyun.com"
  ],
  "insecure-registries": [],
  "live-restore": true,
  "default-ulimits": {
    "nofile": {
      "Name": "nofile",
      "Hard": 65536,
      "Soft": 65536
    }
  },
  "metrics-addr": "127.0.0.1:9323",
  "experimental": false
}
```

```bash
# 重载配置
systemctl daemon-reload
systemctl restart docker
```

### 1.3 核心概念

```text
Docker 架构
├── Docker Client (docker CLI)
│   └── 通过 REST API 与 Daemon 通信
├── Docker Daemon (dockerd)
│   ├── 管理容器、镜像、网络、卷
│   └── 通过 containerd 管理容器运行时
├── containerd
│   └── 容器运行时（OCI 标准）
├── runc
│   └── 底层容器创建（Linux namespace + cgroup）
├── Image（镜像）
│   └── 分层只读文件系统（Union FS）
├── Container（容器）
│   └── 镜像 + 可写层 + 运行时配置
├── Network（网络）
│   └── bridge / host / overlay / macvlan / none
└── Volume（卷）
    └── 数据持久化（bind mount / named volume / tmpfs）
```

---

## 2. 镜像管理

### 2.1 基本操作

```bash
# 搜索镜像
docker search nginx

# 拉取镜像
docker pull nginx:1.25-alpine
docker pull registry.example.com/myapp:v2.1.0

# 列出本地镜像
docker images
docker images --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}"

# 查看镜像详情
docker inspect nginx:1.25-alpine
docker history nginx:1.25-alpine

# 标记镜像
docker tag myapp:latest registry.example.com/myapp:v2.1.0

# 推送镜像
docker login registry.example.com
docker push registry.example.com/myapp:v2.1.0

# 导出/导入镜像
docker save -o nginx.tar nginx:1.25-alpine
docker load -i nginx.tar

# 清理未使用镜像
docker image prune -a              # 删除所有未使用的镜像
docker system prune -a --volumes   # 全面清理（镜像+容器+网络+卷）
```

### 2.2 多阶段构建

```dockerfile
# 构建阶段
FROM golang:1.22-alpine AS builder
WORKDIR /app
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -ldflags="-s -w" -o /server ./cmd/server

# 运行阶段
FROM alpine:3.19
RUN apk --no-cache add ca-certificates tzdata \
    && adduser -D -u 1000 appuser
COPY --from=builder /server /usr/local/bin/server
USER appuser
EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD wget -qO- http://localhost:8080/health || exit 1
ENTRYPOINT ["server"]
```

### 2.3 私有 Registry

```bash
# 部署私有 Registry
docker run -d --name registry \
  -p 5000:5000 \
  -v /opt/registry/data:/var/lib/registry \
  -v /opt/registry/auth:/auth \
  -e "REGISTRY_AUTH=htpasswd" \
  -e "REGISTRY_AUTH_HTPASSWD_REALM=Registry" \
  -e "REGISTRY_AUTH_HTPASSWD_PATH=/auth/htpasswd" \
  --restart=always \
  registry:2

# 创建认证文件
docker run --rm --entrypoint htpasswd registry:2 -Bbn admin password > /opt/registry/auth/htpasswd

# 配置 TLS
# 将证书放到 /opt/registry/certs/
# 添加 -v /opt/registry/certs:/certs 和 TLS 环境变量

# Harbor（企业级 Registry）
# 下载安装包：https://github.com/goharbor/harbor/releases
wget https://github.com/goharbor/harbor/releases/download/v2.10.0/harbor-online-installer-v2.10.0.tgz
tar xzf harbor-online-installer-v2.10.0.tgz
cd harbor
cp harbor.yml.tmpl harbor.yml
# 编辑 harbor.yml 配置域名、端口、密码等
./install.sh --with-trivy  # 带漏洞扫描
```

---

## 3. 容器生命周期

### 3.1 运行容器

```bash
# 基本运行
docker run -d --name myapp \
  -p 8080:80 \
  -v /data/app:/app/data \
  -e "ENV=production" \
  -e "DB_HOST=db01" \
  --restart=unless-stopped \
  --memory=512m \
  --cpus=1.0 \
  myapp:v2.1.0

# 交互模式
docker run -it --rm ubuntu:22.04 /bin/bash

# 后台运行 + 日志
docker run -d --name web \
  --log-driver=json-file \
  --log-opt max-size=50m \
  --log-opt max-file=3 \
  nginx:1.25-alpine
```

### 3.2 容器管理

```bash
# 列出容器
docker ps                    # 运行中的
docker ps -a                 # 所有（含已停止）
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

# 启停容器
docker start myapp
docker stop myapp            # 优雅停止（SIGTERM，10s 后 SIGKILL）
docker stop -t 30 myapp      # 自定义超时
docker restart myapp
docker kill myapp            # 强制停止（SIGKILL）

# 进入容器
docker exec -it myapp /bin/sh
docker exec -it myapp bash
docker exec myapp cat /etc/hostname

# 查看日志
docker logs myapp
docker logs -f --tail 100 myapp           # 实时跟踪最后 100 行
docker logs --since 1h myapp              # 最近 1 小时

# 查看资源使用
docker stats
docker stats --no-stream --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}"

# 查看容器详情
docker inspect myapp
docker inspect --format '{{.State.Status}}' myapp
docker inspect --format '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' myapp

# 容器内文件操作
docker cp myapp:/app/config.yaml ./config.yaml
docker cp ./config.yaml myapp:/app/config.yaml

# 查看变更
docker diff myapp

# 提交为新镜像
docker commit myapp myapp:debug-snapshot

# 删除容器
docker rm myapp
docker rm -f myapp           # 强制删除（含运行中）
docker container prune       # 删除所有已停止容器
```

### 3.3 资源限制

```bash
# 内存限制
docker run -d --name app \
  --memory=1g \
  --memory-swap=2g \
  --memory-reservation=512m \
  --oom-kill-disable=false \
  myapp:latest

# CPU 限制
docker run -d --name app \
  --cpus=2.0 \
  --cpu-shares=1024 \
  --cpuset-cpus="0,1" \
  myapp:latest

# I/O 限制
docker run -d --name app \
  --device-read-bps /dev/sda:100mb \
  --device-write-bps /dev/sda:50mb \
  myapp:latest

# 更新运行中容器的限制
docker update --memory=2g --cpus=4.0 myapp
```

---

## 4. Dockerfile 最佳实践

### 4.1 优化原则

```dockerfile
# ✅ 好的 Dockerfile
FROM python:3.12-slim AS base

# 1. 使用非 root 用户
RUN groupadd -r app && useradd -r -g app -d /app -s /sbin/nologin app

# 2. 合并 RUN 层，减少镜像大小
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       curl \
       ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# 3. 利用构建缓存：先复制依赖文件
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. 最后复制应用代码
COPY --chown=app:app . .

# 5. 使用 HEALTHCHECK
HEALTHCHECK --interval=30s --timeout=3s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

# 6. 切换用户
USER app

# 7. 明确暴露端口
EXPOSE 8000

# 8. 使用 exec 形式（非 shell 形式）
ENTRYPOINT ["python", "-m", "uvicorn", "main:app"]
CMD ["--host", "0.0.0.0", "--port", "8000"]
```

### 4.2 .dockerignore

```text
# .dockerignore
.git
.gitignore
.env
.env.*
*.md
!README.md
Dockerfile*
docker-compose*
.dockerignore
__pycache__
*.pyc
node_modules
.vscode
.idea
tests/
docs/
*.log
```

### 4.3 安全扫描

```bash
# Trivy 漏洞扫描
trivy image myapp:latest
trivy image --severity HIGH,CRITICAL myapp:latest

# Docker Scout
docker scout cves myapp:latest
docker scout recommendations myapp:latest

# Hadolint（Dockerfile 检查）
hadolint Dockerfile
```

---

## 5. Docker Compose

### 5.1 基本配置

```yaml
# docker-compose.yaml（Compose v2 格式）
name: myproject

services:
  web:
    build:
      context: .
      dockerfile: Dockerfile
      args:
        APP_VERSION: "2.1.0"
    image: myapp:latest
    container_name: myapp-web
    ports:
      - "8080:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/mydb
      - REDIS_URL=redis://redis:6379/0
    env_file:
      - .env
    volumes:
      - app-data:/app/data
      - ./config:/app/config:ro
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_started
    deploy:
      resources:
        limits:
          cpus: '2.0'
          memory: 1G
        reservations:
          cpus: '0.5'
          memory: 256M
      replicas: 2
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 5s
      retries: 3
      start_period: 10s
    networks:
      - frontend
      - backend
    logging:
      driver: json-file
      options:
        max-size: "50m"
        max-file: "3"

  db:
    image: postgres:16-alpine
    container_name: myapp-db
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD_FILE: /run/secrets/db_password
      POSTGRES_DB: mydb
    volumes:
      - db-data:/var/lib/postgresql/data
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql:ro
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U user -d mydb"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - backend
    secrets:
      - db_password

  redis:
    image: redis:7-alpine
    container_name: myapp-redis
    command: redis-server --appendonly yes --maxmemory 256mb --maxmemory-policy allkeys-lru
    volumes:
      - redis-data:/data
    ports:
      - "6379:6379"
    networks:
      - backend

  nginx:
    image: nginx:1.25-alpine
    container_name: myapp-nginx
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./certs:/etc/nginx/ssl:ro
    depends_on:
      - web
    networks:
      - frontend

volumes:
  app-data:
    driver: local
  db-data:
    driver: local
  redis-data:
    driver: local

networks:
  frontend:
    driver: bridge
  backend:
    driver: bridge
    internal: true    # 仅内部通信

secrets:
  db_password:
    file: ./secrets/db_password.txt
```

### 5.2 Compose 命令

```bash
# 启动服务
docker compose up -d
docker compose up -d --build          # 重新构建

# 查看状态
docker compose ps
docker compose logs -f web
docker compose top

# 扩缩容
docker compose up -d --scale web=3

# 停止服务
docker compose stop
docker compose down                   # 停止并删除容器/网络
docker compose down -v                # 同时删除卷

# 执行命令
docker compose exec web bash
docker compose run --rm web python manage.py migrate

# 配置验证
docker compose config                 # 验证并输出合并后的配置

# 拉取最新镜像
docker compose pull
```

### 5.3 多环境配置

```yaml
# docker-compose.override.yaml（开发环境，自动加载）
services:
  web:
    build:
      target: development
    volumes:
      - .:/app                        # 热重载
    environment:
      - DEBUG=true
    ports:
      - "5678:5678"                   # 调试端口
```

```bash
# 生产环境
docker compose -f docker-compose.yaml -f docker-compose.prod.yaml up -d
```

---

## 6. 容器网络

### 6.1 网络驱动

```bash
# 列出网络
docker network ls

# 创建自定义网络
docker network create --driver bridge \
  --subnet=172.20.0.0/16 \
  --gateway=172.20.0.1 \
  mynet

# 容器连接到网络
docker network connect mynet myapp
docker network disconnect mynet myapp

# 查看网络详情
docker network inspect mynet
```

### 6.2 网络模式

```bash
# Bridge（默认）— 容器间通过虚拟网桥通信
docker run -d --network bridge --name web nginx

# Host — 共享宿主机网络栈（性能最佳）
docker run -d --network host --name web nginx

# None — 无网络
docker run -d --network none --name isolated alpine

# Container — 共享其他容器的网络栈
docker run -d --name sidecar --network container:web busybox

# Macvlan — 容器获得独立 MAC 地址（直连物理网络）
docker network create -d macvlan \
  --subnet=192.168.1.0/24 \
  --gateway=192.168.1.1 \
  -o parent=eth0 \
  macnet
```

### 6.3 DNS 与服务发现

```bash
# 自定义网络中的容器自动 DNS 解析
docker network create app-net
docker run -d --name db --network app-net postgres:16
docker run -d --name web --network app-net myapp
# web 容器中可以直接用 "db" 作为主机名连接数据库

# 自定义 DNS
docker run --dns 8.8.8.8 --dns-search example.com myapp
```

---

## 7. 容器存储

### 7.1 存储类型

```bash
# Named Volume（推荐用于数据持久化）
docker volume create mydata
docker run -v mydata:/app/data myapp

# Bind Mount（开发环境映射源码）
docker run -v /host/path:/container/path myapp
docker run -v $(pwd):/app:ro myapp                    # 只读

# tmpfs（内存文件系统，敏感数据）
docker run --tmpfs /tmp:rw,noexec,nosuid,size=100m myapp

# 卷管理
docker volume ls
docker volume inspect mydata
docker volume rm mydata
docker volume prune                   # 删除未使用的卷
```

### 7.2 备份与恢复

```bash
# 备份卷
docker run --rm -v mydata:/data -v $(pwd):/backup alpine \
  tar czf /backup/mydata-$(date +%Y%m%d).tar.gz -C /data .

# 恢复卷
docker run --rm -v mydata:/data -v $(pwd):/backup alpine \
  tar xzf /backup/mydata-20260401.tar.gz -C /data
```

---

## 8. 容器安全

### 8.1 安全基线

```bash
# 1. 使用非 root 用户运行
docker run --user 1000:1000 myapp

# 2. 只读根文件系统
docker run --read-only --tmpfs /tmp myapp

# 3. 删除所有 capabilities，按需添加
docker run --cap-drop=ALL --cap-add=NET_BIND_SERVICE myapp

# 4. 禁止提权
docker run --security-opt=no-new-privileges myapp

# 5. 限制系统调用（seccomp）
docker run --security-opt seccomp=profile.json myapp

# 6. AppArmor 配置
docker run --security-opt apparmor=docker-custom myapp

# 7. 资源限制
docker run --memory=512m --cpus=1.0 --pids-limit=100 myapp
```

### 8.2 Docker Bench Security

```bash
# 运行 CIS Docker Benchmark 检查
docker run --rm --net host --pid host \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v /etc:/etc:ro \
  -v /usr/lib/systemd:/usr/lib/systemd:ro \
  -v /var/lib:/var/lib:ro \
  docker/docker-bench-security
```

### 8.3 镜像签名与信任

```bash
# Docker Content Trust（DCT）
export DOCKER_CONTENT_TRUST=1
docker pull nginx:latest      # 只拉取签名镜像
docker push myapp:v1.0        # 自动签名

# Cosign 签名
cosign sign --key cosign.key registry.example.com/myapp:v1.0
cosign verify --key cosign.pub registry.example.com/myapp:v1.0
```

---

## 9. Podman

### 9.1 Podman vs Docker

```text
| 特性 | Docker | Podman |
|------|--------|--------|
| 守护进程 | 需要 dockerd | 无守护进程（daemonless） |
| Root 权限 | 默认需要 | 原生 rootless |
| 兼容性 | Docker CLI | 兼容 Docker CLI |
| Pod 支持 | 无原生支持 | 原生 Pod（类 K8s） |
| Systemd | 需额外配置 | 原生集成 |
| Compose | docker compose | podman-compose / podman compose |
```

### 9.2 Podman 常用操作

```bash
# 安装
dnf install -y podman podman-compose

# 基本命令（与 Docker 兼容）
podman run -d --name web -p 8080:80 nginx:alpine
podman ps
podman logs web
podman exec -it web sh

# Pod 管理（类 K8s Pod）
podman pod create --name mypod -p 8080:80
podman run -d --pod mypod --name web nginx:alpine
podman run -d --pod mypod --name sidecar busybox sleep infinity
podman pod ps
podman pod stop mypod

# 生成 systemd 服务
podman generate systemd --new --name web > ~/.config/systemd/user/container-web.service
systemctl --user daemon-reload
systemctl --user enable --now container-web

# 生成 Kubernetes YAML
podman generate kube mypod > mypod.yaml
podman play kube mypod.yaml    # 从 K8s YAML 创建 Pod

# Rootless 配置
loginctl enable-linger $USER
echo "net.ipv4.ip_unprivileged_port_start=80" >> /etc/sysctl.conf
sysctl --system
```

---

## 10. 日志与监控

### 10.1 日志管理

```bash
# 查看日志
docker logs --tail 100 -f myapp
docker logs --since "2026-04-01T00:00:00" myapp

# 日志驱动配置
# json-file（默认）、syslog、journald、fluentd、gelf、awslogs

# Fluentd 日志收集
docker run -d --name web \
  --log-driver=fluentd \
  --log-opt fluentd-address=localhost:24224 \
  --log-opt tag="docker.{{.Name}}" \
  myapp:latest
```

### 10.2 监控

```bash
# 实时资源监控
docker stats
docker stats --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.NetIO}}\t{{.BlockIO}}"

# cAdvisor（容器级监控）
docker run -d --name cadvisor \
  -p 8088:8080 \
  -v /:/rootfs:ro \
  -v /var/run:/var/run:ro \
  -v /sys:/sys:ro \
  -v /var/lib/docker:/var/lib/docker:ro \
  gcr.io/cadvisor/cadvisor:latest

# Prometheus + cAdvisor + Grafana 监控栈
# prometheus.yml 添加 cAdvisor target
# - job_name: 'cadvisor'
#   static_configs:
#     - targets: ['cadvisor:8080']
```

---

## 11. 容器编排基础

### 11.1 Docker Swarm

```bash
# 初始化 Swarm
docker swarm init --advertise-addr 192.168.1.10

# 加入 Worker 节点
docker swarm join --token SWMTKN-xxx 192.168.1.10:2377

# 部署服务
docker service create --name web \
  --replicas 3 \
  --publish 80:80 \
  --update-delay 10s \
  --update-parallelism 1 \
  --rollback-parallelism 1 \
  nginx:alpine

# 服务管理
docker service ls
docker service ps web
docker service scale web=5
docker service update --image nginx:1.25-alpine web
docker service rollback web

# Stack 部署
docker stack deploy -c docker-compose.yaml mystack
docker stack ls
docker stack ps mystack
docker stack rm mystack
```

### 11.2 Kubernetes 基础

```bash
# kubectl 常用命令
kubectl get pods -A
kubectl get svc,deploy,rs -n myapp
kubectl describe pod myapp-xxx
kubectl logs -f myapp-xxx -c main
kubectl exec -it myapp-xxx -- /bin/sh

# 部署应用
kubectl apply -f deployment.yaml
kubectl rollout status deployment/myapp
kubectl rollout undo deployment/myapp

# 扩缩容
kubectl scale deployment myapp --replicas=5
kubectl autoscale deployment myapp --min=2 --max=10 --cpu-percent=80
```

```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
  labels:
    app: myapp
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  template:
    metadata:
      labels:
        app: myapp
    spec:
      containers:
        - name: myapp
          image: registry.example.com/myapp:v2.1.0
          ports:
            - containerPort: 8080
          resources:
            requests:
              cpu: 250m
              memory: 256Mi
            limits:
              cpu: 1000m
              memory: 512Mi
          livenessProbe:
            httpGet:
              path: /health
              port: 8080
            initialDelaySeconds: 10
            periodSeconds: 10
          readinessProbe:
            httpGet:
              path: /ready
              port: 8080
            initialDelaySeconds: 5
            periodSeconds: 5
          env:
            - name: DATABASE_URL
              valueFrom:
                secretKeyRef:
                  name: myapp-secrets
                  key: database-url
      imagePullSecrets:
        - name: regcred
---
apiVersion: v1
kind: Service
metadata:
  name: myapp
spec:
  selector:
    app: myapp
  ports:
    - port: 80
      targetPort: 8080
  type: ClusterIP
```

---

## 12. 故障排查

### 12.1 容器无法启动

```bash
# 查看容器状态和退出码
docker ps -a --filter "name=myapp"
docker inspect --format '{{.State.ExitCode}}' myapp
# 退出码：0=正常, 1=应用错误, 137=OOM Kill, 139=段错误, 143=SIGTERM

# 查看日志
docker logs myapp 2>&1 | tail -50

# 检查资源限制
docker inspect --format '{{.HostConfig.Memory}}' myapp
dmesg | grep -i "oom\|kill"

# 以交互模式调试
docker run -it --entrypoint /bin/sh myapp:latest
```

### 12.2 网络问题

```bash
# 检查容器网络
docker inspect --format '{{json .NetworkSettings.Networks}}' myapp | jq

# 容器内网络诊断
docker exec myapp ping db
docker exec myapp nslookup db
docker exec myapp curl -v http://web:8080/health

# 检查端口映射
docker port myapp
iptables -t nat -L -n | grep DNAT

# 网络抓包
docker run --rm --net container:myapp nicolaka/netshoot tcpdump -i any -nn port 80
```

### 12.3 存储问题

```bash
# 检查磁盘使用
docker system df
docker system df -v

# 查看容器内磁盘
docker exec myapp df -h

# 清理
docker system prune -a --volumes
docker volume prune
docker builder prune
```

### 12.4 性能问题

```bash
# 实时监控
docker stats myapp --no-stream

# 容器内进程
docker top myapp
docker exec myapp ps aux

# CPU 限流检查
cat /sys/fs/cgroup/cpu/docker/$(docker inspect --format '{{.Id}}' myapp)/cpu.stat

# 使用 nsenter 进入容器网络命名空间
PID=$(docker inspect --format '{{.State.Pid}}' myapp)
nsenter -t $PID -n ss -tlnp
nsenter -t $PID -n ip addr
```
