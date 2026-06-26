# init.sh 模板

通用的环境初始化脚本模板。根据项目类型调整。

## Web 应用

```bash
#!/bin/bash
set -e

PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$PROJECT_DIR"

echo "=== 环境初始化 ==="
echo "项目目录: $PROJECT_DIR"

# 1. 安装依赖
if [ -f "package.json" ]; then
  echo "安装 Node.js 依赖..."
  npm install
fi

if [ -f "requirements.txt" ]; then
  echo "安装 Python 依赖..."
  pip install -r requirements.txt
fi

# 2. 初始化数据库
if [ -f "init_db.sh" ]; then
  echo "初始化数据库..."
  bash init_db.sh
fi

# 3. 启动开发服务器（后台运行）
if [ -f "package.json" ] && grep -q '"start"' package.json; then
  echo "启动开发服务器..."
  npm start &
  sleep 5
  echo "开发服务器已启动"
fi

# 4. 冒烟测试
echo "=== 冒烟测试 ==="
if command -v curl &>/dev/null; then
  HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:3000 2>/dev/null || echo "000")
  if [ "$HTTP_CODE" = "200" ] || [ "$HTTP_CODE" = "302" ]; then
    echo "✅ 服务正常运行 (HTTP $HTTP_CODE)"
  else
    echo "⚠️ 服务未响应或异常 (HTTP $HTTP_CODE)"
  fi
fi

echo "=== 初始化完成 ==="
```

## Python 项目

```bash
#!/bin/bash
set -e

PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$PROJECT_DIR"

echo "=== 环境初始化 ==="

# 创建虚拟环境（如不存在）
if [ ! -d ".venv" ]; then
  python3 -m venv .venv
fi

source .venv/bin/activate

# 安装依赖
pip install -q -r requirements.txt

# 运行测试
if [ -f "tests/" ] || [ -f "test_"*.py ]; then
  echo "=== 运行测试 ==="
  python -m pytest tests/ -v --tb=short 2>&1 | tail -20
fi

echo "=== 初始化完成 ==="
```

## 使用说明

- init.sh 放在项目根目录
- 每次会话启动时由 Agent 运行
- 目的是让 Agent 快速确认环境正常，而不是花时间摸索配置
- 对于不需要初始化的项目（如纯文档项目），可以省略
