# Medium Blog Post Creator

> **Publish blog posts to Medium via GitHub Pages + URL import — no API token required.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/ylnhari/openclaw-skills/blob/main/LICENSE)
[![OpenClaw Skill](https://img.shields.io/badge/OpenClaw-Skill-blueviolet)](https://docs.openclaw.ai/clawhub)

An [OpenClaw](https://openclaw.ai) skill that turns *"write a blog post about X"*
into a finished **Medium draft** — fully automated, end to end, with no Medium
API token.

> **About this README.** It is written for **people** — anyone browsing ClawHub
> or this repo who wants to understand what the skill does and how. The AI agent
> never loads this file; it only loads `SKILL.md` (and the `references/` files a
> step explicitly asks for). So this README costs **zero runtime tokens** — it
> exists purely to make the skill understandable to a human, because `SKILL.md`
> is written as a terse procedure *for the agent* and is hard to read top‑to‑bottom
> as a person.

---

## What problem it solves

Medium **stopped issuing new API integration tokens on January 1, 2025**, so the
old "post to Medium via the API" tools no longer work for new users. The one
stable path that remains is Medium's **URL importer** (`medium.com/p/import`):
give it a public web page and it converts that page into a Medium story.

This skill automates that whole path:

1. Writes your post as a small, strict subset of **HTML** that Medium's importer
   converts cleanly.
2. Publishes that HTML as a public page on **GitHub Pages** (your own repo).
3. Drives a **browser** to Medium's importer, pastes the page URL, and lets
   Medium turn it into a **draft**.

It always **stops at draft** for your review — it never auto-publishes.

---

## The big picture — end-to-end flow

```
You: "Write a blog post about local LLM inference"
        │
        ▼
 [Step 0] Load memory ── first run? ask a few setup questions
        │                later runs? skip straight ahead
        ▼
 [Step 1] Check tools (gh, git, browser signed into Medium)
        │
        ▼
 [Step 2] Make sure your blog repo exists on GitHub
          (first run: create it, enable GitHub Pages, add .nojekyll)
        │
        ▼
 [Step 3-5] Write the post:  posts/<date>-<slug>/index.html
            + meta.json   + update posts/index.json
        │
        ▼
 [Step 6] git push  ─────────►  GitHub auto-builds the Pages site
        │                        (the push IS the trigger; no workflow needed)
        ▼
 [Step 7] Wait until the post URL is live (HTTP 200)
        │
        ▼
 [Step 8] Browser → medium.com/p/import → paste URL → Medium makes a DRAFT
        │
        ▼
 [Step 9] Save the Medium draft link back into your repo's metadata
        │
        ▼
 [Step 10] Report the GitHub + Medium links. You review & click Publish.
```

---

## First run vs. every run after

The skill remembers its setup so it only asks questions once.

| | **First run** | **Every run after** |
|---|---|---|
| Setup questions | Asks for GitHub/Medium accounts, repo name, working dir, etc. | **Skipped** — reads them from memory |
| Blog repo | **Creates** it (e.g. `blog`) and enables GitHub Pages | Reuses the existing repo |
| What it does | Full setup **+** writes the post | Just writes the next post |

It "remembers" using **two small files** (explained below): a machine-local
config (your preferences + which repo to use) and a marker committed inside your
blog repo.

---

## What gets created, and where

Nothing about *you* is ever published to ClawHub. The skill creates files in two
places on **your** side:

| File | Lives in | Purpose |
|------|----------|---------|
| `posts/<date>-<slug>/index.html` | your blog repo | the post itself (constrained HTML) |
| `posts/<date>-<slug>/meta.json` | your blog repo | per-post metadata (title, tags, Medium link…) |
| `posts/index.json` | your blog repo | list of all posts, newest first |
| `.nojekyll` | your blog repo | tells GitHub Pages to serve the HTML as-is |
| `.medium-skill-config.json` | your blog repo | "marker": this repo is managed by the skill (owner, repo, pages URL) |
| `config.json` | your machine (`$MEDIUM_BLOG_CONFIG` or `~/.config/medium-blog-post-creator/`) | your preferences + `last_repo` so later runs find the repo |

---

## Anatomy of `SKILL.md` — what each section tells the agent

`SKILL.md` is the file the agent actually runs. It's ordered for the agent, not
for a human reader, so here is what each part is for and *why it's there*:

| Section in `SKILL.md` | What it is | What it tells the agent |
|---|---|---|
| **Frontmatter** (`name`, `description`, `metadata.openclaw`) | Machine-readable header | The skill's identity, and that it **requires the `gh` and `git` CLIs** (`requires.bins`) so OpenClaw can detect/install them |
| **Intro paragraphs** | One-paragraph "why/what" | The mission: author constrained HTML → GitHub Pages → Medium import → stop at draft |
| **References** (near the top) | Pointers to `references/*.md` and `assets/*` | *"Load these only when a step says to."* It's at the top so the agent knows the detailed docs exist before it starts — e.g. read `html-standards.md` before writing a post |
| **When to use this skill** | Trigger phrases | Recognize requests like "blog about X" / "cross-post to Medium" |
| **What this skill does NOT do** | Guardrails | Never auto-publish; no API token; don't assume an OS |
| **Prerequisites** | Accounts/tools needed | Verify GitHub + Medium accounts, `gh` authenticated, browser signed in |
| **Inputs collected from the user** | The setup questions | Ask topic, audience, tone, length, **repo name (default `blog`)**, etc., in one message |
| **Workflow → Step 0** | Load/initialize config | Read the two memory files (see below) and decide: first run (ask) vs. repeat run (reuse) |
| **Step 1** | Confirm prerequisites | Run `gh --version`, `gh auth status`, `git --version`; stop if anything's missing |
| **Step 2** | Scaffold the repo | Create/clone the blog repo, compute the Pages URL (user-site vs project-site), enable GitHub Pages, add `.nojekyll`, save `last_repo` |
| **Step 3** | Write the post HTML | Read `references/html-standards.md`, start from `assets/post-template.html`, write `index.html` |
| **Step 4** | Write `meta.json` | Per-post metadata sidecar |
| **Step 5** | Update `posts/index.json` | Prepend the new post to the index |
| **Step 6** | Commit & push | `git push` — **this is what triggers GitHub Pages to rebuild** |
| **Step 7** | Wait for deploy | Poll the post URL until it returns HTTP 200 |
| **Step 8** | Import to Medium | Browser → `medium.com/p/import` → paste URL → get a **draft** (never publish) |
| **Step 9** | Link back | Write the Medium draft URL into `meta.json` and `index.json` |
| **Step 10** | Report | Show the GitHub Pages + Medium draft links |
| **Error recovery** | Troubleshooting table | What to do for common failures (auth, 404, empty import…) |
| **Security and privacy notes** | Safety rules | Pages are public before import; no credentials stored; no third-party APIs |
| **Rate limits** | Medium's limits | Drafts don't hit the limit; don't auto-publish past it |

### The two memory files Step 0 reads (demystified)

Step 0 mentions reading a couple of small JSON files. Here's what they are:

- **Per-install config** (`config.json`, on *your machine*, never published):
  your stable preferences (working dir, default audience/tone/length) **plus
  `last_repo`** — the pointer that tells the skill *which* blog repo to reuse and
  *where* it is, so later runs don't re-ask.
- **Per-repo marker** (`.medium-skill-config.json`, committed *inside your blog
  repo*): identifies the repo as "managed by this skill" and records its owner,
  name, and Pages URL. Because it lives in the repo, it travels with it across
  machines.

Full schemas and resolution rules: [`references/configuration.md`](./references/configuration.md).
The HTML rules the agent follows: [`references/html-standards.md`](./references/html-standards.md).

---

## Install

From ClawHub (skills install by slug):

```bash
openclaw skills install medium-blog-post-creator
```

Or from a local checkout of this repository:

```bash
openclaw skills install ./skills/medium-blog-post-creator --as medium-blog-post-creator
```

## Prerequisites

- A **GitHub account** and a **Medium account**
- **`gh` CLI** installed and authenticated (`gh auth login`) — [install](https://cli.github.com)
- **`git`**
- The **OpenClaw `browser` tool**, signed into your Medium account

The skill checks these for you and stops early if anything is missing.

## Usage

Just ask your OpenClaw agent:

> "Write a blog post about local LLM inference optimization"

On the first run it asks a few setup questions and scaffolds your blog repo; on
later runs it remembers everything and goes straight to writing the next post.

## Files in this bundle (what installs to a user)

- [`SKILL.md`](./SKILL.md) — the agent procedure (the file the agent runs)
- [`references/html-standards.md`](./references/html-standards.md) — the HTML subset Medium accepts
- [`references/configuration.md`](./references/configuration.md) — the two config/marker files explained
- [`assets/post-template.html`](./assets/post-template.html) — a ready-to-fill post template
- [`assets/meta.template.json`](./assets/meta.template.json) — the per-post metadata shape
- `README.md` — this file (for humans; not loaded by the agent)

## Notes

- **Stops at draft.** You click Publish when you're happy with it.
- **Posts are public on GitHub Pages** before import (Medium's importer needs a
  fetchable URL) — don't use it for content you don't want publicly visible.
- **Rate limit:** Medium caps publishing at ~2 stories / 24 hours; this skill
  only drafts, so it doesn't hit that — just don't auto-publish past the cap.

## License

MIT — see the umbrella repository's [LICENSE](https://github.com/ylnhari/openclaw-skills/blob/main/LICENSE).
