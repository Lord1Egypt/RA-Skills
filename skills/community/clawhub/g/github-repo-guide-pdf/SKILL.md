---
name: github-repo-guide-pdf
description: Analyze a GitHub repository URL or OWNER/REPO and produce a Chinese user guide focused on how to use the project, not how it is implemented. Build a Markdown guide plus a PDF and send it back with MEDIA lines. Use when the user gives a GitHub repo and asks for usage, introduction, quick start, complete guide, tutorial, learn how to use it, or asks to turn the repo into a PDF/manual.
---

# Github Repo Guide Pdf

Turn a GitHub repository into a usage-first Chinese guide and PDF.

## Inputs

- Accept a GitHub repo URL or `OWNER/REPO`.
- Default audience: user/operator, not maintainer or contributor.
- If the repo is a monorepo, has several products, or mixes SDK plus server plus docs, ask one scoping question before continuing.

## Workflow

1. Normalize the repo identifier.
2. Use `gh` first for repo metadata. Fall back to `browser` only if `gh` is blocked or missing needed details.
3. Clone the repo into a temporary directory with shallow depth when possible.
4. Inspect user-facing docs and entry points.
5. Write a Chinese Markdown guide that teaches usage, not internals.
6. Build a PDF with `scripts/build_pdf.py`.
7. Reply with one short status line plus `MEDIA:` lines for the generated files.

## Collection Rules

Prefer these sources, in this order:

1. `README*` and localized README files
2. `docs/` and obvious user-guide files
3. command reference and configuration docs
4. `package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`, or equivalent manifest files for install/runtime hints
5. examples, templates, or sample config files
6. GitHub repo metadata from `gh repo view`

Use `rg --files` to find files quickly. Favor user-facing docs over architecture or internal implementation notes.

## Analysis Rules

Focus on what a real user needs to learn:

- what the project is
- who it is for
- prerequisites and install
- quick start
- main commands or workflows
- important config options
- when to use which mode or command
- troubleshooting and common pitfalls
- minimal cheat sheet

Avoid deep implementation detail unless it is required to explain usage.

If docs are weak, infer carefully from manifests, command docs, examples, and CLI entry points. State uncertainty briefly instead of pretending.

## Preferred GitHub Retrieval

Use `gh` first.

Examples:

```bash
gh repo view OWNER/REPO --json name,description,url,defaultBranchRef,licenseInfo,stargazerCount,forkCount,updatedAt
```

```bash
gh repo clone OWNER/REPO /tmp/repo -- --depth=1
```

If `gh` is insufficient, use `browser` to inspect the GitHub page or linked docs site.

## Recommended File Discovery

```bash
rg --files . | rg '(^README|^readme|^docs/|guide|manual|command|config|example|package\.json$|pyproject\.toml$|Cargo\.toml$|go\.mod$)'
```

Read only the files needed to build the guide. Do not dump the whole repo into context.

## Output Structure

Use this structure unless the repo clearly needs a different shape:

1. What it is
2. Who it is for
3. Installation and prerequisites
4. Quick start
5. Core workflows or commands
6. Configuration and modes
7. Recommended usage paths by scenario
8. Troubleshooting and common mistakes
9. One-page cheat sheet
10. Sources used

## Output Paths

Write outputs under the workspace media directory so they can be sent directly:

- Markdown: `media/<slug>-user-guide-zh-YYYYMMDD-HHMMSS.md`
- PDF: `media/<slug>-user-guide-zh-YYYYMMDD-HHMMSS.pdf`

Use a short slug derived from the repo name.

## PDF Build

After the Markdown guide is ready, run:

```bash
python3 skills/github-repo-guide-pdf/scripts/build_pdf.py \
  --markdown /absolute/path/to/guide.md \
  --output /absolute/path/to/guide.pdf \
  --title "<title>" \
  --source-url "https://github.com/OWNER/REPO"
```

If font selection fails, rerun with:

```bash
--mainfont "Hiragino Sans GB"
```

## Final Reply

After success, reply with:

1. one short sentence saying the guide is ready
2. one `MEDIA:` line for the Markdown file
3. one `MEDIA:` line for the PDF file

Example:

```text
Done. I turned the repo into a Chinese usage guide and PDF.
MEDIA:media/example-user-guide-zh-20260328-150500.md
MEDIA:media/example-user-guide-zh-20260328-150500.pdf
```

## Validation Checklist

Before replying, verify all of the following:

- the repo URL or `OWNER/REPO` was normalized correctly
- the guide is usage-first, not implementation-first
- the Markdown file exists and is non-empty
- the PDF exists and is non-empty
- both files live under the workspace media directory
- the `MEDIA:` paths match the actual files
