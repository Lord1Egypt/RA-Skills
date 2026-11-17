# EasyDataset 部署指南

## 环境要求

| 组件 | 最低版本 | 说明 |
|------|----------|------|
| Docker | 20.10+ | 容器运行时 |
| Docker Compose | 2.0+ (可选) | 编排工具 |
| 操作系统 | Windows 10+ / Linux / macOS | 需要支持 Docker |

## 部署方式

### 方式一：Docker 命令行部署（推荐）

```bash
# 1. 拉取镜像
docker pull ghcr.io/conardli/easy-dataset:latest

# 2. 创建数据卷
docker volume create easy-dataset-data

# 3. 启动容器
docker run -d \
  --name easy-dataset \
  --restart unless-stopped \
  -p 1717:3000 \
  -v easy-dataset-data:/app/data \
  ghcr.io/conardli/easy-dataset:latest

# 4. 验证运行
curl -s http://localhost:1717/api/projects
```

### 方式二：Docker Compose 部署

创建 `docker-compose.yml`:

```yaml
version: '3.8'
services:
  easy-dataset:
    image: ghcr.io/conardli/easy-dataset:latest
    container_name: easy-dataset
    restart: unless-stopped
    ports:
      - "1717:3000"
    volumes:
      - easy-dataset-data:/app/data
    environment:
      - DATABASE_URL=file:/app/data/db.sqlite

volumes:
  easy-dataset-data:
```

启动：
```bash
docker compose up -d
```

### 方式三：从源码构建

```bash
git clone https://github.com/ConardLi/easy-dataset.git D:/easy-dataset
cd D:/easy-dataset

# 安装依赖并启动
npm install
npm run build
npm start
```

## 部署后验证

```bash
# 检查容器状态
docker ps | grep easy-dataset

# 检查服务是否响应
curl -s http://localhost:1717/api/projects
# 预期返回: [] (空数组，因为是新部署)

# 查看容器日志
docker logs easy-dataset
```

## 配套服务：MongoDB

JY_Knowledge_Skill 需要 MongoDB 存储分类体系和数据集。如果尚未部署：

```bash
# 拉取MongoDB镜像
docker pull mongo:7

# 启动容器（无认证，开发环境）
docker run -d \
  --name knowledge-mongo \
  --restart unless-stopped \
  -p 27017:27017 \
  -v D:/knowledge_skill/mongo-data:/data/db \
  mongo:7
```

## 完整部署脚本（一键）

将以下脚本保存为 `deploy_all.bat`（Windows）或 `deploy_all.sh`（Linux/macOS）：

### Windows (`deploy_all.bat`):
```bat
@echo off
echo ===== 部署 EasyDataset =====
docker pull ghcr.io/conardli/easy-dataset:latest
docker rm -f easy-dataset 2>nul
docker run -d --name easy-dataset --restart unless-stopped -p 1717:3000 ghcr.io/conardli/easy-dataset:latest

echo ===== 部署 MongoDB =====
docker pull mongo:7
docker rm -f knowledge-mongo 2>nul
docker run -d --name knowledge-mongo --restart unless-stopped -p 27017:27017 -v "D:/knowledge_skill/mongo-data:/data/db" mongo:7

echo ===== 安装 Python 依赖 =====
pip install -r D:/knowledge_skill/JY_Knowlgdge_Skill/requirements.txt

echo ===== 验证服务 =====
echo 等待服务启动...
timeout /t 5 >nul
echo EasyDataset: && curl -s http://localhost:1717/api/projects
echo.
echo 全部部署完成！执行 python main.py -t 验证连接
```

### Linux/macOS (`deploy_all.sh`):
```bash
#!/bin/bash
set -e
echo "===== 部署 EasyDataset ====="
docker pull ghcr.io/conardli/easy-dataset:latest
docker rm -f easy-dataset 2>/dev/null || true
docker run -d --name easy-dataset --restart unless-stopped -p 1717:3000 ghcr.io/conardli/easy-dataset:latest

echo "===== 部署 MongoDB ====="
docker pull mongo:7
docker rm -f knowledge-mongo 2>/dev/null || true
docker run -d --name knowledge-mongo --restart unless-stopped -p 27017:27017 -v $(pwd)/mongo-data:/data/db mongo:7

echo "===== 安装 Python 依赖 ====="
pip install -r requirements.txt

echo "===== 验证服务 ====="
sleep 5
echo "EasyDataset: $(curl -s http://localhost:1717/api/projects)"
echo "全部部署完成！执行 python main.py -t 验证连接"
```

## 常见问题

### Q: 端口 1717 被占用
修改 Docker run 命令的 `-p` 参数，如 `-p 1718:3000`，同时修改 `config.json` 中 `easy_dataset.base_url`。

### Q: 数据持久化
EasyDataset 默认使用 SQLite 存储在容器内的 `/app/data/db.sqlite`。通过 `-v` 挂载卷可持久化。

### Q: 升级 EasyDataset
```bash
docker pull ghcr.io/conardli/easy-dataset:latest
docker rm -f easy-dataset
# 重新执行 docker run 命令（使用相同的卷挂载）
```
