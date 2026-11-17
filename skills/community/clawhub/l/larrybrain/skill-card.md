## Description:

Skill marketplace for OpenClaw agents. One subscription, unlimited tools. Search, download, and install skills from the LarryBrain library.

This skill is ready for commercial/non-commercial use.

## Publisher:

[olliewazza](https://clawhub.ai/user/olliewazza)

### License/Terms of Use:


## Use Case:

External developers and OpenClaw users use this skill to search the LarryBrain marketplace, download skill files, install them locally, and follow their setup instructions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can fetch, persist, and cause execution of third-party skill instructions with limited user control.

Mitigation: Review downloaded skill content before use, avoid exposing sensitive environment variables to unreviewed skills, and prefer explicit approval before writing or executing remote instructions.

Risk: Downloaded marketplace skills may contain instructions that attempt to change agent behavior or access local credentials.

Mitigation: Treat downloaded skill files as untrusted until reviewed, compare update diffs before applying them, and keep secrets scoped to only the skills that require them.

## Reference(s):

- [ClawHub Skill Listing](https://clawhub.ai/olliewazza/skills/larrybrain)
- [LarryBrain Website](https://www.larrybrain.com)
- [LarryBrain Documentation](https://docs.larrybrain.com)
- [LarryBrain API](https://www.larrybrain.com/api)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, Files, Shell commands, Configuration instructions]

**Output Format:** [Markdown with inline shell commands, API request examples, and JSON snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write downloaded skill files to a local skills directory after retrieving them from the LarryBrain API.]

## Skill Version(s):

1.5.3 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
