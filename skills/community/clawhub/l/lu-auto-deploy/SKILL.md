# lu-auto-deploy

Docker 自动化部署技能 - 帮助你快速部署常见的 Docker 服务。

## 描述

这个技能提供 Docker 服务自动化部署功能，包括：
- 一键部署常见服务
- 配置文件生成
- 批量部署
- 服务更新

## 触发条件

当用户提到以下关键词时激活：
- "部署"
- "安装 Docker"
- "创建容器"
- "一键部署"
- "服务模板"

## 用法

### 部署服务
```
部署 uptime-kuma
安装 jellyfin
创建 nginx 容器
```

### 查看模板
```
部署模板
可用服务
服务列表
```

### 批量部署
```
批量部署 media-stack
部署监控套件
```

## 示例对话

**用户**: 部署 uptime-kuma
**助手**: 正在部署 Uptime Kuma 服务监控...
```bash
mkdir -p /vol1/1000/Docker/uptime-kuma
cd /vol1/1000/Docker/uptime-kuma
docker-compose up -d
```
✅ 部署完成！访问：http://192.168.3.26:3001

**用户**: 部署模板
**助手**: 可用部署模板：
- 📊 **监控类**: uptime-kuma, prometheus, grafana
- 🎬 **媒体类**: jellyfin, navidrome, qbittorrent
- 🔧 **工具类**: nginx, portainer, file-browser
- 🔐 **安全类**: vaultwarden, authelia

## 部署模板

### 媒体服务栈
```bash
mkdir -p /vol1/1000/Docker/media-stack
cd /vol1/1000/Docker/media-stack

cat > docker-compose.yml << 'EOF'
version: '3.8'
services:
  jellyfin:
    image: jellyfin/jellyfin:latest
    container_name: jellyfin
    ports:
      - "8096:8096"
    volumes:
      - ./jellyfin/config:/config
      - /vol1/1000/媒体:/media
    restart: unless-stopped

  navidrome:
    image: deluan/navidrome:latest
    container_name: navidrome
    ports:
      - "4533:4533"
    volumes:
      - ./navidrome/data:/data
      - /vol1/1000/音乐:/music
    restart: unless-stopped
EOF

docker-compose up -d
```

### 监控服务栈
```bash
mkdir -p /vol1/1000/Docker/monitoring
cd /vol1/1000/Docker/monitoring

cat > docker-compose.yml << 'EOF'
version: '3.8'
services:
  uptime-kuma:
    image: louislam/uptime-kuma:1
    container_name: uptime-kuma
    ports:
      - "3001:3001"
    volumes:
      - ./uptime-kuma-data:/app/data
    restart: unless-stopped

  grafana:
    image: grafana/grafana:latest
    container_name: grafana
    ports:
      - "3000:3000"
    volumes:
      - ./grafana-data:/var/lib/grafana
    restart: unless-stopped
EOF

docker-compose up -d
```

## 快速部署命令

```bash
# Uptime Kuma
docker run -d --name uptime-kuma -p 3001:3001 -v uptime-kuma-data:/app/data --restart unless-stopped louislam/uptime-kuma:1

# Portainer
docker run -d --name portainer -p 9000:9000 -v /var/run/docker.sock:/var/run/docker.sock -v portainer-data:/data --restart unless-stopped portainer/portainer-ce:latest

# File Browser
docker run -d --name file-browser -p 8080:80 -v /vol1/1000:/srv --restart unless-stopped filebrowser/filebrowser:latest

# Vaultwarden
docker run -d --name vaultwarden -p 8000:80 -v vaultwarden-data:/data --restart unless-stopped vaultwarden/server:latest
```

## 作者

- **作者**: jesson1222-ship-it
- **版本**: 1.0.0
- **创建时间**: 2026-03-08
- **许可证**: MIT

## 更新日志

### v1.0.0 (2026-03-08)
- 初始版本
- 支持常见服务部署
- 支持部署模板
- 支持批量部署
