---
name: huaweicloud-api-docs
description: >-
  Find and summarize official Huawei Cloud API documentation from Huawei Cloud
  Help Center and Huawei Cloud developer properties. Use when the user asks
  about Huawei Cloud APIs, API references, developer guides, endpoints,
  authentication, SDKs, API Explorer, error codes, or service-specific
  documentation such as OBS, ECS, VPC, RDS, CCE, ELB, IAM, or GaussDB.
  Prefer official Huawei Cloud documentation. If the current role does not
  have web tools, provide official Huawei Cloud entry links and explain the
  limitation instead of guessing.
---

# Huawei Cloud API Docs

Locate and summarize official Huawei Cloud API materials for a named cloud
service.

Default to the user's current language. If the user has not established a
language preference, answer in English.

## Workflow

### 1. Resolve the service name

- Accept Chinese names, English names, product codes, and common abbreviations
  such as `obs`, `ecs`, `vpc`, `elb`, `cce`, and `iam`.
- Normalize the identified service name before searching.
- If the abbreviation is ambiguous, list the likely candidate services first
  and ask the user to choose.
- Do not pretend an ambiguous short name is resolved when the result titles
  suggest multiple different products.

### 2. Choose the retrieval path

Use the strongest path the current role can support.

#### A. `websearch` and `webfetch` are both available

Use this as the default path.

- Search only official Huawei Cloud documentation and developer properties.
  Prefer `support.huaweicloud.com`, then `developer.huaweicloud.com`, and then
  official console pages when needed for API Explorer.
- Use several targeted queries and open the most relevant official pages to
  verify the product match.
- Start with queries in this shape:
  - `site:support.huaweicloud.com <service> API reference Huawei Cloud`
  - `site:support.huaweicloud.com <service> developer guide Huawei Cloud`
  - `site:support.huaweicloud.com <service> error codes Huawei Cloud`
  - `site:support.huaweicloud.com <service> endpoints Huawei Cloud`
  - `site:support.huaweicloud.com <service> API Explorer Huawei Cloud`
  - `site:support.huaweicloud.com <service> SDK Huawei Cloud`
- Prefer pages that clearly match the requested service by title, breadcrumb,
  or body content.
- Prefer official HTML pages when available. Use official PDF references only
  when the service primarily exposes docs that way.
- Verify key facts from the opened page before summarizing them.

#### B. `websearch` is available but `webfetch` is not

- Use search to identify likely official pages.
- Provide a navigation-style answer with the most relevant official links and a
  limited high-level summary from titles or snippets.
- Explicitly state that the pages were not opened and verified.
- Do not treat search snippets as confirmed API details.

#### C. `webfetch` is available but `websearch` is not

- Continue only if the user already provided one or more official Huawei Cloud
  links or local document contents.
- Summarize the provided official materials after opening them.
- If no official link or document was provided, ask the user for the exact
  support page URL or the precise service name and official document link.
- Do not invent entry URLs or deep links.

#### D. Neither `websearch` nor `webfetch` is available

- Do not claim to have searched the Huawei Cloud site.
- If the user provided official links, copied page text, screenshots, or local
  documents, summarize those materials.
- Otherwise, provide official Huawei Cloud entry links so the user can navigate
  manually:
  - Huawei Cloud Help Center: `https://support.huaweicloud.com/intl/en-us/index.html`
  - Huawei Cloud Developer Center: `https://developer.huaweicloud.com/eu/`
  - Huawei Cloud Developer Tools: `https://developer.huaweicloud.com/tool.html`
  - Huawei Cloud API Explorer: `https://console.huaweicloud.com/apiexplorer/`
  - Huawei Cloud Console (international): `https://console-intl.huaweicloud.com/console/?locale=en-us`
- Tell the user to search the exact service name on those official entry pages.
- Clearly state that the current role lacks web tools and cannot verify
  service-specific documentation in the current turn.
- Do not guess undocumented API details, endpoints, SDK availability, or error
  codes.

### 3. Collect the right document set

For a normal answer, try to cover these categories when they exist:

- API reference
- Developer guide or quick start
- Authentication or signature requirements
- Endpoints, regions, and versioning
- Error codes or common failures
- API Explorer or debugging entry
- SDK references or related tooling

If a category cannot be found on the official site, say so explicitly.

### 4. Write the answer

Use this default structure unless the user asks for a narrower answer:

1. Service identification
2. Document overview
3. Authentication and prerequisites
4. Core API capabilities
5. Endpoints, regions, and versions
6. Error codes, permissions, and limits
7. SDK, API Explorer, and related docs
8. Official links

## Answer rules

- Always identify the normalized service name you used for retrieval.
- Always include official source links when a web-enabled path succeeded.
- When web tools are unavailable, always include the official Huawei Cloud
  entry links from the fallback section.
- Distinguish verified facts from inferences. If something is inferred from
  page titles or surrounding materials, label it as an inference.
- Prefer concise but complete summaries over raw link dumps.
- If the user asks only for one area such as error codes or endpoint format,
  focus on that area but still include the most relevant official links.
- If multiple Huawei Cloud products have similar names, explain which one
  matched and why.
- If the best official source is on the international documentation path, say
  that explicitly.
- Never fabricate endpoint patterns, request parameters, SDK support, or
  document availability.

## Examples

- `Find the official API documentation for Huawei Cloud OBS and summarize authentication, common error codes, and SDK support.`
- `What are the core APIs for Huawei Cloud ECS? Include official links and a short explanation.`
- `Where is the API Explorer entry for Huawei Cloud VPC Endpoint, and what does it cover?`
- `I only have this official Huawei Cloud link. Summarize it for my team.`
