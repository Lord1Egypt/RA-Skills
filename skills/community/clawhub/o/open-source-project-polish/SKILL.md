---
name: open-source-project-polish
description: 'Turn a project folder into a polished open source project. Use when: open source ready, polish README, default MIT license, add LICENSE/CONTRIBUTING/CODE_OF_CONDUCT/CHANGELOG, automatically create public GitHub remote for projects without git remote, prepare repository for public release. Only add or modify project metadata/docs, never change source code.'
argument-hint: 'project folder path and optional GitHub owner/repo override'
---

# Open Source Project Polish

## Goal

Transform an existing project folder into a high-quality open source repository by improving public-facing documentation, community files, repository metadata, and Git/GitHub setup while preserving the original source code.

## Hard Boundaries

- Do not modify original product/source code, generated logic, tests, notebooks, assets, or runtime behavior unless the user explicitly asks.
- Allowed changes are limited to project-facing metadata and documentation such as README, LICENSE, CONTRIBUTING, CODE_OF_CONDUCT, SECURITY, CHANGELOG, SUPPORT, CITATION, issue/PR templates, release notes, badges, `.gitignore`, `.gitattributes`, `.editorconfig`, and GitHub workflow/docs scaffolding.
- Never include user-specific local machine paths in README or public docs, such as `/home/<user>/...`, `/Users/<user>/...`, drive-letter paths, personal workspace names, download folders, or machine-specific absolute project paths. Use relative paths, `$HOME`, `<repo>`, or placeholders instead.
- Default to MIT licensing when no license exists and no user preference overrides it.
- Default to automated public GitHub publication for folders without a Git remote. Determine the target owner/name if not obvious, then create a public remote and push documentation-only changes after secrets checks pass.
- If a network/GitHub command fails, retry once with the configured local proxy before declaring the remote step blocked.
- Preserve existing docs and community files where possible; improve them incrementally rather than replacing useful content.

## Inputs to Clarify When Missing

Ask only for information that materially affects irreversible or public-facing actions:

1. Target scope: workspace project path, or current folder if already clear.
2. Public identity: GitHub owner/repo name before creating any remote if it cannot be inferred from the folder and authenticated GitHub account.
3. License override: use an existing license if present; otherwise apply MIT by default unless the user requests another license.
4. Project positioning: one-sentence value proposition, target users, and maturity if not inferable from code/docs.
5. Source-code edits: assume forbidden; ask before touching anything beyond metadata/docs.

## Procedure

### 1. Audit Project State

- Inspect the folder structure, existing README/docs, package manifests, build files, examples, license files, and Git state.
- Check whether `.git` exists and whether any remote is configured.
- Identify secrets-risk files before any remote creation or push: `.env`, credentials, tokens, large binaries, datasets, private notes, local logs, and machine-specific paths.
- Summarize existing strengths, missing open-source essentials, and any uncertainty that needs user input.

### 2. Plan Non-Code Additions

Create a concise plan covering only allowed documentation and metadata work:

- README improvements using the `create-readme` skill as the basis for structure, tone, and GitHub-flavored Markdown.
- Community health files: MIT license by default, contributing guide, code of conduct, security policy, support guide, changelog, citation, governance, issue templates, PR template.
- Repository hygiene: `.gitignore`, `.gitattributes`, `.editorconfig`, docs index, examples index, badges, project description, topics, funding/sponsor metadata if relevant.
- Git/GitHub setup: initialize Git if absent, create public remote if absent, set default branch, and push documentation-only changes after safety checks.

### 3. Improve README

Use the `create-readme` skill for README creation or refresh. Ensure the README is concise, attractive, and useful:

- Clear project name, tagline, and short value proposition.
- Badges only when truthful and maintainable.
- Quick start with verified commands when possible.
- Commands must be copy-pastable from the repository root and must not contain the current user's absolute local paths; prefer `./script.sh`, `$HOME/...`, `/path/to/...`, or `<repo>/...` examples.
- Installation, usage, configuration, examples, project structure, troubleshooting, and links to dedicated files.
- Do not duplicate full LICENSE, CONTRIBUTING, CHANGELOG, or SECURITY content inside README; link to those files.
- Preserve existing project-specific knowledge and examples.

### 4. Add Community Files

Add or update files only when they help the project appear complete and trustworthy:

- `LICENSE`: use existing license if present; otherwise add MIT by default with the detected current year and owner/project name where appropriate.
- `CONTRIBUTING.md`: development setup, branch/commit conventions if inferable, test expectations, issue/PR process.
- `CODE_OF_CONDUCT.md`: use a standard concise contributor covenant style unless user has another policy.
- `SECURITY.md`: supported versions, responsible disclosure channel placeholder, vulnerability reporting expectations.
- `CHANGELOG.md`: initialize with `Unreleased` and current public baseline; do not invent release history.
- `SUPPORT.md`: where to ask questions, report bugs, and request features.
- `.github/ISSUE_TEMPLATE/*` and `.github/PULL_REQUEST_TEMPLATE.md`: practical forms/checklists tailored to the project.
- `CITATION.cff` only for research/academic/scientific projects or when authorship metadata is available.

### 5. Repository Hygiene

- Create or refine `.gitignore` based on detected languages/tools without excluding files that are likely source artifacts.
- Add `.gitattributes` for text normalization and common binary patterns when useful.
- Add `.editorconfig` with conservative whitespace defaults matching the repo style.
- Do not add CI workflows unless build/test commands are known or verified; if added, keep them minimal and non-invasive.

### 6. Git and Remote Handling

For folders without Git:

1. Initialize a repository for the target folder after verifying the folder path.
2. Stage only metadata/docs files created or changed by this workflow.
3. Commit with a documentation-focused message when publication is proceeding.

For Git repositories without a remote:

1. Infer the GitHub owner from `gh` authentication and the repo name from the folder when possible; ask only if ambiguous.
2. Check for `gh` authentication before creating a remote.
3. Create a public GitHub repository by default.
4. Add `origin`, set the default branch, and push after reviewing staged changes and confirming no secrets are included.

Recommended GitHub CLI flow, adapted to the project:

```bash
git status --short
git remote -v
gh auth status
gh repo create OWNER/REPO --public --source=. --remote=origin --push
```

If network commands fail, retry once with:

```bash
export {HTTP_PROXY,HTTPS_PROXY,ALL_PROXY,http_proxy,https_proxy,all_proxy}=http://127.0.0.1:7890
```

### 7. Quality Checks

Before finalizing:

- Re-open changed Markdown snippets to verify headings, links, code fences, and copy-pastable command indentation.
- Search README and public docs for local machine paths before finalizing, including `/home/`, `/Users/`, drive-letter paths, personal workspace names, and absolute paths copied from the current environment.
- Confirm no source code files were modified unless explicitly approved.
- Confirm all links to local files target files that exist.
- Run lightweight formatting or markdown linting if available; do not install heavy dependencies just for this workflow unless user agrees.
- Show `git diff --stat` and summarize changed files.
- If a remote was created, report the URL, visibility, default branch, and whether anything was pushed.

## Decision Points

- Existing README is strong: preserve structure and patch missing sections rather than rewrite.
- No verified install/test commands: include clearly marked placeholders or "not yet documented" notes instead of inventing commands.
- License unknown: add MIT by default unless the user requests a different license.
- Possible secrets or private data: stop remote creation/push and report the risky paths.
- No `gh` CLI or not authenticated: provide exact commands for the user to run, but still complete local docs polish and prepare a documentation-only commit if safe.
- Monorepo: create or update root community files and per-package README files only when package boundaries are clear.

## Completion Summary

End with:

- Files added/updated.
- What was intentionally not touched, especially source code.
- Validation performed.
- Remote repository status, if applicable.
- Suggested next steps such as enabling CI, adding examples, cutting a first release, or creating project topics.
