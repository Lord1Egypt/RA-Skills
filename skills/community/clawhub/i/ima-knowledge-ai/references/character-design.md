# Character Design / IP 角色设计

> **核心挑战**: 保证角色在多场景下的视觉一致性

---

## 1. 应用场景

| 场景 | 典型产物 | 一致性需求 |
|------|---------|-----------|
| 游戏开发 | 游戏角色、NPC | 多角度 3D 参考 |
| 动画制作 | 主角、配角 | 多表情、动作 |
| 漫画/画册 | 故事角色 | 多场景一致 |
| IP 开发 | 品牌吉祥物 | 跨平台一致 |
| 周边产品 | 手办、玩具 | 实体化参考 |

---

## 2. 核心交付物

### 2.1 多角度视图 (Turnaround)

**标准视图**: 正面 / 侧面 / 背面 / 3/4 视角  
**高级需求**: 45° 完整旋转 (8 方向)

### 2.2 表情库 (Expression Sheet)

**基础**: 喜/怒/哀/惧/惊/中性 (6 个)  
**扩展**: 困惑/害羞/得意/疲惫... (10-20 个)

### 2.3 服装变体 (Outfit Variants)

**类型**: 日常 / 战斗 / 礼服 / 休闲 / 特殊皮肤  
**每套**: 完整 Turnaround + 细节特写

### 2.4 道具/武器 (Props)

**类型**: 武器 / 装备 / 饰品 / 特殊物品  
**需求**: 多角度 + 持握状态 + 特效

### 2.5 动作姿态 (Pose)

**基础**: 站立 / 行走 / 奔跑 / 跳跃 / 攻击 / 防御  
**高级**: 技能动作 / 胜利姿势 / 失败姿势

---

## 3. Reference-Driven 工作流

### 核心方法论

```
Step 1: 生成 Master Reference (基础设定图)
  ↓
Step 2: 用 Master 生成所有 Variants
  ↓
Step 3: reference_strength 分层控制一致性
```

### 工作流程

**Phase 1: Master Reference**
- 生成高质量角色正面图 (SeeDream 4.5 / Nano Banana Pro 4K)
- 提示词: 完整描述 (外貌/服装/特征/风格)
- 质量要求: 清晰、高分辨率、细节丰富

**Phase 2: Turnaround Sheet**
- 用 Master 作为参考图
- 生成侧面/背面/3/4 视图
- reference_strength: 0.90-0.95 (高一致性)
- 提示词: "same character, side view" / "back view"

**Phase 3: Expression Library**
- 用 Master 作为参考图
- 生成各种表情 (喜/怒/哀/惧/惊/中性)
- reference_strength: 0.92-0.95 (面部一致性最重要)
- 提示词: "same character, happy expression" / "angry face"

**Phase 4: Outfit Variants**
- 用 Master 作为参考图
- 生成不同服装
- reference_strength: 0.85-0.90 (允许服装变化)
- 提示词: "same character, battle armor" / "casual outfit"

**Phase 5: Props & Poses**
- 用 Master 作为参考图
- 生成持握道具、动作姿态
- reference_strength: 0.80-0.88 (允许姿势变化)
- 提示词: "same character, holding sword" / "running pose"

---

## 4. reference_strength 策略

| 交付物 | 推荐值 | 说明 |
|--------|--------|------|
| Master Reference | - | 基准图，无参考 |
| Turnaround (正/侧/背) | 0.90-0.95 | 高度一致 |
| Expression (表情) | 0.92-0.95 | 面部特征最重要 |
| Outfit (服装) | 0.85-0.90 | 允许服装变化 |
| Props (道具) | 0.80-0.88 | 允许姿势变化 |
| Action Pose (动作) | 0.75-0.85 | 允许动态变化 |

**原则**: 越需要保持一致的部分，strength 越高

---

## 5. 实战案例模板

### RPG 游戏角色 "Aria"

**需求**: 女剑士，多角度 + 表情 + 装备

**Phase 1: Master Reference**
- 提示词: "Female warrior Aria, 25 years old, short silver hair, blue eyes, leather armor, confident expression, fantasy style, 4K quality"
- 模型: Nano Banana Pro 4K
- 成本: 18 pts

**Phase 2: Turnaround (3 视图)**
- 侧面: "same character, side view, leather armor" (strength 0.92)
- 背面: "same character, back view, leather armor" (strength 0.92)
- 3/4: "same character, 3/4 view, leather armor" (strength 0.90)
- 成本: 3×18 = 54 pts

**Phase 3: Expression (6 表情)**
- 各表情: "same character, [expression] face" (strength 0.94)
- 成本: 6×18 = 108 pts

**Phase 4: Battle Armor**
- Turnaround: "same character, heavy plate armor, [view]" (strength 0.88)
- 成本: 3×18 = 54 pts

**Phase 5: Props (2 武器)**
- 大剑: "same character, holding greatsword, battle stance" (strength 0.85)
- 盾牌: "same character, with shield, defensive pose" (strength 0.85)
- 成本: 2×18 = 36 pts

**总成本**: 270 pts | **总时间**: 2-3 小时  
**交付物**: 1 Master + 3 视图 + 6 表情 + 3 战甲视图 + 2 武器 = **15 张**

---

## 6. 常见错误

### ❌ 错误 1: 跳过 Master Reference
**问题**: 直接生成多个视图，没有统一参考  
**后果**: 每张图都不一样  
**解决**: 必须先生成高质量 Master

### ❌ 错误 2: reference_strength 过低
**问题**: 0.70 以下导致一致性差  
**解决**: Turnaround 用 0.90+，Expression 用 0.92+

### ❌ 错误 3: Master Reference 质量差
**问题**: 模糊、低分辨率、细节缺失  
**解决**: 用高端模型 (Nano Banana Pro 4K / SeeDream 4.5)

### ❌ 错误 4: 提示词不一致
**问题**: Master 描述 "silver hair"，Variant 用 "blonde hair"  
**解决**: 所有 Variant 都用 "same character" + 保持核心特征描述

---

## 7. 工作流对比

| 方法 | 一致性 | 成本 | 时间 | 控制度 |
|------|--------|------|------|--------|
| **Reference-Driven** ✅ | 高 | 中 | 2-3h | 高 |
| 多次独立生成 | 低 | 高 (重复) | 4-6h | 低 |
| 手工修图 | 极高 | 极高 | 数天 | 极高 |

---

## 8. Quick Reference

### 交付物清单

| 项目 | 数量 | reference_strength | 成本估算 |
|------|------|-------------------|---------|
| Master Reference | 1 | - | 18 pts |
| Turnaround | 3-4 | 0.90-0.95 | 54-72 pts |
| Expression | 6-10 | 0.92-0.95 | 108-180 pts |
| Outfit Variants | 2-3 套 × 3 视图 | 0.85-0.90 | 108-162 pts |
| Props | 2-4 | 0.80-0.88 | 36-72 pts |

**典型项目**: 1 Master + 3 视图 + 6 表情 + 2 服装 + 2 道具 = **270-400 pts**

### 核心原则

1. **Master First** — 必须先生成高质量基准图
2. **reference_strength 分层** — 面部最高，动作最低
3. **"same character" 提示词** — 明确告诉模型保持一致
4. **高质量参考图** — 用 4K 模型，清晰细节丰富
5. **迭代优化** — 不满意就调整 strength 重新生成

---

**记住**: Character Design = Master Reference + 分层 reference_strength 🎨
