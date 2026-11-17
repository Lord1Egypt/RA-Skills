---
name: private-github-repo-upload
description: "Safely initialize, sanitize, commit, create, and push a local project with private runtime data to a separate private GitHub repository. Use when the user asks to back up or upload a local data-bearing project to a private GitHub repo while keeping public Skills separate. Never uploads credentials, environments, caches, or public Skill source."
description_zh: "安全上传私有项目到 GitHub"
description_en: "Secure private GitHub upload"
version: "1.1.0"
disable: false
agent_created: true
read_when:
  - "上传本地项目到 GitHub 私有仓库"
  - "建立私人库并和公开 Skill 分开"
  - "push a data-bearing local project to a private GitHub repository"
  - "backup a private runtime project without exposing secrets"
not_for:
  - "publishing a public Skill"
  - "uploading credentials or a whole home directory"
  - "force-pushing or rewriting an existing remote repository without explicit approval"
---

# Private GitHub Repository Upload

Use this as a fixed, auditable workflow. It is a Workflow, not an autonomous discovery agent: project scope, exclusion policy, and repository name must be explicit or use a documented default confirmed by the user.

## Workflow

### Step 1: [Deterministic] Confirm scope
- Identify the exact local project directory.
- Identify the GitHub owner and repository name.
- Confirm the repository is private.
- Treat private strategy state, portfolio state, risk state, reports, and historical snapshots as uploadable only when the user explicitly approves a data-bearing private backup.
- Keep public Skill directories outside the private repository unless the user explicitly asks for a separate copy.

### Step 2: [Deterministic] Inspect and define exclusions
- Verify the project directory exists and is not a broad personal directory.
- Read any existing `.gitignore` before modifying it; create one when absent.
- **Whitelist variant (mixed workspace)**: when the project sits inside a workspace that also holds unrelated personal material (e.g. legal, health, or family documents that must never be tracked), ignore everything by default and negate only allowed paths. Three gotchas: start with `/*` (not `*`); always include `!/.gitignore` itself (easy to miss — `git add .gitignore` then fails with "paths are ignored"); and for nested paths re-include each parent directory before its children (`!/.workbuddy` → `.workbuddy/*` → `!/.workbuddy/build` → `.workbuddy/build/*` → `!/.workbuddy/build/*.py`). The whitelist also protects future files dropped at the root from being tracked by accident.
- Exclude local environments, bytecode, IDE state, temporary files, rebuildable output, machine-local WorkBuddy memory/automation state, backups, credential files, private keys, API keys, and `.env` files.
- Keep the exclusion list narrow enough that approved strategy and research data remain available.

### Step 3: [Deterministic] Initialize and stage safely
- Initialize a local repository with the intended default branch, for example `git init -b main`.
- Stage only after the ignore rules are in place.
- Inspect the staged manifest, file count, and total size.
- Scan staged text for GitHub tokens, bearer tokens, private keys, API keys, passwords, webhook secrets, and unexpected absolute credential paths.
- Run `git diff --cached --check`; existing whitespace warnings are reportable but are not a reason to alter historical material merely for upload.

### Step 4: [Deterministic] Commit locally
- Set a local Git identity only if needed; do not change global identity.
- Create one descriptive initial commit.
- **Stage paths explicitly, one `git add` per logical group, and never pass a gitignored path.** `git add -A <path> <gitignored-path>` exits non-zero, so in an `&&` chain the `git commit` never runs.
- **Verify with `git log -1` that the commit actually exists before pushing.** Do not assume a chained `git commit` succeeded. A commit that silently did not happen leaves HEAD at the previous SHA, and Step 6B will then faithfully replicate that stale HEAD as a spurious empty commit on the remote (identical tree and message, different SHA, `files: []`).
- Verify the commit SHA and that the working tree is clean.
- Do not push until the local commit and staged manifest pass inspection.

### Step 5: [Deterministic] Create or reuse the private remote
- Read the configured GitHub PAT from the approved secure credential source or environment variable without printing it.
- Authenticate with the GitHub REST API and verify the authenticated account.
- Look up the target repository before creating it.
- If lookup returns 404, create it with `private: true`.
- If creation returns 422 because the name already exists, retry by listing the authenticated owner’s repositories and verify the exact repository, privacy, and owner before continuing.
- On a network/API failure, retry once or twice and cross-check with an independent client before reporting an environment failure.

### Step 6: [Deterministic] Push without persisting credentials
- Add or set a credential-free `origin` URL.
- Push with a non-persistent credential mechanism such as `GIT_ASKPASS` or an approved credential helper; do not put the PAT in a remote URL, command argument, shell history, script, or repository.
- Push the intended branch only. Do not force-push.
- **If `git push` hangs with no output** (reproduced repeatedly on Windows/Git Bash behind a proxy): abort it and fall back to Step 6B. Do not keep retrying the same hanging command, and do not report it as a network failure without trying the API path.

### Step 6B: [Deterministic] Manual push via the Git Data API
Use `git/blobs` → `git/trees` → `git/commits` → `PATCH git/refs/heads/<branch>` to advance the remote. Four constraints are mandatory; violating any of them produces a silently divergent history rather than an error:

1. **`base_tree` must be the REMOTE commit's tree.** A local tree oid does not exist on the remote and returns `422 base_tree is not a valid tree oid`.
2. **Pass the local commit's full `author`/`committer` metadata, with the local UTC offset preserved.** GitHub writes the date as `+0000` when omitted. If the local commit is `+0800`, the commit objects differ byte-for-byte and the remote SHA diverges from the local one — the histories look equivalent (identical tree) but fork permanently. Convert git raw `1788157141 +0800` to local wall-clock ISO `2026-08-31T14:19:01+08:00`.
3. **Extract the message with `git cat-file commit HEAD`** and take everything after the first blank line. `git log -1 --format=%B` plus `.trim()` drops the trailing newline and changes the SHA.
4. **Read changed files with `git -c core.quotePath=false diff-tree ...`.** Without it, CJK paths are escaped to `"reports/601985_\345\255\243..."` and `fs.existsSync` fails on every one of them.

After creating the commit, assert `remote_commit.sha === local_head_sha` before advancing the ref. If they differ, do not push — fix the metadata first.

If a divergent commit was already pushed, recover in this order: (a) rebuild the remote commit locally from API metadata and `git reset --soft` to it; (b) only if that fails, `ROLLBACK=<last-good-sha>` with `force: true` to undo a commit that you yourself created minutes earlier and that nobody else is based on. Never force-reset over someone else's history.

### Step 7: [Deterministic] Verify remote state
- Read the remote branch SHA and compare it with the local commit SHA. **Get the remote SHA from the API (`GET /repos/{owner}/{repo}/branches/main`), not `git ls-remote`**: a private repo makes ls-remote require authentication too, and without the same askpass/credential setup used for the push it silently waits on a username/password prompt and hangs (auto-backgrounding, no error). The push itself having succeeded does not make a later bare ls-remote safe.
- Verify the repository is private, the owner and repository name are correct, and the default branch is correct.
- Verify the local working tree is clean and the configured `origin` URL contains no credential.
- Report the exact uploaded scope and exclusions.
- **For gitignored private files (risk-state.json, portfolio-state.json, etc.), verify the CONTENT actually reached the remote — a `files: []` on the created commit is a known false signal, not proof of an empty push.** Do not trust `git hash-object` for this: Git normalizes line endings (CRLF/LF) before hashing the working-tree file, so the local `git hash-object` SHA almost always differs from the remote blob SHA even when the bytes are identical. Instead verify one of two ways:
  1. **Raw-byte blob SHA**: compute `sha1("blob " + byteLength + "\0" + rawFileBytes)` in Node/Python on the local file, and compare it to the `sha` of that path's entry in the remote `git/trees/<sha>?recursive=1`. If they match, the file is byte-identical on the remote.
  2. **Contents API decode**: `GET /repos/{owner}/{repo}/contents/<path>?ref=<remote-sha>`, base64-decode `content`, and compare to the local file bytes (or grep for a known unique substring). This is the most reliable end-to-end check.
  - Do NOT conclude a gitignored file is "missing/lost" from a `git hash-object` mismatch alone. Confirm with method 1 or 2 before re-pushing.

## Hard Rules

1. Public Skills and private runtime data remain separate repositories.
2. Never commit or print GitHub, Notion, webhook, cloud, database, or other credentials.
3. Never upload a home directory, Desktop, Downloads, Documents, or broad personal directory as a project.
4. Never use `git add` before the exclusion policy is established and inspected.
5. Never use force-push, destructive reset, or remote deletion in this workflow.
6. Private repository status must be verified through the authenticated API; a successful push alone is not proof of privacy.
7. A 404/422 or network error must not be treated as a final diagnosis after one request; retry and cross-check first.
8. If the staged scan finds a real secret, stop the upload, remove it from the index and history before any push, and rotate the exposed credential when applicable.

## Pitfalls

- A private repository may return 404 from a direct repository lookup while still appearing in the authenticated owner repository list; treat a 422 name conflict as an identity/visibility lookup problem and cross-check the owner list.
- A credential embedded in a push URL can leak through process arguments, logs, or copied commands even when the remote URL is later reset; use an ephemeral credential channel instead.
- `git diff --cached --check` may report historical trailing whitespace; do not rewrite old reports solely to make the initial backup cosmetically clean.
- A script that imports a public Skill from a sibling directory will not be portable after cloning; report the dependency rather than copying public Skill source into the private repository.
- `git push` can hang indefinitely rather than failing, and the harness may auto-background and then kill it. A hang is not a permission or network verdict; switch to the Git Data API instead of reporting an environment failure.
- A remote commit created through the API can carry an identical tree but a different SHA than the local commit when dates or the message trailing newline differ. Identical trees prove content equality; only a matching commit SHA proves history alignment. Always check the SHA.
- `git diff-tree --name-only` applies `core.quotePath` escaping to non-ASCII paths. This fails silently on Windows with CJK filenames — the file simply appears deleted and gets skipped, producing a commit that is missing files without any error.
- `PATCH /git/refs/heads/<branch>` rejects non-fast-forward updates with `422 Update is not a fast forward`. Undoing a bad commit needs `force: true`, which is exactly the operation Hard Rule 5 forbids, so the correct remedy is to avoid creating the bad commit by validating metadata first.
- **A chained `git commit` can silently not happen, and the push script will then create a spurious empty commit.** `git add -A <good-path> <gitignored-path>` exits non-zero ("The following paths are ignored by one of your .gitignore files"), which short-circuits the `&&` chain, so `git commit` never runs. The push helper still reads `HEAD`, finds the previous commit, and replicates it as a new remote commit with the same tree and message but a different SHA and `files: []`. Detect it by running `git log -1` before pushing and confirming the printed SHA matches the new commit; recover with `ROLLBACK=<previous-sha>` and then commit and push properly. Never chain "add && commit && push" without verifying the commit landed.
- **`git hash-object` lies about gitignored private-file sync because of CRLF normalization.** Git applies the repo's line-ending policy (e.g. `core.autocrlf` / `.gitattributes`) when hashing the working-tree file, so `git hash-object <file>` yields a different SHA than the raw bytes actually stored in the remote blob — even when local and remote are byte-identical. Symptom: `git hash-object` shows local `ce50…` ≠ remote tree `070b…`, but the file is in fact synced. Verify with the raw-byte blob SHA (Node `crypto`: `sha1("blob "+len+"\0"+bytes)`) or a contents-API decode instead. Never treat a `git hash-object` mismatch as evidence that a private file failed to upload.

## Failure Handling

| Scenario | Action |
|---|---|
| Project path is missing or too broad | Stop and request an exact project path |
| User did not approve private data upload | Stage code and non-sensitive research material only; keep runtime state local |
| Secret pattern or credential file is staged | Stop; fix ignore rules and unstage it; do not push |
| Repository lookup is 404 | Create the repository as private, then verify it |
| Creation is 422 name-already-exists | List the authenticated owner repositories and reuse only the exact private target |
| API call fails once | Retry and cross-check with another client before assigning blame to network or permissions |
| Push fails | Keep the local commit; inspect URL, branch, token scope, and remote state; never force-push as a shortcut |
| Push hangs with no output | Abort and switch to Step 6B (Git Data API); a hang is not evidence of a network or permission problem |
| API commit SHA differs from local HEAD | Do not advance the ref. Check the UTC offset in author/committer dates and the trailing newline in the message, then recreate |
| Ref update returns 422 not-a-fast-forward | Never force over unknown history. If the bad commit is your own and unshared, use the documented ROLLBACK path; otherwise stop and report |
| Remote SHA differs | Stop and report; do not overwrite remote history automatically |

## Output Format

Return a concise completion record containing:
- Local project path
- Remote repository URL
- Privacy and default-branch verification
- Local and remote commit SHA comparison
- Uploaded top-level scopes and sensitive/runtime exclusions
- Whether the local working tree is clean
- Any unresolved portability issue, such as a dependency on a public Skill outside the repository
