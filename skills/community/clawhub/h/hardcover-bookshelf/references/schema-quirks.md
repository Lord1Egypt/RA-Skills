# Hardcover schema quirks

These notes come from live testing against the Hardcover GraphQL API.

## Auth

- Endpoint: `https://api.hardcover.app/v1/graphql`
- `HARDCOVER_TOKEN` should contain the **full header value** copied from Hardcover, including `Bearer `.
- Common auth failure:

```json
{"error":"Unable to verify token"}
```

That usually means the token is missing, malformed, or missing the `Bearer ` prefix/value.

## Useful status IDs

- `1` = Want to Read
- `2` = Currently Reading
- `3` = Read
- `4` = Paused
- `5` = Did Not Finish
- `6` = Ignored

## Query quirks

### `me`

`me` returns a **list** with one element, not a single object.

Example:

```graphql
query {
  me {
    id
  }
}
```

Handle it as `data.me[0]`.

### Search

`search(query: ..., query_type: "Book")` does **not** return a typed `books` array.
It returns a `results` JSON blob. Useful book hits live at:

- `search.results.hits[*].document`

Fields observed there include:
- `id`
- `title`
- `release_year`
- `author_names`

## Mutation quirks

### `insert_user_book`

`insert_user_book` does not return the created row directly. It returns a wrapper shape:

```graphql
mutation {
  insert_user_book(object: ...) {
    id
    user_book {
      id
      book { title }
    }
  }
}
```

So read nested data from `insert_user_book.user_book`.

### `update_user_book`

`update_user_book` accepts:
- `id: Int!`
- `object: UserBookUpdateInput!`

Read nested data from `update_user_book.user_book`.

## Start-reading behavior

The current client:
- checks for an existing `user_book` with the same `book_id`
- returns it unchanged if already `Currently Reading`
- otherwise updates the most recent existing row, or inserts a new one if none exists

Fields used:
- `status_id = 2`
- `first_started_reading_date`
- `date_added` on insert

## Finish-reading behavior

Best-effort current behavior:
- pick the existing currently-reading row for the book if present
- otherwise pick the most recent existing `user_book` row for that `book_id`
- update:
  - `status_id = 3`
  - `last_read_date = <finish-date>`

This worked with the current live schema. If Hardcover later exposes a more canonical finish-date field, prefer that.

## Count books read last year

Current implementation counts:
- `status_id = 3`
- `last_read_date` between `YYYY-01-01` and `YYYY-12-31`

This query shape worked live and returned expected samples + aggregate counts.
