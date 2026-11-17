---
name: paper-downloader
description: Download a user-requested public HTTP or HTTPS file, especially research papers and PDFs, into the shared local directory /tmp/skill-downloads for later processing by another skill. Use when the user supplies a public file URL and wants the file saved locally rather than merely fetched as text. Reject local/private-network targets, URL credentials, unsupported ports, and oversized responses.
---

# Paper Downloader

Download one public file and return its saved path.

## Workflow

1. Take the user-provided public HTTP(S) URL exactly as the download source.
2. Run `scripts/download_file.py <URL>`.
3. Treat the script's stdout as the handoff path for another skill.
4. Report the saved path to the caller. Do not parse, summarize, execute, or otherwise interpret the downloaded file in this skill.

## Command

```bash
python scripts/download_file.py [url]
```

The script saves the response, limits downloads to 64 MiB, avoids overwriting an existing file, and prints only the final path on success.
