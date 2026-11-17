# metmuseum

The Metropolitan Museum of Art Collection API.

- Base URL: `https://collectionapi.metmuseum.org/public/collection/v1`
- Docs: https://metmuseum.github.io/
- Auth: none
- Rate limit: 80 requests/second
- License/terms: Open Access dataset is CC0 to the extent possible under law; API use remains subject to Met terms.
- Citation: use `objectURL` for object records.

## Actions

- `departments` — list department IDs and names.
- `list_objects` — list public object IDs. Params: `metadataDate`, `departmentIds` optional.
- `get_object` — fetch one object. Params: `objectID` required.
- `search_objects` — search object metadata. Params: `q` required; optional filters include `isHighlight`, `title`, `tags`, `departmentId`, `isOnView`, `artistOrCulture`, `medium`, `hasImages`, `geoLocation`, `dateBegin`, `dateEnd`.

## Gotchas

Search returns IDs only. Preserve `total` and `objectIDs`; hydrate details only as an explicit follow-up.
