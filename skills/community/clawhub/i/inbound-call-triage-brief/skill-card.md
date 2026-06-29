## Description: <br>
Triage inbound calls to an AI agent line by classifying caller intent, screening questions, escalate-vs-handle rules, message-taking script, and spam signals before the agent picks up. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ruti3](https://clawhub.ai/user/ruti3) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Customer support, sales, receptionist, and operations teams use this skill to prepare an AI phone agent or human supervisor to classify inbound caller intent, ask minimal screening questions, take messages, and route urgent or sensitive calls to a human. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may be used around sensitive caller data. <br>
Mitigation: Collect only the required call-handling fields and do not collect passwords, OTP codes, full card numbers, or SSNs. <br>
Risk: The skill does not configure phone systems, recording disclosures, identity checks, or emergency routing. <br>
Mitigation: Have the deploying team verify phone setup, recording-law compliance, identity verification, and emergency or human handoff paths before use. <br>
Risk: Inbound callers may request regulated advice or describe immediate danger. <br>
Mitigation: Route emergencies to emergency services and default health, legal, and financial advice requests to a human handoff. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ruti3/skills/inbound-call-triage-brief) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown triage brief with routing tables, scripts, screening questions, message-taking template, spam signals, and escalation guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Prompt-only guidance; no code execution, network access, credentials, or persistence.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
