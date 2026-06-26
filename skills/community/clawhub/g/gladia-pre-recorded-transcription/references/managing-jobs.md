# Managing Pre-Recorded Jobs

Reference for retrieving, listing, downloading, and deleting pre-recorded transcription jobs.

## Contents

- Get a Single Job
- List Jobs
- List Query Parameters
- Download Original Audio
- Delete a Job

## Get a Single Job

Fetch the status and full result payload for one job:

```typescript
const job = await client.preRecorded().get(jobId);
console.log(job.status); // "queued" | "processing" | "done" | "error"
console.log(job.result?.transcription?.full_transcript);
```

```python
job = client.prerecorded().get(job_id)
print(job.status)
print(job.result.transcription.full_transcript)
```

Raw REST: `GET /v2/pre-recorded/:id`

## List Jobs

Retrieve jobs with optional filters. The response is paginated.

```typescript
const page = await client.preRecorded().list({
  offset: 0,
  limit: 20,
  status: ["done"],
  after_date: "2026-01-01T00:00:00Z",
  before_date: "2026-06-01T00:00:00Z",
  custom_metadata: { userId: "abc123" },
});

for (const job of page.items) {
  console.log(job.id, job.status);
}

// page.next is the URL for the next page (null when last page)
```

```python
page = client.prerecorded().list(
    offset=0,
    limit=20,
    status=["done"],
    after_date="2026-01-01T00:00:00Z",
    before_date="2026-06-01T00:00:00Z",
    custom_metadata={"userId": "abc123"},
)

for job in page.items:
    print(job.id, job.status)
```

Raw REST: `GET /v2/pre-recorded`

## List Query Parameters

| Parameter         | Type     | Description                                                 |
| ----------------- | -------- | ----------------------------------------------------------- |
| `offset`          | integer  | Pagination start (default `0`)                              |
| `limit`           | integer  | Max items per page (default `20`, min `1`)                  |
| `date`            | string   | Filter to a specific day (`YYYY-MM-DD`)                     |
| `before_date`     | string   | Jobs created before this ISO 8601 datetime                  |
| `after_date`      | string   | Jobs created after this ISO 8601 datetime                   |
| `status`          | string[] | Filter by status: `queued`, `processing`, `done`, `error`   |
| `custom_metadata` | object   | Filter by metadata key/value pairs attached at job creation |

Pagination fields in the response:

- `first` (URL)
- `current` (URL)
- `next` (URL or `null`)
- `items` (array)

## Download Original Audio

Download the original audio used for transcription:

```typescript
const audioBlob = await client.preRecorded().getFile(jobId);
```

```python
audio_bytes = client.prerecorded().get_file(job_id)
```

Raw REST: `GET /v2/pre-recorded/:id/file`

## Delete a Job

Delete a job and associated data:

```typescript
await client.preRecorded().delete(jobId);
```

```python
client.prerecorded().delete(job_id)
```

Raw REST: `DELETE /v2/pre-recorded/:id`
