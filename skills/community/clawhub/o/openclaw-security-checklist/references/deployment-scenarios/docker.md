# Docker 部署检查清单

**适用场景**: 使用 Docker/Docker Compose 部署 OpenClaw

## 前置要求

- [ ] Docker 20.10+ (`docker --version`)
- [ ] Docker Compose 2.0+ (`docker compose version`)
- [ ] 至少 4GB 可用内存
- [ ] 至少 10GB 可用存储

## 安全检查项

### 1. Docker 守护进程安全

- [ ] **启用 Docker TLS 认证**
  ```bash
  # 生成 CA 证书
  mkdir -p ~/docker-certs
  cd ~/docker-certs
  openssl genrsa -aes256 -out ca-key.pem 4096
  openssl req -new -x509 -days 365 -key ca-key.pem -sha256 -out ca.pem
  
  # 生成服务器证书
  openssl genrsa -out server-key.pem 4096
  openssl req -subj "/CN=$(hostname)" -sha256 -new -key server-key.pem -out server.csr
  openssl x509 -req -days 365 -sha256 -in server.csr -CA ca.pem -CAkey ca-key.pem \
    -CAcreateserial -out server-cert.pem -extfile <(echo "subjectAltName=DNS:$(hostname),IP:127.0.0.1")
  
  # 配置 Docker 守护进程
  sudo vim /etc/docker/daemon.json
  ```
  
  ```json
  {
    "tls": true,
    "tlsverify": true,
    "tlscacert": "/home/user/docker-certs/ca.pem",
    "tlscert": "/home/user/docker-certs/server-cert.pem",
    "tlskey": "/home/user/docker-certs/server-key.pem",
    "hosts": ["tcp://0.0.0.0:2376"]
  }
  ```

- [ ] **限制 Docker API 访问**
  ```bash
  # 仅监听本地 socket（推荐）
  # /etc/docker/daemon.json
  {
    "hosts": ["unix:///var/run/docker.sock"]
  }
  
  # 如必须远程访问，使用 SSH 隧道
  ssh -L 2375:localhost:2375 user@docker-host
  ```

- [ ] **启用 Docker 内容信任**
  ```bash
  # 启用镜像签名验证
  export DOCKER_CONTENT_TRUST=1
  
  # 添加到 ~/.bashrc 永久生效
  echo "export DOCKER_CONTENT_TRUST=1" >> ~/.bashrc
  ```

### 2. 容器安全

- [ ] **使用非 root 用户运行容器**
  ```dockerfile
  # Dockerfile 示例
  FROM node:18-alpine
  
  # 创建非 root 用户
  RUN addgroup -g 1001 openclaw && \
      adduser -u 1001 -G openclaw -s /bin/sh -D openclaw
  
  USER openclaw
  
  WORKDIR /home/openclaw
  COPY --chown=openclaw:openclaw . .
  
  CMD ["node", "server.js"]
  ```

- [ ] **限制容器资源**
  ```yaml
  # docker-compose.yml
  services:
    openclaw:
      image: openclaw:latest
      deploy:
        resources:
          limits:
            cpus: '2.0'
            memory: 2G
          reservations:
            cpus: '0.5'
            memory: 512M
  ```

- [ ] **只读文件系统**（如可能）
  ```yaml
  services:
    openclaw:
      image: openclaw:latest
      read_only: true
      tmpfs:
        - /tmp
        - /var/log
      volumes:
        - ./data:/home/openclaw/data:ro  # 只读挂载
  ```

- [ ] **删除不必要的功能**
  ```yaml
  services:
    openclaw:
      image: openclaw:latest
      security_opt:
        - no-new-privileges:true
      cap_drop:
        - ALL
      cap_add:
        - NET_BIND_SERVICE  # 仅添加需要的能力
  ```

### 3. 网络安全

- [ ] **使用自定义网络**
  ```yaml
  # docker-compose.yml
  networks:
    openclaw-net:
      driver: bridge
      ipam:
        config:
          - subnet: 172.28.0.0/16
  
  services:
    gateway:
      networks:
        - openclaw-net
    node:
      networks:
        - openclaw-net
  ```

- [ ] **仅暴露必要端口**
  ```yaml
  services:
    gateway:
      ports:
        - "127.0.0.1:7001:7001"  # 仅本地访问
        # 如需远程访问，使用反向代理
    node:
      ports: []  # 不暴露，仅内网通信
  ```

- [ ] **使用反向代理**（推荐）
  ```yaml
  services:
    nginx:
      image: nginx:alpine
      ports:
        - "80:80"
        - "443:443"
      volumes:
        - ./nginx.conf:/etc/nginx/nginx.conf:ro
        - ./ssl:/etc/nginx/ssl:ro
      depends_on:
        - gateway
  
  # nginx.conf 示例
  # server {
  #     listen 443 ssl;
  #     location / {
  #         proxy_pass http://gateway:7001;
  #     }
  # }
  ```

### 4. 镜像安全

- [ ] **使用官方/可信镜像**
  ```bash
  # 检查镜像来源
  docker inspect openclaw:latest | grep -i "author\|description"
  
  # 优先使用官方镜像
  FROM node:18-alpine  # ✅ 官方
  # FROM some-random/node  # ❌ 避免
  ```

- [ ] **定期扫描镜像漏洞**
  ```bash
  # 安装 Trivy
  brew install trivy  # macOS
  sudo apt install trivy  # Linux
  
  # 扫描镜像
  trivy image openclaw:latest
  
  # 扫描容器
  trivy container <container-id>
  ```

- [ ] **使用最小化基础镜像**
  ```dockerfile
  # 推荐顺序（从最安全到最灵活）
  FROM gcr.io/distroless/nodejs18  # ✅ 最安全（无 shell）
  FROM alpine:3.18  # ✅ 小型（有 shell）
  FROM node:18-alpine  # ⚠️ 标准（较大）
  FROM node:18  # ❌ 避免（完整 Debian）
  ```

- [ ] **固定镜像版本**
  ```yaml
  # ✅ 固定版本
  image: node:18.16.0-alpine
  
  # ❌ 避免（可能意外更新）
  image: node:latest
  image: node:18
  ```

### 5. 密钥管理

- [ ] **使用 Docker Secrets**（Swarm）或外部密钥管理
  ```yaml
  # docker-compose.yml (Swarm 模式)
  services:
    openclaw:
      image: openclaw:latest
      secrets:
        - api_key
  
  secrets:
    api_key:
      external: true
  ```
  
  ```bash
  # 创建 secret
  echo "sk-..." | docker secret create api_key -
  ```

- [ ] **或使用环境变量文件**（开发/测试）
  ```yaml
  services:
    openclaw:
      image: openclaw:latest
      env_file:
        - .env
  ```
  
  ```bash
  # .env 文件权限
  chmod 600 .env
  
  # .gitignore 包含 .env
  echo ".env" >> .gitignore
  ```

- [ ] **不要硬编码到 Dockerfile**
  ```dockerfile
  # ❌ 错误
  ENV API_KEY=sk-1234567890
  
  # ✅ 正确
  ARG API_KEY
  ENV API_KEY=$API_KEY
  ```

### 6. 卷（Volumes）安全

- [ ] **使用命名卷**（非绑定挂载，如可能）
  ```yaml
  volumes:
    openclaw-data:
      driver: local
  
  services:
    openclaw:
      volumes:
        - openclaw-data:/home/openclaw/data
  ```

- [ ] **限制绑定挂载权限**
  ```yaml
  services:
    openclaw:
      volumes:
        - ./config:/home/openclaw/config:ro  # 只读
        - ./logs:/home/openclaw/logs:rw      # 读写
        # ❌ 避免挂载整个主机目录
        # - /:/host:rw
  ```

- [ ] **检查卷权限**
  ```bash
  # 查看卷权限
  docker volume inspect openclaw-data
  
  # 确保挂载点权限正确
  ls -la /var/lib/docker/volumes/openclaw-data/_data
  ```

### 7. 日志和监控

- [ ] **配置日志驱动和轮转**
  ```yaml
  services:
    openclaw:
      logging:
        driver: "json-file"
        options:
          max-size: "10m"
          max-file: "3"
          compress: "true"
  ```

- [ ] **集中日志收集**（可选）
  ```yaml
  services:
    openclaw:
      logging:
        driver: "syslog"
        options:
          syslog-address: "udp://logs-server:514"
  ```

- [ ] **容器监控**
  ```bash
  # 安装 cAdvisor
  docker run \
    --volume=/:/rootfs:ro \
    --volume=/var/run:/var/run:ro \
    --volume=/sys:/sys:ro \
    --volume=/var/lib/docker/:/var/lib/docker:ro \
    --publish=8080:8080 \
    --detach=true \
    --name=cadvisor \
    google/cadvisor:latest
  ```

### 8. 备份和恢复

- [ ] **定期备份卷数据**
  ```bash
  # 备份脚本
  #!/bin/bash
  TIMESTAMP=$(date +%Y%m%d-%H%M%S)
  docker run --rm \
    -v openclaw_data:/data:ro \
    -v $(pwd):/backup \
    alpine tar czf /backup/openclaw-data-$TIMESTAMP.tar.gz -C /data .
  ```

- [ ] **配置自动备份**（cron）
  ```bash
  # crontab -e
  0 2 * * * /path/to/backup-script.sh
  ```

- [ ] **测试恢复流程**
  ```bash
  # 恢复数据
  docker run --rm \
    -v openclaw_data:/data \
    -v $(pwd):/backup \
    alpine tar xzf /backup/openclaw-data-20260315.tar.gz -C /data
  ```

## 快速检查脚本

```bash
#!/bin/bash
# Docker 安全检查

echo "🔍 Docker OpenClaw 安全检查"
echo "============================"

# 检查是否以 root 运行容器
ROOT_CONTAINERS=$(docker ps --format "{{.Names}}" | while read name; do
    docker exec $name whoami 2>/dev/null | grep -q root && echo $name
done)

if [[ -z "$ROOT_CONTAINERS" ]]; then
    echo "✓ 无容器以 root 运行"
else
    echo "⚠ 以下容器以 root 运行：$ROOT_CONTAINERS"
fi

# 检查资源限制
NO_LIMITS=$(docker ps --format "{{.Names}}" | while read name; do
    INSPECT=$(docker inspect $name)
    if echo "$INSPECT" | grep -q '"Memory": 0'; then
        echo $name
    fi
done)

if [[ -z "$NO_LIMITS" ]]; then
    echo "✓ 所有容器有资源限制"
else
    echo "⚠ 以下容器无资源限制：$NO_LIMITS"
fi

# 检查 Docker 内容信任
if [[ "$DOCKER_CONTENT_TRUST" == "1" ]]; then
    echo "✓ Docker 内容信任已启用"
else
    echo "⚠ Docker 内容信任未启用"
fi

# 检查镜像漏洞（如已安装 Trivy）
if command -v trivy &> /dev/null; then
    echo "扫描镜像漏洞..."
    trivy image openclaw:latest --exit-code 0 --severity HIGH,CRITICAL
fi

echo "============================"
echo "检查完成"
```

## 常见问题

### Q: Docker 和 Podman 哪个更安全？

**A**: Podman 无守护进程、默认 rootless，理论上更安全。但 Docker 生态更成熟。选择建议：
- 个人/小团队：Docker（生态好）
- 高安全要求：Podman（无守护进程）

### Q: 需要启用 SELinux/AppArmor 吗？

**A**: **是的**，这是重要的安全层：
```bash
# 检查状态
getenforce  # SELinux (CentOS/RHEL)
aa-status   # AppArmor (Ubuntu/Debian)

# Docker 默认会使用，无需额外配置
```

### Q: 如何限制容器网络访问？

**A**: 使用 Docker 网络策略或防火墙：
```bash
# 使用 Docker 网络
docker network create --internal openclaw-internal

# 或使用 iptables
iptables -A DOCKER-USER -i eth0 -o docker0 -p tcp --dport 7001 -j DROP
```

## 资源链接

- Docker 安全最佳实践：https://docs.docker.com/engine/security/
- CIS Docker Benchmark: https://www.cisecurity.org/benchmark/docker
- Trivy 镜像扫描：https://github.com/aquasecurity/trivy

## 更新记录

- 2026-03-15: 初始版本
