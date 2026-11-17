# Pocket Schema

This generated reference belongs to the adjacent `SKILL.md`. Use it for exact action names, action slugs, parameter summaries, sample parameters, and generated JSON parameter schemas.

Product slug: `pocket-recordings-transcripts`

x402 availability: not enabled for this product.

## `get_audio_download_url`

Action slug: `get-audio-download-url`

Price: `5` credits

Create a temporary audio download link for one recording. Use this for large audio instead of saving the file.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `expires_in` | `integer` | no | Audio URL lifetime in seconds. |
| `recording_id` | `string` | yes | Pocket recording ID. |

Sample parameters:

```json
{
  "expires_in": 60,
  "recording_id": "example recording id"
}
```

Generated JSON parameter schema:

```json
{
  "expires_in": {
    "description": "Audio URL lifetime in seconds.",
    "maximum": 86400,
    "minimum": 60,
    "required": false,
    "type": "integer"
  },
  "recording_id": {
    "description": "Pocket recording ID.",
    "required": true,
    "type": "string"
  }
}
```

## `get_recording`

Action slug: `get-recording`

Price: `5` credits

Get one Pocket recording, optionally including transcript and summarization data.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `include_summarizations` | `boolean` | no | Include summaries in recording detail. |
| `include_transcript` | `boolean` | no | Include transcript in recording detail. |
| `recording_id` | `string` | yes | Pocket recording ID. |
| `summarization_id` | `string` | no | Specific summarization ID. |

Sample parameters:

```json
{
  "include_summarizations": true,
  "include_transcript": true,
  "recording_id": "example recording id",
  "summarization_id": "example summarization id"
}
```

Generated JSON parameter schema:

```json
{
  "include_summarizations": {
    "description": "Include summaries in recording detail.",
    "required": false,
    "type": "boolean"
  },
  "include_transcript": {
    "description": "Include transcript in recording detail.",
    "required": false,
    "type": "boolean"
  },
  "recording_id": {
    "description": "Pocket recording ID.",
    "required": true,
    "type": "string"
  },
  "summarization_id": {
    "description": "Specific summarization ID.",
    "required": false,
    "type": "string"
  }
}
```

## `list_recordings`

Action slug: `list-recordings`

Price: `5` credits

List the user's Pocket recordings with optional date, tag, and pagination filters.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `end_date` | `string` | no | End date in YYYY-MM-DD. |
| `limit` | `integer` | no | Page size. |
| `page` | `integer` | no | Page number. |
| `start_date` | `string` | no | Start date in YYYY-MM-DD. |
| `tag_ids` | `array` | no | Pocket tag IDs. |

Sample parameters:

```json
{
  "end_date": "example end date",
  "limit": 1,
  "page": 1,
  "start_date": "example start date",
  "tag_ids": [
    "example tag id"
  ]
}
```

Generated JSON parameter schema:

```json
{
  "end_date": {
    "description": "End date in YYYY-MM-DD.",
    "required": false,
    "type": "string"
  },
  "limit": {
    "description": "Page size.",
    "maximum": 100,
    "minimum": 1,
    "required": false,
    "type": "integer"
  },
  "page": {
    "description": "Page number.",
    "minimum": 1,
    "required": false,
    "type": "integer"
  },
  "start_date": {
    "description": "Start date in YYYY-MM-DD.",
    "required": false,
    "type": "string"
  },
  "tag_ids": {
    "description": "Pocket tag IDs.",
    "items": {
      "description": "",
      "type": "string"
    },
    "required": false,
    "type": "array"
  }
}
```

## `list_tags`

Action slug: `list-tags`

Price: `5` credits

List tags available in the user's Pocket recording library.

Parameters:

This action does not require parameters.

Sample parameters:

```json
{}
```

Generated JSON parameter schema:

```json
{}
```

## `save_audio_to_files`

Action slug: `save-audio-to-files`

Price: `5` credits

Download one recording's audio and save it to File Manager. Audio over 100 MiB is rejected.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `expires_in` | `integer` | no | Audio URL lifetime in seconds. |
| `recording_id` | `string` | yes | Pocket recording ID. |

Sample parameters:

```json
{
  "expires_in": 60,
  "recording_id": "example recording id"
}
```

Generated JSON parameter schema:

```json
{
  "expires_in": {
    "description": "Audio URL lifetime in seconds.",
    "maximum": 86400,
    "minimum": 60,
    "required": false,
    "type": "integer"
  },
  "recording_id": {
    "description": "Pocket recording ID.",
    "required": true,
    "type": "string"
  }
}
```

## `search_recordings`

Action slug: `search-recordings`

Price: `5` credits

Search Pocket recordings by query. Requires query. Optional limit must be 20 or fewer; filters is an advanced passthrough object.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `filters` | `object` | no | Advanced search filters passed through to Pocket. |
| `limit` | `integer` | no | Page size. |
| `query` | `string` | yes | Search query or member lookup text. |

Sample parameters:

```json
{
  "filters": {},
  "limit": 1,
  "query": "example search query"
}
```

Generated JSON parameter schema:

```json
{
  "filters": {
    "description": "Advanced search filters passed through to Pocket.",
    "required": false,
    "type": "object"
  },
  "limit": {
    "description": "Page size.",
    "maximum": 20,
    "minimum": 1,
    "required": false,
    "type": "integer"
  },
  "query": {
    "description": "Search query or member lookup text.",
    "required": true,
    "type": "string"
  }
}
```

## `upload_recording`

Action slug: `upload-recording`

Price: `5` credits

Upload a File Manager audio file to Pocket for transcription. Requires a valid file_id owned by this budget, rejects files over 100 MiB, and never returns the temporary upload URL.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `duration_seconds` | `number` | no | Recording duration in seconds. |
| `file_id` | `string` | yes | AgentPMT File Manager file ID. |
| `recording_at` | `string` | no | Recording timestamp. |
| `title` | `string` | no | Recording, template, or mutable resource title/name. |

Sample parameters:

```json
{
  "duration_seconds": 1,
  "file_id": "example file id",
  "recording_at": "example recording at",
  "title": "example title"
}
```

Generated JSON parameter schema:

```json
{
  "duration_seconds": {
    "description": "Recording duration in seconds.",
    "exclusiveMinimum": 0,
    "required": false,
    "type": "number"
  },
  "file_id": {
    "description": "AgentPMT File Manager file ID.",
    "required": true,
    "type": "string"
  },
  "recording_at": {
    "description": "Recording timestamp.",
    "required": false,
    "type": "string"
  },
  "title": {
    "description": "Recording, template, or mutable resource title/name.",
    "required": false,
    "type": "string"
  }
}
```
