---
name: keyapi-linkedin-user-analytics
description: Discover, profile, and deeply analyze LinkedIn users — explore professional profiles, contact information, work experience, education, skills, publications, certifications, honors, recommendations, interests, posts, comments, and videos.
metadata: {"openclaw":{"requires":{"env":["KEYAPI_TOKEN"],"bins":["node"]},"primaryEnv":"KEYAPI_TOKEN","emoji":"👔"}}
author: KeyAPI
license: MIT
repository: https://github.com/EchoSell/keyapi-skills
---

# keyapi-linkedin-user-analytics

> Discover, profile, and deeply analyze LinkedIn professionals — from identity resolution and career history to content activity, social graph metrics, and interest mapping.

This skill provides comprehensive LinkedIn user intelligence using the KeyAPI MCP service. It enables retrieval of full professional profiles, contact details, follower/connection counts, published posts, comments, videos, images, work experience, education, skills, certifications, publications, honors, recommendations, and interest groups — all through a unified, cache-first workflow.

Use this skill when you need to:
- Retrieve a complete professional profile for a LinkedIn user by username
- Audit a user's career history, education background, and skill endorsements
- Analyze a professional's published content — posts, comments, videos, and images
- Research contact information, follower counts, and connection network size
- Discover a user's certifications, publications, honors, and recommendations
- Map professional interests via followed groups and companies
- Search and discover LinkedIn professionals by name, title, company, or industry

author: KeyAPI
license: MIT
repository: https://github.com/EchoSell/keyapi-skills
---

## Prerequisites

| Requirement | Details |
|-------------|---------|
| **KEYAPI_TOKEN** | A valid API token from [keyapi.ai](https://keyapi.ai/). Register at the site to obtain your free token. Set it as an environment variable: `export KEYAPI_TOKEN=your_token_here` |
| **Node.js** | v18 or higher |
| **Dependencies** | Run `npm install` in the skill directory to install `@modelcontextprotocol/sdk` |

author: KeyAPI
license: MIT
repository: https://github.com/EchoSell/keyapi-skills
---

## MCP Server Configuration

All tool calls in this skill target the KeyAPI LinkedIn MCP server:

```
Server URL : https://mcp.keyapi.ai/linkedin/mcp
Auth Header: Authorization: Bearer $KEYAPI_TOKEN
```

**Setup (one-time):**

```bash
# 1. Install dependencies
npm install

# 2. Set your API token (get one free at https://keyapi.ai/)
export KEYAPI_TOKEN=your_token_here

# 3. List all available tools to verify the connection
node scripts/run.js --platform linkedin --list-tools
```

author: KeyAPI
license: MIT
repository: https://github.com/EchoSell/keyapi-skills
---

## Analysis Scenarios

| User Need | Node(s) | Best For |
|-----------|---------|----------|
| Full profile snapshot with optional sections | `get_user_profile` | Profile audit, identity resolution, one-call enrichment |
| Personal bio / about section | `get_user_about` | Narrative summary, career positioning |
| Contact details (email, phone, social links) | `get_user_contact_information` | Outreach research, lead enrichment |
| Follower and connection counts | `get_user_follower_and_connection` | Influence sizing, network reach |
| Published posts with engagement | `get_user_posts` | Content strategy analysis, thought leadership audit |
| Comments activity | `get_user_comments` | Engagement behavior, community participation |
| Published videos | `get_user_videos` | Video content inventory, media presence |
| Published images | `get_user_images` | Visual content audit |
| Work experience history | `get_user_experience` | Career trajectory, employer history |
| Skill endorsements | `get_user_skills` | Competency mapping, talent assessment |
| Education background | `get_user_educations` | Academic credentials, institutional affiliations |
| Publications and research | `get_user_publications` | Thought leadership, academic output |
| Professional certifications | `get_user_certifications` | Credential verification, compliance checks |
| Honors and awards | `get_user_honors` | Achievement profiling, recognition history |
| Peer recommendations | `get_user_recommendations` | Social proof, reputation signals |
| Followed interest groups | `get_user_interests_groups` | Community affiliations, niche interests |
| Followed companies | `get_user_interests_companies` | Industry focus, competitive intelligence |
| Search professionals by name, title, or company | `search_people` | Talent discovery, prospect research |

author: KeyAPI
license: MIT
repository: https://github.com/EchoSell/keyapi-skills
---

## Workflow

### Step 1 — Identify Analysis Targets and Select Nodes

Clarify the research objective and map it to one or more nodes. Typical entry points:

- **Profile lookup**: Use `get_user_profile` with `username`. Enable `include_*` flags to fetch additional sections in a single call.
- **Content audit**: Combine `get_user_posts` + `get_user_comments` + `get_user_videos` + `get_user_images`.
- **Career deep-dive**: Use `get_user_experience` + `get_user_educations` + `get_user_skills` + `get_user_certifications`.
- **Reputation research**: Use `get_user_recommendations` + `get_user_honors` + `get_user_publications`.
- **Interest mapping**: Use `get_user_interests_groups` + `get_user_interests_companies`.
- **People discovery**: Use `search_people` with name, title, company, or industry filters.

> **Critical: Two Identifier Types**
>
> LinkedIn endpoints use two distinct identifiers:
> - `username` — the handle from the profile URL (e.g., `https://www.linkedin.com/in/jack` → `jack`). Used by `get_user_profile`, `get_user_contact_information`, `get_user_follower_and_connection`.
> - `urn` — an internal opaque identifier (e.g., `ACoAABCtiL8B26nfi3Nbpo_AM8ngg4LeClT1Wh8`). Required by all other user nodes.
>
> **Always call `get_user_profile` first** with the `username` to obtain the `urn` before calling any `urn`-based endpoint.

> **`get_user_profile` Efficiency Tip**
>
> `get_user_profile` supports optional `include_*` boolean flags: `include_follower_and_connection`, `include_experiences`, `include_skills`, `include_certifications`, `include_publications`, `include_educations`, `include_volunteers`, `include_honors`, `include_interests`, `include_bio`. Enable these to retrieve multiple sections in a single API call and reduce total request count.

### Step 2 — Retrieve API Schema

Before calling any node, inspect its input schema to confirm required parameters and available options:

```bash
node scripts/run.js --platform linkedin --schema <tool_name>

# Examples
node scripts/run.js --platform linkedin --schema get_user_profile
node scripts/run.js --platform linkedin --schema search_people
```

### Step 3 — Call APIs and Cache Results Locally

Execute tool calls and persist responses to the local cache to avoid redundant API calls.

**Calling a tool:**

```bash
# Single call with pretty output
node scripts/run.js --platform linkedin --tool <tool_name> \
  --params '<json_args>' --pretty

# Force fresh data, skip cache
node scripts/run.js --platform linkedin --tool <tool_name> \
  --params '<json_args>' --no-cache --pretty
```

**Example — get full profile with experience and skills:**

```bash
node scripts/run.js --platform linkedin --tool get_user_profile \
  --params '{"username":"jack","include_experiences":true,"include_skills":true}' --pretty
```

**Example — get user posts (first page):**

```bash
node scripts/run.js --platform linkedin --tool get_user_posts \
  --params '{"urn":"ACoAABCtiL8B26nfi3Nbpo_AM8ngg4LeClT1Wh8","page":1}' --pretty
```

**Example — get next page using pagination token:**

```bash
node scripts/run.js --platform linkedin --tool get_user_posts \
  --params '{"urn":"ACoAABCtiL8B26nfi3Nbpo_AM8ngg4LeClT1Wh8","page":2,"pagination_token":"<token_from_previous_response>"}' --pretty
```

**Example — search people by title and company:**

```bash
node scripts/run.js --platform linkedin --tool search_people \
  --params '{"title":"CEO","company":"OpenAI","page":1}' --pretty
```

**Example — get received recommendations:**

```bash
node scripts/run.js --platform linkedin --tool get_user_recommendations \
  --params '{"urn":"ACoAAC3iNKcB3qbWJrP7K5Z3i89AF5c1snr8bhc","type":"received","page":1}' --pretty
```

**Pagination:**

Most user content endpoints use a hybrid pagination model:

| Endpoint group | Pagination parameters | Notes |
|---|---|---|
| `get_user_posts`, `get_user_comments`, `get_user_videos`, `get_user_images`, `get_user_recommendations` | `page` (int, 1-indexed) + `pagination_token` | Pass `pagination_token` from previous response for pages > 1 |
| `get_user_experience`, `get_user_skills`, `get_user_educations`, `get_user_publications`, `get_user_certifications`, `get_user_honors`, `get_user_interests_groups`, `get_user_interests_companies` | `page` (int, 1-indexed) | No token required |
| `search_people` | `page` (int, 1-indexed) | No token required |
| `get_user_profile`, `get_user_about`, `get_user_contact_information`, `get_user_follower_and_connection` | — | Single-call response |

**Cache directory structure:**

```
.keyapi-cache/
└── YYYY-MM-DD/
    ├── get_user_profile/
    │   └── {params_hash}.json
    ├── get_user_about/
    │   └── {params_hash}.json
    ├── get_user_contact_information/
    │   └── {params_hash}.json
    ├── get_user_follower_and_connection/
    │   └── {params_hash}.json
    ├── get_user_posts/
    │   └── {params_hash}.json
    ├── get_user_comments/
    │   └── {params_hash}.json
    ├── get_user_videos/
    │   └── {params_hash}.json
    ├── get_user_images/
    │   └── {params_hash}.json
    ├── get_user_experience/
    │   └── {params_hash}.json
    ├── get_user_skills/
    │   └── {params_hash}.json
    ├── get_user_educations/
    │   └── {params_hash}.json
    ├── get_user_publications/
    │   └── {params_hash}.json
    ├── get_user_certifications/
    │   └── {params_hash}.json
    ├── get_user_honors/
    │   └── {params_hash}.json
    ├── get_user_recommendations/
    │   └── {params_hash}.json
    ├── get_user_interests_groups/
    │   └── {params_hash}.json
    ├── get_user_interests_companies/
    │   └── {params_hash}.json
    └── search_people/
        └── {params_hash}.json
```

**Cache-first policy:**

Before every API call, check whether a cached result already exists for the given parameters. If a valid cache file exists, load from disk and skip the API call.

### Step 4 — Synthesize and Report Findings

After collecting all API responses, produce a structured professional intelligence report:

**For individual profile analysis:**
1. **Profile Overview** — Name, username, URN, headline, location, follower count, connection count, verification status.
2. **Career Summary** — Work experience timeline, current and past employers, tenure patterns, career progression.
3. **Education & Credentials** — Academic institutions, degrees, certifications, publications, honors.
4. **Skills & Endorsements** — Top endorsed skills, skill categories, competency breadth.
5. **Content Activity** — Post frequency, engagement patterns, video and image publishing cadence.
6. **Reputation Signals** — Received recommendations, honors, community recognition.
7. **Interest Profile** — Followed groups and companies, industry focus areas.

**For discovery / shortlist building:**
1. **Search Results** — Matched professionals with headline, company, location.
2. **Comparative Overview** — Side-by-side profile metrics for shortlisted candidates.
3. **Actionable Recommendations** — Best-fit profiles for outreach, partnership, or hiring.

author: KeyAPI
license: MIT
repository: https://github.com/EchoSell/keyapi-skills
---

## Common Rules

| Rule | Detail |
|------|--------|
| **Identifier resolution** | `username` is used by `get_user_profile`, `get_user_contact_information`, `get_user_follower_and_connection`. All other user nodes require `urn` — always call `get_user_profile` first to obtain it. |
| **`get_user_profile` flags** | Use `include_*` boolean flags to fetch multiple profile sections in a single call and minimize API usage. |
| **`get_user_educations` quirk** | The API schema marks `urn` as optional for this endpoint (no `required` constraint), but in practice a valid `urn` is needed to return meaningful data. Always pass `urn`. |
| **`get_user_recommendations` type** | Pass `type: "received"` (default) or `type: "given"` to control which direction of recommendations is returned. |
| **Pagination** | Use `page` (1-indexed) for all paginated endpoints. Pass `pagination_token` from the previous response for content endpoints (`posts`, `comments`, `videos`, `images`, `recommendations`). |
| **`search_people` filters** | Combine `name`, `title`, `company`, `school`, `industry`, `geocode_location`, `current_company`, `profile_language`, `service_category` for precise targeting. All filters are optional. |
| **Success check** | `code = 0` → success. Any other value → failure. Always check the response code before processing data. |
| **Retry on 500** | If `code = 500`, retry the identical request up to 3 times with a 2–3 second pause between attempts before reporting the error. |
| **Cache first** | Always check the local `.keyapi-cache/` directory before issuing a live API call. |

author: KeyAPI
license: MIT
repository: https://github.com/EchoSell/keyapi-skills
---

## Error Handling

| Code | Meaning | Action |
|------|---------|--------|
| `0` | Success | Continue workflow normally |
| `400` | Bad request — invalid or missing parameters | Validate input against the tool schema; ensure `username` or `urn` is correctly provided |
| `401` | Unauthorized — token missing or expired | Confirm `KEYAPI_TOKEN` is set correctly; visit [keyapi.ai](https://keyapi.ai/) to renew |
| `403` | Forbidden — plan quota exceeded or feature restricted | Review plan limits at [keyapi.ai](https://keyapi.ai/) |
| `404` | Resource not found — user may not exist or profile is private | Verify the username; private or restricted profiles may return limited data |
| `429` | Rate limit exceeded | Wait 60 seconds, then retry |
| `500` | Internal server error | Retry up to 3 times with a 2–3 second pause; if it persists, log the full request and response and skip this node |
| Other non-0 | Unexpected error | Log the full response body and surface the error message to the user |
