# 短剧场次字段

根对象使用 `title`、`episode`、`scenes` 和 `gaps`。场次字段为 `scene_id`、`slugline`、`goal`、`characters`、`actions`、`dialogue`、`conflict`、`turn`、`props` 和 `ending_hook`。

`dialogue` 是 `{speaker, line}` 数组；`conflict` 至少包含 `obstacle`、`escalation`、`result`。结尾钩子要能拍出来，例如“门锁转动，屏幕显示失踪者来电”，避免抽象评价。


## 渲染输入

`title` 为非空文本，`episode` 为正整数，`gaps` 为待确认事项的文本数组；`scenes` 至少有一个场次且 `scene_id` 唯一。每场的 `slugline`、`goal`、`turn`、`ending_hook` 和 `conflict` 内的 `obstacle`、`escalation`、`result` 为非空文本。

`characters`、`actions`、`props` 为文本数组；`dialogue` 为 `{speaker, line}` 数组。每场至少包含动作或对白。可选 `camera_notes` 为拍摄建议文本数组。结构以外的字段会保留在 JSON 中；当前 Markdown 只排版上述字段。

需要保留动作和对白交错顺序时，提供 `beats` 数组：动作格式为 `{"type":"action","text":"..."}`，对白格式为 `{"type":"dialogue","speaker":"...","line":"..."}`。按动作和对白分别投影后，必须与 `actions` 和 `dialogue` 完全一致；Markdown 按 `beats` 的原顺序排版。未提供 `beats` 时，Markdown 先列动作再列对白。

由当前 AI 根据用户资料填写真正的剧情；缺失信息记录在 `gaps`。渲染器不判断原文事实是否准确，也不会替代创意审核。见 `examples/success-output.json`。
