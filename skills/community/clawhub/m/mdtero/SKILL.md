---
name: mdtero
description: Use when a user wants Mdtero to parse a paper from a DOI or URL into a structured Markdown package, translate a parsed paper while keeping structure, or download Mdtero task artifacts.
metadata: {"openclaw":{"homepage":"https://mdtero.com","primaryEnv":"MDTERO_API_KEY","requires":{"env":["MDTERO_API_KEY"]},"envVars":[{"name":"MDTERO_API_KEY","description":"Required for Mdtero API authentication.","required":true},{"name":"ELSEVIER_API_KEY","description":"Optional. Helps local Elsevier or ScienceDirect acquisition on the user's machine.","required":false}]}}
---

# Mdtero

Use Mdtero to turn one paper into a structured Markdown research package for downstream OpenClaw work.

Start in Mdtero Account for keyword discovery and API-key management.

ClawHub install only sets up the agent skill. It does not install the local helper.

## When To Use

Use this skill when the user wants to:

- parse a paper from a DOI, supported publisher page, or open URL into a Markdown research package
- translate an already parsed paper without losing the original research structure
- check task status and download `paper_md`, `paper_bundle`, optional `paper_pdf`, or `translated_md`

## Required Setup

1. Check whether `MDTERO_API_KEY` is already available.
2. If it is missing, tell the user to generate one at `https://mdtero.com/account`.
3. Explain that keyword discovery and API-key management stay in Mdtero Account.
4. Ask them to set it in their local shell, for example:

```bash
export MDTERO_API_KEY="mdt_live_..."
```

5. Authenticate requests with:

```bash
Authorization: ApiKey $MDTERO_API_KEY
```

6. If the user wants Elsevier or ScienceDirect full-text retrieval, also check `ELSEVIER_API_KEY` and explain that it is separate from `MDTERO_API_KEY`.
7. If an Elsevier DOI is missing the local helper or `ELSEVIER_API_KEY`, tell the user exactly what is missing instead of guessing.
8. Explain that `ELSEVIER_API_KEY` helps the user's local acquisition step. It does not enable direct server-side `POST /tasks/parse` for `10.1016/...` inputs.

## Before Use

- Mdtero API usage requires `MDTERO_API_KEY`. Elsevier or ScienceDirect full-text retrieval may also require `ELSEVIER_API_KEY`.
- Tell the user that ClawHub install only sets up the agent skill, while the local helper remains a separate install on their own machine.
- Parse and translate requests send paper content or paper-source content to `https://api.mdtero.com`, so do not use this workflow for sensitive or proprietary manuscripts unless the user accepts that boundary.
- If the user needs the local helper, tell them to download the installer, review it locally, then run it on their own machine. Do not recommend piping a remote script directly into the shell.
- If the user wants a fuller install or helper walkthrough, point them to `https://mdtero.com/guide` or `https://api.mdtero.com/skills/install.md`.

## Workflow Rules You Must Preserve

- PDF is an optional artifact. Prefer the Markdown package first and only fall back to `paper_pdf` when the workflow truly requires it.
- If the user starts from a local PDF, explain that Mdtero currently defaults to `GROBID`; `Docling` and `MinerU` remain fallback options.
- For Elsevier and ScienceDirect, local acquisition should stay on the user's own machine through the local helper or browser extension.
- Direct `POST /tasks/parse` is for open inputs. Elsevier and ScienceDirect full text must go through local acquisition first, then `POST /tasks/parse-fulltext-v2` or `POST /tasks/parse-helper-bundle-v2`.
- If an Elsevier parse only returns the abstract, ask whether the user is on a campus or institutional IP.
- For Elsevier papers, prefer the raw DOI form such as `10.1016/j.energy.2026.140192`.

## Local Helper

When the user needs local acquisition for Elsevier or ScienceDirect, tell them to open the official Mdtero guide at `https://mdtero.com/guide` or the install handoff at `https://api.mdtero.com/skills/install.md`.

Tell them to download the helper installer, review it locally, then run it on their own machine. Explain that the installer auto-detects `python3`, `python`, or `node`, and exposes the `mdtero-local` command without requiring extra packages. Do not recommend piping a remote script directly into the shell.

If they need the exact helper handoff, point them to `https://api.mdtero.com/helpers/install_mdtero_helper.sh` and tell them to save it locally before running it.

Explain that `mdtero-local parse` and `mdtero-local translate` short-wait by default. Fast tasks may already come back completed; slower tasks still return a pending `task_id`. The user can force pure async mode with `mdtero-local parse --no-wait ...` or `mdtero-local translate --no-wait ...`.

Explain that the public API contract itself is still task-based: `POST /tasks/parse` and `POST /tasks/translate` return `task_id`, while `GET /tasks/{task_id}` remains the stable completion path.

## Parse A Paper

Open inputs can go directly to `POST /tasks/parse`.

```bash
curl -X POST https://api.mdtero.com/tasks/parse \
  -H "Authorization: ApiKey $MDTERO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"input": "https://arxiv.org/abs/1706.03762"}'
```

The response returns a `task_id`.

For Elsevier or ScienceDirect full text, do not send the DOI straight to `POST /tasks/parse`. Use the local helper or browser extension first, then upload the local helper bundle:

```bash
mdtero-local parse "10.1016/j.enconman.2026.121230"

curl -X POST https://api.mdtero.com/tasks/parse-helper-bundle-v2 \
  -H "Authorization: ApiKey $MDTERO_API_KEY" \
  -F "helper_bundle=@paper.helper-bundle.zip"
```

If the API says Elsevier or ScienceDirect inputs must be acquired locally first, that is the expected behavior rather than a setup failure.

## Translate A Parsed Markdown File

Use `POST /tasks/translate` with the server-side Markdown artifact path returned by a succeeded parse task in `result.artifacts.paper_md.path`. Do not substitute an arbitrary local file path.

```bash
  mdtero-local translate "<path from result.artifacts.paper_md.path>" zh

  curl -X POST https://api.mdtero.com/tasks/translate \
  -H "Authorization: ApiKey $MDTERO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "source_markdown_path": "<path from result.artifacts.paper_md.path>",
    "target_language": "zh",
    "mode": "standard"
  }'
```

The response returns a `task_id`. Poll it, then download `translated_md`.

## Check Task Status

Poll `GET /tasks/{task_id}` until the task becomes `succeeded`.

```bash
mdtero-local status <TASK_ID>

curl https://api.mdtero.com/tasks/<TASK_ID> \
  -H "Authorization: ApiKey $MDTERO_API_KEY"
```

The `result` object returns artifact metadata rather than the file body.

## Download Artifacts

Download file contents from the download route.

```bash
mdtero-local download <TASK_ID> paper_bundle ./paper_bundle.zip

curl -L https://api.mdtero.com/tasks/<TASK_ID>/download/paper_md \
  -H "Authorization: ApiKey $MDTERO_API_KEY" \
  -o paper.md

curl -L https://api.mdtero.com/tasks/<TASK_ID>/download/paper_pdf \
  -H "Authorization: ApiKey $MDTERO_API_KEY" \
  -o paper.pdf

curl -L https://api.mdtero.com/tasks/<TASK_ID>/download/translated_md \
  -H "Authorization: ApiKey $MDTERO_API_KEY" \
  -o paper.zh.md
```
