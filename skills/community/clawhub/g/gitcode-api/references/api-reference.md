# GitCode API Reference

Install:

```bash
pip install -U gitcode-api
```

Primary exports:

- `gitcode_api.GitCode`
- `gitcode_api.AsyncGitCode`
- `gitcode_api.GitCodeError`
- `gitcode_api.GitCodeConfigurationError`
- `gitcode_api.GitCodeAPIError`
- `gitcode_api.GitCodeHTTPStatusError`

Base transport defaults:

- Base URL: `https://api.gitcode.com/api/v5`
- Token env var: `GITCODE_ACCESS_TOKEN`
- Default timeout: `30.0`
- Transport: `httpx.Client` / `httpx.AsyncClient`

## Mental model

The SDK follows a top-level client with resource groups (for example `client.repos`, `client.pulls`):

```python
from gitcode_api import GitCode

client = GitCode(api_key="token", owner="owner", repo="repo")
repo = client.repos.get()
pulls = client.pulls.list(state="open")
user = client.users.me()
```

Async calls mirror the same shape:

```python
from gitcode_api import AsyncGitCode

client = AsyncGitCode(api_key="token", owner="owner", repo="repo")
pulls = await client.pulls.list(state="open")
```

Encrypted token example:

```python
from gitcode_api import GitCode
from trusted_library import decrypt_token

client = GitCode(
    api_key="encrypted-token",
    owner="owner",
    repo="repo",
    decrypt=decrypt_token,
)
```

## Top-level clients

### `GitCode`

Synchronous client with resource groups:

- `repos`
- `contents`
- `branches`
- `commits`
- `issues`
- `pulls`
- `labels`
- `milestones`
- `members`
- `releases`
- `tags`
- `webhooks`
- `users`
- `orgs`
- `search`
- `oauth`

Constructor:

```python
GitCode(
    api_key: str | None = None,
    owner: str | None = None,
    repo: str | None = None,
    base_url: str = "https://api.gitcode.com/api/v5",
    timeout: float | None = None,
    http_client=None,
    decrypt=None,
)
```

Lifecycle:

- Supports `with GitCode(...) as client:`
- Call `client.close()` if not using a context manager
- Closing the SDK client also closes a supplied `http_client`

### `AsyncGitCode`

Asynchronous mirror of `GitCode`.

Constructor:

```python
AsyncGitCode(
    api_key: str | None = None,
    owner: str | None = None,
    repo: str | None = None,
    base_url: str = "https://api.gitcode.com/api/v5",
    timeout: float | None = None,
    http_client=None,
    decrypt=None,
)
```

Lifecycle:

- Supports `async with AsyncGitCode(...) as client:`
- Call `await client.close()` if not using an async context manager
- Closing the SDK client also closes a supplied `http_client`

## Repository-scoped behavior

Many methods operate under `/repos/{owner}/{repo}`.

Use either:

1. Client defaults:

```python
client = GitCode(owner="SushiNinja", repo="GitCode-API")
branches = client.branches.list()
```

2. Per-call overrides:

```python
client = GitCode(api_key="token")
branches = client.branches.list(owner="SushiNinja", repo="GitCode-API")
```

If a repository-scoped method runs without an effective `owner` and `repo`, the SDK raises `GitCodeConfigurationError`.

## Resource introspection (`methods`, `method_signature`)

Each resource group (for example `client.pulls`, `client.repos`) subclasses the shared `SyncResource` or `AsyncResource` base.

### `methods`

A read-only `methods` property returns a `tuple[str, ...]` of **public callable** names in **stable SDK order** (Python `sorted` with a key derived from underscore-separated name segments). That order is **not** plain A–Z sorting on the full method string (for example two-part names are ordered as if `second_first`).

```python
names = client.pulls.methods
assert "list" in names
```

Details:

- Excludes names starting with `_`, the introspection helpers `methods` and `method_signature`, and any non-callable attributes.
- The tuple is computed on first access and cached for the lifetime of that resource instance (`functools.lru_cache` on the property), so repeated reads are cheap.

### `method_signature(method_name)`

`method_signature(name: str) -> str` returns the method name plus the formatted signature from `inspect.signature` for that callable on the resource group (type hints are shortened by stripping the internal `gitcode_api._models.` prefix). Results are cached (`functools.lru_cache`, up to 50 distinct names per instance).

```python
sig = client.pulls.method_signature("list_issues")
# e.g. list_issues(*, number: Union[int, str], owner: Optional[str] = None, ...) -> List[Issue]
```

Use `methods` for discovery and `method_signature` when you need parameters and return type for a specific method without opening the source or full manual.

## Resource groups and common methods

### Repositories and contents

- `client.repos.get()`
- `client.repos.list_user()`
- `client.repos.list_for_owner()`
- `client.repos.create_personal()`
- `client.repos.create_for_org()`
- `client.repos.update()`
- `client.repos.delete()`
- `client.repos.fork()`
- `client.repos.list_forks()`
- `client.repos.list_contributors()`
- `client.repos.list_languages()`
- `client.repos.list_stargazers()`
- `client.repos.list_subscribers()`
- `client.repos.update_module_settings()`
- `client.repos.update_reviewer_settings()`
- `client.repos.set_org_repo_status()`
- `client.repos.transfer_to_org()`
- `client.repos.get_transition()`
- `client.repos.update_transition()`
- `client.repos.update_push_config()`
- `client.repos.get_push_config()`
- `client.repos.upload_image()`
- `client.repos.upload_file()`
- `client.repos.update_repo_settings()`
- `client.repos.get_repo_settings()`
- `client.repos.get_pull_request_settings()`
- `client.repos.update_pull_request_settings()`
- `client.repos.set_member_role()`
- `client.repos.transfer()`
- `client.repos.list_customized_roles()`
- `client.repos.get_download_statistics()`
- `client.repos.get_contributor_statistics()`
- `client.repos.list_events()`

Contents helpers:

- `client.contents.get()`
- `client.contents.create()`
- `client.contents.update()`
- `client.contents.delete()`
- `client.contents.list_paths()`
- `client.contents.get_tree()`
- `client.contents.get_blob()`
- `client.contents.get_raw()`

### Branches and commits

- `client.branches.list()`
- `client.branches.get()`
- `client.branches.create()`
- `client.branches.list_protected()`

- `client.commits.list()`
- `client.commits.get()`
- `client.commits.compare()`
- `client.commits.list_comments()`
- `client.commits.get_comment()`
- `client.commits.create_comment()`
- `client.commits.update_comment()`
- `client.commits.delete_comment()`

### Issues and pull requests

- `client.issues.list()`
- `client.issues.get()`
- `client.issues.create()`
- `client.issues.update()`
- `client.issues.list_comments()`
- `client.issues.create_comment()`
- `client.issues.get_comment()`
- `client.issues.update_comment()`
- `client.issues.delete_comment()`
- `client.issues.list_pull_requests()`
- `client.issues.add_labels()`
- `client.issues.remove_label()`
- `client.issues.list_enterprise()`
- `client.issues.list_user()`
- `client.issues.list_org()`
- `client.issues.get_enterprise_issue()`
- `client.issues.list_enterprise_comments()`
- `client.issues.list_enterprise_labels()`
- `client.issues.list_operation_logs()`

- `client.pulls.list()`
- `client.pulls.get()`
- `client.pulls.create()`
- `client.pulls.update()`
- `client.pulls.merge()`
- `client.pulls.get_merge_status()`
- `client.pulls.list_commits()`
- `client.pulls.list_files()`
- `client.pulls.list_comments()`
- `client.pulls.create_comment()`
- `client.pulls.get_comment()`
- `client.pulls.update_comment()`
- `client.pulls.delete_comment()`
- `client.pulls.list_labels()`
- `client.pulls.add_labels()`
- `client.pulls.replace_labels()`
- `client.pulls.remove_label()`
- `client.pulls.request_review()`
- `client.pulls.list_operation_logs()`
- `client.pulls.request_test()`
- `client.pulls.update_testers()`
- `client.pulls.add_testers()`
- `client.pulls.update_assignees()`
- `client.pulls.add_assignees()`
- `client.pulls.remove_assignees()`
- `client.pulls.list_issues()`
- `client.pulls.list_enterprise()`
- `client.pulls.list_org()`
- `client.pulls.list_issue_pull_requests()`

### Collaboration metadata

- `client.labels.list()`
- `client.labels.create()`
- `client.labels.update()`
- `client.labels.delete()`
- `client.labels.clear_issue_labels()`
- `client.labels.replace_issue_labels()`
- `client.labels.list_enterprise()`

- `client.milestones.list()`
- `client.milestones.get()`
- `client.milestones.create()`
- `client.milestones.update()`
- `client.milestones.delete()`

- `client.members.add_or_update()`
- `client.members.remove()`
- `client.members.list()`
- `client.members.get()`
- `client.members.get_permission()`

### Users, orgs, search, and OAuth

- `client.users.get()`
- `client.users.me()`
- `client.users.list_emails()`
- `client.users.list_events()`
- `client.users.list_repos()`
- `client.users.create_key()`
- `client.users.list_keys()`
- `client.users.delete_key()`
- `client.users.get_key()`
- `client.users.get_namespace()`
- `client.users.list_starred()`

- `client.orgs.list_for_user()`
- `client.orgs.list_authenticated()`
- `client.orgs.get_member()`
- `client.orgs.get()`
- `client.orgs.list_repos()`
- `client.orgs.create_repo()`
- `client.orgs.get_enterprise_member()`
- `client.orgs.get_membership()`
- `client.orgs.list_members()`
- `client.orgs.list_enterprise_members()`
- `client.orgs.remove_member()`
- `client.orgs.list_followers()`
- `client.orgs.get_issue_extend_settings()`
- `client.orgs.invite_member()`
- `client.orgs.update_enterprise_member()`
- `client.orgs.update()`
- `client.orgs.leave()`

- `client.search.users()`
- `client.search.issues()`
- `client.search.repositories()`

- `client.oauth.build_authorize_url()`
- `client.oauth.exchange_token()`
- `client.oauth.refresh_token()`

### Releases, tags, and webhooks

- `client.releases.update()`
- `client.releases.get_by_tag()`
- `client.releases.list()`

- `client.tags.list()`
- `client.tags.create()`
- `client.tags.list_protected()`
- `client.tags.delete_protected()`
- `client.tags.get_protected()`
- `client.tags.create_protected()`
- `client.tags.update_protected()`

- `client.webhooks.list()`
- `client.webhooks.create()`
- `client.webhooks.get()`
- `client.webhooks.update()`
- `client.webhooks.delete()`
- `client.webhooks.test()`

## Response model habits

Responses are lightweight objects instead of raw dictionaries.

Typical usage:

```python
pull = client.pulls.get(number=42)
print(pull.title)
print(pull.get("source_branch"))
payload = pull.to_dict()
```

Practical guidance:

- Use attribute access for common fields
- Use `.get("field_name")` for optional fields
- Convert with `.to_dict()` when another tool expects plain JSON-like data

## Error handling

Common exceptions:

- `GitCodeConfigurationError` for missing token or missing repository context
- `GitCodeHTTPStatusError` for non-2xx responses
- `GitCodeAPIError` and `GitCodeError` for higher-level handling

Example:

```python
from gitcode_api import GitCode, GitCodeConfigurationError, GitCodeHTTPStatusError

try:
    with GitCode(owner="SushiNinja", repo="GitCode-API") as client:
        repo = client.repos.get()
        print(repo.full_name)
except GitCodeConfigurationError as exc:
    print(f"configuration error: {exc}")
except GitCodeHTTPStatusError as exc:
    print(f"http error: {exc.status_code} {exc}")
```
