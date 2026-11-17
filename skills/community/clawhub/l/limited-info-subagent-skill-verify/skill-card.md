## Description:

Validate whether a skill can be executed successfully by a minimally informed subagent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[amourlion](https://clawhub.ai/user/amourlion)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill maintainers use this skill to test whether another skill can complete its intended behavior when a subagent receives only a minimal invocation and artifact, then report pass/fail findings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill spawns a subagent to test another skill, and the target skill may act on supplied files, links, or prompts in the workspace.

Mitigation: Use it in a controlled workspace and review any proposed edits or commands before accepting them.

Risk: Sparse test prompts can produce incomplete or misleading validation if the expected behavior is not represented by the minimal artifact.

Mitigation: Treat pass/fail output as acceptance-test evidence and review residual ambiguity before changing or releasing the target skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/amourlion/skills/limited-info-subagent-skill-verify)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown findings with a pass/fail verdict and improvement guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Concise, language-matched report; may include severity-labeled findings.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
