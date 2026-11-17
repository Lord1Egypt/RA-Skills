## Description:

Image-crawler helps agents collect images from Baidu and Bing image search using keywords, optional keyword expansion, duplicate detection, progress monitoring, and JSON status output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mx2013713828](https://clawhub.ai/user/mx2013713828)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users can use this skill to have an agent plan and run bounded image collection jobs, monitor progress, and report downloaded image counts and output locations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bulk image collection may download content the user does not have rights to collect or reuse.

Mitigation: Confirm rights and applicable site terms before collection, and collect only content the user is permitted to store or use.

Risk: Large scraping jobs can consume disk space or run beyond the intended scope.

Mitigation: Keep counts small, choose a dedicated quota-limited output folder, and monitor JSON progress and stall events.

Risk: Downloaded files may be untrusted or malformed.

Mitigation: Treat downloaded files as untrusted until they are validated before opening, processing, or sharing.

Risk: Anti-scraping guidance could be misused to bypass site rules or terms of service.

Mitigation: Use troubleshooting only for legitimate access issues and do not use the skill to bypass access controls, rate limits, or terms.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mx2013713828/skills/image-crawler)
- [Customization and interface guide](references/customization.md)
- [Baidu image search endpoint](https://image.baidu.com/search/acjson)
- [Bing image search endpoint](https://www.bing.com/images/async)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Files, Markdown, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSONL progress events; downloaded image files are written to the configured output directory.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses --json mode for machine-readable start, info, search, progress, stall, error, and done events.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
