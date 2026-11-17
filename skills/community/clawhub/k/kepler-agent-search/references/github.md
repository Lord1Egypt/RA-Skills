# 开源代码搜索

## 概述

专注于开源项目和代码仓库的搜索能力，适用于技术调研和开源方案发现。

## 支持平台

### GitHub
- **引擎标识**: `"github"`
- **适用场景**: 开源项目、代码仓库、技术文档、开发者资源
- **特点**: 直接返回仓库信息，覆盖全球最大的开源社区

```yaml
query: "react state management"
engines: ["github"]
max_results: 10
```

## 内容类型

- **开源项目**: 完整的代码仓库和项目
- **代码片段**: 特定功能的实现代码
- **技术文档**: README、Wiki、文档站点
- **开发者资源**: Awesome 列表、工具集、框架
- **Issues & Discussions**: 问题讨论和解决方案

## 使用技巧

### 搜索优化
1. **关键词**: 使用英文关键词效果更佳
2. **项目筛选**: 可加上 `stars:>100` 筛选热门项目
3. **语言筛选**: `language:python` 筛选特定编程语言
4. **主题标签**: `topic:machine-learning` 筛选特定主题

### 仓库评估
1. **Stars 数量**: 反映项目受欢迎程度
2. **最近更新**: 查看最后提交时间
3. **Issue 活跃度**: 了解项目维护状态
4. **文档完整度**: README 是否清晰

### URL 读取
- **项目主页**: `github.com/owner/repo`
- **代码文件**: `github.com/owner/repo/blob/main/file.js`
- **Issues**: `github.com/owner/repo/issues`
- **Pull Requests**: `github.com/owner/repo/pulls`

## 示例

```yaml
# 搜索前端框架
query: "vue admin dashboard"
engines: ["github"]

# 搜索特定语言项目
query: "machine learning language:python"
engines: ["github"]

# 搜索热门项目
query: "state management stars:>1000"
engines: ["github"]

# 搜索工具集
query: "developer tools awesome"
engines: ["github"]
```

## 深度使用

### 读取项目 README
```yaml
tool: mcp__kepler__web_reader
url: "https://github.com/facebook/react"
format: "markdown"
```

### 读取代码文件
```yaml
tool: mcp__kepler__web_reader
url: "https://github.com/facebook/react/blob/main/README.md"
format: "markdown"
```

## 应用场景

### 技术选型
- 对比同类开源方案
- 评估技术成熟度
- 查看社区活跃度

### 学习参考
- 阅读优秀项目源码
- 学习最佳实践
- 了解最新技术趋势

### 问题解决
- 查找类似问题的解决方案
- 参考 Issue 讨论
- 寻找代码示例

## 注意事项
- GitHub 搜索结果为公开仓库
- 注意项目的开源协议（License）
- 关注项目的安全性和维护状态
- 商业使用时注意合规性
