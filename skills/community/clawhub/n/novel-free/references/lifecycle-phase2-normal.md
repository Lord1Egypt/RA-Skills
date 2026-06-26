# Phase 2 常规章节工作流（novel-free 轻量版）

> 本文档是 novel-free 的常规章节工作流。相较于 12agent-novel 原版，核心差异为：核心差异：固定层强制读 fixed-context.md；合并触发 SummarizerGuardianCombo 替代分开触发 RollingSummarizer+OOCGuardian。

## 轨道判定

常规章节 = 不满足以下任何条件的章节：
- 用户手动指定"重点章"
- 细纲标注高潮/转折/情感爆发
- 首章(Ch1) / 末章(ChN)
- 幕间分界章（从 meta/config.md 的 key_chapters 读取）

---

## 先决条件（强制）

进入本流程前，Coordinator 必须确认：
1. `meta/workflow-state.json.phaseState.currentPhase = 2`
2. `references/fixed-context.md` 已生成（Phase 2 首次进入时生成）
3. 不存在未闭环章节
4. 已执行 resume-protocol.md 恢复校验

---

## 工作流

### Step 0：恢复与轨道锁定

更新 `meta/workflow-state.json`：
- `currentChapter = chapterNum`
- `currentTrack = "normal"`
- `chapterEntryChecklistComplete = false`
- 重置 `currentChapterArtifacts`
- `resumeRequired = false`

---

### Step 1：写前核查（强制）

**固定层读取（novel-free 规则）：**
- ✅ 读 `references/fixed-context.md`（世界观摘要≤800字 + 角色摘要≤1200字 + 大纲≤3000字）
- ❌ 禁止读 `worldbuilding/world.md` / `characters/*.md` / `outline/outline.md` 作为固定层

**Session Cache：** 同一会话内 fixed-context.md 只读一次，后续章节直接复用，不重复读取文件。世界观/角色/大纲变更后刷新。

**写前核查清单（Coordinator 必须先回答）：**
- [ ] 上章结尾场景/情绪/悬念 → 本章开头如何承接？
- [ ] 主角当前状态（位置/修为/持有物）？
- [ ] 本章需推进/回收的伏笔ID？
- [ ] 本章涉及的角色关系变化？
- [ ] 本章在全书节奏中的定位？
- [ ] 本章字数目标？

完成后更新：
- `chapterEntryChecklistComplete = true`
- `currentChapterArtifacts.plan = true`

---

### Step 2：spawn MainWriter 初稿+润色（单次调用）

```javascript
sessions_spawn({
  task: `${read("references/agent-main-writer.md")}

【本次任务】
完成第${chapterNum}章的初稿+润色，一次性输出可交付版本。

【固定层（来自 fixed-context.md）】
${read("references/fixed-context.md")}

【风格锚定（≤600字）】
${read("meta/style-anchor.md")}

【滚动层】
- 滚动摘要: ${rollingSummary}
- 最近3章原文: ${recentChapters}

【按需层】
- 本章细纲: ${chapterOutline}
- 本章规划: ${chapterPlan}
- 本章相关伏笔/关系: ${onDemandContext}
- 字数目标: ${wordTarget}字`,
  label: "main-writer-ch" + chapterNum,
  model: readConfig("meta/config.md", "mainWriter"),
  mode: "run",
  cleanup: "delete",
  runTimeoutSeconds: 900
})
```

完成后更新：
- `currentChapterArtifacts.draft = true`
- `currentChapterArtifacts.polish = true`

---

### Step 3：一致性检查

**合并触发判定（novel-free 核心优化）：**

```
if (completedChapter % 5 === 0 && currentChapter - lastOocCheckChapter >= 4) {
  → spawn SummarizerGuardianCombo（一次调用，输出摘要+OOC双结果）
  → 完成后：lastRollingSummaryChapter = chapterNum, lastOocCheckChapter = chapterNum
} else if (需要提前OOC触发) {
  // 条件：高潮/转折/新增重要角色/字数≥4800
  → spawn OOCGuardian（单独调用）
  → 完成后：lastOocCheckChapter = chapterNum
} else if (completedChapter % 5 === 0) {
  → spawn RollingSummarizer（单独调用，OOC未到阈值）
  → 完成后：lastRollingSummaryChapter = chapterNum
} else {
  → Coordinator 轻量自查（100-200字，写入 archive/archive.md）
}
```

**SummarizerGuardianCombo spawn 调用：**

```javascript
sessions_spawn({
  task: `${read("references/agent-summarizer-guardian-combo.md")}

【本次任务】
合并执行：第${startCh}-${endCh}章滚动摘要 + 第${chapterNum}章 OOC 检查。

【固定层（来自 fixed-context.md）】
${fixedContext}

【最近5章原文（用于摘要）】
${recentFiveChapters}

【前1章原文（用于OOC章间检查）】
${prevChapter}

【本章正文（用于OOC检查）】
${currentChapterText}

【伏笔追踪表】
${read("references/plot-tracker.md")}`,
  label: "combo-ch" + chapterNum,
  model: readConfig("meta/config.md", "rollingSummarizer"),
  mode: "run",
  cleanup: "delete",
  runTimeoutSeconds: 900
})
```

完成后更新：`currentChapterArtifacts.oocCheck = true`

---

### Step 4：Coordinator 整合 → 输出终稿

依据检查结果修正，输出终稿。P1 以上问题未修复前不得归档。
写入：`chapters/ch{NNN}.md`

---

### Step 5：存档闭环（使用 chapter-commit-template.md）

按顺序一次性完成所有写入：
1. `chapters/ch{NNN}.md`
2. `meta/workflow-state.json`
3. `meta/metadata.json`
4. `chapters/chapter_name.md`
5. `references/state-tracker.md` + `relationship-tracker.md` + `plot-tracker.md`（同一操作轮）
6. `archive/archive.md`（仅有异常时）

完成后更新 `meta/workflow-state.json`：
- `currentChapterArtifacts.archiveSync = true`
- `currentChapterArtifacts.userReport = true`
- `lastClosedChapter = chapterNum`
- `resumeRequired = true`

---

## 典型路径（对比）

| | 标准版（12agent-novel） | novel-free |
|--|--------------|------------|
| 常规章（非5章倍数） | MainWriter(1) + 自查 | MainWriter(1) + 自查（不变）|
| 常规章（5章倍数，OOC≥4） | MainWriter(1) + RollingSummarizer(1) + OOCGuardian(1) | MainWriter(1) + **Combo(1)** |
| 常规章（5章倍数，OOC<4） | MainWriter(1) + RollingSummarizer(1) | MainWriter(1) + RollingSummarizer(1) |
| **每20章节省调用** | 基准 | **约4次** |
