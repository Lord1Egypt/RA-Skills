## Description:

Build and deploy safety-profiled gogcli binaries with compile-time command removal for AI-agent use cases with restricted Google Workspace permissions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brennerspear](https://clawhub.ai/user/brennerspear)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to choose L1, L2, or L3 safety profiles, build gogcli binaries with commands removed at compile time, deploy them to remote hosts, and verify that blocked commands are unavailable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The restricted safety profiles and build process may grant more sensitive authority than the safety framing suggests.

Mitigation: Review the build source and profile files before installation, and pin the upstream repository to an audited commit.

Risk: Forwarding-capable filters, Drive sharing, token handling, or keyring access can expose data or extend account access unexpectedly.

Mitigation: Remove token export/import and keyring access from restricted profiles, and disable forwarding-capable filters and L1 Drive sharing unless explicitly required.

Risk: Remote deployment replaces a host binary with sudo privileges and can affect rollback behavior.

Mitigation: Require human confirmation for remote sudo deployment and rollback, and verify blocked and allowed commands after installation.

## Reference(s):

- [Safety Level Reference](references/levels.md)
- [L1 Draft Profile](references/l1-draft.yaml)
- [L2 Collaborate Profile](references/l2-collaborate.yaml)
- [L3 Standard Profile](references/l3-standard.yaml)
- [gogcli Safety Profiles PR](https://github.com/steipete/gogcli/pull/366)
- [L1 Profile Gist](https://gist.github.com/BrennerSpear/757e23d62af920c6e86630f2eab57dc9)
- [gogcli Safe Build Repository](https://github.com/drewburchfield/gogcli-safe.git)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash commands and references to YAML profile files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Selects among L1, L2, and L3 safety profiles and may direct use of local build and deploy scripts.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
