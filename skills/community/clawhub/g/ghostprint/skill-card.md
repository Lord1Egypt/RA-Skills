## Description: <br>
LLM fingerprint noise injector that sends behaviorally realistic randomized queries to Anthropic, Z.ai, and OpenAI-compatible providers on a schedule to depersonalize usage profiles and reduce behavioral fingerprinting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alarawms](https://clawhub.ai/user/alarawms) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use Ghostprint to run scheduled synthetic LLM requests through configured provider accounts, either as an OpenClaw plugin or a standalone Python script, to add noise to usage patterns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Recurring synthetic LLM requests can create API charges. <br>
Mitigation: Configure explicit provider limits, monitor usage, and consider separate low-budget keys before enabling scheduled traffic. <br>
Risk: Provider logging, account-policy issues, and audit noise may result from traffic that is designed to mimic real usage. <br>
Mitigation: Review provider policies, use the plugin only deliberately, and keep the ability to disable the plugin or remove cron scheduling. <br>
Risk: The skill reuses existing provider credentials in OpenClaw or configured API keys in standalone mode. <br>
Mitigation: Use least-privilege or isolated provider keys where possible and avoid enabling providers that should not receive synthetic traffic. <br>


## Reference(s): <br>
- [Ghostprint ClawHub Release](https://clawhub.ai/alarawms/ghostprint) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and plain text with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Agent-facing tools can fire a noise round immediately or return run history and stats; standalone usage can install a cron schedule.] <br>

## Skill Version(s): <br>
3.0.1 (source: server release metadata; artifact frontmatter and root package metadata list 3.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
