## Description:

Monitor Poe API point balance and usage history from the terminal using poeusage CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rgstephens](https://clawhub.ai/user/rgstephens)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Poe API users use this skill to check point balance, review usage history, and summarize spend from the terminal.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The third-party poeusage CLI receives the user's Poe API key.

Mitigation: Install only from trusted sources and provide POE_API_KEY through a controlled environment rather than command-line arguments or persistent config files.

Risk: Usage, balance, and spend outputs can expose Poe account activity metadata.

Mitigation: Handle JSON, CSV, and table outputs as sensitive operational data and avoid sharing logs or terminal captures broadly.

Risk: Homebrew installation depends on the rgstephens tap.

Mitigation: Review and trust the tap and formula before installation in managed environments.

## Reference(s):

- [Poe Usage ClawHub listing](https://clawhub.ai/rgstephens/skills/poeusage)
- [poeusage-skill homepage](https://github.com/rgstephens/poeusage-skill)
- [rgstephens publisher profile](https://clawhub.ai/user/rgstephens)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON, CSV, or table output examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the poeusage binary and a POE_API_KEY environment variable; command output can include Poe account usage and spend metadata.]

## Skill Version(s):

0.5.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
