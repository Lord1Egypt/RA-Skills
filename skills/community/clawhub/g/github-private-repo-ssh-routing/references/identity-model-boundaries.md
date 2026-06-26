# Identity Model Boundaries

Use this file when deciding whether a GitHub automation task should use a deploy key, a fine-grained personal access token (PAT), a personal SSH key, or a machine user.

## Core distinction

Treat these as two different layers:

- **Git/SSH access**: clone, fetch, pull, push, tag push
- **GitHub API actions**: list PRs, read checks, merge PRs, create releases, inspect workflow state

A deploy key solves the first layer only. Many automation tasks need both.

## Deploy key

Best when:

- one machine touches one private repo
- automation only needs Git transport
- least privilege matters most

Good fit for:

- backup repos
- mirror repos
- plugin/source sync repos
- tag push automation when no PR/release API calls are needed

Usually enough for:

- `git clone`
- `git fetch`
- `git pull`
- `git push`
- `git push --tags`

Usually **not** enough for:

- listing pull requests
- checking mergeability through GitHub API
- merging pull requests
- creating GitHub releases
- inspecting Actions/check-runs through API/CLI

## Fine-grained PAT

Best when:

- automation must act through GitHub API
- scope should stay limited to one repository
- the machine should not gain broad access to unrelated repos

Good fit for:

- dependency-update workflows
- PR triage bots
- auto-merge flows
- release creation workflows
- OpenClaw jobs that need to inspect PRs and merge them safely

Recommended when the task needs any of:

- PR listing/filtering
- CI/check status lookup
- merge actions
- release creation

Typical minimum permissions for one repo:

- **Contents**: Read and write
- **Pull requests**: Read and write
- **Metadata**: Read-only
- optionally **Actions**: Read-only when workflow/check inspection is needed

## Personal SSH key

Best when:

- a human developer uses one workstation across many repos
- convenience matters more than repo isolation

Not ideal for unattended automation with a strict blast-radius requirement.

## Machine user

Best when:

- one automation host needs many private repos
- repo-by-repo deploy-key routing is becoming too heavy
- account-level governance is acceptable

## Fast decision table

- **Only Git transport for one repo** -> deploy key
- **Need PR merge or release API actions** -> fine-grained PAT
- **Human developer workstation across many repos** -> personal SSH key
- **One automation host for many repos** -> machine user

## OpenClaw-specific guidance

For OpenClaw backup and SSH routing issues, deploy keys and SSH aliases are often the right answer.

For OpenClaw jobs that do any of the following:

- inspect pull requests
- decide whether a PR can merge
- merge a PR
- create a GitHub release

prefer a **fine-grained PAT** scoped to the single target repo.

## Safe mixed model

It is valid to use both:

- **deploy key** for Git remote transport
- **fine-grained PAT** for PR/release API operations

This is often the cleanest setup when a machine needs tight Git routing and limited GitHub API authority.
