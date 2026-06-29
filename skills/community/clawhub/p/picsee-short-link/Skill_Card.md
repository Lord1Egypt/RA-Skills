# Skill Card: PicSee Short Link

> Per-skill release record. Lets a reviewer understand the skill's purpose, owner,
> output, risks, and release evidence without reading the source first.
> Format follows the NVIDIA Skill Card structure (https://docs.nvidia.com/skills/skill-cards).

## Description

PicSee URL shortener exposed to AI agents via MCP — shorten URLs, generate QR codes (client-side recipe), view rich click analytics (daily / platform / referrer / region / audience), and manage links (create / list / edit / delete).

## Owner

- **Maintainer**: PicSee Inc. (`picsee`)
- **Repository**: https://github.com/PicSeeInc/picsee-short-link
- **Contact**: https://picsee.io/developers

## License / Terms of Use

- **Skill license**: MIT
- **Service terms**: Use of the PicSee API and MCP server is governed by PicSee's Terms of Service and API plan limits (see https://picsee.io). API quota and lookback windows depend on the account's plan tier.

## Use Case

- **Target users**: AI agents and their operators who need to shorten links, attribute API usage, and read per-link click analytics from inside an MCP-compatible client.
- **Primary applications**: marketing campaign link creation with UTM/attribution, branded short-domain (BSD) management, device-targeted redirects, and analytics reporting (clicks, platforms, referrers, regions, audience labels).
- **Anonymous mode**: `create_short_link` only, pinned to `pse.is`, no attribution/filtering.
- **Authenticated mode (OAuth 2.1)**: full 15-tool surface.

## Deployment Geography

- **Intended regions**: global. No geographic restriction on the skill.
- **Backend endpoints**: `api.picsee.io` (MCP server) and `public-api-oauth.picsee.io` (OAuth 2.1 authorization server). Analytics timestamps are expressed in **Taipei time** (`YYYY-MM-DDTHH:mm:ss`).
- **Network requirement**: outbound internet access to the two endpoints above.

## Known Risks and Mitigations

| Risk | How it could fail | Mitigation |
|------|-------------------|------------|
| Sensitive data in shortened URLs | A destination URL that carries auth tokens, session IDs, or PII in its query string is sent to PicSee and becomes publicly resolvable via the short link | Don't shorten URLs that contain secrets; review/strip query params with the user before calling `create_short_link`. |
| Third-party data egress via recipes | The QR and chart recipes send the short link / click time-series to `api.qrserver.com` and `quickchart.io` — services outside PicSee | These composes are optional and client-side; skip them or render locally when the link or data is sensitive. |
| Unintended link mutation by the agent | OAuth `user:write` lets the agent edit or delete **any** of the account's links, not only ones it created | Confirm edit/delete actions with the user first; `delete_short_link` defaults to recoverable trash (≤30 days). |

## References

- Skill definition: [SKILL.md](SKILL.md)
- User guide: [README.md](README.md)
- PicSee website: https://picsee.io
- Developer docs: https://picsee.io/developers
- MCP spec: https://modelcontextprotocol.io
- OAuth 2.1 (MCP profile): https://modelcontextprotocol.io/specification/draft/basic/authorization

## Skill Output

- **Transport**: MCP over Streamable HTTP (`https://api.picsee.io/mcp`), or stdio bridge via `npx mcp-remote`.
- **Primary output**: `create_short_link` returns `picseeUrl` (the shortened link).
- **Analytics output**: structured JSON — overview totals, daily time-series, and breakdowns by platform / referrer / region / audience label.
- **Composed recipes (client-side)**: QR code via `api.qrserver.com`; daily-clicks chart via `quickchart.io`.
- **Tool count**: 15 total (`create_short_link` anonymous-capable; remaining 14 require OAuth).

## Skill Version

- **Current version**: 3.0.2

| Version | Published | Notable change |
|---------|-----------|----------------|
| 3.0.2 | 2026-06-04 | Added Hermes Agent (Nous Research) install steps to the README; clarified `get_my_tags` result shape as `{ id, value }`. No behavioral change to the skill. |
| 3.0.1 | 2026-06-02 | Added this Skill Card (NVIDIA Skill Card format); no behavioral change to the skill. |
| 3.0.0 | 2026-05-20 | Migrated from a Node.js CLI (encrypted on-disk token) to an MCP server with OAuth 2.1 + PKCE; analytics split into 6 granular tools. |

## Ethical Considerations

- **No deceptive linking**: short links must not be used for phishing, malware distribution, or to disguise malicious destinations; such use violates PicSee Terms.
- **Attribution honesty**: `externalId` is for usage attribution, not user tracking — do not encode personal identifiers.
- **Privacy by design**: audience-label and region data are aggregated and gated (>100 unique clicks; country-level only) to prevent deanonymization.
- **User consent**: authenticated operations require an explicit browser OAuth sign-in granting `user:read` + `user:write`; the skill never bypasses or caches that consent.
