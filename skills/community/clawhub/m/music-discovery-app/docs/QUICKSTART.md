# 快速开始指南

## 5分钟快速启动

### 1. 安装依赖

#### 后端
\`\`\`bash
cd backend
pip install -r requirements.txt
\`\`\`

#### 前端
\`\`\`bash
cd frontend
npm install
\`\`\`

### 2. 启动服务

#### 方式一：使用启动脚本（推荐）
\`\`\`bash
./start.sh
\`\`\`

#### 方式二：手动启动

启动后端：
\`\`\`bash
cd backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
\`\`\`

启动前端（新终端）：
\`\`\`bash
cd frontend
npm run dev
\`\`\`

### 3. 访问应用

- 前端地址: http://localhost:3000
- 后端API: http://localhost:8000
- API文档: http://localhost:8000/docs

## 功能演示

### 搜索音乐
1. 在搜索框输入歌曲名、艺术家或专辑
2. 点击搜索或按回车
3. 查看搜索结果
4. 点击歌曲查看歌词

### 收听电台
1. 点击顶部"电台"标签
2. 浏览热门电台或搜索特定电台
3. 点击电台开始播放

### 查看歌词
1. 搜索并选择一首歌曲
2. 歌词会自动显示在弹窗中
3. 点击X关闭歌词窗口

## 常见问题

### 端口被占用
如果端口被占用，可以修改端口：

后端：
\`\`\`bash
python -m uvicorn app.main:app --port 8001
\`\`\`

前端：
\`\`\`bash
npm run dev -- -p 3001
\`\`\`

### API请求失败
1. 检查后端服务是否正常运行
2. 检查防火墙设置
3. 查看后端日志

### 前端构建失败
1. 清除缓存：`rm -rf .next node_modules`
2. 重新安装：`npm install`
3. 重新构建：`npm run build`

## 开发模式

### 后端开发
- 修改代码后自动重启（--reload）
- 查看API文档：http://localhost:8000/docs
- 运行测试：`pytest`

### 前端开发
- 热更新已启用
- 查看控制台错误
- 使用React DevTools调试

## 下一步

- 添加用户认证
- 实现播放列表功能
- 添加收藏功能
- 集成更多音乐API
- 优化UI/UX
