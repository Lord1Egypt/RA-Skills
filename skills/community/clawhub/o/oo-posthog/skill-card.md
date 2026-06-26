## Description: <br>
Use this skill for PostHog requests involving reading, creating, updating, and deleting data through an OOMOL-connected account. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and analytics teams use this skill to inspect and manage PostHog projects, dashboards, insights, feature flags, cohorts, annotations, definitions, collaborators, and query results through an OOMOL-connected account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can change or delete PostHog dashboards, cohorts, feature flags, definitions, insights, collaborators, and related data. <br>
Mitigation: Require explicit user confirmation for actions marked write or destructive, including the exact target and payload. <br>
Risk: The skill operates through a connected PostHog account and may require sensitive credentials managed outside the skill. <br>
Mitigation: Install only when the publisher is trusted and use OOMOL-managed credentials rather than exposing raw tokens to the agent. <br>


## Reference(s): <br>
- [PostHog homepage](https://posthog.com) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-posthog) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return JSON data from PostHog connector actions when commands are executed.] <br>

## Skill Version(s): <br>
1.0.1 (source: server evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
