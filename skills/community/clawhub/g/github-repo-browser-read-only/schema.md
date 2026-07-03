# GitHub Repo Browser - Read Only Schema

This generated reference belongs to the adjacent `SKILL.md`. Use it for exact action names, action slugs, parameter summaries, sample parameters, and generated JSON parameter schemas.

Product slug: `github-repo-browser-read-only`

x402 availability: not enabled for this product.

## `download_repo_to_storage`

Action slug: `download-repo-to-storage`

Price: `5` credits

Download a repository archive as a .tar.gz file and save it to file storage. Use ref to select a branch, tag, or commit. Use path to optionally filter to a specific subdirectory. Archives up to 100 MB are supported.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `owner` | `string` | yes | Repository owner. |
| `path` | `string` | no | Subdirectory to filter the archive to. Only files under this path will be included. |
| `ref` | `string` | no | Branch, tag, or commit SHA. Defaults to repository default branch. |
| `repo` | `string` | yes | Repository name. |
| `timeout_seconds` | `integer` | no | HTTP timeout in seconds. |

Sample parameters:

```json
{
  "owner": "example owner",
  "path": "example path",
  "ref": "example ref",
  "repo": "example repo",
  "timeout_seconds": 5
}
```

Generated JSON parameter schema:

```json
{
  "owner": {
    "description": "Repository owner.",
    "required": true,
    "type": "string"
  },
  "path": {
    "description": "Subdirectory to filter the archive to. Only files under this path will be included.",
    "required": false,
    "type": "string"
  },
  "ref": {
    "description": "Branch, tag, or commit SHA. Defaults to repository default branch.",
    "required": false,
    "type": "string"
  },
  "repo": {
    "description": "Repository name.",
    "required": true,
    "type": "string"
  },
  "timeout_seconds": {
    "description": "HTTP timeout in seconds.",
    "maximum": 120,
    "minimum": 5,
    "required": false,
    "type": "integer"
  }
}
```

## `download_to_storage`

Action slug: `download-to-storage`

Price: `5` credits

Download a single file from a GitHub repository and save it to file storage with SHA1 integrity verification. Returns a file_id and signed_url. Supports files up to 100 MB including binary files.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `owner` | `string` | yes | Repository owner. |
| `path` | `string` | yes | File path to download. |
| `ref` | `string` | no | Branch, tag, or commit SHA. Defaults to repository default branch. |
| `repo` | `string` | yes | Repository name. |
| `timeout_seconds` | `integer` | no | HTTP timeout in seconds. |

Sample parameters:

```json
{
  "owner": "example owner",
  "path": "example path",
  "ref": "example ref",
  "repo": "example repo",
  "timeout_seconds": 5
}
```

Generated JSON parameter schema:

```json
{
  "owner": {
    "description": "Repository owner.",
    "required": true,
    "type": "string"
  },
  "path": {
    "description": "File path to download.",
    "required": true,
    "type": "string"
  },
  "ref": {
    "description": "Branch, tag, or commit SHA. Defaults to repository default branch.",
    "required": false,
    "type": "string"
  },
  "repo": {
    "description": "Repository name.",
    "required": true,
    "type": "string"
  },
  "timeout_seconds": {
    "description": "HTTP timeout in seconds.",
    "maximum": 120,
    "minimum": 5,
    "required": false,
    "type": "integer"
  }
}
```

## `get_commit`

Action slug: `get-commit`

Price: `5` credits

Fetch a specific commit by SHA, including changed files and commit stats.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `commit_sha` | `string` | yes | Commit SHA to fetch. |
| `owner` | `string` | yes | Repository owner. |
| `repo` | `string` | yes | Repository name. |
| `timeout_seconds` | `integer` | no | HTTP timeout in seconds. |

Sample parameters:

```json
{
  "commit_sha": "example commit sha",
  "owner": "example owner",
  "repo": "example repo",
  "timeout_seconds": 5
}
```

Generated JSON parameter schema:

```json
{
  "commit_sha": {
    "description": "Commit SHA to fetch.",
    "required": true,
    "type": "string"
  },
  "owner": {
    "description": "Repository owner.",
    "required": true,
    "type": "string"
  },
  "repo": {
    "description": "Repository name.",
    "required": true,
    "type": "string"
  },
  "timeout_seconds": {
    "description": "HTTP timeout in seconds.",
    "maximum": 120,
    "minimum": 5,
    "required": false,
    "type": "integer"
  }
}
```

## `get_file`

Action slug: `get-file`

Price: `5` credits

Read a text file from a repository at a branch, tag, or commit. Binary and oversized files are rejected.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `owner` | `string` | yes | Repository owner. |
| `path` | `string` | yes | File path to read. |
| `ref` | `string` | no | Branch, tag, or commit SHA. Defaults to repository default branch. |
| `repo` | `string` | yes | Repository name. |
| `timeout_seconds` | `integer` | no | HTTP timeout in seconds. |

Sample parameters:

```json
{
  "owner": "example owner",
  "path": "example path",
  "ref": "example ref",
  "repo": "example repo",
  "timeout_seconds": 5
}
```

Generated JSON parameter schema:

```json
{
  "owner": {
    "description": "Repository owner.",
    "required": true,
    "type": "string"
  },
  "path": {
    "description": "File path to read.",
    "required": true,
    "type": "string"
  },
  "ref": {
    "description": "Branch, tag, or commit SHA. Defaults to repository default branch.",
    "required": false,
    "type": "string"
  },
  "repo": {
    "description": "Repository name.",
    "required": true,
    "type": "string"
  },
  "timeout_seconds": {
    "description": "HTTP timeout in seconds.",
    "maximum": 120,
    "minimum": 5,
    "required": false,
    "type": "integer"
  }
}
```

## `get_readme`

Action slug: `get-readme`

Price: `5` credits

Fetch the repository README content and metadata.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `owner` | `string` | yes | Repository owner. |
| `ref` | `string` | no | Branch, tag, or commit SHA. Defaults to repository default branch. |
| `repo` | `string` | yes | Repository name. |
| `timeout_seconds` | `integer` | no | HTTP timeout in seconds. |

Sample parameters:

```json
{
  "owner": "example owner",
  "ref": "example ref",
  "repo": "example repo",
  "timeout_seconds": 5
}
```

Generated JSON parameter schema:

```json
{
  "owner": {
    "description": "Repository owner.",
    "required": true,
    "type": "string"
  },
  "ref": {
    "description": "Branch, tag, or commit SHA. Defaults to repository default branch.",
    "required": false,
    "type": "string"
  },
  "repo": {
    "description": "Repository name.",
    "required": true,
    "type": "string"
  },
  "timeout_seconds": {
    "description": "HTTP timeout in seconds.",
    "maximum": 120,
    "minimum": 5,
    "required": false,
    "type": "integer"
  }
}
```

## `get_repo`

Action slug: `get-repo`

Price: `5` credits

Fetch repository metadata, default branch, permissions, and URLs.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `owner` | `string` | yes | Repository owner. |
| `repo` | `string` | yes | Repository name. |
| `timeout_seconds` | `integer` | no | HTTP timeout in seconds. |

Sample parameters:

```json
{
  "owner": "example owner",
  "repo": "example repo",
  "timeout_seconds": 5
}
```

Generated JSON parameter schema:

```json
{
  "owner": {
    "description": "Repository owner.",
    "required": true,
    "type": "string"
  },
  "repo": {
    "description": "Repository name.",
    "required": true,
    "type": "string"
  },
  "timeout_seconds": {
    "description": "HTTP timeout in seconds.",
    "maximum": 120,
    "minimum": 5,
    "required": false,
    "type": "integer"
  }
}
```

## `list_branches`

Action slug: `list-branches`

Price: `5` credits

List repository branches with pagination.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `owner` | `string` | yes | Repository owner. |
| `page` | `integer` | no | Page number. |
| `per_page` | `integer` | no | Items per page. |
| `protected_only` | `boolean` | no | When true, list only protected branches. |
| `repo` | `string` | yes | Repository name. |
| `timeout_seconds` | `integer` | no | HTTP timeout in seconds. |

Sample parameters:

```json
{
  "owner": "example owner",
  "page": 1,
  "per_page": 1,
  "protected_only": true,
  "repo": "example repo",
  "timeout_seconds": 5
}
```

Generated JSON parameter schema:

```json
{
  "owner": {
    "description": "Repository owner.",
    "required": true,
    "type": "string"
  },
  "page": {
    "description": "Page number.",
    "maximum": 1000,
    "minimum": 1,
    "required": false,
    "type": "integer"
  },
  "per_page": {
    "description": "Items per page.",
    "maximum": 100,
    "minimum": 1,
    "required": false,
    "type": "integer"
  },
  "protected_only": {
    "description": "When true, list only protected branches.",
    "required": false,
    "type": "boolean"
  },
  "repo": {
    "description": "Repository name.",
    "required": true,
    "type": "string"
  },
  "timeout_seconds": {
    "description": "HTTP timeout in seconds.",
    "maximum": 120,
    "minimum": 5,
    "required": false,
    "type": "integer"
  }
}
```

## `list_commits`

Action slug: `list-commits`

Price: `5` credits

List commits for a repository, optionally scoped to a branch and filtered to the last N hours. Results are returned newest first.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `owner` | `string` | yes | Repository owner. |
| `page` | `integer` | no | Page number. |
| `path` | `string` | no | Optional file or directory path to filter commits. |
| `per_page` | `integer` | no | Items per page. |
| `ref` | `string` | no | Branch, tag, or commit SHA to scope the commit list. |
| `repo` | `string` | yes | Repository name. |
| `since_hours` | `integer` | no | Only include commits from the last N hours. |
| `timeout_seconds` | `integer` | no | HTTP timeout in seconds. |

Sample parameters:

```json
{
  "owner": "example owner",
  "page": 1,
  "path": "example path",
  "per_page": 1,
  "ref": "example ref",
  "repo": "example repo",
  "since_hours": 1,
  "timeout_seconds": 5
}
```

Generated JSON parameter schema:

```json
{
  "owner": {
    "description": "Repository owner.",
    "required": true,
    "type": "string"
  },
  "page": {
    "description": "Page number.",
    "maximum": 1000,
    "minimum": 1,
    "required": false,
    "type": "integer"
  },
  "path": {
    "description": "Optional file or directory path to filter commits.",
    "required": false,
    "type": "string"
  },
  "per_page": {
    "description": "Items per page.",
    "maximum": 100,
    "minimum": 1,
    "required": false,
    "type": "integer"
  },
  "ref": {
    "description": "Branch, tag, or commit SHA to scope the commit list.",
    "required": false,
    "type": "string"
  },
  "repo": {
    "description": "Repository name.",
    "required": true,
    "type": "string"
  },
  "since_hours": {
    "description": "Only include commits from the last N hours.",
    "maximum": 720,
    "minimum": 1,
    "required": false,
    "type": "integer"
  },
  "timeout_seconds": {
    "description": "HTTP timeout in seconds.",
    "maximum": 120,
    "minimum": 5,
    "required": false,
    "type": "integer"
  }
}
```

## `list_directory`

Action slug: `list-directory`

Price: `5` credits

List the contents of a repository directory at a branch, tag, or commit.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `owner` | `string` | yes | Repository owner. |
| `path` | `string` | no | Directory path. Omit or use empty string for repository root. |
| `ref` | `string` | no | Branch, tag, or commit SHA. Defaults to repository default branch. |
| `repo` | `string` | yes | Repository name. |
| `timeout_seconds` | `integer` | no | HTTP timeout in seconds. |

Sample parameters:

```json
{
  "owner": "example owner",
  "path": "example path",
  "ref": "example ref",
  "repo": "example repo",
  "timeout_seconds": 5
}
```

Generated JSON parameter schema:

```json
{
  "owner": {
    "description": "Repository owner.",
    "required": true,
    "type": "string"
  },
  "path": {
    "description": "Directory path. Omit or use empty string for repository root.",
    "required": false,
    "type": "string"
  },
  "ref": {
    "description": "Branch, tag, or commit SHA. Defaults to repository default branch.",
    "required": false,
    "type": "string"
  },
  "repo": {
    "description": "Repository name.",
    "required": true,
    "type": "string"
  },
  "timeout_seconds": {
    "description": "HTTP timeout in seconds.",
    "maximum": 120,
    "minimum": 5,
    "required": false,
    "type": "integer"
  }
}
```

## `list_my_repos`

Action slug: `list-my-repos`

Price: `5` credits

List repositories the connected GitHub account can access, with pagination and sorting.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `affiliation` | `string` | no | Comma-separated affiliation filter such as owner,collaborator,organization_member. |
| `direction` | `string` | no | Sort direction. |
| `page` | `integer` | no | Page number. |
| `per_page` | `integer` | no | Items per page. |
| `sort` | `string` | no | Sort field. |
| `timeout_seconds` | `integer` | no | HTTP timeout in seconds. |
| `visibility` | `string` | no | Repository visibility filter. |

Sample parameters:

```json
{
  "affiliation": "example affiliation",
  "direction": "asc",
  "page": 1,
  "per_page": 1,
  "sort": "created",
  "timeout_seconds": 5,
  "visibility": "all"
}
```

Generated JSON parameter schema:

```json
{
  "affiliation": {
    "description": "Comma-separated affiliation filter such as owner,collaborator,organization_member.",
    "required": false,
    "type": "string"
  },
  "direction": {
    "description": "Sort direction.",
    "enum": [
      "asc",
      "desc"
    ],
    "required": false,
    "type": "string"
  },
  "page": {
    "description": "Page number.",
    "maximum": 1000,
    "minimum": 1,
    "required": false,
    "type": "integer"
  },
  "per_page": {
    "description": "Items per page.",
    "maximum": 100,
    "minimum": 1,
    "required": false,
    "type": "integer"
  },
  "sort": {
    "description": "Sort field.",
    "enum": [
      "created",
      "updated",
      "pushed",
      "full_name"
    ],
    "required": false,
    "type": "string"
  },
  "timeout_seconds": {
    "description": "HTTP timeout in seconds.",
    "maximum": 120,
    "minimum": 5,
    "required": false,
    "type": "integer"
  },
  "visibility": {
    "description": "Repository visibility filter.",
    "enum": [
      "all",
      "public",
      "private"
    ],
    "required": false,
    "type": "string"
  }
}
```

## `list_org_repos`

Action slug: `list-org-repos`

Price: `5` credits

List repositories for an organization the connected account can access.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `direction` | `string` | no | Sort direction. |
| `org` | `string` | yes | Organization login. |
| `page` | `integer` | no | Page number. |
| `per_page` | `integer` | no | Items per page. |
| `sort` | `string` | no | Sort field. |
| `timeout_seconds` | `integer` | no | HTTP timeout in seconds. |
| `type_filter` | `string` | no | Repository type filter. |

Sample parameters:

```json
{
  "direction": "asc",
  "org": "example org",
  "page": 1,
  "per_page": 1,
  "sort": "created",
  "timeout_seconds": 5,
  "type_filter": "all"
}
```

Generated JSON parameter schema:

```json
{
  "direction": {
    "description": "Sort direction.",
    "enum": [
      "asc",
      "desc"
    ],
    "required": false,
    "type": "string"
  },
  "org": {
    "description": "Organization login.",
    "required": true,
    "type": "string"
  },
  "page": {
    "description": "Page number.",
    "maximum": 1000,
    "minimum": 1,
    "required": false,
    "type": "integer"
  },
  "per_page": {
    "description": "Items per page.",
    "maximum": 100,
    "minimum": 1,
    "required": false,
    "type": "integer"
  },
  "sort": {
    "description": "Sort field.",
    "enum": [
      "created",
      "updated",
      "pushed",
      "full_name"
    ],
    "required": false,
    "type": "string"
  },
  "timeout_seconds": {
    "description": "HTTP timeout in seconds.",
    "maximum": 120,
    "minimum": 5,
    "required": false,
    "type": "integer"
  },
  "type_filter": {
    "description": "Repository type filter.",
    "enum": [
      "all",
      "public",
      "private",
      "forks",
      "sources",
      "member"
    ],
    "required": false,
    "type": "string"
  }
}
```

## `search_code`

Action slug: `search-code`

Price: `5` credits

Search code visible to the connected account, optionally scoped to a specific repository.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `order` | `string` | no | Search order. |
| `owner` | `string` | no | Optional repository owner to scope the search. |
| `page` | `integer` | no | Page number. |
| `per_page` | `integer` | no | Items per page. |
| `query` | `string` | yes | GitHub code search query. You can include qualifiers like language:python or path:src. |
| `repo` | `string` | no | Optional repository name to scope the search; requires owner when provided. |
| `sort` | `string` | no | Search sort field when supported. |
| `timeout_seconds` | `integer` | no | HTTP timeout in seconds. |

Sample parameters:

```json
{
  "order": "asc",
  "owner": "example owner",
  "page": 1,
  "per_page": 1,
  "query": "example search query",
  "repo": "example repo",
  "sort": "indexed",
  "timeout_seconds": 5
}
```

Generated JSON parameter schema:

```json
{
  "order": {
    "description": "Search order.",
    "enum": [
      "asc",
      "desc"
    ],
    "required": false,
    "type": "string"
  },
  "owner": {
    "description": "Optional repository owner to scope the search.",
    "required": false,
    "type": "string"
  },
  "page": {
    "description": "Page number.",
    "maximum": 100,
    "minimum": 1,
    "required": false,
    "type": "integer"
  },
  "per_page": {
    "description": "Items per page.",
    "maximum": 100,
    "minimum": 1,
    "required": false,
    "type": "integer"
  },
  "query": {
    "description": "GitHub code search query. You can include qualifiers like language:python or path:src.",
    "required": true,
    "type": "string"
  },
  "repo": {
    "description": "Optional repository name to scope the search; requires owner when provided.",
    "required": false,
    "type": "string"
  },
  "sort": {
    "description": "Search sort field when supported.",
    "enum": [
      "indexed"
    ],
    "required": false,
    "type": "string"
  },
  "timeout_seconds": {
    "description": "HTTP timeout in seconds.",
    "maximum": 120,
    "minimum": 5,
    "required": false,
    "type": "integer"
  }
}
```

## `search_repositories`

Action slug: `search-repositories`

Price: `5` credits

Search repositories visible to the connected account.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `order` | `string` | no | Search order. |
| `page` | `integer` | no | Page number. |
| `per_page` | `integer` | no | Items per page. |
| `query` | `string` | yes | GitHub repository search query. |
| `sort` | `string` | no | Search sort field. |
| `timeout_seconds` | `integer` | no | HTTP timeout in seconds. |

Sample parameters:

```json
{
  "order": "asc",
  "page": 1,
  "per_page": 1,
  "query": "example search query",
  "sort": "stars",
  "timeout_seconds": 5
}
```

Generated JSON parameter schema:

```json
{
  "order": {
    "description": "Search order.",
    "enum": [
      "asc",
      "desc"
    ],
    "required": false,
    "type": "string"
  },
  "page": {
    "description": "Page number.",
    "maximum": 100,
    "minimum": 1,
    "required": false,
    "type": "integer"
  },
  "per_page": {
    "description": "Items per page.",
    "maximum": 100,
    "minimum": 1,
    "required": false,
    "type": "integer"
  },
  "query": {
    "description": "GitHub repository search query.",
    "required": true,
    "type": "string"
  },
  "sort": {
    "description": "Search sort field.",
    "enum": [
      "stars",
      "forks",
      "help-wanted-issues",
      "updated"
    ],
    "required": false,
    "type": "string"
  },
  "timeout_seconds": {
    "description": "HTTP timeout in seconds.",
    "maximum": 120,
    "minimum": 5,
    "required": false,
    "type": "integer"
  }
}
```
