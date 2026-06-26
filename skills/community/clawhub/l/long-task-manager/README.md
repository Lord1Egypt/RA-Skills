# Long Task Manager

**版本**: v1.0  
**OpenClaw Skill**  
**解决AI Agent长时间任务超时问题**

---

## 📦 功能特性

- ✅ **无超时执行** - 支持任意时长任务
- 📊 **实时进度** - 0-100% 进度可视化
- 🔄 **异步非阻塞** - 提交后立即返回
- ❌ **任务取消** - 支持中途取消
- 💾 **状态持久化** - 跨会话保持

---

## 🚀 快速开始

### 安装

```bash
# 复制到skills目录
cp -r long-task-manager ~/.openclaw/workspace/skills/
```

### 基础用法

```python
from skills.long_task_manager import LongTaskManager

# 初始化
manager = LongTaskManager()

# 提交任务
task_id = manager.submit(
    agent_id="code_gen_ali",
    task_config={
        "name": "生成50个API",
        "total_items": 50
    }
)

# 查询进度
status = manager.get_status(task_id)
print(f"进度: {status['progress']}")
```

---

## 📚 完整文档

- [SKILL.md](SKILL.md) - 详细使用文档
- [examples/](examples/) - 使用示例
- [tests/](tests/) - 测试用例

---

## 📂 文件结构

```
long-task-manager/
├── SKILL.md              # 技能说明文档
├── README.md             # 本文件
├── AGENTS_REGISTER.md    # AGENTS.md注册配置
├── lib/
│   └── long_task_manager.py  # 核心实现
├── examples/
│   └── basic_usage.py    # 使用示例
└── tests/
    └── test_basic.py     # 测试用例
```

---

**🎉 开始使用 Long Task Manager!**
