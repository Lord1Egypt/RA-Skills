## Description:

HardStop helps agents review shell commands and sensitive file reads before execution, blocking clearly dangerous patterns and requiring confirmation for risky actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[frmoretto](https://clawhub.ai/user/frmoretto)

### License/Terms of Use:

CC-BY-4.0

## Use Case:

Developers and agent operators use this skill to add a command-safety checklist before shell execution and file reads. It is intended to reduce accidental destructive commands, credential exposure, and unsafe bypasses by requiring block, warning, or confirmation behavior.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can reduce command-safety friction through /hs skip or /hs off controls.

Mitigation: Use bypass or disable controls only for a known command after explicit user intent, and review the separate Hardstop plugin before relying on those controls.

Risk: Command examples include destructive or credential-related strings that could be misread outside their safety-checklist context.

Mitigation: Treat those strings as block and warning patterns; evidence.security identifies them as examples of what the skill tells the agent to block rather than run.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/frmoretto/skills/hs)
- [Hardstop Plugin](https://github.com/frmoretto/hardstop)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline shell commands and decision checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May instruct the agent to stop, ask for confirmation, suggest safer alternatives, or run local Hardstop plugin control commands only when explicitly requested.]

## Skill Version(s):

1.4.8 (source: server release metadata; artifact frontmatter reports 1.5)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
