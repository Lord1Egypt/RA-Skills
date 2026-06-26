# Posting Queues

Queues publish posts automatically on weekly recurring timeslots, with priorities and natural-looking jitter.

## Queue Concepts

- **Timeslots**: Weekly recurring schedules (day + time in queue's timezone)
- **Priority**: `high` → scheduled first, `medium` → default, `low` → fills remaining slots
- **Jitter**: Random +/- offset (0–60 min) for natural posting patterns
- **Pausing**: Set `enabled: false` to pause; posts won't publish while paused. Unpausing rearranges all posts into future slots.
- **Dynamic Rearrangement**: Queue auto-rearranges all posts when posts are added/removed, timeslots change, timezone changes, or queue is unpaused.

## List Queues
```bash
curl -X GET "https://api.postproxy.dev/api/post_queues" \
  -H "Authorization: Bearer $POSTPROXY_API_KEY"
```
Optional query parameter: `profile_group_id` to filter by profile group.

## Get Queue
```bash
curl -X GET "https://api.postproxy.dev/api/post_queues/{queue_id}" \
  -H "Authorization: Bearer $POSTPROXY_API_KEY"
```

## Get Next Available Slot
```bash
curl -X GET "https://api.postproxy.dev/api/post_queues/{queue_id}/next_slot" \
  -H "Authorization: Bearer $POSTPROXY_API_KEY"
```

## Create Queue
```bash
curl -X POST "https://api.postproxy.dev/api/post_queues" \
  -H "Authorization: Bearer $POSTPROXY_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "profile_group_id": "pg123",
    "post_queue": {
      "name": "Morning Posts",
      "description": "Weekday morning content",
      "timezone": "America/New_York",
      "jitter": 10,
      "queue_timeslots_attributes": [
        { "day": 1, "time": "09:00" },
        { "day": 2, "time": "09:00" },
        { "day": 3, "time": "09:00" },
        { "day": 4, "time": "09:00" },
        { "day": 5, "time": "09:00" }
      ]
    }
  }'
```

Parameters:
- `profile_group_id` (required): Profile group ID to connect the queue to
- `post_queue[name]` (required): Queue name
- `post_queue[description]` (optional): Description
- `post_queue[timezone]` (optional): IANA timezone name (default: `UTC`)
- `post_queue[jitter]` (optional): Random offset in minutes 0–60 applied to scheduled times for natural posting patterns (default: `0`)
- `post_queue[queue_timeslots_attributes]` (optional): Array of timeslots, each with `day` (0=Sunday–6=Saturday) and `time` (24-hour `HH:MM`)

## Update Queue
```bash
curl -X PATCH "https://api.postproxy.dev/api/post_queues/{queue_id}" \
  -H "Authorization: Bearer $POSTPROXY_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "post_queue": {
      "name": "New Name",
      "timezone": "America/Los_Angeles",
      "enabled": false,
      "jitter": 5,
      "queue_timeslots_attributes": [
        { "day": 2, "time": "10:00" },
        { "id": 42, "_destroy": true }
      ]
    }
  }'
```

Parameters (all optional):
- `post_queue[name]`: New queue name
- `post_queue[description]`: New description
- `post_queue[timezone]`: IANA timezone
- `post_queue[enabled]`: `false` to pause, `true` to unpause
- `post_queue[jitter]`: Random offset in minutes (0–60)
- `post_queue[queue_timeslots_attributes]`: Add timeslots with `{ "day": N, "time": "HH:MM" }`, remove with `{ "id": N, "_destroy": true }`

## Delete Queue
```bash
curl -X DELETE "https://api.postproxy.dev/api/post_queues/{queue_id}" \
  -H "Authorization: Bearer $POSTPROXY_API_KEY"
```

## Add Post to Queue
Instead of `scheduled_at`, pass `queue_id` and optionally `queue_priority` when creating a post:
```bash
curl -X POST "https://api.postproxy.dev/api/posts" \
  -H "Authorization: Bearer $POSTPROXY_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "post": {
      "body": "Queued post content"
    },
    "profiles": ["twitter", "linkedin"],
    "queue_id": "q1abc",
    "queue_priority": "high"
  }'
```

Queue parameters on post creation:
- `queue_id` (required): Queue ID
- `queue_priority` (optional): `high`, `medium` (default), or `low`. Higher priority posts get earlier timeslots.

Do not pass `scheduled_at` together with `queue_id` — the queue determines the scheduled time automatically.
