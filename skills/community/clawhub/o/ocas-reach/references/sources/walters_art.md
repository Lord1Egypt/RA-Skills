# walters_art

Walters Art Museum collections data from `WaltersArtMuseum/api-thewalters-org`.

- Repo/docs: https://github.com/WaltersArtMuseum/api-thewalters-org
- API homepage: https://api.thewalters.org/
- Current access: static CSV files; API v1 closed in 2023 while v2 is pending.
- Auth: none
- Rate limit: GitHub raw/API limits; avoid repeated full downloads in loops.
- License/terms: README says data and images are CC0 and reusable, including commercially.
- Citation: prefer `ResourceURL` / `https://purl.thewalters.org/art/...` for object records.

## Actions

- `search_objects` — search `art.csv`. Params: `q` required; `limit`, `fields` optional.
- `get_object` — get object by `ObjectID` or `ObjectNumber`.
- `get_media` — get image filenames listed for object.
- `list_collections` — rows from `collections.csv`.
- `list_exhibitions` — rows from `exhibitions.csv`.
- `refresh_snapshot` — fetch static CSV files and return row counts.

## Gotchas

This is a static dataset/custom connector, not a live REST source. Verify media URL construction before exposing direct image URLs beyond the filenames contained in the CSV.
