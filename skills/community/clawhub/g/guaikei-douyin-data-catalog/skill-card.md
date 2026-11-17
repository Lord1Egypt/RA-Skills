## Description:

This skill helps agents collect public Douyin data for keyword search, creator post retrieval, video comment analysis, and real-time hot-list lookup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and content teams use this skill to query public Douyin results, monitor competitor accounts, inspect comment feedback, and track trending topics through structured command outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends Douyin keywords, account URLs, video URLs, and GUAIKEI_API_TOKEN values to Guaikei's service.

Mitigation: Use only approved tokens, avoid sensitive query material, and run the skill only when sending that data to Guaikei is acceptable.

Risk: Result JSON files may be saved locally under logs and can contain collected social data.

Mitigation: Review log retention, access controls, and cleanup practices before using the outputs in shared environments.

Risk: Server evidence reports misleading token-error behavior and promotional contact output despite the skill text claiming neutral errors.

Mitigation: Treat authentication failures as untrusted diagnostic output and do not expose raw stderr to end users without review.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/engheng-art/skills/guaikei-douyin-data-catalog)
- [Guaikei service site](https://www.guaikei.com)
- [Complete option reference](references/options.md)
- [Input and output JSON schemas](assets/*.schema.json)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Analysis, Files, Guidance]

**Output Format:** [JSON on stdout, diagnostic text on stderr, and optional local JSON log files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 16.14 or newer and a GUAIKEI_API_TOKEN; each command can return up to 10000 records.]

## Skill Version(s):

1.0.0 (source: release metadata, package.json, references/changelog.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
