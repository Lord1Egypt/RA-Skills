---
name: github-forker
description: >
  Use this skill when the user wants to fork a GitHub repository — creating their own copy of a
  repo under their GitHub account. Trigger on any fork or copy-to-account intent paired with a
  GitHub repo reference, whether the URL appears in plain text (with or without https://), or is
  visible inside a screenshot or image the user shares. Applies equally in English and Chinese
  (fork下来, fork一下, 帮我fork, copy to my account). The repo reference may be a full URL, a
  subdirectory URL (strip to owner/repo), or a bare github.com/owner/repo string. Do not trigger
  for cloning locally, submitting PRs, reviewing or analyzing code, checking commit history, or
  searching for repos.
---

# GitHub Forker

Fork GitHub repositories extracted from text or images. You need `GITHUB_TOKEN` set in the
environment with repo permissions.

## What you do

1. **Extract** all GitHub repository URLs from the input (text, image, or both)
2. **Fork** each repository via the GitHub API
3. **Star** the original repository after a successful fork
4. **Report** results clearly

## Step 1: Extract GitHub URLs

### From text
Scan the input for patterns matching:
- `https://github.com/{owner}/{repo}` (with or without trailing slash, path, or fragment)
- `github.com/{owner}/{repo}` (without scheme)
- `{owner}/{repo}` only when context makes it clearly a GitHub repo

Normalize each match to the canonical form: `https://github.com/{owner}/{repo}`
Strip any extra path segments — you only need owner and repo name.

### From images
When the user provides an image (screenshot, photo, diagram), use your vision capabilities to
read the image and identify any GitHub URLs or repo references visible in it. Apply the same
extraction rules as above to whatever text you find.

### Truncated URLs
URLs are often cut off in screenshots or social media previews, like:
- `github.com/openchamber/op...`
- `github.com/some-owner/proj…`

When you detect a truncated URL (ends with `...` or `…`, or the repo name is clearly incomplete):

1. **Search GitHub** for matching repos:
   ```bash
   curl -s -L \
     -H "Authorization: Bearer $GITHUB_TOKEN" \
     -H "Accept: application/vnd.github+json" \
     "https://api.github.com/search/repositories?q={owner}/{partial}+in:full_name&per_page=5"
   ```
   Use whatever partial info you have — owner + partial repo name is ideal; owner alone works too.

2. **Use context to pick the best match.** Look at surrounding text, tweet content, project name
   mentioned, description keywords, and star count. If one result stands out clearly:
   - The repo name starts with the visible partial (e.g. `op...` → `openchamber` matches)
   - The description aligns with what the user said (e.g. "UI真好" → pick the UI-focused one)
   - It has significantly more stars than the others

   If you're confident, proceed directly and tell the user your reasoning:
   ```
   "github.com/openchamber/op..." → inferred openchamber/openchamber ⭐1.5k (Desktop UI for OpenCode, matches context "UI真好")
   ```

3. **Ask the user only when genuinely uncertain** — when multiple results are plausible and
   context doesn't help distinguish them:
   ```
   Found truncated URL "github.com/foo/bar..." — which repo did you mean?
   1. foo/barista ⭐420 — Coffee shop POS system
   2. foo/baroque ⭐38 — Baroque music generator
   Enter number (or 0 to skip):
   ```

   Never fork a truncated URL without either a confident inference or explicit user confirmation.

## Step 2: Fork via GitHub API

For each unique `{owner}/{repo}` pair, call the fork endpoint:

```bash
curl -s -L -X POST \
  -H "Authorization: Bearer $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github+json" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/{owner}/{repo}/forks
```

The `-L` flag is required — GitHub's API returns a 307 redirect that must be followed.

- If `GITHUB_TOKEN` is not set, tell the user to set it and stop:
  ```bash
  export GITHUB_TOKEN="ghp_..."   # classic PAT (recommended)
  # To persist across sessions, add to ~/.zshrc or ~/.bash_profile
  ```
- Fork requests are async on GitHub's side — a 202 response means "accepted", not "done".
- If a repo is already forked, GitHub returns the existing fork (not an error) — that's fine.
- Handle HTTP errors:
  - **401**: bad or expired token
  - **403**: token lacks fork permission. For **classic PATs**, need `repo` or `public_repo` scope. For **fine-grained PATs**, need "Administration: Read and write" permission (not just `contents`).
  - **404**: repo not found or private (token has no access)

## Step 3: Star the original repository

After a successful fork, star the original repo:

```bash
curl -s -L -X PUT \
  -H "Authorization: Bearer $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github+json" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/user/starred/{owner}/{repo}
```

A 204 response means success. Star failures are non-fatal — if starring fails, note it in the
report but don't treat the overall operation as failed.

## Step 4: Report results

After all forks are attempted, show a clear summary:

```
Found X repositories:
✓ owner/repo — forked → https://github.com/YOUR_USERNAME/repo  ⭐ starred
✓ owner/repo — forked → https://github.com/YOUR_USERNAME/repo  (star failed: <reason>)
✗ owner/repo — failed: <reason>
```

If the token's authenticated username isn't obvious, extract it from the fork response
(`full_name` field gives `your-username/repo-name`).

## Edge cases

- **No URLs found**: Tell the user clearly — "No GitHub repository URLs found in the input."
- **Private repos**: Fork will fail with 404 if the token doesn't have access; report the error.
- **Duplicate URLs**: Deduplicate before forking — fork each unique repo once.
- **Non-repo URLs**: Ignore `github.com/` paths that aren't `owner/repo` format (e.g., `github.com/features`, `github.com/login`).
