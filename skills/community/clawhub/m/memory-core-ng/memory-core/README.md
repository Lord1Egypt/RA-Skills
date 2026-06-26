# 🧠 Memory Core

优雅模块化的智能记忆核心系统，支持多平台 embeddings/reranker 和 Flomo 集成。

## 🎯 特性

- **模块化架构**: 抽象接口，支持多平台 (Edgefn, OpenAI, 本地模型等)
- **智能搜索**: embeddings + reranker 双重优化，语义理解更准确
- **弹性设计**: 熔断器、指数退避重试、优雅降级
- **性能优化**: 智能缓存、批量处理、相似度计算优化
- **Flomo 集成**: 一键导入 Flomo 笔记，自动分类和标签提取
- **生产就绪**: 详细统计、错误处理、配置驱动

## 🚀 快速开始

### 安装

```bash
npm install @openclaw/memory-core
```

### 基本使用

```javascript
const { quickStart } = require('@openclaw/memory-core');

async function main() {
  // 1. 快速启动
  const memoryCore = await quickStart({
    apiKey: 'your-edgefn-api-key',
    verbose: true
  });

  // 2. 添加记忆
  const memory = await memoryCore.addMemory('重要信息内容', {
    category: '知识',
    tags: ['学习', '笔记']
  });

  // 3. 搜索记忆
  const result = await memoryCore.search('查找相关信息', {
    topKFinal: 5,
    useReranker: true
  });

  console.log('搜索结果:', result.results);
}

main();
```

## 📁 架构设计

```
memory-core/
├── src/
│   ├── interfaces/       # 抽象接口
│   ├── providers/        # 平台实现 (Edgefn, OpenAI...)
│   ├── services/         # 核心服务
│   ├── managers/        # 服务容器
│   ├── utils/           # 工具模块
│   └── adapters/        # 适配器 (Flomo)
├── examples/            # 使用示例
├── config/              # 配置模板
└── tests/              # 测试
```

## 🔧 配置

### Edgefn 配置示例

```json
{
  "apiKey": "sk-your-edgefn-key",
  "baseUrl": "https://api.edgefn.net/v1",
  
  "embeddingProvider": {
    "type": "edgefn",
    "model": "BAAI/bge-m3",
    "dimensions": 1024
  },
  
  "rerankProvider": {
    "type": "edgefn", 
    "model": "bge-reranker-v2-m3"
  }
}
```

### Flomo 集成

```javascript
const memoryCore = await quickStart(config);
const flomoAdapter = memoryCore.createFlomoAdapter();

// 解析 Flomo 导出
const result = await flomoAdapter.parseFromFile('/path/to/flomo-export.html');

// 导入到记忆系统
const importResult = await flomoAdapter.importToMemory(
  result.notes,
  memoryCore.memoryService,
  { batchSize: 20 }
);
```

## 🎨 高级功能

### 自定义 Provider

```javascript
const { createMemoryCore, components } = require('@openclaw/memory-core');

class CustomEmbeddingProvider extends components.EmbeddingProvider {
  getName() { return 'custom'; }
  async generateEmbeddings(texts) {
    // 自定义实现
    return embeddings;
  }
}

const memoryCore = createMemoryCore(config);
const embeddingService = memoryCore.embeddingService;
embeddingService.registerProvider('custom', new CustomEmbeddingProvider());
```

### 批量操作

```javascript
// 批量添加
const contents = ['记忆1', '记忆2', '记忆3'];
for (const content of contents) {
  await memoryCore.addMemory(content);
}

// 批量搜索
const queries = ['查询1', '查询2'];
const results = [];
for (const query of queries) {
  const result = await memoryCore.search(query);
  results.push(result);
}
```

## 📊 监控与统计

```javascript
const info = memoryCore.getInfo();
console.log('系统信息:', JSON.stringify(info, null, 2));

// 获取服务统计
const memoryStats = memoryCore.memoryService.getStats();
const embeddingStats = memoryCore.embeddingService.getStats();
```

## 🔍 搜索选项

| 选项 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `useReranker` | boolean | true | 是否使用 reranker 优化 |
| `topKInitial` | number | 15 | 初始筛选数量 |
| `topKFinal` | number | 5 | 最终返回数量 |
| `embeddingWeight` | number | 0.4 | embeddings 分数权重 |
| `rerankerWeight` | number | 0.6 | reranker 分数权重 |
| `minScore` | number | 0.1 | 最低相似度分数 |

## 🧪 测试

```bash
# 运行集成测试
npm test

# 运行快速示例
npm start
```

## 🤝 贡献

欢迎贡献代码、报告问题或提出建议！

1. Fork 项目
2. 创建特性分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建 Pull Request

## 📄 许可证

MIT License
```

echo "✅ README.md 完成"

echo "🎉 Memory Core 架构完成度: 100%!"

echo "🧪 运行最终验证测试..."
cd "$MEMORY_CORE_DIR" && node tests/integration.test.js 2>&1 | head -50