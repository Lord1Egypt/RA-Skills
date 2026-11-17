# Cultural Heritage API Candidates

Session-derived notes for evaluating museum/archive collection APIs as Reach sources.

## Fit criteria

Museum collection APIs usually belong in Reach when they are:

- Primary/authoritative institutional data, not scraped gallery pages
- Structured REST/JSON or IIIF endpoints
- Suitable for factual lookups: object metadata, creator/constituent records, provenance, exhibitions, publications, galleries, collection vocabularies, images/manifests
- Citation-friendly via canonical object URLs, IIIF manifests, or stable record IDs
- Clear about auth, rate limits, licensing, attribution, caching, and image reuse

Prefer direct API integration over website scraping. Preserve raw record IDs/counts for search endpoints; add optional hydration helpers only as a convenience layer.

## The Metropolitan Museum of Art Collection API

- Docs: https://metmuseum.github.io/
- Endpoint: `https://collectionapi.metmuseum.org/public/collection/v1`
- Open Access repo: https://github.com/metmuseum/openaccess
- Auth: none
- Rate limit: 80 requests/second
- Coverage: 470k+ object records; departments; object ID listing; search endpoint; object detail endpoint
- Licensing: selected Open Access dataset is CC0 to the extent possible under law; API use remains subject to The Met terms
- Images: direct high-resolution public-domain JPEG URLs when available
- Useful Reach actions: `departments`, `list_objects`, `get_object`, `search_objects`
- Important behavior: search returns object IDs only. Preserve the raw ID list and total count; optionally hydrate first N object details in a separate helper.
- Citation: prefer `objectURL` for object records; docs URL for aggregate endpoints.

Verified live during discovery with `/departments`, `/search?q=sunflowers&hasImages=true`, and `/objects/436524`.

## Harvard Art Museums API

- Docs: https://github.com/harvardartmuseums/api-docs
- Endpoint: `https://api.harvardartmuseums.org`
- Auth: API key required as `apikey`; request key via Harvard's form
- Rate limit: 2,500 requests/day; default page size 10, max `size=100`
- Coverage: objects, people, exhibitions, publications, galleries, classifications, centuries, colors, cultures, groups, media/technique/support/worktype vocabularies, places, activities, sites, video, image, audio, annotations
- Images/IIIF: IIIF image and presentation services; rights-restricted images may be absent or limited
- Terms: free, non-commercial; attribution/link-back required; no storage/cache beyond two weeks without permission; use returned image URLs rather than local copies
- Useful Reach actions: `search_objects`, `get_object`, `search_people`, `get_person`, `search_exhibitions`, `get_exhibition`, `search_publications`, `get_publication`, `iiif_manifest`, plus generic vocabulary/resource passthrough
- Citation: prefer record `url` fields where present; docs URL otherwise.

## Walters Art Museum Collections Data

- Docs/repo: https://github.com/WaltersArtMuseum/api-thewalters-org
- API homepage: https://api.thewalters.org/
- Current access: static CSV files in GitHub; API v1 closed in 2023 while v2 is pending
- Auth: none
- Rate limit: GitHub raw/API limits only
- Coverage: 10,000+ Walters object records plus media/images, relationships, collections, geographies, and exhibitions CSVs
- Licensing: README states data and images are CC0 and reusable, including commercially
- Useful Reach actions: `search_objects`, `get_object`, `get_media`, `list_collections`, `list_exhibitions`, `refresh_snapshot`
- Citation: prefer `ResourceURL` / `https://purl.thewalters.org/art/...` for object records.
- Implementation note: this is a static dataset/custom connector, not a live REST source, until v2 comes online.

## Ranking note

For immediate Reach integration, The Met is highest priority because it needs no key, supports high request rates, and has permissive Open Access terms. Walters is also useful and permissive, but should be implemented as a static dataset snapshot/custom connector rather than a live REST API until v2 is available. Harvard is valuable for richer/varied museum metadata and IIIF but should stay discovery-cataloged until credentials are provisioned and terms-sensitive handling is implemented.
