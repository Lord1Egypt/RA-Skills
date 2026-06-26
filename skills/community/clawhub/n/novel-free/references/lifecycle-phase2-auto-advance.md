# Phase 2 自动推进（novel-free 轻量版）

> 本文档是 novel-free 的自动推进机制。相较于 12agent-novel 原版，差异如下：
> 自动推进流程与原版完全一致；差异仅在合并触发逻辑和固定层来源。

---

## novel-free 差异说明

### 合并触发检查（每章 closed 后）

原版在每章闭环后分别检查 RollingSummarizer 和 ReaderSimulator 触发阈值。
novel-free 在此基础上优先使用 SummarizerGuardianCombo：

```
每章 closed 后：

1. 里程碑审计检查（每20章，优先级最高，与原版相同）

2. 合并触发检查：
   if (lastClosedChapter % 5 === 0 && lastClosedChapter - lastOocCheckChapter >= 4) {
     → spawn SummarizerGuardianCombo（摘要+OOC合并，mode:"run" 异步）
     → lastRollingSummaryChapter = lastClosedChapter
     → lastOocCheckChapter = lastClosedChapter
   } else if (lastClosedChapter % 5 === 0) {
     → spawn RollingSummarizer（单独，mode:"run" 异步）
     → lastRollingSummaryChapter = lastClosedChapter
   } else if (需要提前OOC) {
     → spawn OOCGuardian（单独，mode:"run" 异步）
     → lastOocCheckChapter = lastClosedChapter
   }

3. ReaderSimulator 触发检查（每5章，与原版相同）
   if (lastClosedChapter % 5 === 0) {
     → spawn ReaderSimulator（mode:"run" 异步）
   }
```

> 注意：当同时触发 SummarizerGuardianCombo 和 ReaderSimulator 时，两者均以 mode:"run" 异步执行，不阻塞自动推进循环。

### 固定层

自动推进循环中，Coordinator 使用已加载的 fixed-context.md 缓存，不重复读取原始文档。

### 恢复协议补充

恢复时除原版检查项外，额外验证：
- `references/fixed-context.md` 是否存在且为最新版本
- 若世界观/角色/大纲在上次会话后有变更，先刷新 fixed-context.md 再恢复推进

---

## 完整流程

其余内容（参数定义、状态管理、异常处理、恢复机制）与标准版一致，参见 workflow-state-machine.md 和 resume-protocol.md。

## 调用次数节省预估（自动推进8章）

| 触发类型 | 标准版（12agent-novel） | novel-free |
|---------|--------------|------------|
| 第5章：RollingSummarizer + OOCGuardian | 2次 | **1次（Combo）** |
| 第10章：同上 | 2次 | **1次（Combo）** |
| 8章内其他OOC | 0-1次 | 0-1次 |
| **合计节省** | 基准 | **约2次/8章** |
