## Description:

A documentation-only meta-skill that guides agents in designing, generating, and validating zero-exposure skills for MGC Blackbox 1.5.4.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zkeviny](https://clawhub.ai/user/zkeviny)

### License/Terms of Use:

MIT

## Use Case:

Developers and technical users use this skill to design and validate MGC Blackbox skills intended to keep credentials outside agent-visible prompts and outputs. It guides credential, script, workflow package, and sealed delivery design with templates and an acceptance checklist.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated scripts may mishandle credentials or perform unintended actions when executed.

Mitigation: Review generated scripts before execution, and keep credential values out of prompts and result files.

Risk: A sealed capsule can run with the receiving user's permissions; encryption does not limit its runtime permissions.

Mitigation: Import capsules only from trusted sources and review the generated scripts before execution.

Risk: Installing the documented dependency without quoting its version constraint can be misparsed, or the installed MGC version may be too old.

Mitigation: Quote the dependency requirement during installation and confirm the required MGC version is available.

## Reference(s):

- [Key-Safe Skill Generator on ClawHub](https://clawhub.ai/zkeviny/skills/key-safe-skill-generator)
- [MGC Blackbox skill specification](mgc/docs/skill_spec.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Configuration, Shell commands]

**Output Format:** [Markdown instructions with code and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance and templates for user-reviewed skill specifications, scripts, workflow packages, and sealed delivery.]

## Skill Version(s):

2.0.0 (source: SKILL.md frontmatter, manifest)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
