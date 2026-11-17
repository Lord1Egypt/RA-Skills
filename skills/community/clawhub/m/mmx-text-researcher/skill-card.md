## Description:

Conducts deep multi-source research and synthesis with structured output using MiniMax CLI for complex investigation and fact verification tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ariffazil](https://clawhub.ai/user/ariffazil)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and analysts use this skill to run MiniMax CLI research workflows that search, synthesize, structure, verify, and compile findings for complex questions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and retrieved research content may be sent to MiniMax during use.

Mitigation: Use the skill only for non-sensitive research unless the user is comfortable sending that content to MiniMax.

Risk: The artifact documents an API-key login command that could expose secrets through command-line history or process inspection.

Mitigation: Avoid passing real API keys in command-line arguments; use a safer authentication method if the CLI supports one.

Risk: Broad activation language may cause the skill to run for more knowledge tasks than intended.

Mitigation: Narrow activation conditions before deployment so it is invoked only for appropriate research workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ariffazil/skills/mmx-text-researcher)
- [Publisher profile](https://clawhub.ai/user/ariffazil)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown, JSON, tables, briefs, reports, verdicts, and shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include source citations, confidence levels, unknowns or gaps, and verification notes.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
