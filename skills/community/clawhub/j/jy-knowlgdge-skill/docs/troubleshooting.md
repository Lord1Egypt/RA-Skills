# 问题排查指南

## Python 依赖问题

### 诊断：`ModuleNotFoundError: No module named 'xxx'`

```bash
# 查看已安装的包
pip list

# 安装缺失的包
pip install -r D:/knowledge_skill/JY_Knowlgdge_Skill/requirements.txt

# 额外需要 Pillow（表格截图功能）
pip install Pillow
```

### 诊断：`pip` 不可用

```bash
# 检查 Python 是否安装
python --version

# 如果 Python 已安装但 pip 不可用
python -m ensurepip --upgrade
```

## Docker 问题

### 诊断：`docker: command not found`

- **Windows**: 安装 Docker Desktop https://www.docker.com/products/docker-desktop/
- **Linux**:
  ```bash
  curl -fsSL https://get.docker.com | sh
  sudo systemctl start docker
  sudo usermod -aG docker $USER  # 免 sudo
  ```

### 诊断：`Cannot connect to the Docker daemon`

```bash
# Windows: 确保 Docker Desktop 正在运行（任务栏图标）
# Linux:
sudo systemctl start docker
```

### 诊断：端口被占用

```bash
# 查看谁占用了 1717 端口
netstat -ano | findstr :1717    # Windows
lsof -i :1717                    # Linux/macOS

# 解决方案：换端口
docker run -d --name easy-dataset -p 1718:3000 ghcr.io/conardli/easy-dataset:latest
# 然后修改 config.json 中 easy_dataset.base_url 为 http://localhost:1718
```

## EasyDataset 问题

### 诊断：EasyDataset 启��后立即退出

```bash
docker logs easy-dataset
```

常见原因：
- 数据目录权限不足
- 数据库文件损坏：删除旧卷 `docker volume rm easy-dataset-data` 后重新启动

### 诊断：EasyDataset API 返回 500

查看容器日志定位错误：
```bash
docker logs easy-dataset --tail 50
```

### 诊断：API 返回 `prisma:error`

通常是 SQLite 文件权限问题。检查 volume 映射是否正确：
```bash
docker inspect easy-dataset | grep -A5 Mounts
```

## MongoDB 问题

### 诊断：`pymongo.errors.ServerSelectionTimeoutError`

```bash
# 确认容器在运行
docker ps | grep knowledge-mongo

# 查看日志
docker logs knowledge-mongo

# 测试连接
python -c "from pymongo import MongoClient; c=MongoClient('mongodb://localhost:27017', serverSelectionTimeoutMS=3000); print(c.server_info())"
```

### 诊断：数据丢失

MongoDB 数据存储在 `D:/knowledge_skill/mongo-data/`（通过 Docker volume 映射）。确保该目录未被清空。

## LLM API 问题

### 诊断：`requests.exceptions.ConnectionError`

- 确认 LLM API 地址在 `config.json` 中正确配置
- 确认服务器能访问该地址：`curl http://your-llm-api/v1/models`
- 检查防火墙规则

### 诊断：`401 Unauthorized`

- API Key 过期或错误，更新 `config.json` 中的 `api_key` 字段

## 配置文件问题

### 诊断：`FileNotFoundError: config.json`

若 `D:/knowledge_skill/config.json` 不存在，需要手动创建。最小完整配置：

```json
{
  "llm": {
    "base_url": "http://your-llm-host:port/v1",
    "api_key": "your-api-key",
    "model": "your-model-name",
    "vision_model": "your-vision-model",
    "temperature": 0.7,
    "max_tokens": 4096
  },
  "easy_dataset": {
    "base_url": "http://localhost:1717"
  },
  "mongo": {
    "uri": "mongodb://localhost:27017",
    "database": "knowledge_skill"
  },
  "output": {
    "processed_dir": "D:/knowledge_skill/processed",
    "datasets_dir": "D:/knowledge_skill/datasets",
    "uploads_dir": "D:/knowledge_skill/uploads"
  },
  "dataset_generation": {
    "task_timeout_minutes": 720,
    "include_ga_pairs": true
  },
  "file_filter": {
    "value_threshold": 0.4
  }
}
```
