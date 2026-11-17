## Description:

Curates weekly music album picks with search, scoring, deduplication, Notion writing, and push to configured messaging channels.

This skill is ready for commercial/non-commercial use.

## Publisher:

[romanticmysterylh](https://clawhub.ai/user/romanticmysterylh)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to configure a recurring album curation workflow that searches current releases, applies rating and region criteria, avoids duplicate recommendations, writes selected albums to Notion, and sends a message through a configured channel.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow handles a Notion API key that may grant access to sensitive pages.

Mitigation: Use a narrowly scoped Notion integration, avoid passing the key on the command line, and confirm that ~/.config/music-weekly/config.json is readable only by the user.

Risk: The workflow can write records to Notion and send messages or media to a configured delivery target.

Mitigation: Review the selected Notion database and delivery target before allowing the workflow to run or send recommendations.

Risk: Music recommendations may be misleading if album scores or sources are not checked before publishing.

Mitigation: Follow the artifact workflow requirement to use real, verifiable rating sources and deduplicate against the full recommendation history before writing or sending results.

## Reference(s):

- [Music Weekly ClawHub release](https://clawhub.ai/romanticmysterylh/skills/music-weekly)
- [Workflow reference](references/workflow.md)
- [Configuration template](references/config-template.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, Python snippets, and JSON configuration.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local configuration, history-log, cover/media directories, Notion database records, and outbound channel messages when the user runs the supplied scripts.]

## Skill Version(s):

1.3.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
