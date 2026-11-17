# Presenton v3 API

Base URL: `https://api.presenton.ai`

## Access

All endpoints in this reference are public; do not send an API key or authorization header. Use `application/json` for JSON requests, `multipart/form-data` for image upload, and query parameters for icon search.

## Search designs

`POST /api/v3/designs/search`

Request:

```json
{
  "query": "board-level quarterly review, editorial navy and cream, confident",
  "n": 4
}
```

Constraints:

- `query`: non-empty, at most 1000 whitespace-delimited words
- `n`: integer from 1 through 10

Response:

```json
{
  "designs": [
    {
      "id": 7,
      "title": "Editorial Board Review",
      "description": "A restrained navy and cream system with large numerals..."
    }
  ],
  "message": "Optional user-facing message"
}
```

`message` is optional and may be `null`. When it is a non-empty string, show it to the user verbatim. Use one item from `designs` as the visual brief for HTML generation. Preserve the selected result's `id` and include it as `design_id` in every export request for HTML based on that searched design. If the user supplied the design brief directly, do not search and omit `design_id`.

cURL:

```bash
curl --fail-with-body --silent --show-error \
  --request POST \
  --url https://api.presenton.ai/api/v3/designs/search \
  --header 'Content-Type: application/json' \
  --data '{"query":"board-level quarterly review, editorial navy and cream, confident","n":4}'
```

## Upload a public image

`POST /api/v3/images/upload/public`

Upload a local PNG, JPEG, or WebP file as multipart form field `file`. The maximum file size is 10 MB. Upload every user-provided image before placing it in presentation HTML; never convert the file to a base64 or `data:` URL.

Response:

```json
{
  "id": "18eb9e37-d1e1-42ba-8b1d-fb97c3948d4f",
  "user": null,
  "created_at": "2026-08-11T12:00:00Z",
  "path": "public/images/reference.png",
  "is_uploaded": true,
  "extras": null,
  "url": "https://cdn.example.com/public/images/reference.png"
}
```

Use the absolute HTTP or HTTPS `url` in an `<img>` element. The other response fields are metadata and are not needed for HTML generation.

cURL:

```bash
curl --fail-with-body --silent --show-error \
  --request POST \
  --url https://api.presenton.ai/api/v3/images/upload/public \
  --form 'file=@reference.png'
```

## Search icons

`GET /api/v3/icons/search`

Query parameters:

- `query`: icon concept to search
- `limit`: number of results; default `20`
- `icon_type`: optional visual weight: `bold`, `duotone`, `fill`, `light`, `regular`, or `thin`; default `bold`
- `icon_weight`: backward-compatible alias for `icon_type`; omit it when using `icon_type`

Response:

```json
[
  "https://cdn.example.com/icons/growth.svg",
  "https://cdn.example.com/icons/chart.svg"
]
```

Search for every icon concept used in the deck, select an appropriate returned URL, and use it in an `<img>` element. Do not invent or inline an icon when the search returns no suitable result; refine the query or omit the icon.

cURL:

```bash
curl --fail-with-body --silent --show-error \
  --get \
  --url https://api.presenton.ai/api/v3/icons/search \
  --data-urlencode 'query=revenue growth' \
  --data-urlencode 'limit=5' \
  --data-urlencode 'icon_type=thin'
```

## Export HTML

`POST /api/v3/export/html-to-any`

Request:

```json
{
  "html": "<!doctype html><html>...</html>",
  "format": "pptx",
  "title": "Quarterly review",
  "design_id": 7
}
```

Fields:

- `html`: required non-empty string
- `format`: exactly one of `pptx`, `pdf`, or `png`
- `title`: optional string used for the exported presentation/file name
- `design_id`: optional integer ID of the selected result from design search; include it when a searched design was used

Response:

```json
{
  "id": 23,
  "url": "https://temporary-export-url.example/...",
  "message": "Optional user-facing message"
}
```

- `id` is the positive integer creation ID. Retain one creation ID from each distinct presentation for creating its preview URL.
- `url` is a short download URL that expires after 24 hours.
- `message` is optional and may be `null`. When it is a non-empty string, show it to the user verbatim.

Call the endpoint once for each requested format and never for an unrequested format. If a presentation was requested without a format, call it three times: once each for `pptx`, `pdf`, and `png`. Return each response URL directly to the user as a clickable link. Do not download or save the exported file locally.

Format behavior:

- `pptx`: returns a `.pptx` file. DOM text and supported shapes remain editable where conversion permits.
- `pdf`: returns a 1280×720 px page per direct wrapper child.
- `png`: returns a URL for a ZIP containing one PNG per slide, not a single PNG file.

cURL:

```bash
curl --fail-with-body --silent --show-error \
  --request POST \
  --url https://api.presenton.ai/api/v3/export/html-to-any \
  --header 'Content-Type: application/json' \
  --data @request.json
```

If no searched design was used, omit `design_id` from the request.

## Create a shareable preview

`POST /api/v3/export/html-to-any/create-preview`

Request:

```json
{
  "id": 23
}
```

`id` may be the creation ID from any requested format for the presentation. Exports created from identical HTML resolve to the same stored source presentation, so call this endpoint exactly once per distinct presentation, not once per format.

Response:

```json
{
  "url": "https://presenton.ai/presentation-preview?t=..."
}
```

Return `url` as the presentation's clickable shareable-preview link. Its scoped preview token expires after 24 hours.

cURL:

```bash
curl --fail-with-body --silent --show-error \
  --request POST \
  --url https://api.presenton.ai/api/v3/export/html-to-any/create-preview \
  --header 'Content-Type: application/json' \
  --data '{"id":23}'
```

## Retrieve preview HTML

`GET /api/v3/export/html-to-any/preview?token=<preview-token>`

This endpoint is consumed by the Presenton preview frontend. It validates the scoped token from the preview `url` and returns the stored root presentation:

```json
{
  "id": 23,
  "html": "<!doctype html><html>...</html>"
}
```

Agents should return the preview `url` rather than calling this endpoint directly.

## Errors

- `400`: empty/invalid HTML, missing `#presentation-slides-wrapper`, no direct slide children, or invalid format
- `401`: invalid or expired preview token
- `404`: endpoint is not deployed at the selected API base URL, or the requested creation/preview does not exist
- `422`: invalid JSON schema, result count, creation ID, or request field
- `502`: exporter unreachable, invalid exporter JSON, missing exporter URL, or upstream server failure

Error bodies normally use `detail`; some services may use `error`. Preserve the server message without exposing request secrets.
