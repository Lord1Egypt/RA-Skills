## Description:

Given an Amazon ASIN and marketplace, this skill guides an agent through competitor selection, LinkFox/Keepa/SellerSprite/ABA/AIGC data collection, comparative analysis, SWOT synthesis, and an 11-section HTML competitor report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Marketplace operators and e-commerce analysts use this skill to compare an Amazon target ASIN against selected competitors, gather marketplace and keyword evidence, and generate a structured competitor intelligence report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive LinkFox credentials and onboarding tokens may be sent to environment-configurable endpoints.

Mitigation: Install only in trusted runtimes and leave LINKFOX_TOOL_GATEWAY, LINKFOX_AGENT_API_URL, LINKFOX_LOGIN_API_URL, and LINKFOX_AGENT_USER_API_URL unset unless the alternate host is fully trusted.

Risk: Uploaded files and generated report links may be publicly accessible.

Mitigation: Review report and upload contents before sharing, and avoid uploading confidential data unless public access is acceptable.

Risk: The workflow depends on external marketplace, keyword, ABA, AIGC, and report-generation services, so missing or unavailable upstream data can affect completeness.

Mitigation: Treat unavailable fields as gaps, preserve source traceability in reports, and avoid unsupported conclusions when required data is not returned.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/linkfox-ai/skills/linkfox-expert-amazon-multi-competitor-analysis)
- [LinkFox Skills](https://skill.linkfox.com/)
- [Competitor selector scoring model](artifact/skills/competitor-selector/references/scoring-model.md)
- [Competitor research pipeline I/O](artifact/skills/competitor-research-pipeline/references/io.md)
- [Competitor research data tools reference](artifact/skills/competitor-research-pipeline/references/data-tools-reference.md)
- [Analysis report component library](artifact/skills/linkfox-report-generator/references/analysis-layouts.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance, JSON data structures, shell commands, and HTML report files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces an 11-section HTML competitor report and intermediate JSON analysis artifacts; report values are expected to be traceable to returned skill data.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
