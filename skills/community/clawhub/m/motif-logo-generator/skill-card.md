## Description:

Helps agents generate motif-logo analysis outputs for DNA or protein sequences, currently as ASCII conservation logos or WebLogo command guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and data analysts use this skill to inspect conservation patterns in DNA or protein sequence sets and prepare reproducible motif-logo outputs from trusted sequence files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated WebLogo command text may include user-supplied sequence data.

Mitigation: Use only trusted sequence files in an isolated workspace, review generated commands before execution, and prefer invoking WebLogo safely without a shell.

Risk: The artifact documentation overstates generated image-format support relative to the packaged script.

Mitigation: Validate expected output mode before use and treat image generation as dependent on external WebLogo tooling unless the implementation is updated.

Risk: Dependencies are not pinned.

Mitigation: Pin and review runtime dependencies before deployment.

## Reference(s):

- [WebLogo](https://weblogo.berkeley.edu/)
- [ClawHub skill page](https://clawhub.ai/aipoch-ai/skills/motif-logo-generator)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text or Markdown with inline shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write requested text output files; WebLogo mode emits command text rather than executing WebLogo directly.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
