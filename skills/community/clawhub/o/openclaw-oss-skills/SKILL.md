---
name: openclaw-oss-skills
description: Upload generated artifacts from an OpenClaw workspace to an Alibaba Cloud OSS bucket using credentials from environment variables, then return a temporary signed download link in the conversation. Use when the user asks to upload, share, publish, or return downloadable links for generated files, archives, reports, images, documents, videos, or build outputs via OSS.
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - python3
      env:
        - OSS_ACCESS_KEY_ID
        - OSS_ACCESS_KEY_SECRET
        - OSS_BUCKET
        - OSS_ENDPOINT
    primaryEnv: OSS_ACCESS_KEY_ID
    emoji: "☁️"
    homepage: https://docs.openclaw.ai/tools/skills
    install:
      - kind: brew
        formula: python@3
        bins:
          - python3
        label: Install Python 3
      - kind: uv
        package: oss2
        label: Install Alibaba Cloud OSS Python SDK
---

# OpenClaw OSS Artifact

Use this skill after creating a file, directory, or set of files that the user needs to download from an OSS signed URL.

## Requirements

Credentials and defaults come from environment variables:

- `OSS_ACCESS_KEY_ID` (required)
- `OSS_ACCESS_KEY_SECRET` (required)
- `OSS_BUCKET` (required)
- `OSS_ENDPOINT` (required, for example `https://oss-cn-hangzhou.aliyuncs.com`)
- `OSS_STS_TOKEN` (optional, for temporary credentials)
- `OSS_PREFIX` (optional, object key prefix; default `openclaw-artifacts`)
- `OSS_EXPIRES` (optional, signed URL lifetime in seconds; default `3600`)
- `OSS_PUBLIC_ENDPOINT` (optional, endpoint used in the returned URL if it differs from upload endpoint)
- `OSS_IS_CNAME` (optional, set to `1` when the endpoint is a custom OSS CNAME)

The access key must have permission to put objects into the configured bucket and read them through signed URLs.
The uploader uses the Alibaba Cloud `oss2` Python SDK. If it is not installed, install it with `python3 -m pip install oss2`.

## Workflow

1. Finish generating the artifact locally.
2. Confirm the local artifact path exists.
3. Run the bundled uploader:

```bash
python3 skills/openclaw-oss-skills/scripts/upload_to_oss.py /absolute/path/to/artifact
```

For multiple files or a directory, pass each path. The script automatically creates a zip archive before upload:

```bash
python3 skills/openclaw-oss-skills/scripts/upload_to_oss.py /path/to/file-a.pdf /path/to/output-dir
```

If the skill folder is the current directory, run the script directly:

```bash
python3 scripts/upload_to_oss.py /absolute/path/to/artifact
```

4. Return the `download_url` shown by the script to the user as a Markdown link. Mention the expiration time if the user may need to know it.

## Options

- `--object-key <key>`: upload with an explicit OSS object key. Use only for a single file.
- `--prefix <prefix>`: override `OSS_PREFIX`.
- `--bucket <bucket>`: override `OSS_BUCKET`.
- `--endpoint <endpoint>`: override `OSS_ENDPOINT`.
- `--public-endpoint <endpoint>`: override `OSS_PUBLIC_ENDPOINT`.
- `--expires <seconds>`: override `OSS_EXPIRES`.
- `--json`: print machine-readable JSON only.

## Output Contract

The script prints:

- `object_key`: object path inside the bucket
- `download_url`: signed URL for direct download
- `expires_at`: ISO-8601 UTC expiration time
- `source`: uploaded local file or temporary zip path

In the final answer, include the signed link and keep the local path available for debugging if upload fails.
