# OCAX Passport Skill

## 简介

OCAX Passport 技能用于生成和管理节点身份证，展示节点硬件信息、信誉评分和支持的计算任务类型。

## 功能

- 获取节点硬件信息 (CPU/GPU/内存/存储/网络)
- 计算节点信誉评分
- 生成节点身份证 (Passport ID / Node ID)
- 支持的任务类型检测
- 自动更新节点信息

## 触发词

- "passport" - 获取节点护照
- "节点信息" - 查看硬件信息
- "节点评分" - 查看信誉评分
- "我的节点" - 查看完整节点信息

## 使用方法

```python
from ocax_passport import generate_passport

# 生成节点护照
passport = generate_passport("My-Node", "User-Name")

# 获取节点信息
info = passport.to_json()

# 获取评分
scores = passport.scores

# 获取最佳任务
best_task = passport.scores.get("best_task")

# 启用自动更新
passport.enable_auto_update(86400)  # 24小时
```

## 输出示例

```json
{
  "passport_id": "OCAX-PASSPORT-20260315-xxx",
  "node_id": "OCAX-NODE-20260315-xxx",
  "node_name": "My-PC",
  "hardware": {
    "cpu": {"cores": 16, "model": "AMD Ryzen 9"},
    "memory": "32GB",
    "gpu": "RTX 4090"
  },
  "reputation": {"score": 100, "completed_tasks": 0},
  "supported_tasks": ["image_processing", "ai_inference"]
}
```

## 依赖

- psutil
- python 3.8+

---

*Version: 1.0*
*Author: OCAX Team*
