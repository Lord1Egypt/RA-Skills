## Description:

Generates detailed livestream replay review and growth-planning reports from client and session data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ahsbnb](https://clawhub.ai/user/ahsbnb)

### License/Terms of Use:

MIT-0

## Use Case:

External livestream sellers, operators, and reviewing agents use this skill to prepare replay analysis and growth-plan reports for a named client and session from livestream data, audience profile, and transcript files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can process sensitive customer profiles, livestream data, and transcripts.

Mitigation: Use it only with data that is approved for the configured model provider, and treat stdout, prompt files, and generated reports as sensitive.

Risk: The optional model call can send customer materials to a configurable external endpoint.

Mitigation: Review the configured provider and prefer trusted HTTPS endpoints before enabling direct model calls.

Risk: The API key is read from the local OpenClaw configuration file.

Mitigation: Protect the configuration file and avoid sharing logs or outputs that might expose operational details.

Risk: Client and session values are used to locate input files before path validation is added.

Mitigation: Use trusted client and session names, and validate paths before running the skill with untrusted input.

## Reference(s):

- [Live Replay Analyzer ClawHub page](https://clawhub.ai/ahsbnb/skills/live-replay-analyzer)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown report or assembled text prompt]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can print an assembled prompt or save a timestamped Markdown report when model calling is enabled.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
