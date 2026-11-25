## Description:

Verifies a package exists before install, defending against hallucination and slopsquatting

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill before adding or recommending a package to confirm that its name exists in the relevant registry and to catch likely typosquats.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review was partial because four referenced local paths were not present in the scanned artifact.

Mitigation: Review the unresolved paths and verify the artifact contents before installation.

Risk: A registry lookup can be unverified during network failures, and the guard reports that state without blocking the install.

Mitigation: Treat unverified packages as unresolved and confirm their registry entry before installing or recommending them.

## Reference(s):

- [Night Market Imbue project](https://github.com/athola/claude-night-market/tree/master/plugins/imbue)
- [ClawHub release](https://clawhub.ai/athola/skills/nm-imbue-dependency-verification)
- [Registry checks](modules/registry-checks.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands]

**Output Format:** [Markdown instructions with inline shell examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.10.4 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
