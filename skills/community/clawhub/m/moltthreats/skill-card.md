## Description:

Agent-native security signal feed by PromptIntel for reporting threats, fetching protection feeds, applying security rules, and updating SHIELD.md.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fr0gger](https://clawhub.ai/user/fr0gger)

### License/Terms of Use:


## Use Case:

Developers and security-focused agent operators use MoltThreats to share and consume curated agent threat intelligence, submit threat reports, and maintain a local SHIELD.md policy for runtime decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Remote threat feed entries can influence future agent decisions and local SHIELD.md policy.

Mitigation: Require explicit consent before first use of block rules, keep local override capability, and review feed-derived policy changes before enforcement.

Risk: Report submission can expose sensitive local evidence if raw prompts, paths, tokens, or internal data are included.

Mitigation: Redact secrets, tokens, private paths, prompts, and internal data before submitting any report.

Risk: Authenticated recurring feed syncs contact a third-party API and require PROMPTINTEL_API_KEY.

Mitigation: Send the API key only to api.promptintel.novahunting.ai, store it only as an environment variable, and use per-sync or per-rule approval where appropriate.

## Reference(s):

- [MoltThreats ClawHub listing](https://clawhub.ai/fr0gger/skills/moltthreats)
- [MoltThreats homepage](https://promptintel.novahunting.ai/molt)
- [PromptIntel API base](https://api.promptintel.novahunting.ai/api/v1)
- [SHIELD.md specification](https://nova-hunting.github.io/shield.md/)
- [Feed Consumption and Enforcement](references/feed-and-enforcement.md)
- [Reporting Guide](references/reporting-guide.md)
- [SHIELD.md Template](references/shield-md-template.md)
- [Integration Example](references/integration-example.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON examples, shell commands, code snippets, and SHIELD.md policy content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce or update SHIELD.md and uses authenticated API calls to fetch feeds or submit approved reports.]

## Skill Version(s):

0.6.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
