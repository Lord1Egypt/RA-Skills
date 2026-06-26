# OpenClaw 记忆系统配置指南

## 目录
- [记忆类型](#记忆类型)
- [向量数据库配置](#向量数据库配置)
- [知识图谱配置](#知识图谱配置)
- [记忆策略](#记忆策略)
- [跨会话记忆](#跨会话记忆)

---

## 记忆类型

### 1. Basic Memory (基础记忆)

最简单的对话历史存储方式。

```json
{
  "memory": {
    "type": "basic",
    "config": {
      "max_history": 100,
      "summary_enabled": true,
      "summary_threshold": 50
    }
  }
}
```

**适用场景：**
- 简单对话
- 开发测试
- 资源受限环境

### 2. Vector Memory (向量记忆)

基于向量数据库的语义检索。

```json
{
  "memory": {
    "type": "vector",
    "provider": "chroma",
    "config": {
      "persist_directory": "~/.openclaw/chroma",
      "collection_name": "conversations",
      "embedding_model": "text-embedding-3-small"
    }
  }
}
```

**适用场景：**
- 语义检索
- RAG 应用
- 相似度匹配

### 3. Graph Memory (知识图谱)

基于图的实体关系记忆。

```json
{
  "memory": {
    "type": "graph",
    "provider": "networkx",
    "config": {
      "persist_file": "~/.openclaw/knowledge_graph.gpickle",
      "max_nodes": 10000
    }
  }
}
```

**适用场景：**
- 复杂推理
- 关系分析
- 知识结构化

### 4. Hybrid Memory (混合记忆)

结合多种记忆类型。

```json
{
  "memory": {
    "type": "hybrid",
    "config": {
      "short_term": {"type": "basic"},
      "long_term": {"type": "vector"},
      "transfer": {
        "enabled": true,
        "strategy": "importance"
      }
    }
  }
}
```

---

## 向量数据库配置

### Chroma (推荐)

轻量级向量数据库，适合本地部署。

```json
{
  "memory": {
    "type": "vector",
    "provider": "chroma",
    "config": {
      "persist_directory": "~/.openclaw/chroma",
      "collection": {
        "name": "openclaw_memory",
        "metadata": {"description": "OpenClaw 记忆存储"}
      },
      "embedding": {
        "model": "text-embedding-3-small",
        "dimension": 1536
      }
    }
  }
}
```

### Qdrant

生产级向量数据库，支持云部署。

```json
{
  "memory": {
    "type": "vector",
    "provider": "qdrant",
    "config": {
      "url": "http://localhost:6333",
      "collection": {
        "name": "openclaw_memory",
        "vector_size": 1536,
        "distance": "Cosine"
      },
      "hnsw": {
        "m": 16,
        "ef_construct": 100
      }
    }
  }
}
```

### Milvus

大规模向量检索，适合海量数据。

```json
{
  "memory": {
    "type": "vector",
    "provider": "milvus",
    "config": {
      "host": "localhost",
      "port": 19530,
      "collection": {
        "name": "openclaw_memory",
        "dimension": 1536,
        "metric_type": "IP"
      }
    }
  }
}
```

---

## 知识图谱配置

### NetworkX (轻量)

适合中小规模知识图谱。

```json
{
  "memory": {
    "type": "graph",
    "provider": "networkx",
    "config": {
      "persist_file": "~/.openclaw/knowledge_graph.gpickle",
      "node_types": ["entity", "concept", "event"],
      "edge_types": ["relates", "causes", "implies"],
      "inference": {
        "enabled": true,
        "max_depth": 3
      }
    }
  }
}
```

### Neo4j (生产级)

适合大规模图数据和企业应用。

```json
{
  "memory": {
    "type": "graph",
    "provider": "neo4j",
    "config": {
      "uri": "bolt://localhost:7687",
      "auth": {
        "username": "neo4j",
        "password": "your-password"
      },
      "database": "neo4j",
      "connection_pool": {
        "max_size": 50
      }
    }
  }
}
```

---

## 记忆策略

### 1. 基于时间的保留

```json
{
  "strategy": "time_based",
  "config": {
    "retention": {
      "recent": {"keep_minutes": 60},
      "short_term": {"keep_days": 7},
      "long_term": {"keep_days": 30}
    },
    "cleanup": {
      "schedule": "daily",
      "time": "02:00"
    }
  }
}
```

### 2. 基于重要性的保留

```json
{
  "strategy": "importance_based",
  "config": {
    "scoring": {
      "method": "llm",
      "prompt": "评估重要性 (0-1): {{content}}"
    },
    "retention": {
      "high": {"keep_forever": true},
      "medium": {"keep_days": 30},
      "low": {"keep_days": 7}
    }
  }
}
```

### 3. 基于频率的保留

```json
{
  "strategy": "frequency_based",
  "config": {
    "tracking": {
      "read_count": true,
      "access_history": true
    },
    "retention": {
      "hot": {"access_count": ">10"},
      "warm": {"access_count": "3-10"},
      "cold": {"access_count": "<3"}
    }
  }
}
```

### 4. 语义去重

```json
{
  "strategy": "deduplication",
  "config": {
    "enabled": true,
    "similarity_threshold": 0.95,
    "merge_strategy": "newest"
  }
}
```

---

## 跨会话记忆

### 用户画像

```json
{
  "type": "user_profile",
  "fields": {
    "preferences": {
      "language": "string",
      "topics_of_interest": ["string"]
    },
    "background": {
      "profession": "string",
      "expertise": ["string"]
    }
  }
}
```

### 上下文连续性

```json
{
  "type": "context_continuity",
  "config": {
    "enabled": true,
    "carry_forward": {
      "summary": true,
      "key_decisions": true,
      "pending_tasks": true
    },
    "look_back": {
      "sessions": 3,
      "include_summaries": true
    }
  }
}
```

---

## 配置示例

### 开发环境

```json
{
  "memory": {
    "type": "basic",
    "config": {
      "max_history": 50,
      "summary_enabled": true
    }
  }
}
```

### 生产环境

```json
{
  "memory": {
    "type": "hybrid",
    "config": {
      "short_term": {
        "type": "basic",
        "max_history": 100
      },
      "long_term": {
        "type": "vector",
        "provider": "chroma",
        "persist_directory": "/data/openclaw/chroma"
      },
      "transfer": {
        "enabled": true,
        "strategy": "importance",
        "threshold": 0.7
      }
    }
  }
}
```

### 企业环境

```json
{
  "memory": {
    "type": "hybrid",
    "config": {
      "short_term": {"type": "basic"},
      "long_term": {
        "type": "vector",
        "provider": "qdrant",
        "url": "https://qdrant.example.com:6333"
      },
      "graph": {
        "type": "graph",
        "provider": "neo4j",
        "uri": "bolt://neo4j.example.com:7687"
      }
    }
  }
}
```

---

## 最佳实践

1. **选择合适的记忆类型**
   - 简单对话 → Basic Memory
   - 语义检索 → Vector Memory
   - 复杂推理 → Graph Memory
   - 通用场景 → Hybrid Memory

2. **合理设置阈值**
   - `summary_threshold`: 影响上下文压缩时机
   - `top_k`: 影响检索精度和性能
   - `score_threshold`: 影响检索相关性

3. **定期清理**
   - 配置自动清理策略
   - 避免存储空间耗尽
   - 保持检索效率

4. **备份恢复**
   - 定期备份向量数据
   - 测试恢复流程
   - 验证数据完整性
