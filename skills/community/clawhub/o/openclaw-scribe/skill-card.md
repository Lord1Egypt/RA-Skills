## Description: <br>
Reads OpenClaw session logs, extracts decisions, preferences, framework sentences, project updates, and follow-ups, then writes a structured daily memory file. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[billc8128](https://clawhub.ai/user/billc8128) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and OpenClaw users use Scribe to consolidate session history into durable memory files that an agent can reference across future sessions. It can run manually or as a scheduled nightly job. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read private OpenClaw session logs and send user messages to OpenRouter for summarization. <br>
Mitigation: Review the session directory scope before enabling the skill, narrow SCRIBE_SESSION_DIR and SCRIBE_DAYS where possible, and install only when this data flow is acceptable. <br>
Risk: The skill writes persistent memory files that may preserve sensitive decisions, preferences, project updates, or follow-up tasks. <br>
Mitigation: Review generated memory files regularly and keep SCRIBE_APPEND_LONGTERM disabled unless long-term aggregation is needed. <br>
Risk: The nightly cron job can continue processing sessions automatically after installation. <br>
Mitigation: Remove or disable the scribe-nightly cron job when automatic processing is no longer wanted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/billc8128/openclaw-scribe) <br>
- [OpenClaw](https://openclaw.ai) <br>
- [Cron setup](references/cron-setup.md) <br>
- [Signal classification guide](references/signal-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown memory files with terminal status text and setup commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes memory/YYYY-MM-DD.md and can optionally append extracted content to MEMORY.md when configured.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
