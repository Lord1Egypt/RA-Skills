## Description:

Spawn isolated sub-agents representing distinct worldviews (Elon, Capitalist, Monkey) to debate decisions from multiple angles, expose blind spots through disagreement, and capture debate outputs for future reference.

This skill is ready for commercial/non-commercial use.

## Publisher:

[latentfreedom](https://clawhub.ai/user/latentfreedom)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to stress-test decisions by asking isolated persona agents to argue from distinct viewpoints, then summarize tensions and preserve the result as a Markdown decision archive.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Copy-paste shell workflows can run unintended commands.

Mitigation: Review the helper script and generated commands before execution, especially when debate topics come from untrusted or shared sources.

Risk: Debate archives may contain sensitive decision context, customer data, regulated data, or private session transcript excerpts.

Mitigation: Redact sensitive content and protect archive storage before saving or sharing debate outputs.

Risk: CLI install or publishing instructions may drift or resolve to unexpected versions.

Mitigation: Pin CLI install instructions and review release commands before reuse.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/latentfreedom/skills/multi-viewpoint-debates)
- [Publisher profile](https://clawhub.ai/user/latentfreedom)
- [how-to-debate.md](references/how-to-debate.md)
- [elon.md](references/elon.md)
- [capitalist.md](references/capitalist.md)
- [monkey.md](references/monkey.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and persona response text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update a local debate archive when the user follows the provided workflow.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
