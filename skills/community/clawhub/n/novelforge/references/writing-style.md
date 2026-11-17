# 写作画像契约

除机器字段、命令和文件路径外，项目的写作说明、审查意见与交接内容使用简体中文。

Novel Core does not prescribe an author, genre, or imitation style. A project
profile selects voice, distance, register, pacing, and optional detectors. A
Narrative Engine supplies reasoning tools and scene decisions; it does not
silently overwrite the project's voice.

## Required profile fields

```json
{
  "voice": {"person": "third", "distance": "close", "register": "project-defined"},
  "pacing": {"default": "project-defined"},
  "detectors": [{"id": "optional-rule", "severity": "warning"}]
}
```

## General craft guidance

- Make language serve the current scene's action, feeling, and information.
- Use concrete detail, interiority, dialogue, and summary in the proportion the
  scene needs.
- Let a character's choices expose goals, fears, contradictions, and cost.
- Vary scene movement across a long work; do not repeat a successful surface
  pattern mechanically.
- Treat every style check as a diagnostic unless the project policy promotes it.
