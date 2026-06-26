# Complete Memory System v4.0

完整记忆系统 - 统一整合所有记忆功能

## 功能

- 双脑架构（SQLite + LanceDB）
- 四层记忆栈（工作/情景/语义/程序）
- 四策略检索（归因/时间衰减/重要性/语义）
- ToM心智模型
- 情感分析（EQ改进）
- 增强检索（Memory改进）
- GBrain核心（Originals/Entity/Brain-First等）
- MemPalace（AAAK日记/情感标记）
- Ultimate Memory v3.0（8大系统）
- Ollama本地嵌入（可选）

## 安装

```bash
python scripts/init_complete_database.py
python scripts/verify_complete_install.py
```

## 使用

```python
from complete_memory_system import CompleteMemorySystem

system = CompleteMemorySystem()
system.initialize()

# 添加记忆
mem_id = system.add_memory("learning", "学习Python", "今天学习Python", importance=8)

# 搜索
results = system.search("Python")
smart = system.smart_search("Python", mode="balanced")

# 情感分析
emotion = system.analyze_emotion("I am happy!")

# 写日记
system.write_diary("完成学习", learnings=["Python"], decisions=["继续学习"])

system.close()
```

## 文档

- `docs/GBRAIN_GUIDE.md` - GBrain指南
- `docs/MEMPALACE_USAGE.md` - MemPalace使用
- `docs/ULTIMATE_V3.md` - 终极系统v3.0

## 版本

v4.0 - 2026-04-11
