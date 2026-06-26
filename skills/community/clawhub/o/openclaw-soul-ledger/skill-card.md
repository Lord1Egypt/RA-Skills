## Description: <br>
Gives an AI agent persistent workspace memory of a user's patterns, preferences, personality traits, and behavioral evolution by maintaining a local soul_ledger.json file. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[albionaiinc-del](https://clawhub.ai/user/albionaiinc-del) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent builders use this skill to give an AI agent a persistent, local model of a user's working style and preferences across conversations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill silently builds and reuses a long-term personal profile that can influence future agent responses. <br>
Mitigation: Install only when persistent personalization is intended, review the ledger regularly, and delete or disable soul_ledger.json when stored personal inferences should no longer shape responses. <br>
Risk: The local ledger may contain identifiers or sensitive personal inferences if used in shared repositories or shared workspaces. <br>
Mitigation: Keep soul_ledger.json out of shared repos and shared workspaces, remove identifiers such as email addresses, and edit the file to reduce unnecessary personal detail. <br>
Risk: Stored observations may become outdated or conflict with a user's request to forget information. <br>
Mitigation: Prefer recent signals, review growth notes, and remove requested information from the ledger instead of preserving stale or unwanted inferences. <br>


## Reference(s): <br>
- [Openclaw Soul Ledger on ClawHub](https://clawhub.ai/albionaiinc-del/openclaw-soul-ledger) <br>


## Skill Output: <br>
**Output Type(s):** [Files, JSON, Guidance] <br>
**Output Format:** [JSON file plus agent behavior guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Maintains soul_ledger.json locally, keeps the 50 most recent interaction-history entries, and requires valid JSON writes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
