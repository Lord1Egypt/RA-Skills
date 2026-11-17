## Description:

OpenClaw documentation expert that answers setup, configuration, provider, troubleshooting, and release-change questions using live document fetching, BM25 search, and local cache tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alfonso46674](https://clawhub.ai/user/alfonso46674)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to answer OpenClaw setup, provider configuration, troubleshooting, and release-change questions from OpenClaw documentation and cached searches.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cache path validation can allow maintenance commands to write or delete files outside the intended cache.

Mitigation: Review before installing, validate cache paths, and avoid untrusted version values or environment overrides in less controlled agent environments.

Risk: Cache refresh, cache clearing, index build, document fetch, and change snapshot commands mutate local cache state.

Mitigation: Run cache.sh refresh, cache.sh clear-docs, build-index.sh fetch/build, and track-changes.sh snapshot only in trusted workspaces with intended cache locations.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/alfonso46674/skills/openclaw-sage)
- [OpenClaw Documentation](https://docs.openclaw.ai)
- [OpenClaw Website](https://openclaw.ai)
- [OpenClaw GitHub Repository](https://github.com/openclaw/openclaw)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown answers with cited documentation URLs, inline shell commands, and optional JSON from helper scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and either python3 or python; cache and indexing commands may read, write, or clear local cache state.]

## Skill Version(s):

0.3.1 (source: frontmatter, package.json, changelog released 2026-04-24, server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
