---
name: multi-agent-memory
version: 1.0.0
description: 通用多Agent记忆系统 - 自动捕获、RRF检索、知识图谱、矛盾检测、Token追踪
author: 光光教授 (光光事务所)
license: MIT
tags:
  - memory
  - multi-agent
  - rrf
  - knowledge-graph
  - token-tracking
metadata:
  openclaw:
    emoji: "🧠"
    requires:
      bins: ["python3", "git"]
    install:
      - id: pip
        kind: pip
        package: lancedb
        label: "Install LanceDB"
      - id: pip2
        kind: pip
        package: numpy
        label: "Install NumPy"
---

# 多Agent记忆系统 🧠

**功能**: 通用多Agent记忆系统，支持自动捕获、RRF检索、知识图谱、矛盾检测、Token追踪

**适用场景**:
- 单Agent记忆管理
- 多Agent协作记忆
- 企业级记忆系统

**核心特性**:
- ✅ 8个Hook自动捕获
- ✅ RRF融合检索（BM25 + Vector + Graph）
- ✅ 知识图谱构建
- ✅ 矛盾检测集成（95.7%解决率）
- ✅ Token消耗追踪
- ✅ 检索基准测试（R@5=100%）
- ✅ Git快照管理
- ✅ 工作流引擎
- ✅ 实时可视化面板
- ✅ RRF权重优化
- ✅ **动态Agent管理**（自动增加/减少）

---

## 快速开始

### 1. 安装

```bash
# 使用ClawHub安装
clawhub install multi-agent-memory

# 或手动安装
npx clawhub@latest install multi-agent-memory
```

### 2. 配置

```bash
# 运行配置向导
python3 ~/.openclaw/workspace/skills/multi-agent-memory/scripts/setup.py
```

### 3. 使用

```bash
# 运行集成测试
python3 ~/.openclaw/workspace/skills/multi-agent-memory/scripts/memory-system.py

# 查看可视化面板
open ~/.openclaw/workspace/skills/multi-agent-memory/public/dashboard.html
```

---

## 核心功能

### 1. Hook自动捕获

```bash
python3 ~/.openclaw/workspace/skills/multi-agent-memory/scripts/hook-capture.py
```

### 2. RRF融合检索

```bash
python3 ~/.openclaw/workspace/skills/multi-agent-memory/scripts/rrf-search.py
```

### 3. 知识图谱构建

```bash
python3 ~/.openclaw/workspace/skills/multi-agent-memory/scripts/graph-builder.py
```

### 4. 矛盾检测集成

```bash
python3 ~/.openclaw/workspace/skills/multi-agent-memory/scripts/conflict-detector.py
```

### 5. Token消耗追踪

```bash
python3 ~/.openclaw/workspace/skills/multi-agent-memory/scripts/token-tracker.py
```

### 6. 动态Agent管理

```bash
# 注册Agent
python3 ~/.openclaw/workspace/skills/multi-agent-memory/scripts/agent-manager.py register agent-001

# 注销Agent
python3 ~/.openclaw/workspace/skills/multi-agent-memory/scripts/agent-manager.py unregister agent-001

# 列出Agent
python3 ~/.openclaw/workspace/skills/multi-agent-memory/scripts/agent-manager.py list

# 健康检查
python3 ~/.openclaw/workspace/skills/multi-agent-memory/scripts/agent-manager.py health

# 自动扩展
python3 ~/.openclaw/workspace/skills/multi-agent-memory/scripts/agent-manager.py scale

---

## 配置说明

### 默认配置

```yaml
# config/default-config.yaml
memory:
  vector_model: "nomic-embed-text-v1.5"
  vector_dim: 768
  search_mode: "rrf"  # rrf / vector / bm25
  
hooks:
  enabled: true
  count: 8
  
rrf:
  k: 60
  weights:
    bm25: 0.2
    vector: 0.5
    graph: 0.3
```

### 环境变量

```bash
# .env
MEMORY_WORKSPACE=/path/to/workspace
MEMORY_VECTOR_MODEL=nomic-embed-text-v1.5
MEMORY_LLM_API_KEY=your-api-key
```

---

## 示例项目

### 单Agent示例

```bash
cd examples/single-agent
python3 run.py
```

### 多Agent示例

```bash
cd examples/multi-agent
python3 run.py
```

---

## 测试

```bash
# 运行所有测试
python3 -m pytest tests/

# 运行特定测试
python3 -m pytest tests/test-hooks.py
```

---

## 文档

- [快速开始](docs/quick-start.md)
- [配置指南](docs/configuration.md)
- [API参考](docs/api-reference.md)
- [示例项目](docs/examples.md)
- [常见问题](docs/faq.md)

---

## 贡献

欢迎贡献！请参阅 [CONTRIBUTING.md](CONTRIBUTING.md) 了解指南。

---

## 许可证

MIT License

---

## 支持

- GitHub Issues: https://github.com/light-office/multi-agent-memory/issues
- Discord: https://discord.gg/light-office
- 邮件: professor@light-office.local
