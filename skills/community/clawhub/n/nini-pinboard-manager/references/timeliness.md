# Timeliness Check Mode

Identify tech bookmarks whose content may be outdated using a two-stage approach: heuristic pre-filtering to narrow candidates, then AI content analysis via Jina Reader + current Claude session.

This mode does NOT auto-delete anything -- all actions require user confirmation.

## Step 1: Fetch all bookmarks

Reuse the cached file if available from a previous mode in this session:

```bash
# Only fetch if cache doesn't exist or is stale
if [ ! -f /tmp/pinboard_all.json ]; then
  curl -s "https://api.pinboard.in/v1/posts/all?auth_token=$PINBOARD_AUTH_TOKEN&format=json" > /tmp/pinboard_all.json
fi
```

Parse the JSON and count total bookmarks.

## Step 2: Heuristic pre-filtering

Apply three filters in order to identify candidates for AI analysis:

### Filter 1: Tag filter (tech only)

Include bookmarks with ANY tech-related tags from the tag convention's tech category. If no tag convention exists, use these defaults:

`llm`, `programming`, `python`, `javascript`, `typescript`, `web`, `devops`, `cloudflare`, `shell`, `github`, `database`, `security`, `home_assistant`, `iot`, `zigbee`

Exclude bookmarks with ANY of these meta tags (even if they have tech tags):

`evergreen`, `reference`, `collection`

### Filter 2: Age filter

Include bookmarks saved more than **2 years ago** (based on the Pinboard `time` field).

### Filter 3: Version detection

Include bookmarks whose **title** or **URL** contains version number patterns, regardless of age:

- Named versions: `React 16`, `Python 3.8`, `Vue 2`, `Angular 1.x`
- Version prefixes: `v2.0`, `v1.x`, `v3`
- ECMAScript versions: `ES5`, `ES6`, `ES2015`
- Framework-specific: `Rails 4`, `Django 1.x`, `Node 12`

### Candidate condition

A bookmark is a candidate if it matches: **Filter 1 AND (Filter 2 OR Filter 3)**

Report the number of candidates found before proceeding:

```text
Heuristic pre-filtering complete:
- Total bookmarks: 376
- Tech bookmarks (after tag filter): 120
- Candidates (age > 2y OR version detected): 35
```

## Step 3: Content fetching via Jina Reader

For each candidate, fetch content using Jina Reader:

```bash
CONTENT=$(curl -s "https://r.jina.ai/BOOKMARK_URL" | head -c 5000)
sleep 2  # Rate limiting between requests
```

**Error handling**:

- If Jina Reader returns an error or empty response -> mark as "unable to fetch", skip this bookmark
- If the URL is unreachable -> skip and continue with next candidate
- Always wait 2 seconds between Jina Reader requests

## Step 4: AI timeliness analysis

For each successfully fetched candidate, analyze the content and determine timeliness. Output for each:

| Field | Values | Description |
|-------|--------|-------------|
| Status | `outdated` / `possibly_outdated` / `still_valid` | Timeliness assessment |
| Reason | Free text | One sentence explaining the assessment |
| Suggestion | `delete` / `mark_evergreen` / `keep` | Recommended action |

**Assessment guidelines**:

- **`outdated`**: Content discusses deprecated APIs, removed features, old framework versions with no relevance today, or superseded best practices. Suggest `delete`.
- **`possibly_outdated`**: Content references specific versions but core concepts may still apply, or the technology has evolved significantly. Suggest `keep`.
- **`still_valid`**: Content discusses timeless concepts, patterns, or approaches that remain current. Suggest `mark_evergreen`.

## Step 5: Batch presentation

Present results in batches of **5 candidates**:

```text
### Batch 1: Timeliness Analysis (5 items)

1. 「Introduction to React 16 Lifecycle Methods」
   URL: https://example.com/react-16-lifecycle
   Tags: javascript web
   Status: outdated
   Reason: Article covers React 16 class component lifecycle methods; React 18+ recommends functional components with hooks
   Suggestion: delete

2. 「Understanding Python Type Hints」
   URL: https://example.com/python-types
   Tags: python programming
   Status: still_valid
   Reason: Python type hints syntax and concepts remain current in Python 3.12+
   Suggestion: mark_evergreen

...

Options: [confirm suggestions] [modify individual] [skip all]
```

## Step 6: Apply user actions

For each bookmark based on user decision:

**Delete** (for `outdated` bookmarks user confirms):

```bash
curl -s "https://api.pinboard.in/v1/posts/delete?auth_token=$PINBOARD_AUTH_TOKEN&format=json&url=ENCODED_URL"
sleep 3  # Rate limit
```

**Mark evergreen** (for `still_valid` bookmarks user confirms):

```bash
# Add 'evergreen' to existing tags, preserve ALL other fields
curl -s "https://api.pinboard.in/v1/posts/add?auth_token=$PINBOARD_AUTH_TOKEN&format=json&url=ENCODED_URL&description=ENCODED_TITLE&extended=ENCODED_NOTES&tags=EXISTING_TAGS%20evergreen&shared=ORIGINAL_SHARED&toread=ORIGINAL_TOREAD&replace=yes"
sleep 3  # Rate limit
```

**CRITICAL**: When adding `evergreen` tag, preserve ALL original fields (description, extended, shared, toread). Only append `evergreen` to the tags list.

**Skip**: No API call, move to next item.

## Step 7: Summary

After all batches are processed:

```text
Timeliness Check Complete
- Total bookmarks: 376
- Candidates (after heuristic filter): 35
- Unable to fetch: 3
- Analyzed: 32
  - Outdated: 12 (deleted: 10, kept: 2)
  - Possibly outdated: 8 (all kept)
  - Still valid: 12 (marked evergreen: 10, kept: 2)
- Skipped: 5
```
