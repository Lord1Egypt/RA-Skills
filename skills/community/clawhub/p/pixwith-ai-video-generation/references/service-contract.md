# Pixwith Service Contract

## Authentication

- Auth header: `Api-Key`
- Invalid or inactive keys fail with:
  `Invalid API key. Get a valid API key at https://pixwith.ai/api`
- Only active API keys belonging to active registered users are accepted

## Tool Response Envelope

Pixwith tools return a wrapped response:

- `code = 1`: success
- `code = 0`: general failure
- `code = 2`: authentication failure
- `msg`: backend status message
- `data`: actual payload

Always inspect `code` before trusting `data`.

## Tool Summary

- `list_models(type?)`: list MCP-enabled image or video models, including
  `summary` and `min_credits`
- `get_model_schema(model_id)`: fetch one model's exact Pixwith input schema
- `upload_image(input)`: create a presigned upload target and return a Pixwith-hosted image URL
- `generate(input)`: create an async generation task
- `get_task_result(input)`: poll task status and result URLs
- `get_credits()`: get remaining credits for the current API key

## Model Discovery Contract

`list_models` returns a lightweight discovery view:

- `model_id`
- `name`
- `summary`
- `min_credits`

`min_credits` is the lowest starting credit cost for that model family. It is:

- useful for fast filtering
- not the final price for a concrete request
- not a substitute for `get_model_schema(model_id).input_schema.credits`

## Upload Contract

`upload_image` does not upload file bytes directly. It returns an S3 presigned
POST target and a final Pixwith-hosted `image_url`.

Input constraints:

- `filename` must end with `.jpg`, `.jpeg`, or `.png`
- `content_type` must be `image/jpeg` or `image/png`
- `file_size_bytes` must be `<= 20MB`

Operational requirements:

- upload URL expires in 10 minutes
- the actual upload must be one `multipart/form-data` POST
- include every returned `form_fields` item exactly once
- required field ordering matters for some clients
- the file part must use field name `file`
- the file part should be sent last
- do not send JSON to S3

## Task Lifecycle

`generate` creates an asynchronous task and returns:

- `task_id`
- `estimated_time`

Task statuses from `get_task_result`:

- `1`: processing
- `2`: completed
- `3`: failed

Only completed tasks should be expected to contain usable `result_urls`.

## Failure Handling

### Authentication failure

If `code = 2`, stop and ask the user to provide a valid Pixwith API key from
`https://pixwith.ai/api`.

### Invalid model or schema mismatch

If `generate` fails because of model or option mismatch:

1. re-run `list_models`
2. re-run `get_model_schema`
3. rebuild the request from the current schema

Do not blindly retry the same payload.

### Image fetch failure

If Pixwith cannot fetch a provided image URL:

- switch to `upload_image`
- or ask the user for a directly accessible public URL

### Credits not enough

Do not retry automatically. Tell the user the selected request exceeds the
available Pixwith credits.
