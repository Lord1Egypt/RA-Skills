## Description:

A local missing person assistance tool for organizing cases, managing clues, generating notices, and providing search guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harrylabsj](https://clawhub.ai/user/harrylabsj)

### License/Terms of Use:

MIT-0

## Use Case:

External users and community responders use this skill to organize local missing-person case details, record clues, generate platform-specific notices, and get safety reminders while coordinating with official authorities.

### Deployment Geography for Use:

Global; some emergency-number and social-platform guidance is China-specific and should be adapted for the user's local jurisdiction.

## Known Risks and Mitigations:

Risk: Sensitive missing-person case records may be stored locally in plaintext without strong file protections or reliable deletion controls.

Mitigation: Collect the minimum necessary information, avoid storing ID numbers, exact addresses, family contact details, financial information, or sensitive medical details, and use a separate secure handling plan for real cases.

Risk: Generated notices or clue summaries could expose private information or be mistaken for verified findings.

Mitigation: Review notices before sharing, remove sensitive personal data, obtain consent where appropriate, and present clue analysis only as local organization or rule-based guidance.

Risk: Emergency contacts and platform guidance include China-specific assumptions that may not apply elsewhere.

Mitigation: Replace jurisdiction-specific phone numbers, police procedures, and platform practices with local official guidance before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/harrylabsj/skills/looking-for-someone)
- [Field Definitions and Workflow Guidelines](references/fields-and-workflows.md)
- [Privacy and Security Boundaries](references/privacy-and-boundaries.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Plain text and Markdown with CLI command examples and generated missing-person notice text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local plaintext JSON case records when CLI commands are run.]

## Skill Version(s):

1.0.2 (source: server release evidence and .claw/identity.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
