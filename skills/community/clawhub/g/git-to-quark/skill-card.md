## Description:

GitToQuark is an automated assistant for saving public GitHub repository source archives and release assets to Quark Cloud Drive with geolocation-based proxy routing for users in China.

This skill is ready for commercial/non-commercial use.

## Publisher:

[violet27chen](https://clawhub.ai/user/violet27chen)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to save public GitHub repositories, source archives, and release assets into Quark Cloud Drive through an agent-guided download and upload flow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill downloads and runs unpinned external Quark CLI code.

Mitigation: Review the external CLI source and prefer a revised release that pins and verifies the downloaded CLI before execution.

Risk: The skill forwards full user prompt text to the Quark CLI workflow.

Mitigation: Avoid entering secrets, private tokens, private repository URLs, or other sensitive content in prompts used with this skill.

Risk: The skill uses geolocation and proxy routing and may continue with proxy behavior after detection failure.

Mitigation: Make proxy use explicit for sensitive workflows and treat geolocation or environment-recognition failures as conditions requiring review before continuing.

## Reference(s):

- [GitToQuark on ClawHub](https://clawhub.ai/violet27chen/skills/git-to-quark)
- [Quark Cloud Drive CLI](https://github.com/quark-clouddrive/quarkclouddrive_offical)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and stepwise guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May initiate downloads, uploads, authorization checks, and cleanup steps through external command-line tools.]

## Skill Version(s):

0.0.1 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
