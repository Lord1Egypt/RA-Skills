# 推广方案 JSON 字段

## 状态与用户意图

根对象包含 `status`：`complete`、`needs_review` 或 `needs_more_source`。缺少可改编原文时只需 `status` 和非空 `message`。其他状态需要完整结构。`needs_review` 要附待确认缺口；存在 `source_notes.gaps` 时不得标为 `complete`。

`user_intent` 保留用户提供的 `platform`、`audience`、`objective`、`target_duration_seconds` 和 `cta_preference`。未提供的值设为 `null` 并列入 `not_provided`，不以模型猜测填入用户意图。

## 内容

- `duration_seconds`：画面和口播时间线的最晚结束时间。
- `title_options`：三个不同标题，每项有 `text`（最多30字符）、`angle`、`source_anchor`、`creative_note`。
- `selected_hook`：实际采用的开头钩子；同时提供 `hook_source_anchor` 和 `hook_creative_note`。没有原文锚点时要说明创作补充。
- `characters`：人物身份、目标、阻力、关系、视觉特征、事实、来源锚点与创作补充。未知事实写明未说明。
- `scenes`：每场含 `scene_id`、地点、时间、目标、冲突、动作、对白、视觉焦点、局面变化、来源锚点和创作补充。对白逐项标说话人、原文锚点及创作补充。
- `voiceover`：需要口播时，每段含唯一 `segment_id`、`start`、`end`、`text`、`source_anchor`、`origin`（`source`、`creative`、`cta_requested`、`cta_suggested`）和 `creative_note`。用户要求无口播时允许空数组，此时所有镜头的 `voiceover_ref` 设为 `null`。时间段不能交叠。
- `shots`：至少一个镜头；每镜含唯一 `shot_id`、`start`、`end`、`duration_seconds`、`visual`、`caption`、`voiceover_ref`、`sound`、`source_anchor`、`creative_note`。单镜时长等于结束减开始；口播引用须有效且与镜头时间相交。
- `ending_action`：`status` 为 `none`、`user_requested` 或 `agent_suggestion`，并提供 `text` 与 `note`。`none` 时 `text` 留空。AI 建议必须明确标注为建议。
- `source_notes`：至少包含 `source_scope`、`source_version`（未知可为 `null`）和 `gaps`。

来源锚点用于让 AI 和用户回读原文；结构校验不证明锚点准确、事实完整或创作质量。Markdown 按段落排版，不用可能被原文竖线破坏的表格。
