## Description:

Helps Sora2 creators and analysts review works and creator activity and run video-generation workflows through the MaxHub API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiewxx](https://clawhub.ai/user/xiewxx)

### License/Terms of Use:

MIT-0

## Use Case:

Sora2 creators and analysts can use the skill to review works, comments, Remix activity, and creator profiles, and to support video generation and media workflows through MaxHub. Requests involving writes, uploads, or downloads require confirmation under the skill's documented usage rules.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan marks the skill suspicious, citing reported misleading consent records, behavior mismatches, and privacy and installation concerns; the scan is partial.

Mitigation: Avoid installation until consent-record behavior and download-denial handling are clarified, privacy disclosures are added, and the package is pinned to a reviewed version.

Risk: The skill sends credentials and user-supplied identifiers, keywords, or URLs to the third-party MaxHub API service.

Mitigation: Use only authorized data, minimize personal data, and keep API keys and other secrets out of logs and prompts.

## Reference(s):

- [Server-resolved source repository](https://github.com/XieWxx/maxhub-api-skills/tree/main/maxhub-sora2)
- [MaxHub API service](https://www.aconfig.cn)
- [Recipe index](references/recipes/_index.md)
- [Parameter and field-flow reference](references/param-mappings.md)
- [Sora2 developer platform](https://open.sora2.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Analysis, Guidance]

**Output Format:** [Natural-language responses, summaries, and structured reports in Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include retrieved Sora2 content or media URLs; write, upload, and download actions require confirmation.]

## Skill Version(s):

0.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
