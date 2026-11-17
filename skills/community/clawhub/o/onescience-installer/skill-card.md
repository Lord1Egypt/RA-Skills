## Description:

Guide remote installation of OneScience on DCU clusters via SSH with strict remote-only execution rules.

This skill is ready for commercial/non-commercial use.

## Publisher:

[onescience-ai](https://clawhub.ai/user/onescience-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to plan and execute a remote-only OneScience installation on DCU cluster hosts over SSH. It helps select the target host and science domain, generate the install sequence, and report verification steps and installation risks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads the user's full SSH configuration to discover remote hosts.

Mitigation: Provide the intended host directly when possible, review the selected host before connection, and use a least-privileged remote account.

Risk: The remote install flow uses current upstream tools and installation scripts without pinned versions.

Mitigation: Review the generated remote commands and pin or verify the uv version and OneScience commit before execution.

## Reference(s):

- [OneScience Installer ClawHub page](https://clawhub.ai/onescience-ai/skills/onescience-installer)
- [Publisher profile](https://clawhub.ai/user/onescience-ai)
- [Project homepage](https://github.com/onescience-ai/oneskills)
- [OneScience repository used by install sequence](https://gitee.com/onescience-ai/onescience)
- [Domain map](docs/domain-map.md)
- [Install sequence](docs/install-sequence.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with text, YAML, and inline bash command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Structured sections for environment check, install plan, commands, verification, and risks.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter lists 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
