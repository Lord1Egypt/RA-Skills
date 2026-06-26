# Configuration

To keep the skill reusable and safe to open-source, do not hardcode secrets.

## Required

- GitCode token:
  - Path: `$HOME/.openclaw/workspace/data/gitcode-token.txt`
  - Header used: `PRIVATE-TOKEN: <token>`

## Repos

Configure using env vars (recommended):

- `REPO_OWNER` (default: `ExampleOrg`)
- `REPOS_CSV` (comma-separated repo names)

Example:

```bash
export REPO_OWNER="ExampleOrg"
export REPOS_CSV="example_repo_1,example_repo_2"
```

## Notifications

### DingTalk

```bash
export TARGET_DINGTALK="<your-dingtalk-target>"
```

### WeCom

This skill expects the `wecom-app` channel to be configured in `~/.openclaw/openclaw.json`.

```bash
export TARGET_WECOM="user:<wecom-userid>"
```

## Session reuse

The review session id is rotated daily per repo:

- `gitcode-pr-review-${owner}-${repo}-YYYYMMDD`

This improves cache hit rate while controlling session growth.
