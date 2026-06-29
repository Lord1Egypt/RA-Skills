# Command Safety

HAMMERRR is read-only by default.

## Allowed By Default

- file reads
- `rg`, `find`, `ls`, `sed`, `nl`, `wc`
- `git status`, `git log`, `git show`, `git diff`
- package metadata inspection
- test/build commands only when they are known not to mutate external state
- dry-run commands when the command help confirms they are non-mutating

## Stop Before Running

Stop and report before commands that may:

- install dependencies
- write outside the requested report outputs
- delete, reset, move, or rewrite files
- publish, deploy, push, commit, tag, release, or upload
- alter databases, queues, buckets, accounts, cloud resources, registries, or live services
- print secret values, cookies, tokens, private keys, or credentials

## Ledger

Every command in the final report should include:

- command
- working directory
- status: `passed`, `failed`, `blocked`, or `not_run`
- relevant output summary
- whether it mutated anything
