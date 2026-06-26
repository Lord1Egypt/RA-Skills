#!/bin/bash
# Docker Compose 部署脚本
# 支持 macOS、Linux、Windows (WSL2)

set -e

echo "🐳 OpenClaw Docker 部署脚本"
echo "============================"
echo ""

# 检查 Docker
if ! command -v docker &> /dev/null; then
    echo "❌ 未找到 Docker"
    echo "请先安装 Docker:"
    echo "  macOS: https://docs.docker.com/desktop/install/mac/"
    echo "  Windows: https://docs.docker.com/desktop/install/windows/"
    echo "  Linux: https://docs.docker.com/engine/install/"
    exit 1
fi

# 检查 Docker Compose
if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    echo "❌ 未找到 Docker Compose"
    echo "请先安装 Docker Compose"
    exit 1
fi

# 创建工作目录
WORK_DIR="$HOME/nexusbot-docker"
mkdir -p "$WORK_DIR"
cd "$WORK_DIR"

echo "📁 工作目录: $WORK_DIR"
echo ""

# 创建 docker-compose.yml
echo "📝 创建 docker-compose.yml..."

cat > docker-compose.yml << 'EOF'
version: '3.8'

services:
  nexusbot:
    image: markovmodcn/nexusbot:latest
    container_name: nexusbot
    restart: unless-stopped
    ports:
      - "3000:3000"
    volumes:
      - nexusbot-data:/data
      - ./config.yaml:/app/config.yaml:ro
      - ./logs:/app/logs
    environment:
      - NODE_ENV=production
      - LOG_LEVEL=info
      - TZ=Asia/Shanghai
    networks:
      - nexusbot-network
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

  # 可选: Ollama 服务（本地模型）
  ollama:
    image: ollama/ollama:latest
    container_name: nexusbot-ollama
    restart: unless-stopped
    ports:
      - "11434:11434"
    volumes:
      - ollama-data:/root/.ollama
    networks:
      - nexusbot-network
    profiles:
      - with-ollama
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]

volumes:
  nexusbot-data:
  ollama-data:

networks:
  nexusbot-network:
    driver: bridge
EOF

# 创建配置文件（如果不存在）
if [ ! -f config.yaml ]; then
    echo "📝 创建默认配置文件..."

    cat > config.yaml << 'EOF'
ai:
  provider: ollama
  ollama:
    host: http://ollama:11434
    model: qwen2.5:7b
    temperature: 0.7

platforms:
  dingtalk:
    enabled: false
  feishu:
    enabled: false
  wecom:
    enabled: false

logging:
  level: info

performance:
  max_concurrent: 10
  timeout: 30
EOF

    echo "⚠️  请修改 config.yaml 配置你的 AI 模型和消息平台"
    echo ""
fi

# 创建日志目录
mkdir -p logs

echo ""
echo "🚀 启动方式选择:"
echo "  1) 基础版（仅 NEUXSBOT，使用外部 AI）"
echo "  2) 完整版（NEUXSBOT + Ollama 本地模型）"
echo ""

read -p "请选择 (1-2): " choice

case $choice in
    1)
        echo "🚀 启动基础版..."
        docker-compose up -d
        ;;
    2)
        echo "🚀 启动完整版（含 Ollama）..."
        docker-compose --profile with-ollama up -d

        echo ""
        echo "⏳ 等待 Ollama 启动..."
        sleep 5

        echo "📥 下载模型..."
        docker-compose exec ollama ollama pull qwen2.5:7b
        ;;
    *)
        echo "❌ 无效选择"
        exit 1
        ;;
esac

echo ""
echo "✅ 部署完成！"
echo ""
echo "📊 服务状态:"
docker-compose ps

echo ""
echo "🌐 访问地址:"
echo "  Web 界面: http://localhost:3000"
echo "  API 接口: http://localhost:3000/api"

if [ "$choice" = "2" ]; then
    echo "  Ollama: http://localhost:11434"
fi

echo ""
echo "📝 常用命令:"
echo "  查看日志: docker-compose logs -f"
echo "  停止服务: docker-compose down"
echo "  重启服务: docker-compose restart"
echo "  更新镜像: docker-compose pull && docker-compose up -d"

echo ""
echo "⚙️  配置文件: $WORK_DIR/config.yaml"
echo "📁 数据目录: $WORK_DIR/"
