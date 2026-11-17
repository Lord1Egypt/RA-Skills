# Character design

Characters are stateful agents in the story model. A character file should be
short enough to load when needed and precise enough to test continuity.

```json
{
  "id": "character.example",
  "type": "character",
  "name": "Project-defined",
  "goal": "",
  "fear": "",
  "constraint": "",
  "values": [],
  "voice": {"rhythm": "", "avoidances": []},
  "knowledge": [],
  "relationships": [],
  "state": {},
  "personality": {
    "core_temperament": "",
    "current_flaw": "",
    "arc_direction": "",
    "resistance": 0.7,
    "pressure_log": []
  }
}
```

## Personality fields

| Field | Description |
|---|---|
| `core_temperament` | 角色底色性格（如"刚直"、"多疑"、"懦弱"），建立后极少改变 |
| `current_flaw` | 当前最突出的性格缺陷或盲区，是弧光推进的目标 |
| `arc_direction` | 弧光走向的一句话描述（如"从多疑走向信任"） |
| `resistance` | 抗变阈值，0–1 浮点数。值越高越难改变（固执≈0.8，圆滑≈0.3）。默认 0.7 |
| `pressure_log` | 压力事件列表，由结算层写入，不由蓝图或正文直接修改 |

### pressure_log entry

```json
{"chapter": "v01-c003", "event": "被师兄出卖", "weight": 0.2, "toward": "trust→distrust"}
```

## Pressure accumulation rules

1. `pressure_log` 只能通过 Settlement 的 `pressure_event` 字段写入。
2. 当 `sum(p.weight for p in pressure_log if p.toward matches arc_direction)` ≥
   `resistance` 时，story-builder 应规划一个显性转折场景。
3. 转折完成后清空对应方向的 pressure_log，更新 `current_flaw` 和
   `arc_direction`。
4. 单个事件的 weight 不得 > 0.5（除非是足以改变任何人的极端事件）。
5. 角色可能长期不发生性格变化——这是正常的，不需要为了"有弧光"而
   人为加速压力。

## Design questions

1. What is the character's core temperament, and what kind of pressure could
   crack it?
2. What cost, fear, obligation, or blind spot limits their choices right now?
3. What accumulated evidence would push them past their resistance threshold?
4. How does their speech and action differ as pressure builds but before
   they break?
5. After a personality shift, what new flaw or blind spot emerges?

Important actions must be explainable from the current `personality`,
`goal`, `knowledge`, `values`, and `relationships`. A surprising action is
welcome when the Settlement records the cause and consequence.
