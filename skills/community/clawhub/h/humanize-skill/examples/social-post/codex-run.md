# Codex Skill E2E Run: Social Post

Run date: 2026-06-04
Host: Codex
Mode: agent-native semantic rewrite, no CLI or regex rewrite pass

## Scope

- Surface: personal social post.
- Audience: followers who respond better to understated build notes than launch copy.
- Goal: improve the post by keeping it personal, concise, and honest about what the skill can do.
- Evidence policy: do not imply automatic social scraping; say samples or exported posts.

## Voice Profile

- Source: `sample.txt`
- Style: short, informal, low-hype.
- Rhythm: small paragraphs and fragments.
- Constraint: allow personality, but no fake excitement or broad creator claims.

## AI-pattern Audit

- Removed launch cliche: "thrilled to announce".
- Removed inflated language: "groundbreaking", "AI era".
- Removed generic positioning: "empowers creators", "definitive solution".
- Replaced automatic social-history claim with user-controlled samples/exports.

## Fact Decisions

| Claim | Decision | Evidence handling |
| --- | --- | --- |
| Uses samples or exported posts | Kept | Supported by `evidence.md` |
| Builds a compact voice profile | Kept | Supported by `evidence.md` |
| Verifies every fact | Softened | Evidence supports lightweight fact-check pass, not perfect verification |
| Analyzes social media history automatically | Corrected | Evidence says only user-provided exports or explicit connection |

## Final Rewrite

Small ship: I made a skill for cleaning up AI-looking drafts.

It is not magic. It looks at the sample or export you choose, rewrites the draft in that direction, and checks claim-like sentences before they go out.

Useful little thing.

## Final Audit

- Kept the post short and understated.
- Removed automatic social-history and "verifies every fact" claims.
- Matched the sample's "not magic, useful checklist" tone.
