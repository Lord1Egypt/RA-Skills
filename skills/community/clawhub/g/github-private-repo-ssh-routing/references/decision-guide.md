# Decision Guide

Use this file when deciding which GitHub identity model fits the machine.

## 1. Deploy key

Best when:

- one machine touches one private repo
- the workflow is narrow and automated
- least privilege matters more than convenience

Pros:

- repo-scoped permission
- small blast radius
- easy to revoke per repo

Cons:

- one key cannot be reused as a deploy key across multiple repos
- many repos means many aliases and more routing overhead

Choose this when the repo is a backup target, plugin repo, or single-purpose automation repo.

## 2. Personal SSH key

Best when:

- a human developer is actively working across many repos
- convenience matters more than strict repo isolation
- the machine is a personal workstation, not a shared automation host

Pros:

- simple multi-repo workflow
- less alias overhead

Cons:

- broader permissions
- weaker separation between repos
- less ideal for unattended automation

## 3. Machine user

Best when:

- one machine needs access to many private repos
- unattended automation is expected across many repos
- deploy-key-per-repo overhead is becoming a burden

Pros:

- more scalable than many deploy keys
- clean for dedicated automation hosts

Cons:

- broader access than per-repo deploy keys
- requires account-level governance

## Fast choice

- One repo, one purpose, one automation path -> deploy key
- One person, many repos, local dev workflow -> personal SSH key
- One server, many repos, long-lived automation -> machine user
