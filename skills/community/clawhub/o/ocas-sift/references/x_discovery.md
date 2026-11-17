# Public X Discovery (No-Auth)

Sift implements a non-authenticated pipeline for X/Twitter content discovery to bypass login walls and API restrictions.

## Pipeline Architecture

The discovery process follows a sequential fallback strategy:

### 1. Mirror Rotator
Sift maintains a dynamic list of Nitter/Mirror instances.
- **Operation**: Sequential polling of candidate mirrors.
- **Validation**: For each mirror, Sift validates that the resulting page:
  - Loads successfully (HTTP 200).
  - Does not contain login-wall elements or "Instance Down" banners.
- **Provenance**: Entries extracted via this method are tagged as `source: nitter`.

### 2. Search Bridge (Fallback)
If all candidate mirrors fail or the content is unavailable, Sift leverages the existing web search tier.
- **Operation**: Constructing specific "dork" queries to index X content cached by search engines.
- **Query Patterns**:
  - For users: `site:x.com "from:username"`
  - For hashtags: `site:x.com "#hashtag"`
- **Provenance**: Entries extracted via this method are tagged as `source: search-index`.

### 3. Extraction & Verification
- **Extraction**: Sift parses mirrored HTML or search snippets for tweet text, timestamps, and handle/display names.
- **Verification**: Extracted names are cross-referenced against the target entity name to ensure identity match before acceptance.
- **Output**: Cleaned text is passed to the standard Sift synthesis pipeline.

## Implementation Logic
- **Sequential Attempt**: Mirror A $\rightarrow$ Mirror B $\rightarrow$ ... $\rightarrow$ Mirror N $\rightarrow$ Search Bridge.
- **Rate Limiting**: Sift implements small random delays between mirror attempts to avoid instance-level blocking.
