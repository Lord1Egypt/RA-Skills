## Description:

Generates nine stylistically varied Chinese prose essays from a topic and can optionally score and rank them.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dthinkr](https://clawhub.ai/user/dthinkr)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to request a batch of Chinese prose essays on a topic, save the generated essays as local Markdown files, and review a compact summary table with optional scoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends email addresses and writing topics to a hosted third-party service.

Mitigation: Require explicit user consent before registration or generation requests, and disclose what information is sent to prose-kit.com.

Risk: Raw shell and Python snippets handle user-controlled topic values and write local files.

Mitigation: Escape command inputs, validate API responses, sanitize filenames, and confine writes to the intended prose-kit-output/ directory.

Risk: The security evidence marks the release as suspicious due to account, email, command, and file-write behavior.

Mitigation: Review and scan the skill before deployment, and install only when the data-sharing and local-write behavior is acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dthinkr/skills/prose-kit)
- [Publisher profile](https://clawhub.ai/user/dthinkr)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and generated Markdown essay files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Saves generated essays under prose-kit-output/ and prints a summary table instead of full essay text.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
