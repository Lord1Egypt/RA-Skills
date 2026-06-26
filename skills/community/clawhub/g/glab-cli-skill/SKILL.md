---
name: glab-cli
description: Guidance for using the GitLab CLI (`glab`) from the terminal for merge requests, issues, CI/CD pipelines and jobs, repository targeting and inspection, clone and fork workflows, self-hosted GitLab instances, and direct GitLab REST or GraphQL API calls.
---

# GitLab CLI (glab) Skill

Use `glab` when the user wants to operate on GitLab from the terminal. These instructions are verified against `glab 1.90.0`.

This hot path is intentionally narrow: merge requests, issues, CI/CD, repo targeting, repo view/clone/fork, and `glab api`. Broader project administration should only be documented through a dedicated reference file.

## When to Use

Invoke this skill when the user needs to:
- Create, review, update, merge, or inspect merge requests
- Create, inspect, or update issues
- Check, run, retry, cancel, or inspect CI/CD pipelines and jobs
- Target a repository explicitly, or view, clone, or fork it
- Work with self-hosted GitLab instances
- Make direct GitLab REST or GraphQL API calls with `glab api`

## Preflight

Run these checks before doing real work:

```bash
glab --version
glab auth status
git remote -v
```

If not inside a Git repository, do not guess context. Use one of these patterns instead:

```bash
glab mr list -R group/project
glab issue list -R group/project
glab repo view group/project
glab repo view https://gitlab.example.org/group/project.git
```

For self-hosted GitLab, set the host explicitly when needed:

```bash
glab auth login --hostname gitlab.example.org
GITLAB_HOST=gitlab.example.org glab repo view group/project
glab api --hostname gitlab.example.org projects/:id
```

## Execution Policy

- Prefer read-only commands first: `list`, `view`, `status`, `trace`.
- Prefer structured output when the user wants filtering or automation:
  - `--output json` for `mr`, `ci`, and `repo` commands
  - `-O json` for `issue list`
  - `--output ndjson` for large `glab api --paginate` responses piped to `jq`
- Before remote mutations, confirm the repository, target object, and branch. This matters for `mr create`, `mr merge`, `mr close`, `issue close`, `ci run`, `ci retry`, `ci cancel`, `ci delete`, and `repo fork` commands.
- If `glab auth status` shows missing or invalid credentials, stop and ask the user to authenticate instead of retrying failing API calls.
- Use `glab <command> --help` before guessing flags. CLI behavior changes across releases.
- For `glab api`, pagination belongs in the endpoint query string. Example:

```bash
glab api "projects/:id/jobs?per_page=100" --paginate --output ndjson
```

## Common Workflows

### Merge Requests

```bash
glab mr list --reviewer=@me --output json
glab mr checkout 123
glab mr view 123 --comments
glab mr create -t "Add feature" -d "Implements X" --reviewer alice,bob -l feature
glab mr create --related-issue 123 --fill --yes
glab mr update 123 --ready
glab mr note 123 -m "Please add tests"
glab mr merge 123 --auto-merge
```

`glab mr create --fill` sets `push` to true. Confirm `git status`, the current branch, and the target remote before using `--fill --yes`.

### Issues

```bash
glab issue list --assignee=@me -O json
glab issue view 456 --comments
glab issue create -t "Bug in login" -l bug -d "Steps to reproduce"
glab issue update 456 --label "bug,confirmed"
glab issue close 456
```

### CI/CD

```bash
glab ci list -s failed -F json
glab ci status --live
glab pipeline ci view -b main
glab ci trace lint
glab ci run -b main --variables DEPLOY_ENV:staging
glab ci retry lint
glab ci cancel pipeline 123
```

## References

Load only the smallest file that matches the task:

- `references/quick-reference.md` for a short cheat sheet
- `references/auth.md` for authentication, repo context, self-hosted hosts, and 401/403/404 errors
- `references/merge-requests.md` for MR workflows, comments, merge strategies, and MR-specific failures
- `references/issues.md` for issue creation, editing, linking, and issue-specific failures
- `references/ci.md` for pipeline and job inspection, reruns, cancelation, variables, and CI failures
- `references/api.md` for `glab api`, pagination, GraphQL, and automation patterns

Load a reference only when the task needs deeper flags, examples, or troubleshooting than this file provides.
