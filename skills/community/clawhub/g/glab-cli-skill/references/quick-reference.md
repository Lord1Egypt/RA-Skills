# glab Quick Reference

Verified against `glab 1.90.0`.

## Preflight

```bash
glab --version
glab auth status
git remote -v
```

## Authentication and Context

```bash
glab auth login
glab auth login --hostname gitlab.example.org
glab auth status
glab repo view group/project
glab mr list -R group/project
```

## Merge Requests

```bash
glab mr list --reviewer=@me --output json
glab mr list --source-branch="$(git branch --show-current)"
glab mr checkout 123
glab mr view 123 --comments
glab mr create -t "Fix bug" -d "Fixes #123" --reviewer alice,bob -l bug
glab mr create --related-issue 123 --fill --yes
glab mr update 123 --ready
glab mr note 123 -m "Please update tests"
glab mr merge 123 --auto-merge
```

## Issues

```bash
glab issue list --assignee=@me -O json
glab issue view 456 --comments
glab issue create -t "Bug in login" -l bug -d "Steps to reproduce"
glab issue update 456 --label "bug,confirmed"
glab issue close 456
glab issue reopen 456
```

## CI/CD

```bash
glab ci list -s failed -F json
glab ci status --live
glab pipeline ci view -b main
glab ci view -p 123
glab ci trace lint
glab ci run -b main --variables DEPLOY_ENV:staging
glab ci run -b main --variables-file CONFIG_JSON:config.json
glab ci run -b main --variables-from variables.json
glab ci retry lint
glab ci cancel pipeline 123
glab ci cancel job 456
```

## Repository

```bash
glab repo view
glab repo view group/project --output json
glab repo clone gitlab-org/cli -- --branch main --depth 1
glab repo fork namespace/repo --clone
```

## API

```bash
glab api projects/:fullpath/releases
glab api "projects/:id/jobs?per_page=100" --paginate --output ndjson
glab api graphql -f query='query { currentUser { username } }'
```

## Notes

- `glab mr view 123` already renders in the terminal. Use `--web` only when the browser is the goal.
- `glab mr create --related-issue 123` is the supported issue-linking form. Do not pass the issue IID positionally.
- `glab mr create --fill` sets `push` to true. Confirm the current branch, remote, and pending changes before using `--fill --yes`.
- `glab ci retry` retries jobs, not whole pipelines.
- `glab ci cancel` uses subcommands: `pipeline <id>` or `job <id>`.
- `glab issue close` does not accept a comment flag.
