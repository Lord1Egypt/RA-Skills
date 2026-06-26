---
name: mediaio-ai-character-generator
description: Generate AI images of girls, characters, and fictional personas using Media.io OpenAPI. Creates detailed, stylized character portraits in various styles. AI character generator, AI girl generator, character design AI.
metadata: {"openclaw": {"homepage": "https://platform.media.io/docs/", "requires": {"bins": ["curl"], "env": ["MEDIAIO_API_KEY"]}, "primaryEnv": "MEDIAIO_API_KEY"}}
---

# Media.io AI Character Generator Skill

## Overview
This skill calls Media.io OpenAPI to run character generation using model code `character-generator-media-2.0`.
The API is asynchronous:
1. Submit generation request and get `task_id`.
2. Poll task result endpoint until the task is finished.

## When To Use
- The user wants stylized character images from prompt plus reference image.
- The user can provide an image URL reachable by Media.io servers.
- The user wants task-based generation with polling.

## When Not To Use
- The user asks for local file upload only (this API expects image URL input).
- The user asks for non-Media.io providers.
- The user asks for real-time synchronous image output in one call.

## Requirements

### Environment Variables
| Variable | Required | Description |
|---|---|---|
| `MEDIAIO_API_KEY` | Yes | Media.io OpenAPI key, used in header `X-API-KEY`. |

### Base Headers
- `Content-Type: application/json`
- `X-API-KEY: $MEDIAIO_API_KEY`

## Supported Endpoints

### 1) Query Credits
- Method: `POST`
- Endpoint: `https://openapi.media.io/user/credits`
- Body: `{}`
- Purpose: check available credits before generation.

### 2) Create Character Task
- Method: `POST`
- Endpoint: `https://openapi.media.io/generation/effects/character-generator-media-2.0`
- Body:
```json
{
	"data": {
		"images": "https://example.com/input.jpg",
		"prompt": "anime style fantasy heroine",
		"ratio": "9:16"
	}
}
```
- Required fields:
	- `data.images` (string URL)
	- `data.prompt` (string)
- Optional fields:
	- `data.ratio` (string): `9:16`, `16:9`, `1:1`, `4:3`, `3:4`, `3:2`, `2:3`, `21:9`

### 3) Query Task Result
- Method: `POST`
- Endpoint: `https://openapi.media.io/generation/result/{task_id}`
- Body: `{}`
- Path parameter:
	- `task_id` (string, required)

## Request and Response Contract

### Common Success Envelope
```json
{
	"code": 0,
	"msg": "",
	"data": {},
	"trace_id": "..."
}
```

### Create Task Response
- On success, `data.task_id` is returned.

### Task Result Response
- `data.status` can be one of the following values:
	- `waiting`: queued
	- `processing`: running
	- `completed`: completed successfully
	- `failed`: failed
	- `timeout`: timed out
- `data.reason`: provides additional context (e.g., `success` or error message)
- When status is `completed`:
	- `data.result` is an array of output objects with generated URLs
	- Each result object contains `val` (internal path), `preview` (public HTTPS URL), and `status` (completion status)

## Standard Invocation Flow
1. Call `user/credits` to verify balance.
2. Call `character-generator-media-2.0` with `data.images`, `data.prompt`, and optional `data.ratio`.
3. Extract `task_id`.
4. Poll `generation/result/{task_id}` every 3 to 5 seconds.
5. Stop when status is `completed` or `failed`.
6. Return output URLs from `data.result` when `completed`.

## cURL Examples

### Query Credits
```bash
curl --request POST \
	--url https://openapi.media.io/user/credits \
	--header 'Content-Type: application/json' \
	--header "X-API-KEY: $MEDIAIO_API_KEY" \
	--data '{}'
```

### Create Character Task
```bash
curl --request POST \
	--url https://openapi.media.io/generation/effects/character-generator-media-2.0 \
	--header 'Content-Type: application/json' \
	--header "X-API-KEY: $MEDIAIO_API_KEY" \
	--data '{
	"data": {
		"images": "https://example.com/input.jpg",
		"prompt": "anime style fantasy heroine",
		"ratio": "9:16"
	}
}'
```

### Query Task Result
```bash
curl --request POST \
	--url https://openapi.media.io/generation/result/<task_id> \
	--header 'Content-Type: application/json' \
	--header "X-API-KEY: $MEDIAIO_API_KEY" \
	--data '{}'
```

#### Successful Response Example
```json
{
	"code": 0,
	"msg": "",
	"data": {
		"task_id": "effect-86f0f82a-36dc-4a7c-928a-721a18ef482f",
		"status": "completed",
		"reason": "success",
		"result": [
			{
				"val": "aicloudtmp/550160908/3/202603/1/combo_tm_alg-20260317165022-802800-60eb3-dwt.png",
				"preview": "https://url_to_generated_image.png",
				"status": "completed"
			}
		]
	},
	"trace_id": "a18315ba568b5c34407808d12cbc8457"
}
```

Response fields when status is `completed`:
- `data.task_id`: unique task identifier
- `data.status`: `completed` indicates successful completion
- `data.reason`: `success` indicates no error occurred
- `data.result`: array of output objects, each containing:
	- `val`: internal file path of the generated asset
	- `preview`: publicly accessible HTTPS URL for the generated asset
	- `status`: `completed` for each result item

## Error Handling Guidance
- Treat `code != 0` as failure.
- Typical authentication errors:
	- `374004`: not authenticated. Apply for an APP KEY at https://developer.media.io/.
- Typical request validation error:
	- `490000`: params error
- Typical billing/credits error:
	- `490505`: insufficient credits. Recharge before invoking generation APIs.
- Always include `trace_id` in logs for troubleshooting.

## Agent Behavior Requirements
- Validate that input contains a non-empty image URL and prompt before calling the create endpoint.
- Do not claim immediate output after task creation; always poll by `task_id`.
- If credits are insufficient, return a clear message and stop instead of retry loops.
- Avoid exposing raw API keys in logs or responses.

## Safety and Compliance Notes
- Only process user-provided or user-authorized images.
- Do not imply identity verification or biometric certainty from generated images.
- Generated output is synthetic media and should be presented as edited content.

## References
- Media.io platform: https://developer.media.io/
- API documentation: https://platform.media.io/docs/
