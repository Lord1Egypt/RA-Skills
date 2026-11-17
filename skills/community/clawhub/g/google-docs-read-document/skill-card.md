## Description:

Atomic node skill to read a Google Doc using the gog CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zvirb](https://clawhub.ai/user/zvirb)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to retrieve the plain text contents of a Google Doc through the gog CLI when they have a document ID and appropriate access.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The command template uses an unvalidated Google Doc ID in a terminal command.

Mitigation: Install only when document IDs come from trusted sources or the runtime passes CLI arguments safely; prefer validating Google Doc IDs and invoking gog with structured arguments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zvirb/skills/google-docs-read-document)

## Skill Output:

**Output Type(s):** [Shell commands, Text]

**Output Format:** [Plain text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the gog CLI and a Google Doc ID that the runtime is authorized to access.]

## Skill Version(s):

1.0.2 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
