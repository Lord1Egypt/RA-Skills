## Description: <br>
Turn recruiting emails into native Apple Reminders. AI-powered parsing extracts interview/assessment events and syncs to iPhone. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nissoncx](https://clawhub.ai/user/nissoncx) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Job seekers and recruiting workflow users use OfferCatcher to scan Apple Mail for interviews, assessments, deadlines, and related recruiting events, then create native Apple Reminders from parsed results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads recent Apple Mail content and passes it through the OpenClaw LLM workflow. <br>
Mitigation: Configure a specific account and mailbox, limit the scan window and result count, and inspect scan output before applying events. <br>
Risk: The Reminders bridge includes delete and clear-list operations that can remove reminders. <br>
Mitigation: Use dry-run before applying events and do not expose delete or clear-list commands to unattended automation. <br>
Risk: The artifact documents a curl-to-bash installation path. <br>
Mitigation: Prefer the ClawHub install path or review the install script before running it. <br>


## Reference(s): <br>
- [OfferCatcher ClawHub listing](https://clawhub.ai/nissoncx/offercatcher) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [OpenClaw](https://github.com/NissonCX/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON event data] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can return scanned email JSON for LLM parsing and can create or update Apple Reminders when parsed events are applied.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
