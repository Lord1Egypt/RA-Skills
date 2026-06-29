# Google SERP Images Search operations

Generated from Just Serp API OpenAPI for group key `google`.

Endpoint group: `images/search`.

## `imagesSearch`

- Method: `GET`
- Path: `/api/v1/google/images/search`
- Summary: Search
- Description: Get Google images Search data, including image URLs and metadata, for filtered image discovery for research and monitoring workflows.
- Tags: `Google Images`

### Parameters

| Name | In | Required | Type | Default | Description |
| --- | --- | --- | --- | --- | --- |
| `query` | `query` | yes | `string` | n/a | The search query for images (e.g., 'mountain landscape', 'luxury cars'). |
| `html` | `query` | no | `boolean` | n/a | Set to true to return the raw HTML of the Google search results page alongside the structured data. |
| `page` | `query` | no | `integer` | n/a | The results page number. Use 0 for the first page, 1 for the second, and so on. |
| `domain` | `query` | no | `string` | n/a | The Google domain to use for the search (e.g., 'google.com', 'google.co.uk'). See <a href="/reference/google-domains">Google Domains</a>. |
| `country` | `query` | no | `string` | n/a | Set the target country code (e.g., 'us', 'uk') to localize results. See <a href="/reference/google-countries">Google Countries</a>. |
| `cr` | `query` | no | `string` | n/a | Limits results to search results from specific countries. Format: 'countryXX'. See <a href="/reference/google-cr-countries">Google CR Countries</a>. |
| `language` | `query` | no | `string` | n/a | Set the language for the results using its two-letter code (e.g., 'en' for English, 'fr' for French). See <a href="/reference/google-language">Google Language</a>. |
| `lr` | `query` | no | `string` | n/a | Restrict results to one or more languages using the 'lang_{language_code}' format (e.g., 'lang_en'). See <a href="/reference/google-lr-language">Google LR Language</a>. |
| `uule` | `query` | no | `string` | n/a | Encoded location string (UULE) used to precisely localize Google search results. This is an advanced/technical parameter — if you’re not familiar with it, you can leave it empty and omit it. |
| `period_unit` | `query` | no | `string` | n/a | Time unit for 'recent' image results. Supported values: 's' (Second), 'n' (Minute), 'h' (Hour), 'd' (Day), 'w' (Week), 'm' (Month), 'y' (Year). |
| `period_value` | `query` | no | `string` | n/a | Time duration value used with 'period_unit' (e.g., 15 for 15 days). Default: 1. |
| `start_date` | `query` | no | `string` | n/a | Start date for restricting images to a time range. Format: 'YYYYMMDD' (e.g., '20241201'). |
| `end_date` | `query` | no | `string` | n/a | End date for restricting images to a time range. Format: 'YYYYMMDD' (e.g., '20241231'). |
| `chips` | `query` | no | `string` | n/a | Additional suggested search terms (chips) to filter images. Values are obtained from previous responses. |
| `tbs` | `query` | no | `string` | n/a | Advanced search filter parameter (tbs) used to apply Google result filters (e.g. time range). This is an advanced parameter — if you’re not familiar with it, you can leave it empty. |
| `imgar` | `query` | no | `string` | n/a | Filter by image aspect ratio. Supported values: 's' (Square), 't' (Tall), 'w' (Wide), 'xw' (Panoramic). |
| `imgsz` | `query` | no | `string` | n/a | Filter by image size. Supported values: 'l' (Large), 'm' (Medium), 'i' (Icon), and specific resolutions like '4mp', '10mp'. |
| `image_color` | `query` | no | `string` | n/a | Filter images by a dominant color (e.g., 'red', 'blue', 'bw' for black and white, 'trans' for transparent). |
| `image_type` | `query` | no | `string` | n/a | Filter by image type. Supported values: 'face', 'photo', 'clipart', 'lineart', 'animated'. |
| `licenses` | `query` | no | `string` | n/a | Filter by usage rights and licenses. Supported values: 'f' (Free to use), 'fc' (Commercial use), 'cl' (Creative Commons). |
| `safe` | `query` | no | `string` | n/a | SafeSearch filter setting. Set to 'active' to filter adult content, or 'off' to disable it. |
| `nfpr` | `query` | no | `string` | n/a | Controls Google's auto-correction. Set to '1' to exclude corrected results, '0' to include them. |
| `filter` | `query` | no | `string` | n/a | Toggle 'Similar Results' and 'Omitted Results' filters. Set to '1' (default) to enable, '0' to disable. |

### Request body

No request body.

### Responses

- `200`: OK
- `401`: Authentication failed: API Key is invalid or missing
- `403`: Access denied: Insufficient credits or quota exceeded
- `500`: Internal server error or upstream service exception
