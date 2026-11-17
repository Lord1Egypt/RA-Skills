---
name: import-skills-to-skilder
description: Import the Agent Skills already present on this machine or in this repo into a Skilder workspace, so the whole team's agents can discover and run them from one governed endpoint. Trigger on requests like "import my skills to Skilder", "publish these skills to my team", "get my local skills into Skilder", "centralize our agent skills".
version: 1.0.0
homepage: https://github.com/skilder-ai/skills
---

Move the user's existing local Agent Skills into their Skilder workspace. Skills use the open Agent Skills format on both sides, so content imports as-is: frontmatter and body stay what they are.

## Step 1: Be connected

You need the Skilder MCP server (`https://app.skilder.ai/mcp`) with an active session:

1. If the server isn't registered yet, follow the `connect-to-skilder` skill from this same repo (one endpoint, OAuth sign-in, no keys).
2. Call `init_skilder` and keep the session id it returns; every other Skilder tool call needs it.
3. Importing uses the `manage` tool, which is available to workspace admins. The first user of a workspace is its admin, so a user on their own workspace qualifies. If `manage` isn't in your tool list, tell the user to ask their workspace admin to run the import.

## Step 2: Discover local skills

Scan these locations, nearest first. Each directory containing a `SKILL.md` is one skill:

- `./.claude/skills/` and `./.agents/skills/` (project)
- `~/.claude/skills/` and `~/.agents/skills/` (user)
- `./skills/` in the current repo, including one level of category subdirectories

For each skill found, read the `SKILL.md`: YAML frontmatter gives `name` and `description`, the body is the instructions. Note any extra files next to it (a `references/` folder, scripts, other documents).

## Step 3: Confirm the list once

Show the user a single inventory: skill name, one-line description, file count, and source path. Ask once which to import (default: all). Also call `manage` → `list-skills` and flag any name that already exists in the workspace; for those, ask whether to skip or import under a suffixed name. This is the only confirmation round; after it, proceed without further questions.

## Step 4: Import

For each approved skill, in this order:

1. `manage` → `create-skill` with `name`, `description` (from frontmatter), and `instructions` (the SKILL.md body, verbatim). Keep the returned skill `id`.
2. For each companion file, `manage` → `create-skill-content` with `skillId` set to that id:
   - Markdown and text documents: `contentType: "reference"`, `name` set to the filename, `instructions` set to the file content verbatim.
   - `.py`, `.sh`, `.js`, `.ts` files: `contentType: "script"`, with `type` set to PYTHON, BASH, JAVASCRIPT, or TYPESCRIPT and `code` set to the file content.
   - Binary files (images, PDFs): skip them and record the filename; they're added later through the web app.

Import content verbatim. Do not rewrite, summarize, or "improve" the user's instructions.

## Constraints

- **Never import secrets.** Before importing any file, check it for API keys, tokens, passwords, or `.env`-style content. Skip such files, name them in the report, and do not echo their contents.
- **Don't guess.** If a `SKILL.md` has no name in its frontmatter, use its directory name. If a file's role is ambiguous, import it as a reference.
- **One failure doesn't stop the run.** If a create call errors, record it and continue with the remaining skills.

## Step 5: Report

End with a single summary: skills imported (with names), files attached per skill, anything skipped (binaries, secrets, duplicates, errors). Then point the user at their library at `https://app.skilder.ai` to review the imports, compose them into roles, and publish. From there, every agent connected to the workspace can discover and run them.
