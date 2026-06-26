# GitCode API Workflow Patterns

## First-run checklist

1. Install the SDK:

```bash
pip install -U gitcode-api
```

2. Export a token if you do not want to pass `api_key=` explicitly:

```bash
export GITCODE_ACCESS_TOKEN="your-token"
```

If the token is encrypted, pass `decrypt=` on the client so it can decode an
encrypted `api_key=` value or encrypted `GITCODE_ACCESS_TOKEN` at runtime.

3. Decide whether your task is repository-scoped.

- Repository-scoped: set `owner=` and `repo=` on the client for convenience.
- Account-wide: use `users`, `orgs`, `search`, or `oauth` without repository defaults.

4. Prefer context managers so the underlying `httpx` client closes cleanly, including a supplied `http_client=`.
5. If you need a runnable baseline, start from `examples/README.md` and the scripts in `examples/`.

## Pick the best reference

Use:

- [Project README](https://github.com/Trenza1ore/GitCode-API/blob/main/README.md) for overview and short common workflows
- [SDK quickstart](https://gitcode-api.readthedocs.io/en/latest/sdk/quickstart.html) for first-use SDK patterns
- [Client API](https://gitcode-api.readthedocs.io/en/latest/sdk/client_api.html) when you need exact chained method coverage
- [REST API index](https://gitcode-api.readthedocs.io/en/latest/rest_api/index.html) when you need endpoint-level REST behavior
- `references/api-reference.md` when a compact skill-local summary is enough

If you are editing the repository itself, the same content lives under `docs/sdk/` and `docs/rest_api/` as Sphinx sources.

## Picking the client

Use `GitCode` when:

- the surrounding code is synchronous
- you want the simplest script or REPL flow

Use `AsyncGitCode` when:

- the surrounding code already uses `asyncio`
- you need to integrate into an async service or worker

Keep the same resource names across both forms. Only the calling style changes:

- sync: `client.pulls.list(...)`
- async: `await client.pulls.list(...)`

## OpenAI-style mental model

Think in the same shape as modern API SDKs that expose resource groups on the client:

1. Create one root client
2. Pick a resource group (for example `client.repos`, `client.pulls`)
3. Call an action method
4. Work with the returned object

Example:

```python
from gitcode_api import GitCode

with GitCode(owner="SushiNinja", repo="GitCode-API") as client:
    repo = client.repos.get()
    pulls = client.pulls.list(state="open")
    print(repo.full_name)
    print(len(pulls))
```

## Common decision rules

- Need repository metadata, branches, commits, contents, issues, or pull requests:
  create the client with `owner=` and `repo=` up front.
- Need current-user, organization, search, or OAuth actions:
  start with `GitCode()` or `AsyncGitCode()` and only add repo context if a later call needs it.
- Need a quick demo or smoke test:
  prefer `examples/`, the built-in [`gitcode-api` CLI](https://gitcode-api.readthedocs.io/en/latest/sdk/cli.html), or `python scripts/check_env.py` before writing fresh code.
- Need plain JSON-like data for another tool:
  call `.to_dict()` on response objects.

## Common tasks

### Inspect a repository

```python
from gitcode_api import GitCode

with GitCode(owner="SushiNinja", repo="GitCode-API") as client:
    repo = client.repos.get()
    branches = client.branches.list(per_page=5)
    commits = client.commits.list(per_page=5)
```

Closest runnable example: `examples/get_repository_overview.py`

### List pull requests

```python
from gitcode_api import GitCode

with GitCode(owner="SushiNinja", repo="GitCode-API") as client:
    pulls = client.pulls.list(state="open", per_page=20)
    for pull in pulls:
        print(pull.number, pull.title, pull.source_branch, pull.target_branch)
```

Closest runnable example: `examples/list_pull_requests.py`

### Search repositories

```python
from gitcode_api import GitCode

with GitCode() as client:
    repos = client.search.repositories(q="sdk language:python", per_page=10)
    for repo in repos:
        print(repo.full_name)
```

### Get the authenticated user

```python
from gitcode_api import GitCode

with GitCode() as client:
    user = client.users.me()
    print(user.login)
```

Closest runnable example: `examples/get_current_user.py`

### Async branch listing

```python
import asyncio
from gitcode_api import AsyncGitCode


async def main() -> None:
    async with AsyncGitCode(owner="SushiNinja", repo="GitCode-API") as client:
        branches = await client.branches.list(per_page=5)
        for branch in branches:
            print(branch.name)


asyncio.run(main())
```

Closest runnable example: `examples/async_list_branches.py`

## Troubleshooting

### Missing token

Symptom:

- `GitCodeConfigurationError` during client creation

Fix:

- pass `api_key="..."`, or
- export `GITCODE_ACCESS_TOKEN`
- if the stored token is encrypted, pass `decrypt=...`

### Missing repository context

Symptom:

- `GitCodeConfigurationError` when calling `branches`, `commits`, `repos`, `contents`, `issues`, `pulls`, or related repository methods

Fix:

- set `owner=` and `repo=` on the client, or
- pass `owner=` and `repo=` to the specific call

### HTTP errors

Symptom:

- `GitCodeHTTPStatusError`

Fix:

- inspect the status code and message
- confirm the endpoint supports the requested action
- confirm the token has permission for the resource
- verify repository identifiers and numeric IDs
- compare the intended call with the [Client API](https://gitcode-api.readthedocs.io/en/latest/sdk/client_api.html) page and the matching topic under [REST API](https://gitcode-api.readthedocs.io/en/latest/rest_api/index.html)

### Lifecycle issues

Symptom:

- warnings or leaked connections in long-running code

Fix:

- prefer `with GitCode(...) as client:`
- prefer `async with AsyncGitCode(...) as client:`
- remember that closing the SDK client also closes a supplied `http_client=`

## CLI helpers

Prefer the package's experimental built-in CLI ([documentation](https://gitcode-api.readthedocs.io/en/latest/sdk/cli.html)):

```bash
export GITCODE_ACCESS_TOKEN="your-token"
gitcode-api repos get --owner SushiNinja --repo GitCode-API
gitcode-api pulls list --owner SushiNinja --repo GitCode-API --state open --per-page 10
gitcode-api search repositories --q "sdk language:python" --per-page 10
```

Environment validation (bundled skill script):

```bash
python scripts/check_env.py
```

The legacy `scripts/gitcode_api_cli.py` remains for backward compatibility but emits a `DeprecationWarning` directing you to the built-in CLI above.

## Practical debugging order

1. Run `python scripts/check_env.py`.
2. If the task is repository-scoped, confirm `owner` and `repo` are set either on the client or on the call.
3. Reproduce with the smallest relevant example from `examples/` or the `gitcode-api` CLI.
4. If the method name is unclear, check the [Client API](https://gitcode-api.readthedocs.io/en/latest/sdk/client_api.html) documentation.
5. If behavior still looks wrong, compare with the mirrored REST docs under the [REST API](https://gitcode-api.readthedocs.io/en/latest/rest_api/index.html) section.
