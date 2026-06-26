# Chapter Commit Template（章节闭环一次性提交规范）

> 目标：将每章闭环的 6-8 次分散写入，合并为一次集中提交，减少遗漏概率和主控决策负担。

---

## 一、使用时机

Step 5（存档闭环）开始时，Coordinator 先填写本模板，确认所有待写内容，然后**一次性执行所有写入操作**，而不是逐文件分批写入。

---

## 二、提交清单模板

在执行任何写入前，先在内存中组织以下内容：

```
【章节闭环提交清单 — 第 {N} 章】

□ metadata.json 更新
  - currentChapter: {N}
  - lastCompletedChapter: {N}
  - chapters.ch{NNN}: { title, wordCount, completedAt }

□ workflow-state.json 更新
  - chapterWorkflow.currentChapter: {N}
  - chapterWorkflow.lastClosedChapter: {N}
  - currentChapterArtifacts: 全部 true
  - resumeRequired: true
  - chapterEntryChecklistComplete: false
  - （若触发摘要）lastRollingSummaryChapter: {N}
  - （若触发反馈）lastReaderFeedbackChapter: {N}

□ chapter_name.md 追加
  - | ch{NNN} | 《{章节名称}》 | {字数} | {日期} |

□ state-tracker.md 更新
  - 主角当前状态（位置 / 修为 / 持有物）
  - 重要 NPC 状态变更

□ relationship-tracker.md 更新
  - 本章关系变化条目（如有）

□ plot-tracker.md 更新
  - 本章新埋设伏笔（如有）
  - 本章回收伏笔（标记已回收）

□ archive/archive.md 追加日志（如有异常 / OOC 修改 / 降级处理）

□ 异步任务确认（如有）
  - RollingSummarizer 是否已触发（每5章）
  - ReaderSimulator 是否已触发（每5章）
```

---

## 三、写入顺序

按以下顺序写入，优先级从高到低：

1. `chapters/ch{NNN}.md`（正文，最重要）
2. `meta/workflow-state.json`
3. `meta/metadata.json`
4. `chapters/chapter_name.md`
5. `references/state-tracker.md`
6. `references/relationship-tracker.md`
7. `references/plot-tracker.md`
8. `archive/archive.md`（仅有异常时）

> 1-4 为最低必须完成项；5-7 为 tracker 更新，**三个 tracker 须在同一操作轮内完成，不得跨步骤分批写入**（对应 iron-rules.md「Tracker 合并写入」铁律），若写入中断视为 `archiveSync = false`，须在下次恢复协议中补齐。

---

## 四、写入失败处理

若某项写入失败：
1. 立即停止后续写入
2. 记录失败的文件名和章节号
3. 标记 `archiveSync = false`、`resumeRequired = true`
4. 向用户报告失败项
5. 不得进入下一章

---

## 五、与现有流程的对应关系

| 本模板步骤 | 对应 lifecycle-phase2 Step |
|-----------|---------------------------|
| 填写提交清单 | Step 5 开始前 |
| 执行写入 1-4 | Step 5 必须完成项 |
| 执行写入 5-7 | Step 5 tracker 更新 |
| 触发异步任务 | Step 5 触发检查 |
| 向用户汇报 | Step 5 结尾 |

---

## 六、对主控压力的影响

- 从"逐项确认 6-8 个文件"变为"填一张表再统一提交"
- 减少因分散决策导致的遗漏
- 失败时有明确的中断点，便于恢复协议定位问题
