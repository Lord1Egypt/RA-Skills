## Description: <br>
Capture short personal notes about people you mention, store them in a lightweight DB, and recall those details whenever you ask about them later. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[charbeld](https://clawhub.ai/user/charbeld) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agent operators use this skill to save, search, summarize, recall, and export short notes about people, including preferences, reminders, and relationship context. It is suited for personal memory workflows where persistent storage of people-related notes is intentional. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Transcript-derived personal data may be saved quietly to a persistent people-memory database. <br>
Mitigation: Enable the skill only for intentional people-memory use, avoid storing sensitive third-party details, and inspect or clear ~/.clawdbot/people-memory.json and related logs regularly. <br>
Risk: Voice transcript auto-capture may save notes without an explicit confirmation step. <br>
Mitigation: Confirm whether auto-capture can be disabled or changed to confirm-before-save before using it in conversations. <br>
Risk: Reminder automation describes background delivery through cron and Telegram without clear opt-in or disable controls. <br>
Mitigation: Verify whether any reminder job is installed, review its schedule and delivery channel, and disable it when reminders are not desired. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/charbeld/people-memories) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, configuration] <br>
**Output Format:** [Plain text CLI responses, Markdown exports, JSON exports, and command/configuration snippets.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Persists people notes locally and can generate reminder text for scheduled delivery.] <br>

## Skill Version(s): <br>
0.1.0 (source: evidence release and plugin manifest) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
