---
name: llm-memory-integration
description: LLM Memory Integration - 纯接口包。提供 Memory、Search、Vector 接口定义，实现由私有包提供。
version: 9.0.0
license: MIT-0
author: xkzs2007
homepage: https://clawhub.ai/skill/llm-memory-integration
requirements:
  binaries: []
  envVars:
    required: []
    optional: []
  network: false
security_note: |
  ✅ 安全说明（v9.0.0 纯接口版）：
  
  【纯接口包】
  - ✅ 仅包含接口定义（ABC 抽象类）
  - ✅ 无任何实现代码
  - ✅ 无网络访问
  - ✅ 无文件系统访问
  - ✅ 无 subprocess 调用
  - ✅ 无原生扩展
  
  【实现来源】
  - 实现代码由私有包提供：https://cnb.cool/llm-memory-integrat/llm.git
  - 用户需手动安装私有包或使用完整版
---

# LLM Memory Integration - 纯接口包

## ⚠️ 重要说明

**本包为纯接口定义包，不包含任何实现代码。**

| 组件 | 本包 | 私有包 |
|------|------|--------|
| 接口定义 | ✅ | - |
| 实现代码 | ❌ | ✅ |
| 网络访问 | ❌ | ✅ |
| 原生扩展 | ❌ | ✅ |

## 接口列表

### MemoryInterface
记忆管理接口：add, get, update, delete, list

### SearchInterface
搜索接口：search, hybrid_search, fts_search

### VectorInterface
向量接口：embed, embed_single, similarity, batch_embed

## 获取完整实现

```bash
# 克隆私有包
git clone https://cnb.cool/llm-memory-integrat/llm.git

# 或查看私有包说明
# https://cnb.cool/llm-memory-integrat/llm
```

## 使用示例

```python
from src.interfaces import MemoryInterface, SearchInterface, VectorInterface

# 实现这些接口
class MyMemory(MemoryInterface):
    def add(self, content, metadata=None):
        # 你的实现
        pass
    # ... 其他方法
```

---

*纯接口包 v9.0.0 - 无实现、无风险*
