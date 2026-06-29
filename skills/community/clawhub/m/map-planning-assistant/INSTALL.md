# 全能地图规划助理 - 安装指南

## 快速开始

### 1. 环境准备

确保你的系统已安装 Node.js（版本 >= 14.0.0）：

```bash
node --version
npm --version
```

### 2. 获取高德API密钥

1. 访问 [高德开放平台](https://lbs.amap.com/)
2. 注册开发者账号
3. 进入控制台，创建新应用
4. 选择"Web服务"类型
5. 获取API Key

### 3. 配置环境变量

**方式一：临时配置（当前会话有效）**

```bash
# Linux/Mac
export AMAP_API_KEY=你的API密钥

# Windows
set AMAP_API_KEY=你的API密钥
```

**方式二：永久配置**

创建 `.env` 文件：

```bash
cp .env.example .env
```

编辑 `.env` 文件，填入你的API密钥：

```
AMAP_API_KEY=你的API密钥
```

### 4. 安装依赖（可选）

本项目使用纯Node.js实现，无第三方依赖。如需使用Node.js运行：

```bash
npm install
```

### 5. 运行测试

```bash
npm test
```

## 在Claude Code中使用

### 方式一：作为Skill使用

将本项目目录添加到Claude Code的Skill搜索路径中，然后直接使用自然语言指令：

```
帮我生成北京市全能游玩地图
```

### 方式二：作为模块引用

```javascript
const { main } = require('./src/index');

async function example() {
  const result = await main({
    userMessage: '帮我生成北京市全能游玩地图',
    userId: 'user_123'
  });

  console.log(result.content);
}
```

## 常见问题

### Q: 提示"AMAP_API_KEY未配置"

A: 请确保已正确设置环境变量。可以运行以下命令检查：

```bash
echo $AMAP_API_KEY
```

### Q: API请求失败

A: 可能的原因：
1. API密钥无效或已过期
2. 网络连接问题
3. API调用次数已用完

请检查：
- API密钥是否正确
- 网络连接是否正常
- 高德开放平台控制台中的调用统计

### Q: 搜索结果为空

A: 可能的原因：
1. 城市名称不正确
2. 该地区POI数据较少
3. 搜索关键词过于具体

建议：
- 使用标准城市名称（如"北京"而非"帝都"）
- 尝试更通用的关键词
- 扩大搜索范围

### Q: 如何添加自定义场景

A: 编辑 `src/config/scenes.js` 文件，按照现有格式添加新的场景配置：

```javascript
module.exports = {
  // 现有场景...

  // 新增场景
  myScene: {
    name: '我的自定义场景',
    icon: '🎯',
    description: '场景描述',
    keywords: ['关键词1', '关键词2'],
    types: 'POI类型编码',
    searchKeywords: ['搜索词1', '搜索词2'],
    minRating: 4.0,
    maxResults: 20,
    // 其他配置...
  }
};
```

## 高级配置

### 修改POI过滤规则

编辑 `src/config/scenes.js` 中的 `minRating` 和 `maxResults` 参数。

### 修改记忆系统参数

编辑 `src/memory/index.js` 中的常量：

```javascript
// 临时记忆过期时间（7天）
const TEMPORARY_EXPIRY = 7 * 24 * 60 * 60 * 1000;
```

### 修改路线规划策略

编辑 `src/route/index.js` 中的 `ROUTE_STRATEGIES` 配置。

## 技术支持

如遇到问题，请：

1. 查看本文档的常见问题部分
2. 检查 `data/` 目录下的日志文件
3. 提交Issue到项目仓库

## 更新日志

### v1.0.0 (2026-06-12)
- 初始版本发布
- 支持八大场景地图生成
- 实现长记忆系统
- 实现用户画像功能
- 实现活动管理功能
- 实现路线规划功能
- 实现人文知识库
