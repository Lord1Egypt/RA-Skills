# Persistent configuration (sticky state)

After the first successful run, the skill remembers its setup so subsequent
invocations skip the scaffolding questions. State is stored in **two places**,
checked in this order on every invocation.

## 1. Per-install config (machine-local)

Lives at (first match wins):

1. `$MEDIUM_BLOG_CONFIG` (if the environment variable is set), or
2. the per-user config directory, **outside the installed skill folder**:
   - Linux/macOS: `${XDG_CONFIG_HOME:-~/.config}/medium-blog-post-creator/config.json`
   - Windows: `%APPDATA%\medium-blog-post-creator\config.json`

Keep this file **out of the skill's install directory.** OpenClaw installs
skills into the active workspace's `skills/` folder (or the shared managed
skills directory with `--global`), and `openclaw skills update` matches
installed bundles by hashing their files — a stray runtime file inside the
bundle can interfere with updates or be overwritten by them.

It is **never committed, never bundled, never published.** Holds personal
preferences that are stable across posts but not across machines, plus
`last_repo` — the machine-local pointer to which blog repo to reuse, so later
runs can locate it without asking (the marker lives *inside* the repo, so the
skill needs this to know where the repo is in the first place):

```json
{
  "schema_version": 1,
  "default_working_dir": "~/Projects",
  "default_audience": "technical",
  "default_tone": "casual",
  "default_length": "medium",
  "default_branch": "main",
  "last_repo": {
    "github_owner": "<github-username-or-org>",
    "github_repo": "<repo-name>",
    "pages_url": "<pages-base-url>",
    "branch": "main"
  }
}
```

`last_repo` is absent until the first repo is set up; the skill writes it at
the end of the first run and reads it on every run after to compute
`<repo-local-path> = <default_working_dir>/<github_repo>`.

## 2. Per-repo marker (travels with the blog)

Lives at `<repo-local-path>/.medium-skill-config.json` and is committed to the
blog repository itself, so the blog's identity follows the repo — switch
machines, and a fresh clone brings the marker with you.

The file is **public** (it lives in a public GitHub repository), so it holds
only values that are safe to expose:

```json
{
  "schema_version": 1,
  "github_owner": "<github-username-or-org>",
  "github_repo": "<repo-name>",
  "pages_url": "https://<github-username-or-org>.github.io/<repo-name>/",
  "default_author": "<github-username-or-org>",
  "branch": "main"
}
```

`pages_url` is the resolved `<pages-base-url>` (see SKILL.md Step 2): the
domain root for a `<owner>.github.io` repo, or `https://<owner>.github.io/<repo>/`
for a project repo. The example above shows the project-site form.

## Resolution rules

`last_repo` (in the per-install config) is the machine-local pointer to "which
blog repo to use"; the per-repo marker is the in-repo source of truth that
travels with the repo. Resolve in this order:

- **`last_repo` is set:** reuse that repo. Step 2 ensures the local clone
  exists (a fresh clone brings the marker with it). Do not re-ask setup
  questions.
- **Marker readable but `last_repo` unset** (e.g. the agent is already running
  inside the blog repo): adopt the marker's repo and save `last_repo` back to
  the per-install config — no need to ask.
- **First run on this machine (no `last_repo`, no readable marker):** ask the
  full input set, then in Step 2 create/clone the repo, write
  `.medium-skill-config.json` into it, and save `last_repo`.
- **One-off override:** if the user names a different repo for a single post,
  honor it for that invocation only and leave `last_repo` unchanged.
- **Unknown `schema_version`:** if a file's `schema_version` is not `1`, warn
  the user, treat unrecognized fields as defaults, and continue.

## Per-invocation overrides

The user can override any sticky value for one invocation without touching the
config files. For example: *"Use `acme-corp/engineering-blog` for this post"*
is honored as a one-off; afterwards the config files are left unchanged.

## Resetting persistent state

| User says | Action |
|-----------|--------|
| "Forget my local config" / "Reset skill state" | Delete the per-install config file (`$MEDIUM_BLOG_CONFIG`, or the per-user config path). The per-repo marker is untouched. |
| "Forget this blog" / "Detach this repo from the skill" | Delete `<repo-local-path>/.medium-skill-config.json` and commit the removal. The per-install config is untouched. |
| "Forget everything" / "Start over" | Delete both files. The next invocation goes through the original first-run flow. |
| "Use a different blog for this post" | Override the GitHub owner + repo for this invocation only; do not touch the configs. |
