## Description:

Research any topic from the last 30 days on Reddit, X, and the web, synthesize findings, and write copy-paste-ready prompts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiangwzh](https://clawhub.ai/user/jiangwzh)

### License/Terms of Use:


## Use Case:

External users, developers, and researchers use this skill to gather recent social and web discussion about a topic, identify recommendations, news, or prompting patterns, and produce concise summaries or copy-paste-ready prompts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Research topics may be sent to OpenAI or xAI when API keys are configured.

Mitigation: Use the skill only for topics appropriate to share with those providers, and review provider data handling requirements before configuring API keys.

Risk: Optional API keys can be stored in a local .env file under ~/.config/last30days.

Mitigation: Prefer environment variables or a secret manager where possible, restrict file permissions, and remove keys from ~/.config/last30days when uninstalling.

Risk: Research outputs and caches may be saved under ~/.local/share/last30days and ~/.cache/last30days.

Mitigation: Review saved reports for sensitive topics and clear ~/.config/last30days, ~/.cache/last30days, and ~/.local/share/last30days when removing the skill.

Risk: The security review notes promotional setup messages in responses.

Mitigation: Review generated responses before sharing them and remove promotional setup text when it is not appropriate for the audience.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jiangwzh/skills/moss-last30days)
- [ClawHub publisher profile](https://clawhub.ai/user/jiangwzh)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with concise summaries, source statistics, setup commands, and copy-paste-ready prompts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local research reports, cached results, raw API responses, and reusable context snippets under the user's home directory.]

## Skill Version(s):

1.0.0 (source: release metadata and artifact/_meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
