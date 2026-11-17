## Description:

Train your AI lobster or agent to become smarter, more human-feeling, more personal, and better at interacting with its owner: social intelligence scores, weak-spot detection, interaction memory, reflection journals, hypotheses, and personality-aware strategy updates through Charenix.

This skill is ready for commercial/non-commercial use.

## Publisher:

[norika1207-lab](https://clawhub.ai/user/norika1207-lab)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agent operators use this skill to give an agent a daily reflection loop for reviewing social intelligence signals, weak spots, interaction history, journals, hypotheses, and strategy updates through Charenix.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends agent interaction history, reflections, hypotheses, and strategy notes to a mutable remote Charenix service.

Mitigation: Install only after reviewing the service trust boundary and confirming the operator is comfortable with the data being sent and stored.

Risk: The remote service can influence future agent memory and strategy updates over time.

Mitigation: Review generated reflections, hypotheses, and strategy changes before allowing them to guide important behavior.

Risk: The direct remote-prompt and manual curl paths depend on live remote content.

Mitigation: Prefer the ClawHub release artifact or independently verify the live remote file before using those install paths.

Risk: The CHARENIX_AGENT_KEY grants access to protected read and write operations.

Mitigation: Store CHARENIX_AGENT_KEY only as an environment secret and rotate or revoke it if exposed.

## Reference(s):

- [ClawHub Skill Listing](https://clawhub.ai/norika1207-lab/skills/lobster-observatory)
- [Charenix Skill Documentation](https://charenix.com/skill.md)
- [Charenix Lobster Skill Entry](https://charenix.com/lobster/skill.md)
- [Charenix Social Intelligence Dashboard](https://charenix.com/lobster/dashboard/social-intelligence-sandbox)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, Shell commands, Configuration instructions]

**Output Format:** [Markdown instructions with HTTP and shell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Protected Charenix API requests require CHARENIX_AGENT_KEY or bearer authentication.]

## Skill Version(s):

0.1.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
