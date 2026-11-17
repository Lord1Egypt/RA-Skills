## Description:

Use when looking for a CLI, API wrapper, scraper, data-source tool, automation tool, or focused agent skill for a task; searches the Printing Press Library and installs matching tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tmchow](https://clawhub.ai/user/tmchow)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to discover focused CLIs, API wrappers, scrapers, automation tools, data-source tools, and matching agent skills in the Printing Press Library. It helps select and install a narrow tool for a specific task while preserving approval and verification checkpoints.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mutable package-manager commands can install or overwrite local CLIs and future agent skills.

Mitigation: Review the selected catalog entry before installation, prefer pinned or reviewed versions where possible, and require explicit approval before install, overwrite, or bulk update commands.

Risk: Recurring update jobs create durable side effects that may refresh third-party code later without immediate operator attention.

Mitigation: Create scheduled update jobs only after explicit approval, use a low-frequency consolidated update policy, and summarize failures or changes without printing secrets.

Risk: Installed focused skills may not be visible to the running agent until the session or gateway reloads.

Mitigation: Verify the CLI with a harmless command and reload or restart the relevant agent harness before relying on the installed skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tmchow/skills/printing-press-library)
- [Printing Press Library homepage](https://github.com/mvanhorn/printing-press-library)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include catalog selection rationale, install or update commands, PATH or reload guidance, and credential-presence checks without printing secrets.]

## Skill Version(s):

0.2.2 (source: frontmatter and ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
