## Description:

AI KEY·短命令 is a short-command alias that routes `/key` users to the main AI KEY toolbox entry point and clarifies that it is not for API keys, secrets, or credentials.

This skill is ready for commercial/non-commercial use.

## Publisher:

[iamzifei](https://clawhub.ai/user/iamzifei)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill as a shorter `/key` command that hands off to the main AI KEY toolbox for content and business decision workflows. It also tells agents not to use this skill for API keys, secrets, passwords, tokens, environment variables, or credentials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The fallback installation command uses a global npx install path and is not pinned to an immutable version.

Mitigation: Run it only after reviewing and trusting the iamzifei/aikey source, or install from an approved pinned source when required by local policy.

Risk: The alias depends on the main AI KEY skill being present; without it, the alias cannot perform the routed workflow.

Mitigation: Install and review the main AI KEY skill before relying on `/key` for content or business decision workflows.

Risk: Users may confuse the skill name with API keys, secrets, passwords, tokens, environment variables, or credentials.

Mitigation: Do not use this skill for credential-related requests; route those requests to the appropriate security or platform guidance.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/iamzifei/skills/key)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Routes users to the main AI KEY skill and may provide a global npx install command when that skill is missing.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
