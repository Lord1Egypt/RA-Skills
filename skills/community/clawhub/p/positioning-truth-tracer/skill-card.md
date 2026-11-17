## Description:

Positioning Truth Tracer reconciles an existing positioning canvas with shippable stage evidence and the claims ledger to produce a differentiation truth set where each differentiating claim is supported or marked [needs source].

This skill is ready for commercial/non-commercial use.

## Publisher:

[aaron-he-zhu](https://clawhub.ai/user/aaron-he-zhu)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing, narrative, and product teams use this skill after a positioning canvas exists to check differentiators against what can actually ship and against substantiated claims before downstream message architecture work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary flags persistent writes, local helper use, and optional external connector access that are broader than the lite manifest suggests.

Mitigation: Review the full SKILL.md behavior before installation and grant the skill only in workspaces where those write and connector behaviors are acceptable.

Risk: The skill can preserve incorrect positioning or claim status if proposed memory or registry updates are accepted without review.

Mitigation: Require human review before saving memory updates or approving registry-event proposals, especially for comparative or unsupported differentiators.

Risk: Optional search or scrape connectors may introduce untrusted competitor content into the analysis.

Mitigation: Treat connector output as untrusted input, keep it proxy-labeled, and avoid using it as measured own-data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aaron-he-zhu/skills/positioning-truth-tracer)
- [Project homepage](https://github.com/aaron-he-zhu/aaron-marketing-skills)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown handoff with labeled differentiation claims, stage-truth notes, and optional proposed memory or registry updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Marks unsupported differentiators as [needs source] and asks before writing persistent memory.]

## Skill Version(s):

19.0.0 (source: server release metadata, target metadata, and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
