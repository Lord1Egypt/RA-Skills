# 音乐发现应用

一个完全免费的音乐发现应用，集成多个免费音乐API，无需任何认证。

## 功能特性

- 🎵 **音乐搜索** - 使用iTunes Search API搜索歌曲、专辑和艺术家
- 📝 **歌词显示** - 使用Lyrics.ovh API获取歌词
- 📻 **网络电台** - 使用Radio Browser API收听全球网络电台
- 🎤 **演唱会信息** - 使用Bandsintown API查看艺术家演唱会信息
- 🎨 **现代UI** - 基于Next.js和TailwindCSS的现代化界面
- 🌐 **响应式设计** - 支持桌面和移动设备

## 技术栈

### 前端
- Next.js 14
- React 18
- TypeScript
- TailwindCSS
- Axios

### 后端
- FastAPI
- Python 3.11+
- httpx
- Pydantic

## 集成的API

| API | 用途 | 认证 |
|-----|------|------|
| iTunes Search | 音乐搜索 | ❌ |
| Lyrics.ovh | 歌词获取 | ❌ |
| MusicBrainz | 音乐元数据 | ❌ |
| Radio Browser | 网络电台 | ❌ |
| Bandsintown | 演唱会信息 | ❌ |

## 快速开始

### 前置要求

- Node.js 18+
- Python 3.11+
- npm 或 yarn

### 安装

1. 克隆项目
\`\`\`bash
git clone <repository-url>
cd music-discovery-app
\`\`\`

2. 安装后端依赖
\`\`\`bash
cd backend
pip install -r requirements.txt
\`\`\`

3. 安装前端依赖
\`\`\`bash
cd frontend
npm install
\`\`\`

### 运行

1. 启动后端服务
\`\`\`bash
cd backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
\`\`\`

2. 启动前端服务
\`\`\`bash
cd frontend
npm run dev
\`\`\`

3. 访问应用
打开浏览器访问 http://localhost:3000

## 项目结构

\`\`\`
music-discovery-app/
├── backend/                 # 后端服务
│   ├── app/
│   │   ├── main.py         # FastAPI主应用
│   │   ├── api/            # API路由
│   │   ├── models/         # 数据模型
│   │   ├── services/       # 业务逻辑
│   │   └── utils/          # 工具函数
│   ├── tests/              # 测试文件
│   └── requirements.txt    # Python依赖
├── frontend/               # 前端应用
│   ├── src/
│   │   ├── app/           # Next.js页面
│   │   ├── components/    # React组件
│   │   ├── api/          # API服务
│   │   ├── styles/       # 样式文件
│   │   └── utils/        # 工具函数
│   ├── public/           # 静态资源
│   └── package.json      # Node依赖
└── docs/                 # 文档
\`\`\`

## API端点

### 后端API

- `GET /` - API信息
- `GET /api/search` - 搜索音乐
- `GET /api/lyrics` - 获取歌词
- `GET /api/artist/{id}` - 获取艺术家信息
- `GET /api/radio/search` - 搜索电台
- `GET /api/radio/top` - 获取热门电台
- `GET /api/events` - 获取演唱会信息
- `GET /api/health` - 健康检查

## 部署

### 后端部署

推荐使用Railway、Render或Vercel部署后端服务。

### 前端部署

推荐使用Vercel部署前端应用。

## 贡献

欢迎提交Issue和Pull Request！

## 许可证

MIT License

## 致谢

- [iTunes Search API](https://affiliate.itunes.apple.com/resources/documentation/itunes-store-web-service-search-api/)
- [Lyrics.ovh](https://lyricsovh.docs.apiary.io/)
- [MusicBrainz](https://musicbrainz.org/)
- [Radio Browser](https://api.radio-browser.info/)
- [Bandsintown](https://www.bandsintown.com/)
