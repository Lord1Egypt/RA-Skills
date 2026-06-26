# Phase 2 重点章节工作流（novel-free 轻量版）

> 本文档是 novel-free 的重点章节工作流。相较于 12agent-novel 原版，核心差异为：
> 核心差异：固定层强制读 fixed-context.md；合并触发逻辑与 lifecycle-phase2-normal.md 一致。
> 重点章节流程步骤数与原版相同（Step 0-9），仅固定层输入来源和合并触发逻辑有变化。

## 重点章节判定

满足任一条件即为重点章节：
- 用户手动指定"重点章"
- 细纲标注：高潮/转折/情感爆发
- 首章(Ch1)
- 末章(ChN，从meta/config.md读取total_chapters)
- 幕间分界章（从meta/config.md的key_chapters读取）

---

## novel-free 差异说明

### 固定层输入（所有 spawn 调用统一变更）

所有子 Agent 的固定层输入改为：
```javascript
// ❌ 原版（禁止）
${read("worldbuilding/world.md")}
${read("characters/protagonist.md")}

// ✅ novel-free（强制）
${read("references/fixed-context.md")}
```

### Step 6 OOC 检查（重点章节强制执行）

重点章节的 OOC 检查**不使用** SummarizerGuardianCombo，始终单独调用 OOCGuardian（保持重点章节的审校质量）。

同时检查是否需要合并触发摘要：
```
if (completedChapter % 5 === 0) {
  // 额外单独触发 RollingSummarizer（重点章节 OOC 已单独执行，不合并）
  → spawn RollingSummarizer
}
```

### Step 2/3/4 FinalReviewer + MainWriter

所有 spawn 调用中，固定层部分替换为 `${read("references/fixed-context.md")}`，其余与 novel-free 原版完全一致。

---

## 完整流程

完整流程步骤（Step 0-9）详见 references/lifecycle-phase2-key-chapter.md，以下仅列出差异点。

**唯一变更点：**
1. 所有 sessions_spawn 中的固定层输入改为 `references/fixed-context.md`
2. Step 6 OOC 检查始终单独调用（不合并），但额外检查是否触发独立 RollingSummarizer
3. style-anchor.md 上限 ≤600字（硬限）

---

## 子 Agent 调用次数对比

| 场景 | 标准版（12agent-novel） | novel-free |
|------|--------------|------------|
| 重点章（非5章倍数） | 5次 | 5次（不变）|
| 重点章（5章倍数） | 6次（+RollingSummarizer） | 6次（OOC单独+RollingSummarizer单独）|

> 重点章节不合并，保留最高质量审校流程。节省来自固定层 token 压缩，不来自调用次数减少。
