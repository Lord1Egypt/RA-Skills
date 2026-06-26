# 部署指南

## 后端部署

### Railway部署

1. 创建Railway账号并登录
2. 点击"New Project"
3. 选择"Deploy from GitHub repo"
4. 选择你的仓库
5. 配置环境变量（如果需要）
6. 点击"Deploy"

### Render部署

1. 创建Render账号并登录
2. 点击"New +"
3. 选择"Web Service"
4. 连接GitHub仓库
5. 配置构建和启动命令：
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
6. 点击"Create Web Service"

## 前端部署

### Vercel部署

1. 创建Vercel账号并登录
2. 点击"Add New Project"
3. 导入GitHub仓库
4. 配置环境变量：
   - `NEXT_PUBLIC_API_URL`: 后端API地址
5. 点击"Deploy"

### 环境变量

前端需要配置以下环境变量：

\`\`\`env
NEXT_PUBLIC_API_URL=https://your-backend-api.com
\`\`\`

## Docker部署

### 后端Dockerfile

\`\`\`dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
\`\`\`

### 前端Dockerfile

\`\`\`dockerfile
FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build

EXPOSE 3000

CMD ["npm", "start"]
\`\`\`

### Docker Compose

\`\`\`yaml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
  
  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    environment:
      - NEXT_PUBLIC_API_URL=http://localhost:8000
    depends_on:
      - backend
\`\`\`

## 常见问题

### CORS错误

确保后端配置了正确的CORS设置：

\`\`\`python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
\`\`\`

### API超时

如果API请求超时，可以增加超时时间：

\`\`\`python
client = httpx.AsyncClient(timeout=60.0)
\`\`\`

### 前端构建失败

确保Node.js版本符合要求：

\`\`\`bash
node --version  # 应该是18+
npm --version
\`\`\`
