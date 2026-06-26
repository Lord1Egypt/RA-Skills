# Phase 3 维护迭代详细流程

## 先决条件

进入 Phase 3 前，Coordinator 必须确认：
- `meta/metadata.json.project.phase = 3` 或本次修改属于已写正文项目的维护迭代
- `meta/workflow-state.json.phaseState.currentPhase = 3` 或已显式切换到 `phase3_ready`
- 若当前存在未闭环章节，先完成闭环再进入维护

## 触发时机

用户要求重写/补设定/改大纲/调整风格/段落重写。

---

## 场景处理表

| 场景 | 处理方式 |
|------|----------|
| 重写某章节 | MainWriter重写 → OOCGuardian检查 → FinalReviewer终审 → 更新存档 |
| 段落重写 | 调取上下文 → 调用相关Agent → 一致性检查 → 版本管理 |
| 补设定/世界观扩展 | spawn 最强模型 → 更新 worldbuilding/world.md → 级联一致性检查 |
| 修改大纲 | spawn OutlinePlanner → 输出新大纲 → FinalReviewer终审 → 用户确认 |
| 风格调整 | 更新 style-anchor.md → 对近期章节检查偏离 → 标记需处理的章节 |

---

## 章节重写流程

1. 备份：将当前版本移入 `chapters/history/ch{NNN}-v{N}.md`
2. 读取存档：固定层+滚动层+该章相关上下文
3. spawn MainWriter 重写
4. spawn OOCGuardian 一致性检查
5. [如为重点章节] spawn FinalReviewer 终审
6. Coordinator 整合
7. 写入新版本 chapters/ch{NNN}.md
8. 更新 metadata.json 版本号
9. 记录到 archive/archive.md
10. 汇报用户

---

## 段落级别重写

1. 解析指令（章节号+段落位置+段落类型）
2. 调取该段前后各500字上下文
3. 确定 Agent（战斗→BattleAgent，情感→MainWriter+高敏感约束，普通→MainWriter）
4. spawn Agent 重写
5. spawn OOCGuardian 检查连贯性
6. 版本管理（旧版移入 history/）
7. 更新 metadata.json
8. 汇报用户

---

## 级联一致性检查

当重写章节或修改设定后：

1. 分析影响范围（哪些后续章节引用了被修改的内容）
2. 对涉及的所有后续章节逐一进行一致性检查
3. 标记不一致的章节供用户选择处理
4. 用户可选择：自动重写受影响章节 / 暂不处理

### 级联影响状态追踪

级联检查完成后，Coordinator 必须将结果写入 `references/plot-tracker.md` 和 `archive/archive.md`：

**plot-tracker.md 追加格式：**
```
## 级联影响记录 — Phase 3 修改
| 修改来源章节 | 影响章节范围 | 影响类型 | 处理状态 |
|------------|-------------|---------|----------|
| ch{NNN} | ch{AAA}-ch{BBB} | 设定变更/角色弧光/伏笔 | 已处理/待处理/用户跳过 |
```

**workflow-state.json 补充字段：**
```json
{
  "phase3Maintenance": {
    "lastModifiedChapter": 0,
    "cascadeAffectedChapters": [],
    "pendingRewrites": [],
    "lastMaintenanceAt": ""
  }
}
```

> 若用户选择"暂不处理"，受影响章节必须加入 `pendingRewrites` 列表，下次恢复协议时提示用户。

---

## 大纲调整流程

1. 用户提出大纲修改需求
2. spawn OutlinePlanner 生成新版大纲
3. spawn FinalReviewer 评估影响
4. 输出影响分析报告：
   - 已写章节中受影响的部分
   - 未写章节的细纲需要更新的部分
5. 用户确认后：
   - 更新 outline/outline.md
   - [可选] 更新受影响的已写章节
   - 更新 outline/chapter-outline.md（未写部分）

---

## 风格调整流程

1. 用户提出风格修改
2. Coordinator 更新 meta/style-anchor.md
3. 对最近 5 章进行语言风格一致性检查
4. 标记有偏离的章节
5. 用户选择是否重新润色

---

## 状态同步要求

- 进入维护前：`meta/workflow-state.json.phaseState.status = "phase3_ready"`
- 完成维护后：更新 `meta/metadata.json.project.lastUpdated`
- 若修改影响章节闭环或追踪表，必须同步更新 `workflow-state.json` 中对应章号与 `resumeRequired`

## 存档维护原则

- 每次修改前先备份当前版本（移入 history/）
- 所有改动必须记录到 archive/archive.md
- 版本号语义：主版本（架构大改）.次版本（章节增删）.修订（文字修改）
