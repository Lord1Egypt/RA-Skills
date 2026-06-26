## Description: <br>
Step-by-step onboarding guide for setting up a new AI Personal Assistant on OpenClaw. Use when: a new PA is being created, someone asks how to set up an agent, or guiding a user through the full setup process from account creation to first response. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[netanel-abergel](https://clawhub.ai/user/netanel-abergel) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and personal-assistant owners use this skill to guide a new AI Personal Assistant through account setup, WhatsApp verification, integrations, configuration, and first-response checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The onboarding flow can grant broad account access across WhatsApp, Google Calendar, Gmail, Drive, contacts, and monday.com. <br>
Mitigation: Use least-privilege service accounts, enable only integrations needed for the assistant, and define which messages, calendar edits, workspace changes, and briefings require explicit owner approval. <br>
Risk: The monday.com setup stores an API token in plaintext. <br>
Mitigation: Store the token in a secret manager or locked-down credentials file, restrict file permissions, and rotate or revoke the token when no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/netanel-abergel/pa-onboarding) <br>
- [monday.com agents signup](https://monday.com/agents-signup) <br>
- [pa-skills reference repository](https://github.com/netanel-abergel/pa-skills) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with checklists and inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [One-step-at-a-time procedural guidance with confirmation before continuing] <br>

## Skill Version(s): <br>
1.1.1 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
