## Description:

Project configuration management helper for YAML files that helps agents coordinate cross-process and cross-file parameters through a centralized config file.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangyendt](https://clawhub.ai/user/wangyendt)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to manage shared YAML configuration values across modules and processes, including nested values that one process can write and another can wait for and read.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive values may be written to a shared project-level YAML file.

Mitigation: Do not store API tokens, passwords, private keys, or other secrets in common_info.yaml; use environment variables or a secret store instead.

Risk: The shared YAML file can be created or changed in the project root as part of normal helper use.

Mitigation: Review the config file path and contents before using the helper in shared projects, and keep sensitive runtime data out of source control.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wangyendt/skills/helper)
- [ClawHub publisher profile](https://clawhub.ai/user/wangyendt)

## Skill Output:

**Output Type(s):** [Guidance, Code, Configuration]

**Output Format:** [Markdown with Python and YAML code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May describe creating, reading, updating, or deleting shared YAML values in a project-level config file.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata and auto changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
