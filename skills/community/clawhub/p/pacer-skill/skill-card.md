## Description:

Your AI career companion. Helps you scan your current situation, map possible paths, simulate futures, and track progress week by week.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hectormeta](https://clawhub.ai/user/hectormeta)

### License/Terms of Use:

MIT-0

## Use Case:

External users use Pacer to clarify career or startup options by scanning their current situation, comparing possible paths, simulating future outcomes, and tracking weekly progress. The skill is suited to career planning, transition planning, early startup direction finding, and personal productivity follow-up.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores sensitive CV, career, financial runway, network, motivation, and progress details in local memory.

Mitigation: Redact unnecessary CV contact details, avoid exact financial or sensitive personal facts unless needed, and review local memory retention before installation.

Risk: The skill renders user-derived data through generated HTML chart templates.

Mitigation: Render chart HTML only in a sandboxed context and properly escape interpolated values before display.

## Reference(s):

- [Pacer Skill on ClawHub](https://clawhub.ai/hectormeta/skills/pacer-skill)
- [Chart.js CDN referenced by chart templates](https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js)

## Skill Output:

**Output Type(s):** [text, markdown, HTML, guidance]

**Output Format:** [Conversational Markdown with snapshot cards, planning tables, weekly review text, and generated HTML chart blocks.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May parse CV files and persist career profile, financial runway, network, motivation, milestones, and progress details in local OpenClaw memory.]

## Skill Version(s):

0.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
