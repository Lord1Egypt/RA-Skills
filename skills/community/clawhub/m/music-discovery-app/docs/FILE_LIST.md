# 项目文件清单

## 后端文件

### 主应用
- backend/app/main.py - FastAPI主应用

### API路由
- backend/app/api/__init__.py - API路由初始化
- backend/app/api/music.py - 音乐相关API
- backend/app/api/radio.py - 电台相关API
- backend/app/api/events.py - 演唱会相关API

### 数据模型
- backend/app/models/__init__.py - 模型初始化
- backend/app/models/music.py - 音乐数据模型
- backend/app/models/radio.py - 电台数据模型
- backend/app/models/events.py - 演唱会数据模型

### 业务逻辑
- backend/app/services/__init__.py - 服务初始化
- backend/app/services/itunes.py - iTunes API服务
- backend/app/services/lyrics.py - 歌词API服务
- backend/app/services/musicbrainz.py - MusicBrainz API服务
- backend/app/services/radio.py - 电台API服务
- backend/app/services/events.py - 演唱会API服务

### 工具函数
- backend/app/utils/__init__.py - 工具初始化
- backend/app/utils/cache.py - 缓存工具
- backend/app/utils/logger.py - 日志工具

### 测试
- backend/tests/test_api.py - API测试
- backend/pytest.ini - pytest配置

### 配置
- backend/requirements.txt - Python依赖
- backend/.env.example - 环境变量示例

## 前端文件

### 主应用
- frontend/src/app/layout.tsx - 根布局
- frontend/src/app/page.tsx - 主页面

### 组件
- frontend/src/components/SearchBar.tsx - 搜索栏组件
- frontend/src/components/MusicResults.tsx - 音乐结果组件
- frontend/src/components/RadioPlayer.tsx - 电台播放器组件
- frontend/src/components/LyricsDisplay.tsx - 歌词显示组件

### API服务
- frontend/src/api/music.ts - 音乐API服务
- frontend/src/api/radio.ts - 电台API服务
- frontend/src/api/events.ts - 演唱会API服务

### 样式
- frontend/src/styles/globals.css - 全局样式

### 配置
- frontend/package.json - Node依赖
- frontend/next.config.js - Next.js配置
- frontend/tsconfig.json - TypeScript配置
- frontend/tailwind.config.js - TailwindCSS配置
- frontend/postcss.config.js - PostCSS配置

## 文档文件

- README.md - 项目说明
- docs/QUICKSTART.md - 快速开始指南
- docs/DEPLOYMENT.md - 部署指南
- docs/PROJECT_SUMMARY.md - 项目总结
- docs/COMPLETION_REPORT.md - 完成报告
- docs/FILE_LIST.md - 文件清单

## 配置文件

- .env.example - 环境变量示例
- .gitignore - Git忽略文件
- start.sh - 启动脚本

## 统计

- 后端文件: 20+
- 前端文件: 15+
- 文档文件: 6+
- 配置文件: 4+
- 总计: 45+ 文件
