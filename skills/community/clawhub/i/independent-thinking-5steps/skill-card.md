## Description:

独立思考五部曲 guides agents through a five-step self-validation workflow for architecture discussion, debugging, retrospectives, decisions, and uncertain knowledge.

This skill is ready for commercial/non-commercial use.

## Publisher:

[markma84](https://clawhub.ai/user/markma84)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users can use this skill to structure deeper thinking before acting on architecture, troubleshooting, retrospective, decision, or uncertain-knowledge tasks. The workflow emphasizes retrieving prior experience, checking conclusions against a wiki, and closing the loop by saving review conclusions for future use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow requires an unaudited local vector-search script.

Mitigation: Install only after reviewing and trusting the local script, and confirm what task context will be sent to it.

Risk: The workflow disables platform memory search in favor of a custom vector and wiki backend.

Mitigation: Prefer deployments that keep platform memory controls intact or document why the custom backend is required.

Risk: The workflow saves review conclusions into a persistent wiki without clear user control.

Mitigation: Ask before writing to persistent knowledge stores and provide a way to inspect or remove saved conclusions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/markma84/skills/independent-thinking-5steps)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown or text guidance with inline shell commands and checklist-style review notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May rely on a local vector-search script and wiki-backed knowledge checks when the triggering task warrants the full workflow.]

## Skill Version(s):

5.0.0 (source: server release evidence and skill body release note)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
