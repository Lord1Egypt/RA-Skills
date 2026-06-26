# 与 Novel Studio 的迁移与交接指引

本 Skill 输出不直接写入 novel-studio 项目文件，需用户确认后手动迁移或通过 novel-studio 指令衔接。以下为可执行步骤。

---

## 开题输出 → outline / timeline / characters

1. **已有 novel-studio 项目时**
   - 将「调研报告 + 总体故事线」全文或摘录粘贴到该项目的 `dagang.md` 中，放在 `## 待更新内容` 下。
   - 在 Cursor 中触发 novel-studio：「更新 [项目名] 的设定」。
   - novel-studio 会读取 `dagang.md` 的待更新内容，同步到 `outline.md`、`timeline.md`、`characters.md`。
   - 若一次粘贴内容过多，可分批：先粘贴「总体大纲 + 时间线草图」，同步后再粘贴「人物特征草图」并再次「更新设定」。

2. **新项目时**
   - 先触发 novel-studio：「创建新小说」或「新建小说项目 [项目名]」，按提示提供书名、类型、项目代号等（可从开题报告中的「创作目标与主题陈述」提取）。
   - 项目创建后，将开题报告中的「分幕式总体大纲」「时间线草图」「人物特征草图」粘贴到 `dagang.md` 的 `## 待更新内容`，再执行「更新 [项目名] 的设定」。

---

## 续写输出 → 后续章节写作

1. 将「未来 3–5 章推进要点」复制到该项目的 `dagang.md` 的 `## 待更新内容`（可选），或直接保留在对话/报告中。
2. 写具体章节时触发 novel-studio：「写 [项目名] 的第 X 章」，写作时参照续写策略报告中的「推荐路线」与「节奏与冲突控制建议」。
3. 若续写报告里建议调整大纲，可把建议段落粘贴到 `dagang.md` 再「更新设定」，使 outline/timeline 与后续写作一致。

---

## 改写输出 → 执行改写与回归

1. 改写策略报告中的「改写蓝图」与「验收清单」供用户或 AI 执行改写时对照。
2. 若在 novel-studio 中重写某章：可用「写 [项目名] 的第 X 章」并说明「按改写方案重写」，或用户自行编辑章节文件。
3. 改写后若导致与现有大纲不一致，可触发「按照文章回归一下大纲」或「将正文同步回大纲」，让 novel-studio 根据新正文反向更新 outline/timeline/characters。
4. **可选**：改写落地后，可建议用户使用 novel-qa Skill 对人设、时间线、空间布置、伏笔等做一致性检查。

---

## 文件位置速查

- novel-studio 项目路径：`novel-studio/novels/[project-name]/`
- 需粘贴的 file：`dagang.md`（段落标题 `## 待更新内容`）
- 被同步的 file：`outline.md`、`timeline.md`、`characters.md`
