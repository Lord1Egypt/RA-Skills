## Description:

Gives an AI agent persistent workspace memory of a user's patterns, preferences, personality traits, and behavioral evolution by maintaining a soul_ledger.json file.

This skill is ready for commercial/non-commercial use.

## Publisher:

[albionaiinc-del](https://clawhub.ai/user/albionaiinc-del)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to give an agent continuity across conversations by maintaining a workspace-local JSON model of the user's preferences, communication style, traits, and recent interaction history.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill silently creates and maintains a persistent behavioral profile in soul_ledger.json, which may contain sensitive personal patterns and preferences.

Mitigation: Use only when persistent personalization is intended; keep the ledger in a private workspace, inspect or delete it as needed, avoid sensitive conversations, and do not commit or sync it without review.

Risk: The security summary notes limited opt-in and deletion reliability for the persistent profile.

Mitigation: Require explicit user consent before enabling the skill and provide a documented process for locating, reviewing, and deleting soul_ledger.json.

## Reference(s):

- [Openclaw Soul Ledger ClawHub release](https://clawhub.ai/albionaiinc-del/skills/openclaw-soul-ledger)

## Skill Output:

**Output Type(s):** [Files, JSON, Guidance]

**Output Format:** [Markdown instructions that guide creation and updates of a workspace-local JSON file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Maintains soul_ledger.json with a distilled user model and up to 50 recent interaction history entries.]

## Skill Version(s):

1.0.0 (source: server release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
