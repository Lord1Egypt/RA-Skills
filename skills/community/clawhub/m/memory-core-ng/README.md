# 🧠 Memory Core - 智能记忆系统架构

一套优雅的模块化智能记忆系统，支持 embeddings、reranker 和 Flomo 笔记集成。

## 🎯 核心特性
- **模块化设计**: 抽象接口，依赖倒置
- **生产就绪**: 熔断器、缓存、弹性机制
- **多平台支持**: Edgefn API 集成 + 预留接口
- **完整生态**: OpenClaw 技能 + Smart Memory 集成
- **安全优先**: 配置驱动，无硬编码密钥

## 📦 项目结构
```
memory-core-repo/
├── memory-core/          # 核心架构 (2580行代码)
├── openclaw-skill/       # OpenClaw 技能包
├── smart-memory-integration/ # Smart Memory 集成
└── docs/                # 文档和指南
```

## 🚀 快速开始
```bash
# 安装核心库
cd memory-core
npm install

# 使用示例
node examples/quick-start.js
```

## 🔧 使用方式
1. **直接 API**: require('memory-core')
2. **OpenClaw 技能**: `/memory search <查询>`
3. **Smart Memory 集成**: 自动路由到 Memory Core

## 📊 性能指标
- 搜索延迟: ~394ms/查询
- 缓存命中率: 智能动态调整
- 错误恢复: 4级降级机制
- API 成功率: 监控 + 自动重试

## 🔐 安全
- ✅ 无硬编码敏感信息
- ✅ 配置驱动密钥管理
- ✅ 环境变量支持
- ✅ .gitignore 安全配置

## 📄 许可证
MIT
