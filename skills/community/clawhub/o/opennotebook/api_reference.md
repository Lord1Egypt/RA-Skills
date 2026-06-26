# OpenNotebook API Reference

## Table of Contents

1. [Authentication](#authentication)
2. [Notebooks](#notebooks)
3. [Sources](#sources)
4. [Notes](#notes)
5. [Search](#search)
6. [Transformations](#transformations)
7. [Models](#models)
8. [Chat](#chat)
9. [Podcasts](#podcasts)
10. [Credentials](#credentials)
11. [Error Handling](#error-handling)

---

## Authentication

OpenNotebook uses API key authentication for protected endpoints.

### Auth Status
```
GET /api/auth/status
```
Returns current authentication status.

---

## Notebooks

Notebooks are containers for organizing sources and notes.

### List Notebooks
```
GET /api/notebooks
Query Parameters:
  - archived: boolean (filter by archived status)
  - order_by: string (field to order by)
```

### Get Notebook
```
GET /api/notebooks/{notebook_id}
```

### Create Notebook
```
POST /api/notebooks
Body: { "name": string, "description": string? }
```

### Update Notebook
```
PUT /api/notebooks/{notebook_id}
Body: { "name": string?, "description": string?, "archived": boolean? }
```

### Delete Notebook
```
DELETE /api/notebooks/{notebook_id}
Query Parameters:
  - delete_exclusive_sources: boolean (delete sources only in this notebook)
```

### Add/Remove Source
```
POST /api/notebooks/{notebook_id}/sources/{source_id}
DELETE /api/notebooks/{notebook_id}/sources/{source_id}
```

---

## Sources

Sources are content containers (files, URLs, text) that can be processed and embedded.

### List Sources
```
GET /api/sources
Query Parameters:
  - notebook_id: string
  - limit: integer (default: 50)
  - offset: integer (default: 0)
  - sort_by: string (default: "created_at")
  - sort_order: string ("asc" | "desc", default: "desc")
```

### Create Source (JSON)
```
POST /api/sources/json
Body: {
  "type": string,        # "file", "url", "text", "youtube"
  "notebook_id": string?,
  "url": string?,        # for url/youtube types
  "content": string?,    # for text type
  "title": string?,
  "transformations": string[]?,
  "embed": boolean (default: true),
  "async_processing": boolean (default: true)
}
```

### Upload File
```
POST /api/sources
Content-Type: multipart/form-data
Fields:
  - file: binary
  - notebook_id: string?
  - title: string?
  - transformations: json string
  - embed: string ("true" | "false")
```

### Get Source
```
GET /api/sources/{source_id}
```

### Update Source
```
PUT /api/sources/{source_id}
Body: { "title": string?, "topics": string[]? }
```

### Delete Source
```
DELETE /api/sources/{source_id}
```

### Source Status
```
GET /api/sources/{source_id}/status
```
Returns processing status (pending, processing, completed, failed).

### Retry Processing
```
POST /api/sources/{source_id}/retry
```

### Download Source
```
GET /api/sources/{source_id}/download
```

---

## Notes

Notes are user-created text content within notebooks.

### List Notes
```
GET /api/notes
Query Parameters:
  - notebook_id: string (filter by notebook)
```

### Create Note
```
POST /api/notes
Body: {
  "content": string,
  "title": string?,
  "note_type": string?,
  "notebook_id": string?
}
```

### Update Note
```
PUT /api/notes/{note_id}
Body: { "title": string?, "content": string?, "note_type": string? }
```

### Delete Note
```
DELETE /api/notes/{note_id}
```

---

## Search

Search and ask questions against the knowledge base.

### Search
```
POST /api/search
Body: {
  "query": string,
  "type": string?,
  "limit": integer?,
  "search_sources": boolean (default: true),
  "search_notes": boolean (default: true),
  "minimum_score": number?
}
```

### Ask (Streaming)
```
POST /api/search/ask
Body: {
  "question": string,
  "strategy_model": string,
  "answer_model": string,
  "final_answer_model": string
}
```

### Ask Simple (Non-streaming)
```
POST /api/search/ask/simple
Body: { same as /ask }
```

---

## Transformations

Transformations are AI-powered content processing pipelines.

### List Transformations
```
GET /api/transformations
```

### Create Transformation
```
POST /api/transformations
Body: {
  "name": string,
  "title": string,
  "description": string,
  "prompt": string,
  "apply_default": boolean?
}
```

### Execute Transformation
```
POST /api/transformations/execute
Body: {
  "transformation_id": string,
  "input_text": string,
  "model_id": string
}
```

### Default Prompt
```
GET /api/transformations/default-prompt
PUT /api/transformations/default-prompt
Body: { "transformation_instructions": string }
```

---

## Models

Model configuration for various AI providers.

### List Models
```
GET /api/models
Query Parameters:
  - type: string (filter by type)
```

### Create Model
```
POST /api/models
Body: {
  "name": string,
  "provider": string,
  "type": string,
  "credential": string?
}
```

### Default Models
```
GET /api/models/defaults
PUT /api/models/defaults
Body: {
  "default_chat_model": string?,
  "default_transformation_model": string?,
  "large_context_model": string?,
  "default_text_to_speech_model": string?,
  "default_speech_to_text_model": string?,
  "default_embedding_model": string?,
  "default_tools_model": string?
}
```

### Sync Models
```
POST /api/models/sync
POST /api/models/sync/{provider}
```

---

## Chat

Interactive chat with context from sources and notebooks.

### Chat Sessions
```
GET /api/chat/sessions
POST /api/chat/sessions
GET /api/chat/sessions/{session_id}
PUT /api/chat/sessions/{session_id}
DELETE /api/chat/sessions/{session_id}
```

### Execute Chat
```
POST /api/chat/execute
```

### Source-specific Chat
```
GET /api/sources/{source_id}/chat/sessions
POST /api/sources/{source_id}/chat/sessions
POST /api/sources/{source_id}/chat/sessions/{session_id}/messages
```

---

## Podcasts

Generate audio podcasts from content.

### Generate Podcast
```
POST /api/podcasts/generate
```

### Episodes
```
GET /api/podcasts/episodes
GET /api/podcasts/episodes/{episode_id}
DELETE /api/podcasts/episodes/{episode_id}
GET /api/podcasts/episodes/{episode_id}/audio
```

### Profiles
```
GET /api/episode-profiles
GET /api/speaker-profiles
```

---

## Credentials

Manage API credentials for AI providers.

### List Credentials
```
GET /api/credentials
GET /api/credentials/by-provider/{provider}
```

### Create Credential
```
POST /api/credentials
```

### Test Credential
```
POST /api/credentials/{credential_id}/test
```

---

## Error Handling

All errors return JSON with the following structure:

```json
{
  "detail": "Error message description"
}
```

Common HTTP Status Codes:
- 400: Bad Request - Invalid input
- 401: Unauthorized - Authentication required
- 403: Forbidden - Insufficient permissions
- 404: Not Found - Resource doesn't exist
- 500: Internal Server Error