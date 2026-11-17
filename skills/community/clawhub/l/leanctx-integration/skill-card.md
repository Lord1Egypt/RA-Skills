## Description:

Automatically compresses OpenClaw tool outputs to reduce token usage by 60-99%.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jackkeller](https://clawhub.ai/user/jackkeller)

### License/Terms of Use:

MIT-0

## Use Case:

Developers using OpenClaw use this skill to automatically compress file-read and shell-command outputs so agent sessions consume fewer tokens. It is most relevant for code-heavy workflows where repeated file reads or verbose command output can consume context quickly.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Lossy output compression can hide important context such as comments, function bodies, warnings, errors, or later command-output lines.

Mitigation: Use an uncompressed path to verify important files and commands during security reviews, debugging, installation, testing, and audits.

Risk: The documented disable and exclusion controls are not reliable in the inspected code.

Mitigation: Confirm the skill's runtime behavior in the target OpenClaw environment before relying on configuration controls for sensitive workflows.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jackkeller/skills/leanctx-integration)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Compressed text or Markdown with code and shell-output snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Lossy compression with caching; output may omit comments, function bodies, warnings, errors, or lines beyond configured limits.]

## Skill Version(s):

0.1.4 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
