---
name: adversarial-engine
version: 2.0.0
priority: P1
description: "多模型对抗引擎 - 四模型真实对抗辩论系统。架构师+工程师+安全官+仲裁者协作，代码沙箱验证，向量检索增强，收敛判断自动熔断。"
author: 海狸 🦫
triggers:
  - 多模型对抗
  - 对抗辩论
  - 方案评审
  - 代码验证
---

# 多模型对抗引擎 v2.0

## 核心能力

| 能力 | 说明 |
|------|------|
| 🎭 四模型对抗 | 架构师/工程师/安全官/仲裁者真实协作 |
| 🔧 代码沙箱 | 工程师生成代码 → Python执行验证 |
| 📚 向量检索 | 对话前检索知识库，避免假数据 |
| ⚖️ 收敛判断 | 仲裁者动态判断，避免无限循环 |
| 🔄 断点续传 | 中断后可恢复辩论 |
| 📡 WebSocket | 实时推送辩论进度 |

---

## 四模型配置

| 角色 | 模型 | 职责 |
|------|------|------|
| 🏗️ 架构师 | qwen3.5-plus | 方案生成 |
| 🔧 工程师 | qwen3-coder-plus | 代码实现+验证 |
| 🔍 安全官 | kimi-k2.5 | 漏洞攻击 |
| ✅ 仲裁者 | MiniMax-M2.5 | 收敛判断 |

---

## 执行流程

```
用户输入
    ↓
[1] 向量检索 → 知识库增强
    ↓
[2] 架构师 → 提出方案
    ↓
[3] 工程师 → 生成代码 → Python沙箱执行
    ↓
[4] 安全官 → 攻击漏洞
    ↓
[5] 仲裁者 → 收敛判断
    ↓
[6] 未收敛 → 返回[2]继续
    ↓ 已收敛
[7] 保存结论 → 知识库固化
```

---

## API接口

### 启动对抗

```python
from adversarial_engine import AdversarialEngine

engine = AdversarialEngine()
session = engine.run_debate(
    topic="如何设计高并发CNC报价系统？",
    max_rounds=5,
    enable_code_sandbox=True,
    enable_vector_search=True
)
```

### WebSocket实时推送

```
ws://host:8083/ws
→ 实时推送每轮辩论内容
```

---

## 文件结构

```
adversarial-engine/
├── SKILL.md           # 本文件
├── engine.py          # 核心引擎
├── code_sandbox.py    # Python沙箱
├── vector_enhancer.py # 向量检索增强
├── ws_server.py       # WebSocket服务
└── database.py        # 数据持久化
```

---

🦫 海狸 | 靠得住、能干事、在状态