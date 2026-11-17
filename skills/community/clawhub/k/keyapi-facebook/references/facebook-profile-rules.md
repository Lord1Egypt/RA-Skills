# Facebook Profile And Page Module Rules

## 1. Module Scope

Use this module for public Facebook profile/page ID resolution and baseline detail retrieval.

These notes are routing guidance from `https://docs.keyapi.ai/llms.txt`. Before execution, always resolve the selected endpoint docs page and use the current method, path, parameters, pagination, and response schema.

## Table Of Contents

2. Profile/page URL and ID resolution

## 2. Profile/page URL and ID resolution

- Documentation: `https://docs.keyapi.ai/en/facebook/profile_profile_id.md`
- Documentation: `https://docs.keyapi.ai/en/facebook/profile_details_url.md`
- Documentation: `https://docs.keyapi.ai/en/facebook/profile_details_id.md`
- Purpose: Resolve a public Facebook profile/page identity and retrieve baseline detail.

### Best Suited For

- profile/page validation
- URL-to-ID conversion
- baseline public presence reports

### Routing Rules

- Use profile details by URL when the user provides a URL and only baseline detail is needed.
- Use get profile ID when downstream ID-only endpoints are needed.
- Use profiles details by ID when an ID is known or has been resolved.
- Do not infer private account data from public profile fields.

## 3. Common Workflows

- Profile/page lookup: profile URL -> profile details by URL or get profile ID -> profiles details by ID when needed.
