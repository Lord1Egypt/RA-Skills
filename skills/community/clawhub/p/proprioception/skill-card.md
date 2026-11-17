## Description:

Self-spatial awareness for AI agents that monitors goal alignment, confidence boundaries, conversation drift, and response quality during an interaction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jcools1977](https://clawhub.ai/user/jcools1977)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to add local response-quality monitoring to agent conversations. It produces signals and alerts that can help an agent re-anchor to the user's goal, disclose uncertainty, or avoid drifting into unreliable answers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Always-on local monitoring may interrupt or reshape agent answers based on broad heuristic scores.

Mitigation: Deploy with explicit opt-in controls, visible disablement, and review of any intervention behavior before production use.

Risk: Sensitive conversation text can be passed to the local engine through command-line arguments.

Mitigation: Avoid sensitive conversations unless the host limits retained history and changes engine input to a protected channel such as stdin or an equivalent non-argument transport.

## Reference(s):

- [The Proprioceptive Model](references/proprioceptive-model.md)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [JSON or ASCII dashboard text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a local Node.js runtime and analyzes conversation text locally without external API calls.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
