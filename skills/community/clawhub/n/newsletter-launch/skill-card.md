## Description:

Plug-and-play newsletter launcher that runs a setup wizard, scaffolds newsletter project files, and wires up automation crons for a fully operational newsletter.

This skill is ready for commercial/non-commercial use.

## Publisher:

[micphigoo](https://clawhub.ai/user/micphigoo)

### License/Terms of Use:

MIT-0

## Use Case:

External users and operators use this skill to launch a new Beehiiv-based newsletter from scratch, generate the project workspace, and schedule recurring research, writing, evergreen, and keyword-refresh automation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Beehiiv API keys may be exposed through plaintext config storage, printed command payloads, cron schedules, or commits.

Mitigation: Use a secret store or environment variable for Beehiiv credentials, avoid printing tokens, and never commit configuration files containing secrets.

Risk: Auto-publishing can create live public posts using the configured Beehiiv account.

Mitigation: Enable auto-publishing only with a least-privilege API key and explicit approval controls for publication.

Risk: The skill depends on several other newsletter and SEO skills plus Python 3.

Mitigation: Confirm dependencies are installed and run the provided validation step before relying on scheduled automation.

## Reference(s):

- [Newsletter Launch Skill Page](https://clawhub.ai/micphigoo/skills/newsletter-launch)
- [Beehiiv Setup Guide](artifact/references/beehiiv-setup.md)
- [Config Schema](artifact/references/config-schema.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration]

**Output Format:** [Conversational setup prompts, Markdown project files, JSON configuration, generated cron definitions, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates newsletter project files and cron configuration; may call Beehiiv APIs when configured by the user.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
