---
name: "medium-blog-post-creator"
description: "Publish blog posts to Medium via GitHub Pages + URL import — no API token required."
homepage: "https://github.com/ylnhari/openclaw-skills/tree/main/skills/medium-blog-post-creator"
license: "MIT"
metadata:
  openclaw:
    emoji: "✍️"
    requires:
      bins: ["gh", "git"]
---

# Medium Blog Post Creator

Publish a fully formatted blog post to **Medium** without an API token.

Medium stopped issuing new integration tokens on **January 1, 2025**. This
skill works around that closure using the only remaining stable import path:
author a constrained HTML post, deploy it as a public URL via GitHub Pages, and
let Medium's own URL-import tool fetch and convert it into blocks.

It is **end-to-end agent-driven** — no external repos or local paths to
remember. It asks the user for what it needs, scaffolds a static blog repo in
their own GitHub account, deploys each post to GitHub Pages, and drives the
browser through Medium's import flow until the draft is ready for review. It
always stops at **draft** — it never auto-publishes.

## References

Load these when the workflow points to them:

- `references/html-standards.md`: the HTML subset Medium's importer accepts.
  **Read it before writing a post.**
- `references/configuration.md`: persistent-config schemas, resolution rules,
  and reset patterns (used in Step 0).
- `assets/post-template.html`: ready-to-fill post template implementing every
  HTML rule.
- `assets/meta.template.json`: the per-post metadata sidecar shape.

## When to use this skill

Trigger when the user says any of: "write a blog post about X", "create a
Medium post about X", "publish a draft to Medium about X", "blog about X",
"cross-post this to Medium", or provides content (Markdown, outline, notes) and
mentions Medium.

## What this skill does NOT do

- **No auto-publish.** Always stops at **draft** for human review.
- **No Medium API token required.** Uses the public URL-import endpoint.
- **No pre-existing blog repo needed.** Scaffolds one from scratch.
- **No OS assumptions.** Paths derive from user inputs and the working
  directory; works on Windows, macOS, and Linux.

## Prerequisites (collected from the user)

| Need | Why |
|------|-----|
| **GitHub account** | Host the static blog repo and serve it via GitHub Pages |
| **Medium account** | Destination for the imported draft |
| **`gh` CLI** (authenticated) | Create/clone/push the repo from the agent's shell |
| **`git`** | Standard repo operations |
| **OpenClaw `browser` tool** (signed into Medium) | Drive Medium's URL-import UI |

`gh` and `git` are declared in frontmatter `requires.bins` so OpenClaw can
detect them. Still verify at runtime: `gh auth status` must show an
authenticated user, and the browser tool must be logged into Medium. If any
prerequisite is missing, stop and tell the user what to install or sign into.
Do not proceed with placeholders.

## Inputs collected from the user (in one message, before any work)

Ask for these together; if some are omitted, use the defaults and **state your
assumptions explicitly** before proceeding:

1. **Topic / title** (required).
2. **Target audience** — `technical` / `general` / `beginner`. Default: `technical`.
3. **Tone** — `casual` / `formal` / `tutorial`. Default: `casual`.
4. **Length** — `short` (~500w) / `medium` (~1000w) / `long` (~2000w+). Default: `medium`.
5. **Key sections or bullet points** the post must cover.
6. **GitHub username or org** to host the blog repo (required). Example: `octocat`.
7. **Repository name**. Default suggestion: `blog` — a normal project repo,
   served at `https://<username>.github.io/blog/`. (Advanced: naming the repo
   exactly `<username>.github.io` serves the blog at your account root,
   `https://<username>.github.io/`, but it uses your one and only user site,
   so most people keep `blog`.)
8. **Local working directory** to clone into. Default: current working directory.
9. **Tags** for Medium (2–5 short keywords).
10. **Optional: cover image URL.** If absent, pick a relevant free-license
    Unsplash image.

## Workflow

11 steps (Step 0–10). **Do not skip Step 0 even on first run.**

### Step 0 — Load or initialize persistent config

Load the per-install config (`$MEDIUM_BLOG_CONFIG`, else the per-user config
dir) and, if the blog repo is already cloned, its per-repo marker
(`<repo-local-path>/.medium-skill-config.json`). Schemas and full rules are in
`references/configuration.md`. Then:

- **The per-install config names a repo (`last_repo` set):** reuse it. Skip all
  setup questions and go to Step 2, which ensures the local clone exists (a
  fresh clone brings the marker with it). `<repo-local-path>` =
  `<default_working_dir>/<github_repo>`.
- **Marker readable but `last_repo` unset** (e.g. the agent is already inside
  the blog repo): adopt the marker's repo and save `last_repo` — don't re-ask.
- **First run on this machine (no `last_repo`, no readable marker):** ask the
  full input set above; Step 2 creates the repo, writes the marker into it, and
  saves `last_repo` to the per-install config so later runs skip setup.
- **One-off override:** if the user names a different repo for this post, use it
  for this invocation only; do not change `last_repo`.

### Step 1 — Confirm prerequisites

Verify in the agent's shell: `gh --version`, `gh auth status` (authenticated),
`git --version`, and that the OpenClaw `browser` tool is reachable. If any
check fails, stop and report the exact missing item.

### Step 2 — Scaffold the blog repository

Scaffold a **minimal static site**: a single page that lists posts, each post
in its own folder. No frameworks, no build step — plain HTML, CSS, and a JSON
index. `<repo-local-path>` is the local path of the cloned repo (typically
`<default_working_dir>/<github_repo>`).

**Resolving `<pages-base-url>`** (used for every post URL and the marker's
`pages_url`). GitHub serves user/org sites and project sites at different
paths, so compute the base once and reuse it:

- If `<github_repo>` equals `<github_owner>.github.io` (a **user/org site**),
  the base is `https://<github_owner>.github.io/`.
- Otherwise (a **project site**), the base is
  `https://<github_owner>.github.io/<github_repo>/`.

Keep the trailing slash. A post then lives at
`<pages-base-url>posts/<YYYY-MM-DD>-<slug>/`. Never hand-build
`https://<owner>.github.io/<repo>/...` unconditionally — for a
`<owner>.github.io` repo that produces a broken double path.

**If the repo is already known (`last_repo` set, or the marker is present):**
it already exists and Pages was enabled during initial setup. Skip creation and
the Pages-enable step below; just ensure the local clone is present and current:

```bash
mkdir -p "<default_working_dir>"
if [ ! -d "<repo-local-path>" ]; then
  gh repo clone <github_owner>/<github_repo> "<repo-local-path>"
else
  cd "<repo-local-path>" && git pull --rebase origin <branch>
fi
```

**If no repo is known yet (fresh setup):**

1. Create and clone the repo (run from `<default_working_dir>` so the clone
   lands at `<repo-local-path>`):

   ```bash
   mkdir -p "<default_working_dir>"
   cd "<default_working_dir>"
   gh repo create <github_owner>/<github_repo> \
     --public \
     --description "Static blog for Medium cross-posting" \
     --clone \
     --add-readme
   # Now cloned at <default_working_dir>/<github_repo> = <repo-local-path>
   ```

2. If the repo already exists on GitHub but the local clone is missing, fall
   back to `gh repo clone <github_owner>/<github_repo> "<repo-local-path>"`.

3. Write the per-repo marker (schema in `references/configuration.md`):

   ```bash
   # On Unix (bash)
   printf '%s\n' '{' \
     '  "schema_version": 1,' \
     "  \"github_owner\": \"<github_owner>\"," \
     "  \"github_repo\": \"<github_repo>\"," \
     "  \"pages_url\": \"<pages-base-url>\"," \
     "  \"default_author\": \"<github_owner>\"," \
     "  \"branch\": \"<branch>\"" \
     '}' > "<repo-local-path>/.medium-skill-config.json"
   ```

   ```powershell
   # On Windows (PowerShell)
   @{
     schema_version = 1
     github_owner    = "<github_owner>"
     github_repo     = "<github_repo>"
     pages_url       = "<pages-base-url>"
     default_author  = "<github_owner>"
     branch          = "<branch>"
   } | ConvertTo-Json | Set-Content "<repo-local-path>\.medium-skill-config.json"
   ```

4. Create an empty `.nojekyll` at the repo root so GitHub Pages serves the
   HTML as-is (no Jekyll processing), then commit it with the marker:

   ```bash
   cd "<repo-local-path>"
   touch .nojekyll          # Windows PowerShell: New-Item -ItemType File .nojekyll
   git add .nojekyll .medium-skill-config.json
   git commit -m "chore: mark repo as managed by medium-blog-post-creator + add .nojekyll"
   git push origin <branch>
   ```

5. **Enable GitHub Pages** (do this now, before any post is written):

   - **User/org site** (`<github_repo>` == `<github_owner>.github.io`): Pages
     is enabled automatically at the domain root. Nothing to do.
   - **Project site** (any other name): enable Pages via the API. This is
     idempotent — a `409` means it is already enabled, which is fine:

     ```bash
     gh api -X POST "repos/<github_owner>/<github_repo>/pages" \
       --input - <<'JSON' || true
     {"source":{"branch":"<branch>","path":"/"}}
     JSON
     ```

     If the call fails for any reason other than "already enabled", direct the
     user to enable Pages manually at
     `https://github.com/<github_owner>/<github_repo>/settings/pages`
     (Source: **Deploy from a branch** → `<branch>` / `/ (root)`), and wait for
     confirmation before continuing.

6. **Save the repo to the per-install config** so future runs reuse it without
   asking: write `last_repo` (`github_owner`, `github_repo`, `pages_url` =
   `<pages-base-url>`, `branch`) into the per-install config file. Schema in
   `references/configuration.md`.

### Step 3 — Create the post HTML file

**Read `references/html-standards.md` first**, then start from
`assets/post-template.html`. Write the post to:

```
<repo-local-path>/posts/<YYYY-MM-DD>-<slug>/index.html
```

`<slug>` derives from the title: lowercase, hyphens only, max 60 chars
(e.g. `running-llms-locally`). The body should include an opening hook, 3–6
`<h2>` sections, code examples where relevant, at least one Unsplash image,
bold/italic emphasis, a `<blockquote>`, and a closing call to action. No
hallucinated facts, no filler, no LLM-tells.

### Step 4 — Create the metadata sidecar

Write `<repo-local-path>/posts/<YYYY-MM-DD>-<slug>/meta.json` from
`assets/meta.template.json`:

```json
{
  "title": "Full post title",
  "date": "YYYY-MM-DD",
  "author": "<github-username-or-org>",
  "description": "1-2 sentence summary, max 200 chars",
  "tags": ["tag1", "tag2", "tag3"],
  "status": "draft",
  "medium_url": null,
  "cover_image": "https://images.unsplash.com/photo-...?w=1200&q=80"
}
```

`medium_url` is filled in after Step 8 so the post is traceable end-to-end.

### Step 5 — Update the post index

The repo keeps a top-level `posts/index.json` (newest first):

1. Read `posts/index.json`; if missing, create it as `[]`.
2. **Prepend** the new entry. Do not re-sort existing entries.
3. Write it back.

Entry shape:

```json
{
  "slug": "YYYY-MM-DD-slug",
  "title": "Full post title",
  "date": "YYYY-MM-DD",
  "description": "1-2 sentence summary, max 200 chars",
  "tags": ["tag1", "tag2"],
  "cover_image": "https://images.unsplash.com/photo-...?w=1200&q=80",
  "status": "draft",
  "medium_url": null
}
```

### Step 6 — Commit and push

```bash
cd "<repo-local-path>"
git add posts/<YYYY-MM-DD>-<slug>/ posts/index.json
git commit -m "feat(posts): add \"<POST TITLE>\" [<YYYY-MM-DD>]"
git push origin <branch>
```

If push fails with an auth error, ask the user to run `gh auth login` and retry
(max 2 attempts), then report the error and stop.

### Step 7 — Wait for GitHub Pages to deploy

Pages was already enabled in Step 2, so this step only waits for the new commit
to go live. Build the post URL from `<pages-base-url>` resolved in Step 2 —
never hand-build the path.

```powershell
# PowerShell 7+ (Windows, macOS, Linux) — poll until HTTP 200, max 3 min.
$url = "<pages-base-url>posts/<YYYY-MM-DD>-<slug>/"
$deadline = (Get-Date).AddMinutes(3)
while ((Get-Date) -lt $deadline) {
  try {
    $code = (Invoke-WebRequest -Uri $url -UseBasicParsing -MaximumRedirection 5 -ErrorAction Stop).StatusCode
    if ($code -eq 200) { exit 0 }
  } catch {
    $code = 404
  }
  if ($code -eq 200) { exit 0 }
  Start-Sleep -Seconds 15
}
exit 1
```

```bash
# macOS / Linux — poll until HTTP 200, max 3 min.
deadline=$(( $(date +%s) + 180 ))
url="<pages-base-url>posts/<YYYY-MM-DD>-<slug>/"
while [ "$(date +%s)" -lt "$deadline" ]; do
  code=$(curl -fsS -o /dev/null -w "%{http_code}" "$url" 2>/dev/null || echo 000)
  if [ "$code" = "200" ]; then exit 0; fi
  sleep 15
done
exit 1
```

If it times out (still `404`), direct the user to the repo's Actions tab
(`https://github.com/<github_owner>/<github_repo>/actions`) and report back.
**Do not proceed to Step 8 until the URL returns 200.**

### Step 8 — Import to Medium via the browser

Use the OpenClaw `browser` tool to drive Medium's URL import.

1. Navigate to `https://medium.com/p/import`. Wait for full load.
2. In the URL field, paste `<pages-base-url>posts/<YYYY-MM-DD>-<slug>/`
   (include the trailing slash — Medium's importer is sensitive to it).
3. Click Import.
4. Wait for confirmation (text like "Imported the story").
5. Click "See your story" / "Open draft" to open the draft editor at
   `https://medium.com/p/<draft-id>/edit`.
6. **Do not click Publish.** Leave it as a draft.
7. Copy the draft editor URL.

**Tag handling:** if the user supplied tags, attempt to add each. If Medium's
UI rejects one, skip it and continue. Do not loop more than twice on tag UI
failures.

### Step 9 — Update metadata with the Medium URL

1. Set `medium_url` in `posts/<YYYY-MM-DD>-<slug>/meta.json` to the draft URL.
2. Set `medium_url` for the same post in `posts/index.json`.
3. Commit and push:

   ```bash
   git add posts/<YYYY-MM-DD>-<slug>/meta.json posts/index.json
   git commit -m "chore(posts): link medium draft for \"<POST TITLE>\""
   git push origin <branch>
   ```

### Step 10 — Report to the user

```
✅ Post created: "<TITLE>"
📄 GitHub Pages: <pages-base-url>posts/<YYYY-MM-DD>-<slug>/
📝 Medium draft: <draft-editor-url>

The draft is ready for your review. Open the Medium link, make any edits, and
click Publish when you're happy with it.
```

If anything failed, report the exact step, the exact error, and the next
action the user should take. Do not invent success messages.

## Error recovery

| Problem | Fix |
|---------|-----|
| `gh` not installed | Ask the user to install it: https://cli.github.com |
| `gh auth status` unauthenticated | Ask the user to run `gh auth login` |
| Repo creation fails (already exists) | Fall back to cloning the existing repo |
| Git push fails with auth error | Ask the user to run `gh auth login`, then retry (max 2) |
| GitHub Pages returns 404 | Wait 60s, retry. If still 404 after 3 min, check the Actions tab |
| Medium import shows empty content | The HTML must be static — verify the Pages URL loads in a browser first |
| Medium import fails silently | Verify the Pages URL returns HTTP 200 and includes the trailing slash |
| `posts/index.json` merge conflict | `git pull --rebase origin <branch>`, then re-add changes |
| Browser times out on Medium | Close the tab, open a fresh one, retry the navigate step |
| Tag won't add in Medium UI | Skip that tag, continue. Do not loop. |

## Security and privacy notes

- **Posts are public on GitHub Pages** before being imported to Medium — by
  design, since Medium's importer requires a publicly fetchable URL. Do not use
  this skill for posts containing secrets or anything the user does not want in
  a public repository.
- **No credentials are stored by the skill.** Auth is delegated to
  `gh auth login` and the user's existing browser session.
- **The skill calls no third-party API** beyond the user's own GitHub
  repository and Medium's public import endpoint.

## Rate limits

Medium enforces a daily publishing limit (as of early 2026: **2 stories +
100 responses per rolling 24 hours**). This skill stops at draft, so the limit
doesn't block automated drafting — but the user should not auto-publish more
than 2 stories per day from this skill's output.
