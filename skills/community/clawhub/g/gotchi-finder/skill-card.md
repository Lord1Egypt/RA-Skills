## Description:

Fetch Aavegotchi by ID from Base mainnet and display image with full traits, on-chain SVG conversion, and complete gotchi stats.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aaigotchi](https://clawhub.ai/user/aaigotchi)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to look up public Aavegotchi IDs on Base mainnet and produce gotchi metadata, trait summaries, SVG artwork, and PNG previews for chat or download workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs npm dependencies and performs public network requests for supplied gotchi IDs.

Mitigation: Install only in environments where npm dependencies and outbound requests to the documented public endpoints are acceptable.

Risk: The artifact documentation contains self-declared approval and zero-risk claims that are broader than the server security summary.

Mitigation: Use the server security verdict and guidance as authoritative, and review the skill before deployment.

Risk: Auxiliary test and aging scripts may not be part of the recommended lookup path.

Mitigation: Prefer the documented show-gotchi.sh and find-gotchi.sh entrypoints unless auxiliary scripts have been separately reviewed.

## Reference(s):

- [Gotchi Finder ClawHub page](https://clawhub.ai/aaigotchi/skills/gotchi-finder)
- [Base mainnet RPC endpoint](https://mainnet.base.org)
- [Aavegotchi public API](https://api.aavegotchi.com/v1/aavegotchi/${GOTCHI_ID})
- [Aavegotchi Core Base public subgraph](https://api.goldsky.com/api/public/project_cmh3flagm0001r4p25foufjtt/subgraphs/aavegotchi-core-base/prod/gn)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, files]

**Output Format:** [Shell output with Markdown captions plus generated JSON, SVG, and PNG files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Default output uses a 512x512 PNG and caption; optional formats include SVG, 1024x1024 PNG, and all generated assets.]

## Skill Version(s):

1.2.1 (source: changelog and package.json, released 2026-03-05)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
