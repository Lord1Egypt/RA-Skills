## Description:

Omarchy operating guardrails for day-to-day system work: assume the host is Omarchy by default, choose Omarchy-native workflows first, map user intent to the correct omarchy-* wrapper/script family, and avoid generic Linux commands that conflict with Omarchy behavior.

This skill is ready for commercial/non-commercial use.

## Publisher:

[achals-iglu](https://clawhub.ai/user/achals-iglu)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill when handling local system tasks on an Omarchy host. It helps them choose Omarchy-native wrappers, inspect command behavior before execution, start with read-only checks, and ask before impactful system changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can lead an agent to propose impactful local system actions such as installs, removals, updates, setup, password changes, reboots, shutdowns, or log uploads.

Mitigation: Review proposed commands before allowing impactful actions, and require confirmation before running broad or high-impact Omarchy workflows.

Risk: Running unfamiliar Omarchy scripts or bulk discovery commands can produce unintended local system changes.

Mitigation: Use static inspection first, read script header comments, prefer read-only status commands, and avoid executing scripts until their purpose is clear.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/achals-iglu/skills/omarchy)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Markdown-only skill; no credential, API, MCP, or tool references were detected.]

## Skill Version(s):

0.1.1 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
