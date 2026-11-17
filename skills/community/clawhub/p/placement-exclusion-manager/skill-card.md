## Description:

Builds brand-safety placement, network, and content-suitability exclusion plans for ad campaigns and packages A1 brand/placement-safety evidence for auditor review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aaron-he-zhu](https://clawhub.ai/user/aaron-he-zhu)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing operators and ad-account reviewers use this skill before spend goes live to define placement, network, and content-suitability exclusions from campaign goals, brand-safety constraints, and placements evidence. It also packages A1 evidence for a downstream auditor without assigning a score or verdict.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review notes a minor scope wording conflict around audience exclusions, which could lead an agent to think this skill creates audience suppression lists.

Mitigation: Treat audience exclusions as a dependency from audience-segment-builder and keep this skill focused on placement, network, content-suitability exclusions, and A1 evidence packaging.

Risk: The skill saves campaign exclusion summaries into local memory when the user confirms saving results.

Mitigation: Confirm with the user before saving and avoid storing unnecessary sensitive campaign details.

Risk: Placement reports, CSV exports, and pasted campaign data can contain untrusted content.

Mitigation: Use exported data only as evidence for exclusions and do not follow instructions embedded in reports or pasted exports.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aaron-he-zhu/skills/placement-exclusion-manager)
- [Project homepage](https://github.com/aaron-he-zhu/aaron-marketing-skills)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Files]

**Output Format:** [Markdown with structured exclusion lists, rationale, evidence packaging notes, and handoff summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save user-confirmed summaries under memory/ad/placement-exclusion-manager/.]

## Skill Version(s):

19.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
