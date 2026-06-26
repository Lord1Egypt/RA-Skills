## Description: <br>
Tracks OpenClaw LLM token usage and costs from OpenRouter and produces rolling usage reports with model breakdowns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[joeyiptk](https://clawhub.ai/user/joeyiptk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to collect OpenRouter usage facts from local OpenClaw session logs, maintain a local usage database, and generate cost/token reports for recent time windows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads local OpenClaw session logs and local OpenRouter credentials to collect and verify usage. <br>
Mitigation: Install it only in environments where that local access is expected, and review the configured session path and credential source before running collection or reporting commands. <br>
Risk: The skill stores usage metadata in a local SQLite database. <br>
Mitigation: Treat config/usage.db as local usage history, restrict filesystem access to it, and exclude it from shared snapshots or published artifacts. <br>
Risk: The documented prune_usage.py --dry-run behavior is flagged as deleting records. <br>
Mitigation: Avoid prune_usage.py --dry-run until the deletion-order issue is fixed, and back up config/usage.db before using pruning commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/joeyiptk/llm-cost-tracker-openrouter-api) <br>
- [Publisher profile](https://clawhub.ai/user/joeyiptk) <br>
- [Setup guide](artifact/SETUP_GUIDE.md) <br>
- [Changelog](artifact/CHANGELOG.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text, terminal tables, JSON, and Markdown guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports can cover rolling 24-hour and calendar 7-day, 30-day, 90-day, and 365-day windows.] <br>

## Skill Version(s): <br>
1.1.2 (source: frontmatter, changelog, version.txt, server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
