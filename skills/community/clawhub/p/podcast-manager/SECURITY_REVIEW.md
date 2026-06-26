# DD Security/Privacy Review — podcast-manager

## Scope
- Skill instruction content (`SKILL.md`)
- Feed probe helper (`scripts/feed_probe.py`)

## Data handling
- Uses public RSS/Atom feeds by URL.
- Tracks only podcast metadata and local progress files.
- No API keys or credentials required.
- No external write actions.

## Risks
1. Malformed XML feeds could break parsing.
2. User-provided feed URLs could point to non-podcast content.
3. Metadata may include unexpected HTML/text.

## Mitigations
- Feed URLs must be HTTP/HTTPS and their hostnames resolve to public IP addresses; localhost, loopback, link-local, private, and IANA-reserved ranges are rejected after DNS resolution.
- HTTP responses are required to return a 2xx status and an XML/RSS/Atom-like Content-Type before any parsing occurs, and server-side HTTP errors are surfaced through structured failure messages.
- Downloads are streamed with a strict 5 MB limit and any overflow aborts the probe; suspicious XML constructs (DOCTYPE/ENTITY) are detected and rejected before parsing.
- XML parser errors and failed validations exit non-zero with sanitized JSON errors, and the skill outputs only the selected podcast metadata fields.
- Skill text forbids fabricating details and auto-subscribing without explicit intent.

## Residual risk
- Low: relies on external feed quality and availability.

## Verdict
- **PASS (Low risk)** for publication.
