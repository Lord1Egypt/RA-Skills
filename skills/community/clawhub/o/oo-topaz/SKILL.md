---
name: oo-topaz
description: "Topaz (topazlabs.com). Use this skill for ANY Topaz request — reading, creating, updating, and deleting data. Whenever a task involves Topaz, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Topaz"
  author: "OOMOL"
  version: "1.0.1"
  services: ["topaz"]
  icon: "https://static.oomol.com/logo/third-party/topaz.svg"
---

# Topaz

Operate **Topaz** through your OOMOL-connected account. This skill calls the `topaz` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Topaz. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "topaz" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "topaz" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `accept_video_request` — Accept estimated video costs and reserve credits. External sources start processing automatically. Otherwise PUT source bytes to the returned upload URLs and call complete_video_upload; repeated calls return the same URLs. [write]
- `cancel_image_job` — Cancel a pending image job. Completed or non-cancellable jobs return a conflict. [destructive]
- `cancel_video_job` — Cancel a video job. Topaz may refund credits in full before processing or partially during processing. [destructive]
- `complete_video_upload` — Complete an externally performed video upload and start processing. For one upload URL send [{partNum:1,eTag:unused}]; multipart uploads require the actual ordered part numbers and ETags returned by storage. [write]
- `create_video_request` — Create a standard video request and receive cost estimates. No credits are charged and processing does not start until accept_video_request. Prefer submit_video_enhancement for automatic external-source processing. [write]
- `delete_all_image_job_statuses` — Delete all image processing status records, clearing the account's job history. [destructive]
- `delete_image_job_status` — Delete one image job status record. This is separate from cancelling a running job. [destructive]
- `delete_video_files` — Permanently delete the source and enhanced video files stored by Topaz for a request. [destructive]
- `estimate_generative_image` — Estimate generative image processing credits and duration without submitting a job.
- `estimate_image` — Estimate standard image processing credits and duration without submitting a job.
- `estimate_images_bulk` — Estimate multiple image jobs in one request. Each result may succeed or contain its own error.
- `estimate_video_cancellation` — Preview credits committed and refunded if a video request were cancelled now, without cancelling it.
- `get_credit_balance` — Get available, reserved and total Topaz API credits.
- `get_credit_usage` — Get historical API credit consumption by time bucket. Explicit date ranges override period. period=1d covers 48 hours; sparse buckets do not imply missing requests.
- `get_image_download` — Get a completed image's temporary download and HEAD URLs, valid for one hour.
- `get_image_input_download` — Get temporary download and HEAD links for the original input image.
- `get_image_job` — Get an image job status and progress. After completion use get_image_download to retrieve the result URL.
- `get_video_job` — Get video processing status, progress, estimates and the completed result download link. Download links are reused and expire after their original lifetime.
- `get_video_metrics` — Get video processing metrics. Requests without chunked processing may return only a message indicating metrics are unavailable.
- `get_video_request` — Get the full video request record, including unaccepted requests, corrected source metrics, credit transactions and signed downloads.
- `get_video_system_status` — Get video service availability and the authoritative list of currently supported model codes.
- `list_image_jobs` — List image jobs. Pagination defaults to true; non-paginated mode returns jobs up to seven days old. Follow next_cursor while has_next_page is true.
- `list_video_requests` — List accepted video requests newest first. Follow nextCursor until null, even when a page has fewer than 50 entries. Unaccepted requests are omitted.
- `submit_generative_image_enhancement` — Submit a generative image enhancement job to Topaz. Returns a job ID for polling. [write]
- `submit_generative_image_sharpening` — Submit generative image sharpening for severe blur recovery. [write]
- `submit_image_denoising` — Submit image denoising to remove noise while retaining detail. [write]
- `submit_image_enhancement` — Submit a precision image upscale job to Topaz. Returns a job ID for polling. [write]
- `submit_image_lighting` — Submit image lighting, white balance or colorization processing. [write]
- `submit_image_matting` — Submit image object matting and return a PNG with transparency. [write]
- `submit_image_restoration` — Submit generative photo restoration to remove dust and scratches. [write]
- `submit_image_sharpening` — Submit image sharpening to restore sharpness and reduce blur. [write]
- `submit_image_tool` — Submit transparency-preserving image upscaling using the Tool API. [write]
- `submit_video_enhancement` — Submit video enhancement or frame interpolation through Express using S3 external storage. Topaz fetches the source and starts processing immediately. Preserve audio explicitly with audioTransfer and audioCodec. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Topaz state — confirm the exact payload and effect with the user before running.**
- **Actions tagged `[destructive]` remove or overwrite data — always confirm the target and get explicit approval first.**

## First-time setup

These are **one-time** steps — do not repeat them on every call. Run a step only when a command fails for the matching reason.

- **`oo: command not found`** — install the oo CLI (other platforms: <https://cli.oomol.com/install-guide.md>):

  ```bash
  curl -fsSL https://cli.oomol.com/install.sh | bash    # macOS / Linux
  ```

  ```powershell
  irm https://cli.oomol.com/install.ps1 | iex           # Windows PowerShell
  ```

- **Not signed in / authentication error** — sign in to your OOMOL account once:

  ```bash
  oo auth login
  ```

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Topaz is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/topaz
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Topaz homepage: https://www.topazlabs.com
