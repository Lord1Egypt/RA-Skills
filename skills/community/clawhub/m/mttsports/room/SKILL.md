---
name: mttsports-room
description: "Use when the task is specifically about `mttsports room`: listing rooms, creating rooms, entering a room, joining a table, adding chips, or leaving. Use structured commands and preserve room/table metadata for later session startup."
---

# mttsports room

When this sub-skill is loaded, the task is already in the `mttsports room` domain.

## Core Rules

1. If the user wants to create a room, fetch available parameters with `room start-info` first, then create it with `room start`.
2. `play-time` is the thinking time per action in seconds.
3. Use structured room commands throughout: `room list/enter/join/add-on/leave/start-info/start`.
4. If a session will be started next, preserve the table metadata returned by `enter` or `join`.

## Intent To Command

| Intent | Recommended Command | Notes |
|---|---|---|
| List rooms with pagination | `mttsports room list --page ... --page-size ... --output json` | When exact paging matters |
| Inspect room creation parameters | `mttsports room start-info --output json` | Check before creating a room |
| Create a room | `mttsports room start --room-level-id ... --big-blind ... --player-per-table ... --play-time ... [--disable-insurance] --output json` | Run `enter` after receiving `room_key` |
| Fetch table metadata after entry | `mttsports room enter --room-key ... --output json` | Common before starting a session |
| Join a table directly | `mttsports room join --room-key ... --pay-amount ... --seat ... --output json` | Standard structured command |
| Add chips | `mttsports room add-on --room-key ... --pay-amount ... --seat ... --output json` | Additional buy-in while seated |
| Leave the table | `mttsports room leave --room-key ... --output json` | Exit the current table |

## Common Examples

```bash
mttsports room list --page 1 --page-size 20 --output json
mttsports room start-info --output json
mttsports room start --room-level-id 1001 --big-blind 200 --player-per-table 9 --play-time 15 --output json
mttsports room enter --room-key <room_key> --output json
mttsports room join --room-key <room_key> --pay-amount <amount> --seat 1 --output json
mttsports room add-on --room-key <room_key> --pay-amount <amount> --seat 1 --output json
mttsports room leave --room-key <room_key> --output json
```

## Command Schema

### `mttsports room list`

```json
{
  "rooms": [
    {
      "room_key": "room_xxx",
      "small_blind": "1",
      "big_blind": "2",
      "player_per_table": 9,
      "register_num": 6
    }
  ],
  "total": 100
}
```

### `mttsports room enter`

```json
{
  "room_key": "room_xxx",
  "room_id": "1001",
  "table_key": "table_xxx",
  "small_blind": "1",
  "big_blind": "2",
  "ante": "0",
  "seats": [
    {
      "seat_no": 1,
      "user": ""
    }
  ],
  "chips_config": {
    "hand_chips": "100",
    "hand_amount": {
      "amount": "1",
      "symbol": "MTT"
    },
    "min_buy_in_amount": {
      "amount": "100",
      "symbol": "MTT"
    },
    "max_buy_in_amount": {
      "amount": "1000",
      "symbol": "MTT"
    }
  },
  "enable_straddle": false,
  "enable_insurance": true,
  "is_short_deck": false,
  "is_run_it_twice": true,
  "play_time": 15,
  "table_srv_id": 123
}
```

### `mttsports room start-info`

```json
{
  "list": [
    {
      "roomLevelID": 1001,
      "smallBlind": 100,
      "bigBlind": 200,
      "enableInsurance": true,
      "rewardBBNum": 20
    }
  ]
}
```

Here, `reward_bb_num` / `rewardBBNum` means the number of big blinds awarded for opening a table.
For example, if the value is `25`, the user receives a `25 BB` reward after creating the room.

### `mttsports room start`

```json
{
  "roomKey": "room_xxx"
}
```

### `mttsports room join`

```json
{
  "success": true
}
```

### `mttsports room add-on`

```json
{
  "success": true
}
```

### `mttsports room leave`

```json
{
  "instant_leave": true
}
```

## Notes

1. Parameters for room creation should come from `room start-info`. Do not invent `room-level-id`, blind levels, or player counts.
2. When asking about room creation parameters, describe `play-time` as "action thinking time (seconds)".
3. Recommended confirmation prompt:

```text
Level 1 has 4 blind levels. Which one should I use?
1/2 (smallest)
10/20
50/100
100/200

Also confirm:
Players per table: 6 / 8 / 9? (default: 9)
Action thinking time: 10 / 15 / 20 seconds? (default: 15)
```

4. After `room start` returns `roomKey`, continue with `enter`, and then `join` if needed.
5. If the user did not provide `room_key` and candidate rooms differ clearly in mode or risk, ask once instead of choosing a high-risk table blindly.
6. If the next step is a full game flow, return to the "Common Workflows" section in [`../SKILL.md`](../SKILL.md).
