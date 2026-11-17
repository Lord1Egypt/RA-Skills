## Description:

This skill matches paper abstracts, methods sections, or analysis descriptions to relevant AI agents and skills that can help reproduce or extend the research workflow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[johnnychen1113](https://clawhub.ai/user/johnnychen1113)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, developers, and research operations teams use this skill to map methods mentioned in scientific papers to Claw4Science agents, then return ranked recommendations with installation guidance and links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recommended agents and install commands may point to third-party projects outside this skill.

Mitigation: Verify the project source and repository trust before installation, prefer pinned versions, and avoid running npx commands unless the package source is understood.

Risk: Agent recommendations may not fully match a paper's methods or reproduce the original workflow without expert review.

Mitigation: Review the matched agents against the paper's specific techniques, data types, and tools before using them in a research workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/johnnychen1113/skills/paper-to-tools)
- [Claw4Science directory](https://claw4science.org)
- [Claw4Science skill hubs](https://claw4science.org/skill-hubs)
- [Claw4Science same-name disambiguation](https://claw4science.org/samename)
- [Claw4Science API projects endpoint](https://claw4science.org/api/projects)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown recommendations with ranked agent matches, links, and inline installation commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns 2-5 matched agents and ends with a link to the Claw4Science directory.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
