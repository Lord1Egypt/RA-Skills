# Managing Live Sessions

Reference for retrieving, listing, downloading, and deleting live sessions after initialization.

## Contents

- Get a Single Session
- List Sessions
- List Query Parameters
- Download Recorded Audio
- Delete a Session

## Get a Single Session

Fetch the status and full result payload for one live session:

```typescript
const session = await client.liveV2().get(sessionId);
console.log(session.status); // "queued" | "processing" | "done" | "error"
console.log(session.result?.transcription?.full_transcript);
```

```python
session = client.live().get(session_id)
print(session.status)
print(session.result.transcription.full_transcript)
```

Raw REST: `GET /v2/live/:id`

## List Sessions

Retrieve sessions with optional filters. The response is paginated.

```typescript
const page = await client.liveV2().list({
  offset: 0,
  limit: 20,
  status: ["done"],
  after_date: "2026-01-01T00:00:00Z",
  before_date: "2026-06-01T00:00:00Z",
  custom_metadata: { userId: "abc123" },
});

for (const session of page.items) {
  console.log(session.id, session.status);
}

// page.next is the URL for the next page (null when last page)
```

```python
page = client.live().list(
    offset=0,
    limit=20,
    status=["done"],
    after_date="2026-01-01T00:00:00Z",
    before_date="2026-06-01T00:00:00Z",
    custom_metadata={"userId": "abc123"},
)

for session in page.items:
    print(session.id, session.status)
```

Raw REST: `GET /v2/live`

## List Query Parameters

| Parameter         | Type     | Description                                                 |
| ----------------- | -------- | ----------------------------------------------------------- |
| `offset`          | integer  | Pagination start (default `0`)                              |
| `limit`           | integer  | Max items per page (default `20`, min `1`)                  |
| `date`            | string   | Filter to a specific day (`YYYY-MM-DD`)                     |
| `before_date`     | string   | Sessions created before this ISO 8601 datetime              |
| `after_date`      | string   | Sessions created after this ISO 8601 datetime               |
| `status`          | string[] | Filter by status: `queued`, `processing`, `done`, `error`   |
| `custom_metadata` | object   | Filter by metadata key/value pairs attached at session init |

Pagination fields in the response:

- `first` (URL)
- `current` (URL)
- `next` (URL or `null`)
- `items` (array)

## Download Recorded Audio

Download the recorded audio file for a session:

```typescript
const audioBlob = await client.liveV2().getFile(sessionId);
```

```python
audio_bytes = client.live().get_file(session_id)
```

Raw REST: `GET /v2/live/:id/file`

## Delete a Session

Delete a session and associated data:

```typescript
await client.liveV2().delete(sessionId);
```

```python
client.live().delete(session_id)
```

Raw REST: `DELETE /v2/live/:id`
