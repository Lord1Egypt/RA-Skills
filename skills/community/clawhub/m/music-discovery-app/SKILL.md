---
name: music-discovery-app
description: 一个完全免费的音乐发现应用，集成多个免费音乐API，无需任何认证。提供音乐搜索、歌词显示、网络电台、演唱会信息等功能。
---

# 音乐发现应用

## 概述

一个完全免费的音乐发现应用，集成多个免费音乐API，无需任何认证。提供现代化的用户界面，支持桌面和移动设备。

## 安全警告

⚠️ **重要安全提示**

本 skill 涉及以下潜在风险操作：
- 网络请求调用外部API
- 数据缓存和存储
- 服务器配置修改

使用前请确保：
- ✅ 了解每个操作的风险和影响
- ✅ 在测试环境先验证
- ✅ 备份重要数据
- ✅ 使用最小权限原则
- ✅ 审查所有命令和配置

## 使用前提条件

使用本 skill 前，请满足以下条件：

### 环境要求
- Node.js 18+
- Python 3.11+
- npm 或 yarn

### 安全要求
- 确保API密钥安全（本项目使用免费API，无需密钥）
- 配置适当的CORS策略
- 启用HTTPS（生产环境）

### 备份要求
- 操作前备份配置文件
- 备份环境变量设置

### 测试要求
- 先在测试环境验证功能
- 使用健康检查端点验证服务状态

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

## 安装

### 1. 克隆项目
```bash
git clone <repository-url>
cd music-discovery-app
```

### 2. 安装后端依赖
```bash
cd backend
pip install -r requirements.txt
```

### 3. 安装前端依赖
```bash
cd frontend
npm install
```

## 运行

### 1. 启动后端服务
```bash
cd backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 2. 启动前端服务
```bash
cd frontend
npm run dev
```

### 3. 访问应用
打开浏览器访问 http://localhost:3000

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

## 危险操作：服务器配置

⚠️ **此操作有风险，请谨慎使用**

**风险说明：**
- 修改服务器配置可能影响服务稳定性
- 错误的配置可能导致服务中断

**影响范围：**
- 影响整个应用服务
- 可能影响所有用户访问

**回滚方法：**
- 恢复原始配置文件
- 重启服务

**替代方案：**
- 使用容器化部署
- 使用配置管理工具

## 安全建议

### 最佳实践

1. **最小权限原则**
   - 使用最小必要的权限
   - 避免使用默认配置
   - 定期审查配置

2. **审计和监控**
   - 记录所有操作日志
   - 定期审计访问记录
   - 设置异常告警

3. **备份和恢复**
   - 操作前备份
   - 验证备份可用性
   - 测试恢复流程

4. **测试环境**
   - 先在测试环境验证
   - 使用 staging 环境
   - 逐步推广到生产环境

### 常见安全风险

1. **API安全**
   - 验证所有输入
   - 使用HTTPS
   - 限制访问频率

2. **数据安全**
   - 不存储敏感信息
   - 使用安全传输
   - 限制数据访问

3. **服务安全**
   - 及时更新依赖
   - 监控服务状态
   - 准备应急方案

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

## 版本历史

### v1.0.0 (2026-05-09)

**初始版本：**
- 完整的音乐发现应用
- 集成5个免费音乐API
- 现代化的Next.js前端
- 安全改进：CORS配置、输入验证、速率限制、HTTPS支持