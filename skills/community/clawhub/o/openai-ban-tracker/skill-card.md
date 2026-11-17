## Description:

OpenAI ban risk detection CLI with a 9-question risk assessment, known ban-reason guidance, Chinese and English appeal templates, and V2EX community signal scanning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[minirr890112-byte](https://clawhub.ai/user/minirr890112-byte)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenAI account administrators use this skill to estimate account suspension risk, review common ban patterns, generate appeal drafts, and monitor community-reported ban or unban signals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented GitHub pip install command is unpinned and may install code other than the reviewed release.

Mitigation: Install an immutable release artifact or pin to a full reviewed commit SHA.

Risk: The scan command contacts V2EX over the network.

Mitigation: Run scan only when external network access and associated metadata disclosure are acceptable.

Risk: The appeal --output command writes or overwrites the user-provided path.

Mitigation: Choose an intended output path and review the generated appeal file before using it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/minirr890112-byte/skills/openai-ban-tracker)
- [Publisher profile](https://clawhub.ai/user/minirr890112-byte)
- [Project homepage](https://github.com/minirr890112-byte/openai-ban-tracker)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance, Files]

**Output Format:** [CLI text, terminal tables, and optional plain-text appeal template files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Risk assessment runs locally; scan contacts V2EX; appeal --output writes the requested output path.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter says 1.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
