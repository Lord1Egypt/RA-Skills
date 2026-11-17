## Description:

Routes any task to the right specialist agent automatically — multi-agent task routing with keyword matching.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tiny-coder-2104](https://clawhub.ai/user/tiny-coder-2104)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to route tasks, tickets, alerts, and agent-swarm work to a matching specialist agent based on keyword patterns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad keyword routing can assign sensitive, ambiguous, or high-impact tasks to the wrong specialist.

Mitigation: Narrow activation criteria, customize keyword mappings for the deployed agent set, and review routing results before using them in automated workflows.

Risk: The optional external API example could expose sensitive tickets, prompts, incidents, or customer data if used with an untrusted endpoint.

Mitigation: Use only trusted endpoints and redact sensitive content before sending task text to an external service.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tiny-coder-2104/skills/oracle-coordination)
- [Server-resolved GitHub provenance](https://github.com/tiny-coder-2104/toolbox/tree/master/clawhub-skills/oracle-coordination)
- [Publisher homepage](https://tinycoderstudio.gumroad.com/l/7-agent-skills-pack)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JavaScript and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Routes are keyword-pattern based and intended to be customized for local agent names and workflows.]

## Skill Version(s):

0.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
