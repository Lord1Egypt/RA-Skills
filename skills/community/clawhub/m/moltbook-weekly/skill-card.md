## Description:

Generates weekly project reports in Markdown and provides guidance for publishing them to WeCom documents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rf-ai-wh](https://clawhub.ai/user/rf-ai-wh)

### License/Terms of Use:

MIT-0

## Use Case:

Project teams and operators use this skill to assemble weekly status reports from documented project data sources and prepare Markdown content for WeCom document publication.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated reports may include business data from documented local project data sources.

Mitigation: Review report contents before publishing and install only where access to those data sources is acceptable.

Risk: Generated shell or WeCom command examples may include untrusted titles or report content.

Mitigation: Inspect and sanitize generated commands before copying or executing them.

Risk: Reports written under /tmp may be exposed to other local users.

Mitigation: Use a controlled output path and remove temporary report files when they are no longer needed.

Risk: Publishing depends on configured WeCom/OpenClaw authority and may require manual action despite automation-oriented documentation.

Mitigation: Confirm the active WeCom/OpenClaw environment and user authority before publishing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/rf-ai-wh/skills/moltbook-weekly)
- [ClawHub publisher profile](https://clawhub.ai/user/rf-ai-wh)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown report text with command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can write generated reports to a local file path and print WeCom publishing steps.]

## Skill Version(s):

1.0.0 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
