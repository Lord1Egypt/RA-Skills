## Description:

Skill Hunter helps agents search for existing skills, tools, workflows, repositories, APIs, and templates before implementation, then recommend the best candidate with risk, effort, and an approval prompt.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mturac](https://clawhub.ai/user/mturac)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use Skill Hunter to avoid rebuilding existing solutions by performing a discovery pass for reusable tools before coding, automation, integration, or content-generation work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill redirects many normal coding and automation requests into a discovery workflow, which may add extra steps or change the expected execution flow.

Mitigation: Review whether discovery-first behavior matches local agent policy before installing, and use the documented skip conditions for trivial or explicitly manual work.

Risk: The skill may lead an agent to search for external tools, repositories, registries, APIs, or workflows before implementation.

Mitigation: Require user approval before using any discovered third-party tool and review credentials, permissions, licensing, and maintenance status before installation or execution.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/mturac/skills/openclaw-skill-hunter)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown recommendation with approval options]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include candidate summaries, risk notes, effort estimates, and an approval prompt.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
