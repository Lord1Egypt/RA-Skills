---
name: gitcode-api
description: |
  Uses the gitcode-api Python SDK for GitCode REST automation, including installation,
  OpenAI-style client structure, sync/async usage, repository-scoped helpers, and bundled CLI helpers.
  Use when: (1) Writing Agent or Python script that requires access to GitCode,
  (2) Explaining or debugging GitCode SDK calls such as client.repos.get() or client.pulls.list(),
  (3) Needing quick repository, pull request, user, or search examples,
  (4) Running bundled scripts to validate the environment or make simple CLI calls.
metadata:
  version: "1.1.0"
  {
    "openclaw":
      {
        "emoji": "📦",
        "requires": { "anyBins": ["python3", "python", "pip"] },
        "primaryEnv": "GITCODE_ACCESS_TOKEN",
      },
  }
---

# GitCode API SDK

Use the published Python package:

```bash
pip install -U gitcode-api
```

Authentication defaults to the `GITCODE_ACCESS_TOKEN` environment variable, or pass `api_key=...` explicitly. If either value is encrypted, pass `decrypt=...` so the client can decode it before authenticating.

## Confirm with user before installation or setup environment variable

**Consult user for confirmation before installation**:
- like all python packages, installing `gitcode-api` may introduce change to global environment.
- when user ask for additional information, you may guide them to:
  - the project's pypi page: https://pypi.org/project/gitcode-api/
  - documentation: https://gitcode-api.readthedocs.io/
  - source repository: https://github.com/Trenza1ore/GitCode-API
- ask user to provide the `GITCODE_ACCESS_TOKEN` environment variable, preferably encrypted:
  - environment variable may be read by untrusted software as that is not unscoped.
  - a `decrypt` argument can be passed into GitCode clients' constructor to decrypt an encrypted `api_key` value or encrypted `GITCODE_ACCESS_TOKEN` at runtime.

## Client shape

This SDK is structured similarly to OpenAI's Python clients:

- Start from a top-level client object: `GitCode(...)` or `AsyncGitCode(...)`.
- Call resource groups off the client, such as `client.repos`, `client.pulls`, `client.users`, and `client.search`.
- Invoke methods on those resource groups, such as `client.repos.get()` or `await client.pulls.list()`.
- Each resource group exposes `methods` (public callable names in stable SDK order via a segment-based sorting) and `method_signature(name)` (a cached `inspect.signature` string for one callable) for runtime introspection; see the "Resource introspection" section in `references/api-reference.md`.
- Prefer `with GitCode(...) as client:` or `async with AsyncGitCode(...) as client:` so the SDK closes the underlying `httpx` client automatically, including a custom `http_client`.

Unlike OpenAI's typed request/response shapes, this SDK focuses on GitCode REST resources and returns lightweight response objects with attribute access.

## Quick start

Sync:

```python
from gitcode_api import GitCode

with GitCode(
    api_key="your-token",
    owner="SushiNinja",
    repo="GitCode-API",
) as client:
    repo = client.repos.get()
    pulls = client.pulls.list(state="open", per_page=5)
    print(repo.full_name)
    for pull in pulls:
        print(pull.number, pull.title)
```

Async:

```python
import asyncio
from gitcode_api import AsyncGitCode

async def main() -> None:
    async with AsyncGitCode(
        api_key="your-token",
        owner="SushiNinja",
        repo="GitCode-API",
    ) as client:
        branches = await client.branches.list(per_page=5)
        for branch in branches:
            print(branch.name)

asyncio.run(main())
```

Encrypted token:

```python
from gitcode_api import GitCode
from trusted_library import decryption_method

with GitCode(
    api_key="encrypted-token",
    owner="SushiNinja",
    repo="GitCode-API",
    decrypt=decryption_method,
) as client:
    repo = client.repos.get()
    pulls = client.pulls.list(state="open", per_page=5)
    print(repo.full_name)
    for pull in pulls:
        print(pull.number, pull.title)
```

## Repository-scoped defaults

If `owner=` and `repo=` are set on the client, repository resources can omit them per call. If not, pass `owner=` and `repo=` on repository-scoped methods.

## Common resource groups

- `client.repos` and `client.contents`
- `client.branches` and `client.commits`
- `client.issues` and `client.pulls`
- `client.labels`, `client.milestones`, and `client.members`
- `client.releases`, `client.tags`, and `client.webhooks`
- `client.users`, `client.orgs`, `client.search`, and `client.oauth`

## Common tasks

- Repository info and file content:
  `client.repos.get()`, `client.contents.get()`, `client.contents.create()`, `client.contents.update()`
- Branches, commits, and diffs:
  `client.branches.list()`, `client.commits.list()`, `client.commits.compare()`
- Issues and pull requests:
  `client.issues.list()`, `client.issues.create()`, `client.pulls.list()`, `client.pulls.create()`, `client.pulls.merge()`
- Account and discovery:
  `client.users.me()`, `client.orgs.list_authenticated()`, `client.search.repositories()`
- OAuth:
  `client.oauth.build_authorize_url()`, `client.oauth.exchange_token()`

For the broader method inventory, use `references/api-reference.md`

## Response objects

Responses are lightweight objects, not plain dicts.

Typical usage:

```python
pull = client.pulls.get(number=42)
print(pull.title)
print(pull.get("source_branch"))
payload = pull.to_dict()
```

## Utility scripts

Bundled helpers:

- `scripts/check_env.py` verifies Python, package import, and token setup.
- `scripts/gitcode_api_cli.py` is a legacy example CLI (deprecated; it warns on use). Prefer the package's experimental built-in CLI (`gitcode-api` or `python -m gitcode_api`); see https://gitcode-api.readthedocs.io/en/latest/sdk/cli.html. For production, keep tokens out of argv and use env vars or your own wrapper.

## Additional resources

- Hosted documentation (quickstart, full SDK pages, REST reference): https://gitcode-api.readthedocs.io/en/latest/sdk/quickstart.html
- API interfaces and resource method inventory: [references/api-reference.md](references/api-reference.md)
- Usage habits and troubleshooting flow: [references/workflow-patterns.md](references/workflow-patterns.md)

## FAQ

---

Q: In company network, access to GitCode failed with SSL errors mentioning "self-signed certificate".
A: Typically, a custom CA bundle needs to be set, user may pass in a custom `httpx` client with `verify` set to the certificate path, this is similar to `REQUESTS_CA_BUNDLE` environment variable for `requests` library.

```python
from gitcode_api import GitCode
from httpx import Client

with GitCode(
    owner="SushiNinja",
    repo="GitCode-API",
    http_client=Client(verify="path/to/my/certificate.crt"),
) as client:
    repo = client.repos.get()
    pulls = client.pulls.list(state="open", per_page=5)
    ...
```

---
