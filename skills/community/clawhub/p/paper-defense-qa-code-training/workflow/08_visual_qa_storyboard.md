# Workflow 08 — 图文答辩卡片与生图提示词

## 何时使用

当用户要求“图文并茂”“画一组插图”“做视觉化问答卡”“把高危问题做成图解”“答辩时更直观”时，执行本流程。

## 输入

优先读取：

- `defense_qa_bank_cn.json`
- `defense_qa_bank_cn.md`
- `claim_evidence_map_cn.md`
- `code_training_audit_cn.md`
- `backup_slide_plan_cn.md`
- 用户指定的视觉风格、画幅、用途：PPT / 海报 / 讲义 / 复习卡 / 社媒长图

## 步骤

### 1. 选择需要图解的问题

优先选择：

- P0/P1 高风险问题；
- 代码、训练、可复现性问题；
- 方法流程复杂、口头解释容易绕的问题；
- 容易过度声称、必须强调边界的问题；
- 需要备份页支撑的问题。

### 2. 为每个问题选择视觉类型

| 问题类型 | 推荐图型 |
|---|---|
| 贡献与创新性 | Claim-evidence map / closest-prior-work map |
| 方法结构 | Method pipeline |
| 数学公式到实现 | Equation-to-code bridge |
| 训练流程 | Training timeline |
| baseline 公平性 | Baseline fairness board |
| 证据薄弱或缺失 | Evidence gap triage card |
| 被追问如何恢复 | Recovery answer card |

### 3. 先写文字卡片

每张卡先完成：

```text
Q_ID：
问题：
短回答：
证据标签：
不能过度声称：
备份页用途：
图解目的：
```

### 4. 再写生图提示词

提示词必须说明：

- 画幅：默认 16:9；
- 风格：clean academic infographic；
- 主要布局：pipeline / radar / timeline / map / flashcard；
- 要表达的关系；
- 哪些文字必须留给后期叠加；
- 不要生成 fake citations、fake table numbers、过度夸张结论。

### 5. 明确生图分离

在交付任何文字回复或提示词时，最终必须使用下面这句提醒：

```text
“请用chatgpt images 2.0 生成一系列 16:9 辅助答辩的插图，这些插图可以图文并茂的覆盖上面文字中的问题以及用生动的图表来解释回答，有助于更好准备答辩回答。”
```

Codex / CLI 中则提醒：

```text
请把 visual_qa_storyboard_cn.json 当成生图任务清单；如果在 Codex 内使用，实际生图时优先调用 imagegen skill，否则交给 ChatGPT Images 2.0 / gpt-image-2 或用户批准的高级文生图 API。不要在当前文字回答步骤中直接混合执行生图。
```

### 6. 输出文件

```text
visual_qa_storyboard_cn.md
visual_qa_storyboard_cn.json
visual_image_prompt_pack_cn.md
visual_generation_handoff_cn.md
visual_card_copy_cn.md
```

## 质量检查

- 每张图是否绑定 Q_ID？
- 是否有证据标签？
- 是否包含 safe boundary？
- 是否真的帮助回答问题，而不只是好看？
- 是否避免假引用、假表格、假代码路径？
- 是否把文字回答和生图步骤分开？
