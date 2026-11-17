## Description:

Media Search helps agents query a media big-data API for news and social media content by keyword, time range, source, and content type.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liushilong-dodo](https://clawhub.ai/user/liushilong-dodo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, journalists, analysts, and content teams can use this skill to retrieve media articles and source material for reporting, background research, monitoring, competitive intelligence, and content planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles API credentials and access tokens through local storage and outbound API calls.

Mitigation: Install only when the media API integration is trusted, keep credentials in environment variables, enforce owner-only permissions on the token cache, and rotate tokens if local storage may have been exposed.

Risk: Transport and logging practices can expose token-bearing requests or weaken API confidentiality.

Mitigation: Enable normal TLS certificate verification before production use and remove or redact token-bearing request headers from logs.

Risk: Broad activation could run media searches or persist result files outside an explicit user workflow.

Mitigation: Activate the skill only for user-directed media searches and review generated result files before retaining or sharing them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/liushilong-dodo/skills/media-search)
- [Media big-data API endpoint](https://mbdapi.fzdzyun.com)
- [README](artifact/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands]

**Output Format:** [Markdown or JSON search results with source metadata, summaries, timestamps, and URLs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write result files under sources/ or to a user-specified JSON output path.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
