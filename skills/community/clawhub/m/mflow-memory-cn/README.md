# mflow-memory-cn 中式智慧记忆引擎

> "君子务本，本立而道生。" — 《论语》

基于M-flow知识图谱的长期记忆系统，融合中国人的优秀基因，让AI既有能力，又有情商。

## 五大核心模块

| 模块 | 对应 | 功能 |
|------|------|------|
| MemoryStore | 仁 (Ren) | 以人为本，存储人情而非只存事实 |
| PromiseTracker | 义 (Yi) | 一诺千金，承诺追踪 |
| RelationshipManager | 五伦 | 关系亲密度管理 |
| TimingSensor | 礼 (Li) | 懂分寸，审时度势 |
| WisdomEngine | 智 (Zhi) | 举一反三，触类旁通 |

## 安装

```bash
cd skills
clawhub install mflow-memory-cn
```

## 使用

### Python API

```python
from core.main import ChineseMemoryEngine

# 创建引擎
engine = ChineseMemoryEngine()

# 存储记忆（自动识别情感和承诺）
engine.remember("我不喜欢太复杂的工具", emotion="明确", value="效率优先")

# 检索记忆（举一反三）
results = engine.recall("想要一个简单的工作流工具")

# 承诺追踪
engine.register_promise("周末把报告发我", deadline="本周末")

# 检查承诺状态
status = engine.check_promises()

# 响应前分析（最重要）
analysis = engine.analyze_before_response("有什么工具推荐吗？")
```

### OpenClaw工具

```python
from openclaw_tools import *

# 响应前必调
analysis = analyze_before_response(user_message)

# 存储记忆
remember("用户偏好简洁界面", emotion="明确")

# 承诺追踪
register_promise("明天发报告")
```

## 数据存储

所有数据存储在 `~/.mflow-memory-cn/`:

```
.mflow-memory-cn/
├── data/           # 主记忆文件
├── promises/       # 承诺追踪
├── relationships/  # 关系管理
└── wisdom/         # 智慧引擎
```

## 设计理念

西方技术 + 中国智慧 = 既有能力，又有情商

- **西方**: 知识图谱、向量检索、语义理解
- **中国**: 人情世故、审时度势、举一反三

---

*Created by 马斯克 for JOJO | 2026-04-23*
