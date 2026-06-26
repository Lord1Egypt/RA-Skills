# Mode Routing

This skill supports `one-shot` and `project`.

## Route to `one-shot`

Use `one-shot` when the user primarily wants a single outcome:
- one image
- one image edit
- one short video
- one script
- one outline
- one voice clip
- one BGM track
- one storyboard pack

Default behavior:
- no project required
- no workspace link required
- return result + quote + task status

## Route to `project`

Use `project` when the user is building a lasting production:
- multiple episodes
- ongoing revisions
- project continuation
- explicit request to persist into workspace
- explicit request for project link or web access

Default behavior:
- resolve project first
- persist outputs into project
- update materials and canvas
- return project summary + workspace link

## Ambiguity rule

If unclear, ask one short question:

`这次是单次生成结果，还是作为项目持续推进？`

Do not ask more than that before producing value.
