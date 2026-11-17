# harvard_art_museums

Harvard Art Museums API.

- Base URL: `https://api.harvardartmuseums.org`
- Docs: https://github.com/harvardartmuseums/api-docs
- Auth: required API key in `HARVARD_ART_MUSEUMS_KEY`, passed as `apikey`.
- Account/key request: https://docs.google.com/forms/d/1Fe1H4nOhFkrLpaeBpLAnSrIMYvcAxnYWm0IU9a6IkFA/viewform
- Rate limit: 2,500 requests/day; max `size=100`.
- Terms: free, non-commercial; attribution/link-back required; no caching/storage beyond two weeks without written permission; use returned image URLs rather than copies.
- Citation: prefer record `url`; docs URL otherwise.

## Actions

- `search_objects` — GET `/object`; supports documented filters such as `q`, `keyword`, `title`, `classification`, `person`, `yearmade`, `hasimage`, `size`, `page`, `fields`.
- `get_object` — GET `/object/{id}`.
- `people` / `person`
- `exhibitions` / `exhibition`
- `publications` / `publication`
- `resource` — generic resource query; params include `resource` plus source-supported query fields.
- `iiif_manifest` — GET `https://iiif.harvardartmuseums.org/manifests/object/{id}`.

## Hard blocker

Runtime API verification is blocked until `HARVARD_ART_MUSEUMS_KEY` is provisioned. The source is registered so Reach fails explicitly with an auth-required envelope rather than silently staying discovery-only.
