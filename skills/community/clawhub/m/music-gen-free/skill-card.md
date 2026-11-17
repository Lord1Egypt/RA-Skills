## Description:

Generates AI music prompts and style-controlled music generation guidance for content creation and multimedia workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, developers, and solo operators use this skill to turn text inputs and style parameters into structured AI music generation guidance for content creation, design generation, and multimedia production workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests broad read, write, and shell execution permissions without clear music-specific limits.

Mitigation: Install only in an environment where those permissions are acceptable, or require the publisher to remove exec/write and document exact allowed operations before deployment.

Risk: Generated music guidance may include incorrect assumptions about copyright or commercial rights.

Mitigation: Review generated outputs and licensing claims before using generated music or prompts in commercial releases.

Risk: The artifact includes API key setup guidance.

Mitigation: Keep credentials in environment variables or a managed secret store and avoid pasting secrets into prompts, logs, or generated files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/music-gen-free)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, shell commands, guidance]

**Output Format:** [Markdown guidance with JSON-style result examples and optional shell snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The artifact describes music prompts, style parameters, status metadata, and optional environment configuration; actual audio generation depends on the hosting agent and connected services.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
