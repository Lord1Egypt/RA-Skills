## Description:

This skill helps agents query public Kuaishou/Kwai data for keyword video search, creator post lookup, and video comment retrieval.

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT

## Use Case:

Content creators, marketers, market researchers, and data analysts use this skill to collect structured public Kuaishou video, creator, and comment data for trend research, competitor monitoring, topic planning, and reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends user-provided keywords, Kuaishou URLs or IDs, limits, and the GUAIKEI_API_TOKEN to the third-party GuaiKei API.

Mitigation: Use it only when third-party API use is approved, avoid sending unnecessary inputs, and keep the API token scoped and protected.

Risk: Retrieved public comments, creator details, and video data are saved locally under logs/.

Mitigation: Limit collection to the task need, apply local access and retention controls, and delete exports that are no longer required.

Risk: Bulk collection or reuse of public platform data may create platform, privacy, or internal policy concerns.

Mitigation: Review Kuaishou platform rules, privacy obligations, and internal data-handling requirements before bulk export or redistribution.

## Reference(s):

- [Server-resolved GitHub provenance](https://github.com/why20261/kuaishou-decomposer)
- [ClawHub skill page](https://clawhub.ai/why20261/skills/kuaishou-decomposer)
- [GuaiKei Kuaishou data API](https://www.guaikei.com)
- [Complete option reference](references/options.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, JSON, configuration, guidance]

**Output Format:** [Markdown guidance with CLI commands and structured JSON command results.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Command results include status, error_code, request metadata, runtime metadata, and results; successful runs are also saved under logs/.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata; artifact metadata reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
