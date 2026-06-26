# M*A*L*P Indexing States

A project-local `.malp/` can exist in one of three indexing states.

## 1. Active

Definition:
- the project has a `.malp/`
- that `.malp/` path appears in `~/.malp-home/MAP.txt`

Meaning:
- normal malp discovery may surface it
- it can be opened during ordinary active malp work

## 2. Attic

Definition:
- the project has a `.malp/` or an attic snapshot
- the relevant path appears in `~/.malp-home/attic/MAP.txt`
- it does not appear in active `~/.malp-home/MAP.txt`

Meaning:
- cold storage
- do not load during normal discovery or ordinary malp work unless the user explicitly asks for attic/archived/retired material

## 3. Unindexed

Definition:
- a project-local `.malp/` exists on disk
- its path is in neither active `~/.malp-home/MAP.txt` nor `~/.malp-home/attic/MAP.txt`

Meaning:
- unmanaged / unclassified
- not automatically active
- not automatically attic
- presence on disk alone is not permission to load it into context during normal malp discovery

## Default handling

Treat unindexed malps as a state to report, not a state to automatically open.

If the user asks for malp discovery in a scope where unindexed malps are found:
- present them separately from active malps
- label them clearly as unindexed
- ask the user why they think it is unindexed before proposing a change
- then ask whether it should become active, attic, or remain unindexed

Do not silently add an unindexed malp to either map.

Do not silently read an unindexed malp into context just because it exists.

## Suggested wording

- `Found 2 active malps and 1 unindexed malp.`
- `This path has a .malp on disk, but it is not registered in active MAP.txt or attic/MAP.txt.`
- `Do you know why this one is unindexed?`
- `Do you want to classify it as active, attic, or leave it unindexed?`
