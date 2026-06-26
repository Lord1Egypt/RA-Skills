# Hardcover GraphQL Patterns

Use this file as a working reference while executing the skill.

## Auth & Endpoint

- Endpoint: Hardcover GraphQL endpoint from official docs.
- Token source: `HARDCOVER_TOKEN`
- Add auth headers as documented by Hardcover.

If requests fail due to auth/header shape, re-check docs before retrying many variants.

## Reusable Query Shapes (pseudocode)

> Note: field names can evolve. Treat this as intent-level scaffolding and align exact schema names to the current docs/schema.

### 1) Search books by title

```graphql
query SearchBooks($q: String!) {
  # Search books by text query
  # Return enough metadata for disambiguation: title, author, edition/year, id
}
```

### 2) Fetch user shelf entries

```graphql
query ShelfEntries($shelf: String!, $limit: Int, $offset: Int) {
  # Get user books for a shelf/status such as WANT_TO_READ or CURRENTLY_READING
  # Include book id/title/author and reading entry id if available
}
```

### 3) Mark book as currently reading

```graphql
mutation StartReading($bookId: ID!, $startedAt: Date) {
  # Create/update user-book relationship to currently reading
}
```

### 4) Mark book as finished

```graphql
mutation FinishReading($entryIdOrBookId: ID!, $finishedAt: Date!) {
  # Transition to finished/read and store finish date
}
```

### 5) Count finished in year

```graphql
query FinishedInRange($from: Date!, $to: Date!) {
  # Fetch finished entries between date bounds
  # Return count (+ optional list)
}
```

## Matching Heuristics

When user gives only a short title:

1. Check currently-reading shelf first (for finish/start intents).
2. Prefer exact normalized title match.
3. Break ties with author match.
4. If still tied, ask user to choose.

## Confirmation Template

- Write success: `Done — marked "<Title>" as <status> (<date>).`
- Ambiguity: `I found multiple matches. Which one did you mean? 1) ... 2) ...`
