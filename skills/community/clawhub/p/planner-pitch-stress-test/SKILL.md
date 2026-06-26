---
name: planner-pitch-stress-test
description: "策划案压力测试：在隔离环境中对通过 Pitch Review 的策划案执行四轮对抗式攻击，验证不可替代性。触发词：压力测试、stress test、对抗审查、不可替代性验证、pitch攻击。"
metadata:
  tier1_summary: "Pitch Review通过后强制执行：四轮隔离对抗攻击（市场/引擎/角色/情感），任何一轮REJECT则打回重写"
---

# Planner Pitch Stress Test（策划案压力测试）

**触发条件**：Pitch Review（节点 5）通过后，Downstream Development（节点 6）之前。是 Downstream Development 的强制前置门控。

**核心使命**：证明这个 pitch **还不够好**。

> 你不是来确认它没问题的，你是来证明它有问题的。

参考皮克斯 Brain's Trust 机制——审查的价值不在于放行，而在于拦截。宁可误杀，不可放水。

---

## 运行方式

**必须在 isolated session 中运行**（`sessions_spawn`），与创作流程隔离。创作惯性是最危险的盲区——写 pitch 的人不可能公正地审查自己的 pitch。

---

## 四轮攻击

### 第 1 轮：市场攻击

**身份**：平台采购总监

**核心问题**：如果我是平台采购，我为什么不买？

**攻击清单**：
- [ ] Comparable Triple 中的差异化是否真正不可替代？还是"我们也有一个XX元素"式的微调？
- [ ] 目标受众是否足够清晰？还是"老少皆宜"式的自欺？
- [ ] 这个 pitch 的 30 秒电梯演讲能打动我吗？还是需要 5 分钟才能解释清楚"它好在哪"？
- [ ] 市场上有没有已经在做类似事情的项目？如果有，你的优势是什么？
- [ ] 标题/概念是否在 3 秒内让人想点进来？

**评分**：1-5 分

### 第 2 轮：引擎攻击

**核心问题**：这个设定能出 50 集不同的故事吗？

**攻击清单**：
- [ ] 列举 10 个不同的集数前提——如果列不出来或大量重复 → 引擎不够
- [ ] 拿掉主角，世界还在生故事吗？如果不能 → 世界只是背景板
- [ ] 换一组角色进入同一世界，故事还能成立吗？如果能 → 角色和世界没有有机联系
- [ ] 每集的冲突来源是角色内在矛盾还是外部事件堆砌？如果主要是外部 → 引擎不可持续
- [ ] 第三季还能有新东西吗？还是第二季就开始重复？

**评分**：1-5 分

### 第 3 轮：角色攻击

**核心问题**：拿掉任何一个核心角色，故事还成立吗？

**攻击清单**：
- [ ] 每个核心角色都有 Want/Need/Wound 三层吗？只有 Want → 是工具人
- [ ] 遮住名字只看行为，能分辨出谁是谁吗？如果不能 → 声纹缺失
- [ ] 反派的动机是否与主角一样有说服力？如果反派只是"坏人" → 对抗不够
- [ ] 角色之间的关系是动态的还是固定的？如果从第 1 集到第 50 集关系不变 → 没有成长空间
- [ ] 删除任何一个核心角色后，重新审视——如果故事基本不受影响 → 这个角色是多余的

**评分**：1-5 分

### 第 4 轮：情感攻击

**核心问题**：观众看到第 10 集还关心这些人吗？

**攻击清单**：
- [ ] Emotional Promise 是否清晰？观众在第 1 集就知道自己被承诺了什么情感体验吗？
- [ ] Theme Statement 是否在情感层面被感受到，而不是被"说"出来？
- [ ] 观众对主角的情感连接是建立在理解还是同情上？同情 → 不可持续
- [ ] 如果提前知道结局，观众还愿意看过程吗？如果不愿意 → 过程没有独立价值
- [ ] 第 10 集的情感赌注比第 1 集更高吗？如果不是 → 情感弧线在退化

**评分**：1-5 分

---

## 判定规则

| 条件 | 判定 | 处理 |
|------|------|------|
| 任意轮 ≤ 2 分 | **REJECT** | 强制打回 Pitch Review 重写，附 mandatory_rewrites |
| 平均分 < 3.5 | **CONDITIONAL** | 需针对 mandatory_rewrites 修改后重新提交压力测试 |
| 平均分 ≥ 3.5 且无 ≤ 2 分 | **PASS** | 进入 Downstream Development |

---

## 输出格式

```json
{
  "stress_test": {
    "market_attack": { "score": 4, "notes": "...", "mandatory_rewrites": [] },
    "engine_attack": { "score": 3, "notes": "...", "mandatory_rewrites": ["引擎需补充至少3种独立冲突模式"] },
    "character_attack": { "score": 5, "notes": "..." },
    "emotional_attack": { "score": 2, "notes": "...", "flag": "REJECT", "mandatory_rewrites": ["Emotional Promise 不清晰，需在第1集建立明确承诺"] },
    "verdict": "REJECT",
    "all_mandatory_rewrites": ["引擎需补充至少3种独立冲突模式", "Emotional Promise 不清晰，需在第1集建立明确承诺"]
  }
}
```

---

## 与上下游的关系

| 上下游 | 关系 |
|-------|------|
| Pitch Review（上游） | Stress Test 的输入是 Pitch Review 的通过稿 |
| Pitch Draft（更上游） | REJECT 时回到 Pitch Review 重写，Pitch Review 可能决定回到 Pitch Draft 重新生成 |
| Downstream Development（下游） | 只有 PASS 的项目才能进入 |
| Theme Lock | 第 4 轮情感攻击以 Theme Statement 为核心评判依据 |

---

## REJECT 后的重试规则

1. 第一次 REJECT → 回到 Pitch Review，附 mandatory_rewrites → 修改后重新 Stress Test
2. 第二次 REJECT → 回到 Pitch Draft 重新生成，原稿存档
3. 第三次 REJECT → `help_requested`，标记为"项目基础可能不成立"

---

## 硬规则

1. **必须在 isolated session 中运行**——与创作流程隔离，不受创作惯性影响
2. **不得手下留情**——审查者的价值在于拦截，不在于放行
3. **每条 notes 必须指向具体问题**——"感觉不够好"不是有效审查
4. **只提问题，不给答案**——改写是 Pitch Review 的工作，Stress Test 只负责暴露问题
5. **Stress Test 是 Downstream Development 的强制前置门控**——未通过不得进入下游
6. **REJECT 后的重试最多 3 次**——3 次仍不通过说明项目基础可能不成立
