---
name: gitlab
description: Interact with GitLab API for managing projects, issues, merge requests, branches, pipelines, users, groups, and more. Use when the user needs to perform GitLab operations like creating issues, reviewing merge requests, managing branches, or querying project data via the GitLab REST API.
allowed-tools: Bash(gitlab-client:*)
---

# GitLab API Skill

Node.js client for the GitLab REST API (v4). Reads config from `./.env`.

## Security Rules

- **NEVER** read, cat, print, grep, or expose the `GITLAB_TOKEN` value.
- **NEVER** use `curl`, `wget`, or any tool to call GitLab API directly. All access MUST go through `gitlab-client`.
- AI may read/write `.env` to manage `GITLAB_URL`, but **GITLAB_TOKEN must be set by the user manually**.

## Setup

Requires `./.env` with:

```
GITLAB_URL=https://gitlab.fullnine.com.cn
GITLAB_TOKEN=<your-personal-access-token>
```

If token is missing, prompt the user to edit `./.env` and create a token at `<GITLAB_URL>/-/profile/personal_access_tokens` (scope: `api`).

Install (first time): `source ~/.nvm/nvm.sh && npm install`

## Quick Start

```bash
gitlab-client users me                                    # Current user
gitlab-client projects list --owned                       # My projects
gitlab-client issues list --project 42 --state opened     # Project issues
gitlab-client mrs create --project 42 --source-branch feat --target-branch main --title "My MR"
```

## Commands Reference

Format: `gitlab-client <resource> <action> [id] [--key value ...]`

All list actions support `--page N --per-page N` (default 20, max 100).

### Projects

| Action | Usage | Options |
|--------|-------|---------|
| list | `projects list` | `--search --owned --membership --visibility` |
| get | `projects get <id>` | |
| search | `projects search "term"` | |
| create | `projects create --name "name"` | `--description --visibility --namespace-id --initialize-with-readme` |
| edit | `projects edit <id>` | `--name --description --visibility` |
| delete | `projects delete <id>` | |
| fork | `projects fork <id>` | `--namespace` |
| members | `projects members <id>` | |
| hooks | `projects hooks <id>` | |

### Issues

| Action | Usage | Options |
|--------|-------|---------|
| list | `issues list --project <id>` | `--state --labels --milestone --assignee-id --search` |
| get | `issues get --project <id> --iid <iid>` | |
| create | `issues create --project <id> --title "T"` | `--description --labels --assignee-ids --milestone-id --due-date --confidential` |
| edit | `issues edit --project <id> --iid <iid>` | `--title --description --state-event --labels --assignee-ids` |
| close | `issues close --project <id> --iid <iid>` | |
| reopen | `issues reopen --project <id> --iid <iid>` | |
| delete | `issues delete --project <id> --iid <iid>` | |
| notes | `issues notes --project <id> --iid <iid>` | |
| add-note | `issues add-note --project <id> --iid <iid> --body "text"` | |

### Merge Requests

| Action | Usage | Options |
|--------|-------|---------|
| list | `mrs list --project <id>` | `--state --labels --milestone --source-branch --target-branch --search` |
| get | `mrs get --project <id> --iid <iid>` | |
| create | `mrs create --project <id> --source-branch "src" --target-branch "tgt" --title "T"` | `--description --assignee-id --reviewer-ids --labels --milestone-id --remove-source-branch --squash` |
| edit | `mrs edit --project <id> --iid <iid>` | `--title --description --state-event --labels --assignee-id` |
| merge | `mrs merge --project <id> --iid <iid>` | `--merge-commit-message --squash --should-remove-source-branch` |
| changes | `mrs changes --project <id> --iid <iid>` | |
| commits | `mrs commits --project <id> --iid <iid>` | |
| notes | `mrs notes --project <id> --iid <iid>` | |
| add-note | `mrs add-note --project <id> --iid <iid> --body "text"` | |
| approve | `mrs approve --project <id> --iid <iid>` | |
| pipelines | `mrs pipelines --project <id> --iid <iid>` | |

### Branches

| Action | Usage | Options |
|--------|-------|---------|
| list | `branches list --project <id>` | `--search` |
| get | `branches get --project <id> --branch "name"` | |
| create | `branches create --project <id> --branch "name" --ref "main"` | |
| delete | `branches delete --project <id> --branch "name"` | |
| delete-merged | `branches delete-merged --project <id>` | |

### Commits

| Action | Usage | Options |
|--------|-------|---------|
| list | `commits list --project <id>` | `--ref-name --since --until --path` |
| get | `commits get --project <id> --sha "abc123"` | |
| diff | `commits diff --project <id> --sha "abc123"` | |
| comments | `commits comments --project <id> --sha "abc123"` | |
| add-comment | `commits add-comment --project <id> --sha "abc123" --note "text"` | |

### Repository / Files

| Action | Usage | Options |
|--------|-------|---------|
| tree | `repo tree --project <id>` | `--path --ref --recursive` |
| file | `repo file --project <id> --file-path "path"` | `--ref` |
| raw | `repo raw --project <id> --file-path "path"` | `--ref` |
| create-file | `repo create-file --project <id> --file-path "p" --branch "b" --content "c" --commit-message "m"` | |
| update-file | `repo update-file --project <id> --file-path "p" --branch "b" --content "c" --commit-message "m"` | |
| delete-file | `repo delete-file --project <id> --file-path "p" --branch "b" --commit-message "m"` | |
| compare | `repo compare --project <id> --from "main" --to "feat"` | |

### Pipelines

| Action | Usage | Options |
|--------|-------|---------|
| list | `pipelines list --project <id>` | `--status --ref` |
| get | `pipelines get --project <id> --pipeline-id <pid>` | |
| jobs | `pipelines jobs --project <id> --pipeline-id <pid>` | |
| job-log | `pipelines job-log --project <id> --job-id <jid>` | |
| retry | `pipelines retry --project <id> --pipeline-id <pid>` | |
| cancel | `pipelines cancel --project <id> --pipeline-id <pid>` | |
| create | `pipelines create --project <id> --ref "main"` | `--variables "K1=v1,K2=v2"` |

### Groups

| Action | Usage | Options |
|--------|-------|---------|
| list | `groups list` | `--search --owned` |
| get | `groups get <id>` | |
| projects | `groups projects <id>` | `--search` |
| members | `groups members <id>` | |
| issues | `groups issues <id>` | `--state` |
| mrs | `groups mrs <id>` | `--state` |

### Users

| Action | Usage |
|--------|-------|
| me | `users me` |
| list | `users list [--search "john"]` |
| get | `users get <id>` |
| projects | `users projects <id>` |

### Labels

| Action | Usage | Options |
|--------|-------|---------|
| list | `labels list --project <id>` | |
| create | `labels create --project <id> --name "bug" --color "#FF0000"` | `--description` |
| edit | `labels edit --project <id> --name "bug"` | `--new-name --color` |
| delete | `labels delete --project <id> --name "bug"` | |

### Milestones

| Action | Usage | Options |
|--------|-------|---------|
| list | `milestones list --project <id>` | `--state` |
| get | `milestones get --project <id> --milestone-id <mid>` | |
| create | `milestones create --project <id> --title "v1.0"` | `--description --due-date --start-date` |
| edit | `milestones edit --project <id> --milestone-id <mid>` | `--title --state-event` |
| delete | `milestones delete --project <id> --milestone-id <mid>` | |

### Tags & Releases

| Action | Usage | Options |
|--------|-------|---------|
| tags list | `tags list --project <id>` | `--search` |
| tags create | `tags create --project <id> --tag-name "v1.0" --ref "main"` | `--message` |
| tags delete | `tags delete --project <id> --tag-name "v1.0"` | |
| releases list | `releases list --project <id>` | |
| releases create | `releases create --project <id> --tag-name "v1.0" --name "R1"` | `--description` |

### Snippets

| Action | Usage | Options |
|--------|-------|---------|
| list | `snippets list --project <id>` | |
| get | `snippets get --project <id> --snippet-id <sid>` | |
| create | `snippets create --project <id> --title "T" --file-name "f" --content "c"` | `--visibility` |

### Search

| Action | Usage |
|--------|-------|
| global | `search global --scope <scope> --search "query"` |
| project | `search project --project <id> --scope <scope> --search "query"` |
| group | `search group --group <id> --scope <scope> --search "query"` |

Scopes — global: `projects|issues|merge_requests|milestones|snippet_titles|users`. Project: `issues|merge_requests|milestones|notes|wiki_blobs|commits|blobs`. Group: `projects|issues|merge_requests|milestones`.

### Runners

| Action | Usage | Options |
|--------|-------|---------|
| list | `runners list --project <id>` | |
| all | `runners all` | `--type --status` |

### Webhooks

| Action | Usage | Options |
|--------|-------|---------|
| list | `hooks list --project <id>` | |
| create | `hooks create --project <id> --url "url"` | `--push-events --merge-requests-events --issues-events --token` |
| delete | `hooks delete --project <id> --hook-id <hid>` | |

## Usage Notes

- **Auth**: Uses `PRIVATE-TOKEN` header. Scopes: `api` (full), `read_api` (read-only), `read_user`, `read_repository`.
- **Project ID**: Use numeric ID or URL-encoded path (`my-group%2Fmy-project`).
- **Output**: JSON. Pipe to `jq` for filtering: `gitlab-client projects list | jq '.[].name'`
- **Dates**: ISO 8601 format (`YYYY-MM-DDTHH:MM:SSZ`).
- **Labels**: Comma-separated: `--labels "bug,feature,urgent"`.
- **Errors**: `401` unauthorized, `403` forbidden, `404` not found, `422` validation, `429` rate limited.
