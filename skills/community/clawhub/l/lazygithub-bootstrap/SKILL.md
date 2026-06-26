---
name: github-repo-bootstrap
description: Publish, bootstrap, or tidy a GitHub repository so the README and full GitHub About metadata stay in sync. Use when an agent is asked to create a new repo, push an existing local project to GitHub, fill or fix the About section, set description/homepage/topics, or make the README and repository presentation match.
---

# GitHub Repo Bootstrap

Create a repo with both code/docs and metadata, not just the remote shell.

## Workflow

1. Inspect local project files first.
   - Read `README.md` if present.
   - Read package metadata (`package.json`, `pyproject.toml`, etc.) if present.
   - Infer a short project summary and 3-5 relevant topics from the project itself.
2. Ensure these fields are set:
   - repository name
   - visibility (`public` or `private`)
   - description
   - homepage if available
   - topics
3. If information is missing, ask for only the missing decision that cannot be inferred safely.
4. Create or update the repo with GitHub CLI.
   - Create: `gh repo create ... --description ... [--homepage ...]`
   - Topics: `gh repo edit ... --add-topic ...`
5. Verify the result by reading back repo metadata with `gh repo view --json name,description,homepageUrl,repositoryTopics,url` or `gh api`.
6. If verification shows zero topics, do not declare success. Infer better topics, update the repo, and verify again. Only stop if there is a real blocker you can name.

## Rules

- Treat GitHub **About** as the combination of:
  - description
  - homepage / website
  - topics
- Do not stop after setting only description.
- Topics are mandatory by default.
- Prefer 3-5 concise lowercase topics.
- Avoid generic filler topics like `code`, `app`, or `project` unless they are truly useful.
- Keep the description to one sentence.
- If README is missing, create a minimal one before publishing.
- If the user says “fill the about section,” interpret that as description + homepage + topics.
- Treat an empty `repositoryTopics` result during verification as a failed task state, not a soft warning.

## Topic Heuristics

Derive topics from:
- primary language or framework
- deployment target or platform
- project type (`cli`, `library`, `automation`, `bot`, `tooling`, etc.)
- domain keywords from README

Good examples:
- `cli,github,automation`
- `typescript,react,chrome-extension`
- `python,fastapi,api`

## Commands

Create repo:

```bash
gh repo create <name> --public --description "<summary>"
```

Add homepage and topics:

```bash
gh repo edit <owner>/<repo> \
  --homepage "<url>" \
  --add-topic topic1 \
  --add-topic topic2 \
  --add-topic topic3
```

Verify:

```bash
gh repo view <owner>/<repo> --json name,description,homepageUrl,repositoryTopics,url
```

Verification passes only if `repositoryTopics` is non-empty.

## Resources

- Prompt templates: read `references/prompt-templates.md` when the user wants a reusable prompt for Codex, Claude, or another agent.
- Wrapper script: use `scripts/lazygithub.sh` when a single command is faster than repeated manual `gh` commands.
