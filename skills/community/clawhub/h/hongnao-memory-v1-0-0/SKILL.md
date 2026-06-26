# 弘脑记忆系统 (HongNao Memory OS)

为 OpenClaw 打造的长期记忆操作系统，实现跨 Session 记忆持久化、智能检索和用户偏好学习。

## 快速开始

### 安装

```bash
# 自动安装 (推荐)
python3 install_hongnao.py

# 或手动安装
pip3 install -r requirements.txt
```

### 基本使用

```python
from memory_api import HongNaoMemorySystem, MemorySystemConfig

# 初始化
config = MemorySystemConfig()
memory_system = HongNaoMemorySystem(config)

# 添加记忆
memory_system.add_memories_from_text("用户喜欢简洁的沟通风格", source="chat")

# 检索记忆
result = memory_system.retrieve_memories("用户偏好")
print(result['context'])
```

## 核心功能

- **4 层记忆架构**: 抽取 → 巩固 → 检索 → 更新
- **OpenClaw 集成**: Session 自动同步到记忆系统
- **用户偏好学习**: 自动识别用户习惯和偏好
- **混合检索**: 向量 + 关键词，召回率>90%
- **记忆压缩**: Token 节省~45%

## 性能指标

| 指标 | 目标 | 实测 |
|------|------|------|
| 添加延迟 | <10ms | **0.03ms** ✅ |
| 检索延迟 | <100ms | **0.27ms** ✅ |
| 召回率 | >90% | **100.0%** ✅ |
| Token 节省 | >40% | **~45%** ✅ |

## 配置

编辑 `hongnao_memory_config.ini`:

```ini
[memory]
db_path = ~/.openclaw/workspace/hongnao_memory/hongnao.db
vector_store_path = ~/.openclaw/workspace/hongnao_memory/chroma_db

[preference_learning]
enable_preference_learning = true
confidence_threshold = 0.6
```

## 文档

- **快速入门**: `快速入门.md`
- **集成指南**: `集成指南.md`
- **发布说明**: `RELEASE_NOTES.md`

## 测试

```bash
# 核心模块测试
python3 test_core_modules.py

# 性能基准测试
python3 quick_benchmark.py
```

## 系统要求

- Python >= 3.8
- OpenClaw >= 0.1.0
- 支持平台：Linux, macOS, Windows

## 依赖

- chromadb >= 0.4.0
- numpy >= 1.20.0
- sentence-transformers >= 2.2.0

## 许可证

MIT License

## 联系方式

- 作者：燧弘华创
- 邮箱：contact@hongnao.ai
- 主页：https://github.com/hongnao/hongnao_memory
