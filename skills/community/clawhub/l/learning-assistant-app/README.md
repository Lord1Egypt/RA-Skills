# 学习助手应用

一个集成多个免费API的学习助手应用，提供词典查询、翻译、有趣事实、数学计算和历史事件等功能。

## 功能特性

### 🔤 词典查询
- 使用DictionaryAPI查询英文单词
- 显示词性、定义和例句
- 支持发音信息

### 🌍 翻译工具
- 支持多种语言互译（英语、中文、西班牙语、法语、德语）
- 使用LibreTranslate API
- 实时翻译功能

### 💡 有趣事实
- 随机获取有趣的事实
- 每日更新内容
- 增加知识面

### 🔢 数学计算
- 支持基本数学运算
- 支持JavaScript数学函数
- 实时计算结果

### 📜 历史事件
- 每日历史事件
- 多个备用API支持
- 详细历史信息

## 技术栈

- **后端**: Node.js + Express
- **前端**: HTML + CSS + JavaScript
- **API集成**: RESTful API调用
- **数据存储**: 本地文件系统
- **样式**: 响应式设计

## 安装和运行

### 1. 安装依赖
```bash
npm install
```

### 2. 配置环境变量
复制 `.env` 文件并根据需要修改配置：
```bash
cp .env.example .env
```

### 3. 启动应用
```bash
# 开发模式
npm run dev

# 生产模式
npm start
```

### 4. 访问应用
打开浏览器访问：`http://localhost:3000`

## API集成

### DictionaryAPI
- **URL**: `https://api.dictionaryapi.dev/api/v2/entries/en/`
- **认证**: 无需认证
- **限制**: 免费

### LibreTranslate
- **URL**: `https://libretranslate.de`
- **认证**: 无需认证
- **限制**: 免费使用

### Useless Facts
- **URL**: `https://uselessfacts.jsph.pl/api/v2/facts/random`
- **认证**: 无需认证
- **限制**: 免费

### MathJS
- **类型**: 本地计算
- **认证**: 无需认证
- **限制**: JavaScript标准功能

### History API
- **主要**: `https://history.muffinlabs.com/date`
- **备用**: `https://api.api-ninjas.com/v1/historicalevents`
- **认证**: 无需认证
- **限制**: 免费

## 数据管理

应用包含完整的数据管理系统：

### 用户偏好
- 主题设置
- 语言偏好
- 工具收藏
- 翻译设置

### 搜索历史
- 自动保存查询记录
- 最多保存50条历史
- 支持导出功能

### 统计数据
- 工具使用统计
- 查询次数统计
- 最后使用时间

## 项目结构

```
learning-assistant-app/
├── server.js              # 主服务器文件
├── dataManager.js         # 数据管理类
├── api/
│   └── data.js           # 数据管理路由
├── public/
│   ├── index.html        # 主页
│   ├── style.css         # 样式文件
│   └── script.js         # 前端脚本
├── data/                 # 数据存储目录
├── package.json          # 项目配置
└── .env                  # 环境变量
```

## 使用说明

### 词典查询
1. 输入要查询的英文单词
2. 点击"查询"按钮
3. 查看词性、定义和例句

### 翻译工具
1. 选择源语言和目标语言
2. 输入要翻译的文本
3. 点击"翻译"按钮
4. 查看翻译结果

### 有趣事实
1. 点击"获取随机事实"按钮
2. 阅读有趣的事实
3. 可以多次获取不同的事实

### 数学计算
1. 输入数学表达式
2. 支持基本运算和JavaScript数学函数
3. 点击"计算"按钮查看结果

### 历史事件
1. 点击"获取历史事件"按钮
2. 查看今日历史上的重要事件
3. 了解历史知识

## 开发计划

- [ ] 添加更多API支持
- [ ] 实现用户账户系统
- [ ] 添加数据备份功能
- [ ] 优化移动端体验
- [ ] 添加离线功能

## 许可证

MIT License

## 贡献

欢迎提交Issue和Pull Request！

## 联系方式

如有问题请提交Issue或联系开发者。