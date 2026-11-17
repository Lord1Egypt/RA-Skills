## Description:

LYGO Kickstart Wizard provides plain-English onboarding for the ClawHub lattice by mapping ecosystem entry points, checking public lattice health, analyzing user-provided text for ops signals, and guiding mint-to-verify-to-anchor workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deepseekoracle](https://clawhub.ai/user/deepseekoracle)

### License/Terms of Use:

MIT No Attribution (MIT-0)

## Use Case:

External users and developers use this skill to choose the right LYGO or ClawHub next step, run basic lattice checks, analyze explicitly provided text, and understand minting workflows in plain language.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The analysis feature may import a local companion Python module that is outside this release artifact.

Mitigation: Use analyze only with a trusted lygo-ops-detector installation, and avoid private or sensitive text unless that local code has been reviewed.

Risk: Install guidance uses mutable latest-version commands.

Mitigation: Prefer pinned, trusted installer and companion versions before deployment.

Risk: The security verdict requires review before installation.

Mitigation: Review the security summary, run the included self-check, and confirm the fixed network and opt-in file/write behavior before use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/deepseekoracle/skills/lygo-kickstart-wizard)
- [Publisher Profile](https://clawhub.ai/user/deepseekoracle)
- [Project Homepage](https://github.com/DeepSeekOracle/lygo-protocol-stack/tree/main/docs/skills/lygo-kickstart-wizard)
- [Quickstart](examples/quickstart.md)
- [LYGO adoption roadmap](references/ROADMAP.md)
- [Security - LYGO Kickstart Wizard v1.0.0](references/SECURITY.md)
- [SkillSpector - lygo-kickstart-wizard v1.0.0](references/SKILLSPECTOR_AUDIT.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown and terminal-oriented text with command examples and JSON-style results where applicable]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May perform fixed allowlist HTTPS GET requests for lattice health and may read user-specified files only for selected intents.]

## Skill Version(s):

1.0.0 (source: frontmatter, claw.json, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
