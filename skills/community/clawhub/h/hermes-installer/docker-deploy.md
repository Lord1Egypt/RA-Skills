# Docker 部署指南

## 安装

```bash
# 1. 克隆仓库
git clone https://github.com/NousResearch/hermes-agent.git ~/.hermes/hermes-agent
cd ~/.hermes/hermes-agent

# 2. 构建镜像
docker build -t hermes-agent .

# 3. 运行容器
docker run -d -v ~/.hermes:/opt/data hermes-agent
```

---

## 升级

```bash
# 1. 进入映射目录
cd ~/.hermes/hermes-agent

# 2. 拉取最新代码
git pull origin main

# 3. 重新构建镜像
docker build -t hermes-agent .

# 4. 停止旧容器并重新运行
docker stop hermes-container 2>/dev/null || true
docker rm hermes-container 2>/dev/null || true
docker run -d --name hermes-container -v ~/.hermes:/opt/data hermes-agent
```

---

## 卸载

```bash
# 1. 停止并删除容器
docker stop hermes-container
docker rm hermes-container

# 2. 删除镜像
docker rmi hermes-agent

# 3. 删除配置目录（可选）
# rm -rf ~/.hermes
```

---

## 配置持久化

- 配置目录映射：`~/.hermes` → `/opt/data`
- 在宿主机上编辑 `~/.hermes/config.yaml` 和 `~/.hermes/.env`
- 容器重启后配置保持不变
