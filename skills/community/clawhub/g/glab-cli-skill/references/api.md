# `glab api`

Verified against `glab 1.90.0`.

## When to Use

Use `glab api` when the regular high-level commands do not expose the GitLab object or filter you need, or when the user wants raw REST or GraphQL output.

## Core Patterns

```bash
# REST
glab api projects/:fullpath/releases
glab api projects/:id/merge_requests

# POST with typed fields
glab api --method POST projects/:id/issues --field title="Bug" --field description="Details"

# GraphQL
glab api graphql -f query='query { currentUser { username } }'
```

Useful placeholders for repository-aware calls:

- `:branch`
- `:fullpath`
- `:group`
- `:id`
- `:namespace`
- `:repo`
- `:user`
- `:username`

## Pagination

For REST endpoints, keep page-size parameters in the endpoint itself and use `--paginate` to follow all pages:

```bash
glab api "projects/:id/jobs?per_page=100" --paginate
glab api "projects/:id/pipelines?per_page=100" --paginate --output ndjson
```

Do not invent separate pagination flags for endpoint-specific parameters such as `per_page`.

## Automation

```bash
glab api issues --paginate --output ndjson | jq 'select(.state == "opened")'
glab api graphql --paginate -f query='
query($endCursor: String) {
  project(fullPath: "gitlab-org/graphql-sandbox") {
    issues(first: 2, after: $endCursor) {
      edges { node { title } }
      pageInfo { endCursor hasNextPage }
    }
  }
}'
```

Use `--output ndjson` for large paginated responses that will be piped into shell tools.

## Host Selection

Outside a Git directory, `glab api` defaults to `gitlab.com`. Override it for self-hosted instances:

```bash
glab api --hostname gitlab.example.org projects/:id
```

## Common Pitfalls

- `--field` changes the default method to `POST`
- `--input -` reads the raw request body from stdin
- `--paginate` works for both REST and GraphQL, but GraphQL queries must request `pageInfo { hasNextPage endCursor }`
