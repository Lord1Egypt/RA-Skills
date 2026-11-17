## Description:

Generates Kuaishou AI content reports by scanning RedFox data, clustering viral videos, and summarizing trends, creators, growth signals, and investigation directions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[redfox-data](https://clawhub.ai/user/redfox-data)

### License/Terms of Use:

MIT-0

## Use Case:

External content operators, creators, MCNs, brands, and industry researchers use this skill to generate structured Kuaishou AI trend reports, identify viral topics and creators, and guide follow-up investigations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill contacts RedFox and may use locally stored API credentials.

Mitigation: Use a scoped REDFOX_API_KEY from a verified RedFox account, prefer environment variables over plaintext config files, and rotate any shared or exposed keys.

Risk: The subscription feature can install a daily scheduled task.

Mitigation: Avoid --subscribe until the scheduled-task behavior and command construction have been reviewed; use manual runs when persistence is not required.

Risk: Generated reports and the localhost preview server can render upstream content and proxy requests.

Mitigation: Treat generated reports as untrusted HTML, keep the preview server bound to localhost, and stop it when review is complete.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/redfox-data/skills/ks-ai-feed)
- [RedFox API key settings](https://redfox.hk/settings/api-keys?souce=github)
- [RedFox Kuaishou AI batch API](https://redfox.hk/story/api/parseWork/queryKsAiMsgs/batch)
- [engine-strategy.md](references/engine-strategy.md)
- [investigation-modes.md](references/investigation-modes.md)
- [investigation-templates.md](references/investigation-templates.md)
- [investigator-config.json](references/investigator-config.json)

## Skill Output:

**Output Type(s):** [text, markdown, HTML, files, shell commands, configuration, guidance]

**Output Format:** [Structured Markdown summary, local HTML report file, and localhost preview URL.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Saves reports under ~/Downloads/QoderReports by default, requires REDFOX_API_KEY for RedFox access, and can optionally install a daily scheduled run.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
