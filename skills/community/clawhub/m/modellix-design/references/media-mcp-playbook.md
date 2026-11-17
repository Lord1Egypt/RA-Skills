# Media Generation MCP

Use this playbook only when `modellix_submit_task` is available and the input is a prompt or a public URL. Endpoint: `https://tool.modellix.ai/mcp/media`. The server requires MCP **2026-07-28**. Older clients receive a protocol error; treat that as "this path is unavailable" and use the CLI.

The host must attach `Authorization: Bearer <MODELLIX_API_KEY>`. This plugin does not store that header. `modellix_get_schema` is public and needs no key; the other tools do.

The server does not choose a model or estimate a price. Use the `provider/model` slug the user named. If they did not name one, ask before calling a tool.

## Tools

| Tool | Role |
| --- | --- |
| `modellix_list_models` | Page the catalog. Optional `type` or `keyword`. `limit` default 20, maximum 100, with `offset`. |
| `modellix_get_schema` | Public input contract for an exact `provider/model` slug. |
| `modellix_upload_file` | One of `url` or `base64_content`. Base64 also needs a plain `filename`. |
| `modellix_list_files` | Files already uploaded, for reuse or an explicit delete. |
| `modellix_delete_file` | Delete one `file_id` the user selected. Absent ids return `already_absent`. |
| `modellix_submit_task` | One paid submit. Keep `task_id`. |
| `modellix_get_task` | Immediate snapshot. |
| `modellix_wait_task` | Wait up to 45 seconds. Default 30. Range 1–45. |

## Schema references

`modellix_get_schema` returns the original document plus an `input_schema` projection and a `reference_scope` note. Resolve input-local references against `input_schema`. Resolve document-scoped references against the original document. Keep the document root when references use `paths`, `post`, or `components`. Copying only the projection drops those references.

## Upload

Pass exactly one of `url` and `base64_content`. The server cannot read a path on the user's computer. A local image, video, or audio file stays on the CLI `file upload` path.

URL downloads accept public HTTP(S) destinations and reject private, local, reserved, or credential-bearing targets, including redirects. The limit is 16 MiB (16777216 bytes). Supported extensions: JPG, JPEG, PNG, WebP, GIF, BMP, TIFF, TIF, HEIC, HEIF, MP4, M4V, WebM, MOV, MKV, AVI, MP3, WAV, M4A, AAC, OGG, FLAC, OPUS, WEBA.

Default team settings allow 10 files, 2 concurrent uploads, and about 7 days of retention. On a quota error, list files, ask the user to pick an unneeded `file_id`, and only then call `modellix_delete_file`. Do not delete automatically and do not re-upload to free space.

## Submit and wait

Confirm the model and the input with the user, then call `modellix_submit_task` once.

`modellix_wait_task` returning `data.wait.timed_out=true` is a successful snapshot. Call it again with the same `task_id`. Terminal states are `success`, `failed`, and `canceled`.

Read outputs from `data.result.resources` and save them before the URLs expire (about 7 days). This server has no local `task download`. When the CLI is also installed, `modellix-cli task download <task_id>` is a valid way to persist those resources. Do not start a new generation in order to download.

## Unknown outcome

`submission_unknown` means the submit may have succeeded and no task id is guaranteed. The same is true when the connection fails before a trustworthy response.

Do not call `modellix_submit_task` again, and do not fall through to `modellix-cli model run` or a REST POST for that same request. If a `task_id` is present, continue with `modellix_get_task` or `modellix_wait_task`. If it is not, use `modellix-cli task history` when the CLI is available, or the console, before any new submit.
