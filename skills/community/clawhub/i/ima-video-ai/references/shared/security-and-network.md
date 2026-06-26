# Security And Network

The active operator surface is:

- `python3 scripts/ima_runtime_cli.py ...` for video generation
- `python3 scripts/route_and_execute.py --request "..."` for parse + validate + execute
- `python3 scripts/validate_params.py --request "..."` for natural-language validation against the live catalog
- `python3 scripts/ima_runtime_setup.py` for first-run preference setup
- `python3 scripts/ima_runtime_doctor.py` for low-cost environment and connectivity checks

`parse_user_request.py` is local-only and does not touch the network.
The other operator surfaces use the same network and credential surface described below.

## Endpoint Disclosure

The shipped runtime can talk to four network surfaces:

| Domain | Used for | Trigger |
| --- | --- | --- |
| `api.imastudio.com` | product list, task create, task detail polling | all runs |
| `imapi.liveme.com` | upload-token requests | when local media uploads or derived cover uploads are needed |
| pre-signed HTTPS storage URL returned as `ful` | binary PUT upload for local media bytes or derived cover frames | only after a successful upload-token request |
| user-supplied public HTTPS media origin | temporary local download for metadata probing, Seedance preflight checks, and video-cover extraction | only when the operator provides remote HTTPS media |

If a task already uses direct HTTPS media URLs, the upload-token path is skipped for the original asset.
Plain remote `http://` media URLs are not supported.

Remote-media restrictions:

- only direct `https://` URLs are accepted
- URLs with embedded credentials are rejected
- hosts must resolve to public IP addresses; private, loopback, link-local, and other non-public addresses are rejected
- redirects are rejected
- streaming download caps are enforced before or during local probing:
  - image: 30 MB
  - video: 50 MB
  - audio: 15 MB

## Credential Flow

`IMA_API_KEY` is sent to:

- `api.imastudio.com` as the Bearer token for product and task APIs
- `imapi.liveme.com` for the upload-token flow used before local media or derived cover uploads

Binary media bytes are then uploaded to the pre-signed HTTPS storage URL returned by the upload-token API. The runtime validates that upload target as a public HTTPS URL before sending bytes.

The script also sends `APP_ID` and `APP_KEY` request-signing constants to the upload service. Those values are hard-coded client constants in `shared/config.py`, not repository secrets.

## Local Persistence

The runtime writes local operational state:

- `~/.openclaw/memory/ima_prefs.json` for saved model preferences
- `~/.openclaw/logs/ima_skills/` for logs, cleaned up after seven days by `ima_logger.py`

The runtime also creates temporary files in the OS temp directory when it downloads remote media for probing or extracts a cover frame from a video. Those temp files are deleted after validation/extraction.

The repo does not persist `IMA_API_KEY` into tracked files.

## Privacy Notes

- prompts and task parameters go to `api.imastudio.com`
- media bytes go to the pre-signed HTTPS upload target only when upload is needed
- remote HTTPS media may be downloaded locally without credentials for metadata probing and validation before the original public URL is passed through to the task payload
- plain remote `http://` media URLs are rejected rather than fetched and re-uploaded
- `user_id` is used for local preference storage, not sent in API payloads by the current CLI flow

This is the complete network and credential surface for the shipped video-only runtime.

## Rate And Batch Guidance

The repo does not encode a published backend rate limit. The guidance below is conservative operator policy for this skill, not a server-side guarantee:

- keep active create-task concurrency at or below 3 tasks per API key
- leave about 500 ms between create requests when sending a batch
- queue large batches instead of submitting everything at once
- use `ima_runtime_doctor.py` first when repeated create requests begin failing, before retrying the whole batch
