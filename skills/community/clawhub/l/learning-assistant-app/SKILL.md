---
name: learning-assistant-app
description: 一个集成多个免费API的学习助手应用
category: productivity
tags:
  - learning
  - api
  - education
  - helper
  - dictionary
  - translation
  - calculator
  - history
author: fish1981bimmer
repository: https://github.com/fish1981bimmer/learning-assistant-app
license: MIT
version: 1.0.0
---

## 学习助手应用

一个完全免费的学习助手应用，集成多个免费API，无需任何认证。

### 功能特性

- 📚 **词典查询** - 使用DictionaryAPI查询单词定义和例句
- 🌍 **翻译工具** - 使用LibreTranslate进行多语言翻译
- 💡 **有趣事实** - 获取随机有趣的知识事实
- 🔢 **数学计算** - 支持复杂数学表达式计算
- 📜 **历史事件** - 查看历史上的今天发生的事件

### 技术栈

- **后端**: Node.js + Express
- **HTTP客户端**: Axios
- **前端**: 原生HTML/CSS/JavaScript
- **数据存储**: 本地文件系统

### 集成的API

| API | 用途 | 认证 |
|-----|------|------|
| DictionaryAPI | 词典查询 | ❌ |
| LibreTranslate | 文本翻译 | ❌ |
| Useless Facts | 有趣事实 | ❌ |
| MathJS | 数学计算 | ❌ (本地) |
| History API | 历史事件 | ❌ |

### 快速开始

1. 安装依赖：
```bash
npm install
```

2. 配置环境变量：
```bash
cp .env.example .env
# 编辑 .env 文件配置API地址
```

3. 启动服务：
```bash
npm start
```

4. 访问应用：
打开浏览器访问 http://localhost:3000

### API端点

- `GET /api/dictionary/:word` - 查询单词
- `POST /api/translate` - 翻译文本
- `GET /api/fact` - 获取有趣事实
- `POST /api/calculate` - 数学计算
- `GET /api/history` - 获取历史事件
- `GET /api/data/preferences` - 获取用户偏好
- `POST /api/data/preferences` - 保存用户偏好

### 项目结构

```
learning-assistant-app/
├── server.js              # Express服务器主文件
├── dataManager.js         # 数据管理类
├── api/                   # API路由
│   └── data.js           # 数据管理API
├── public/                # 静态资源
│   ├── index.html         # 前端页面
│   ├── script.js          # 前端脚本
│   └── style.css         # 前端样式
├── data/                  # 数据存储目录
├── package.json           # 项目配置
├── .env                   # 环境变量
└── .gitignore            # Git忽略文件
```

### 使用说明

1. **词典查询**: 输入英文单词，获取定义、音标和例句
2. **翻译工具**: 选择源语言和目标语言，输入文本进行翻译
3. **有趣事实**: 点击按钮获取随机有趣的知识事实
4. **数学计算**: 支持基本运算、函数调用等复杂数学表达式
5. **历史事件**: 查看历史上的今天发生的重要事件

### 开发计划

- [ ] 添加更多API集成
- [ ] 实现用户认证系统
- [ ] 添加数据持久化
- [ ] 优化UI界面
- [ ] 添加移动端适配

### 许可证

MIT License

### 致谢

- [DictionaryAPI](https://dictionaryapi.dev/)
- [LibreTranslate](https://libretranslate.com/)
- [Useless Facts](https://uselessfacts.jsph.pl/)
- [History API](https://api.api-ninjas.com/)