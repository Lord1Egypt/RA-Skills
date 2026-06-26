# session watch

## Scope

Use this reference for `mttsports session watch` NDJSON events, decision events, and non-decision events.

## Core Rules

1. `mttsports session watch` is machine-facing NDJSON. Do not mix explanatory text into stdout.
2. Action decisions must come only from `session watch` events. Do not inject room history, extra summaries, or manually added context into the decision input.
3. Use no-thinking mode for decisions: act quickly and do not produce long reasoning.
4. In auto mode, direct action is the default. Strategy boundaries still come from [`../../SKILL.md`](../../SKILL.md).
5. Keep responses minimal. Do not narrate the hand.

## Command Schema

### `mttsports session watch`

```json
{
  "schema": "table.event",
  "type": "turn.changed",
  "ts": "2026-04-02T12:34:56Z",
  "seq": 123,
  "room_key": "room_xxx",
  "table_key": "table_xxx",
  "turn_changed": {}
}
```

Use only the current `watch` event when deciding. Do not append extra background or long-form reasoning.

## Currently Supported Watch Events

Only two push event types are currently used for in-hand decision making:

### `turn.changed`

Source: `NotifyOperateStart`, and it is emitted to `watch` only when `IsSelf=true`.

Purpose: it means it is your turn to act. This is the most important decision event.

Key fields:

```json
{
  "schema": "table.event",
  "type": "turn.changed",
  "room_key": "room_xxx",
  "table_key": "table_xxx",
  "turn_changed": {
    "turn": {
      "user_id": 12345,
      "options": ["fold", "check", "call", "raise", "allin"],
      "min_call_chip": "2",
      "min_raise_chip": "4",
      "max_raise_chip": "200",
      "last_greatest_raise_chip": "4",
      "time_ms": 15000,
      "extra_time_ms": 0,
      "total_op_time_ms": 15000,
      "is_self": true,
      "seq": 123,
      "desc": "operate_start"
    },
    "round": {
      "id": 888,
      "stage": "pre_flop",
      "public_cards": []
    },
    "pod": {
      "total_chip": "6",
      "min_raise_chip": "4",
      "min_call_chip": "2"
    }
  }
}
```

The event itself is not the action. After receiving `turn.changed`, move to [`operate.md`](operate.md) and choose a legal action to execute.

### `round.result`

Source: `NotifyRoundResult`.

Purpose: the current hand has finished settling. Do not send more actions for this hand. Wait for the next `turn.changed`.

Key fields:

```json
{
  "schema": "table.event",
  "type": "round.result",
  "room_key": "room_xxx",
  "table_key": "table_xxx",
  "round_result": {
    "round": {
      "public_cards": ["Ah", "Kd", "7c", "2s", "2d"],
      "quick_end": false
    },
    "self_result": {
      "user_id": 12345,
      "chip": "120",
      "win_round": true,
      "change_chip": "+18",
      "change_type": "win",
      "card_type": "two_pair"
    }
  }
}
```

When this event arrives:

1. Treat the current round as finished.
2. Do not send any more `operate` actions for this hand.
3. Keep `watch` running and wait for the next new `turn.changed`.

## Non-Decision Events

`watch` may also emit a small set of non-decision events that should not be used as action triggers:

- `session.opened`: session established successfully
- `table.snapshot`: full-table snapshot after reconnect
- `error`: session or call error
- `session.closing`: session is closing

These events are for connection-state judgment only, not poker action decisions.
