# Memory Core - 智能记忆核心技能

基于模块化架构的智能记忆系统，支持多平台 embeddings/reranker 和 Flomo 笔记集成。

## 快速开始

```javascript
const { quickStart } = require('./index');
const memoryCore = await quickStart({ apiKey: 'your-key' });
const result = await memoryCore.search('查询内容');
```

## OpenClaw 配置

在 ~/.openclaw/openclaw.json 中添加：
```json
"skills": {
  "memory-core": {
    "enabled": true,
    "config": { "apiKey": "sk-your-key" }
  }
}
```

## 命令
- /memory search <查询> - 搜索记忆
- /memory add <内容> - 添加记忆  
- /memory stats - 查看统计
- /memory import-flomo <文件> - 导入 Flomo
- /memory help - 显示帮助

## 技术特性
- 多平台 embeddings 支持 (Edgefn, OpenAI, 本地)
- 智能重排序 (reranker)
- Flomo 笔记集成
- 语义搜索
- 模块化架构

## 文件结构
```
memory-core/
├── SKILL.md              # 技能文档
├── package.json          # 配置
├── index.js              # 主入口
├── entry.js              # OpenClaw 集成入口
├── config/               # 配置
│   └── openclaw.json    # OpenClaw 配置模板
├── src/                  # 核心代码
├── examples/             # 示例
└── tests/               # 测试
```