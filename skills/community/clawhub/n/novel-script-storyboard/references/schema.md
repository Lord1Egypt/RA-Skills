# 分镜 JSON 字段

根对象包含 `status`（`complete`、`needs_review` 或 `needs_more_source`）、`title`、`source_type`、`duration_seconds`、`characters`、`scenes` 和 `gaps`。当 `status` 为 `needs_more_source` 时，只需提供非空 `message` 说明缺少什么材料。其余状态需要完整分镜结构。

`characters` 为人物数组；每个人物包括 `name`、`role`、`goal`、`conflict`、`relationship`、`facts` 和 `source_anchor`。原文未交代的字段需明确写“原文未说明”或在缺口中说明，不能编成事实。

`scenes` 是场次数组，每场包含 `scene_id`、`location`、`time`、`purpose`、`characters`、`actions`、`dialogue`、`source_anchor`、`shots`，可选 `gaps`。`scene_id` 不能重复；全部场景中的 `shot_id` 也不能重复。

每个对白对象包含 `speaker` 和 `line`。每个 `shot` 必须包含：

- `shot_id`：场次内可辨识的镜头编号
- `duration_seconds`：正数
- `framing`：景别，例如远景、中景、近景、特写
- `camera`：视角和运动
- `visual`：观众能看到的主体、动作和构图
- `action`：镜头中的具体动作
- `dialogue_or_voiceover`：对白或旁白，没有则为空字符串
- `sound`：环境声、音效或音乐建议
- `source_anchor`：对应原文的短引用或段落序号
- `creative_note`：新增的制作/创作建议，没有则为空字符串

根 `duration_seconds` 必须等于所有镜头时长之和。`gaps` 记录未解决信息；存在缺口时不能标 `complete`。Markdown 按镜头逐项呈现画面、动作、声音、原文锚点、创作补充、时长、景别、运镜和对白/旁白，避免表格字符破坏排版。结构校验不验证原文引用真实性或创作质量，由执行改编的 AI 对照原文检查。
