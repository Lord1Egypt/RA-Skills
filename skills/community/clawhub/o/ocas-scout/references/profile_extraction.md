# Scout Person Research: Profile Extraction

Scout extracts a structured **profile** (name, bio, avatar) from every URL it visits. This page documents how it works and how to use it independently.

## Why structured profiles

Raw evidence text is useful; structured identity data is stronger. A profile with `name` + `bio` + `avatar` can be compared across sources (correlation), fed into entity resolution, and verified against other signals. The structured form is required before the cross-site correlation engine will treat it as an identity candidate — raw page text alone leaves too much room for noise to masquerade as signal.

Two extraction layers, both per-site overrideable:

| Source | Priority | Notes |
|---|---|---|
| Per-site CSS selectors (`data/site_profiles.json`) | 1 | Exact selectors for known sites. Authoritative when present. |
| OpenGraph `og:title` / `og:description` / `og:image` | 2 | Provider-agnostic. Strong on any site that emits OG tags. |
| JSON-LD `Person` schema | 2 | `name`, `image`, `description` from structured markup. |
| `<title>` / `<meta name="description">` | 3 | Page chrome fallback only. |

### `name_from_profile` — the gate that matters

`name` is reported as the displayed page title **only** when it came from a structured source (OG or JSON-LD). A bare `<title>` is page chrome — "Someone · GitHub" on a profile page looks like a name but is really branding that could be anything. Profiles whose name came from a fallback have `name_from_profile: false` and their `name` field is flagged as unverified. Cross-site correlation requires a structured name — it will not cluster on bare titles.

## Usage

```bash
# Extract from a URL (fetches + parses in one step)
python3 profile_extract.py --url https://github.com/someonetw

# Extract from a saved HTML file
python3 profile_extract.py --html path/to/page.html --site github

# Extract from a research result JSON (one shot over all Found URLs)
python3 profile_extract.py --input research_result.json --format detailed

# Use per-site selector overrides (same format as site_profiles.json)
python3 profile_extract.py --url https://example.com/user \
    --site-profiles '{"example.com": {"name": "h1.username", "bio": ".bio-text"}}'
```

## Output

Every profile carries:

- `name` — display name, empty if no extractable signal found
- `name_from_profile` — **true only if OG or JSON-LD**; title fallback is false
- `bio` — page description text
- `avatar` — `og:image` URL (URLs are checked for public reachability)
- `sources` — which source each field came from (`og`, `json_ld`, `title_fallback`, `meta_description`, `site_selector`)

The structured name is the field that feeds correlation. If `name_from_profile` is false, treat the name as context, not identity evidence.

## Integrating with the pipeline

In the research pipeline, profile extraction runs automatically on every Found URL. For a targeted job, run it first to enrich the result before correlation:

```bash
python3 research_person.py --name "Someone" --url https://github.com/someonetw --format detailed
python3 correlate_profiles.py --input result.json --no-avatars
```

Or for a saved report, run profile extraction over all URLs in the report before correlating.
