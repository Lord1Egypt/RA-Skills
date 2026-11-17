## Description:

Analyzes suspicious email, SMS, voice-mail script, or .eml text offline, extracts URL and message signals, scores phishing risk from 0 to 100, and explains the evidence in plain language before the user clicks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[voronindenis5](https://clawhub.ai/user/voronindenis5)

### License/Terms of Use:

MIT

## Use Case:

Employees, external users, families, and small-team security reviewers use this skill to triage suspicious messages, inspect URLs without visiting them, and learn which phishing signals drove the risk score.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The analyzer works on message contents that may include personal or sensitive inbox data.

Mitigation: Provide only the suspicious message or .eml needed for review, and avoid pasting unrelated mailbox contents.

Risk: Users may be tempted to open suspicious links while investigating the message.

Mitigation: Keep review textual and follow the skill guidance to avoid visiting extracted URLs.

Risk: A low score is not proof that a message is legitimate.

Mitigation: Use the report's independent verification steps, such as opening the official app or calling a known number, before acting on credential or payment requests.

## Reference(s):

- [README](README.md)
- [Signal Reference - Phishing Detection](references/signal-reference.md)
- [Synthetic Sample Phish](references/sample-phish.txt)
- [ClawHub Skill Page](https://clawhub.ai/voronindenis5/skills/phishing-spotter)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, guidance]

**Output Format:** [Plain text or Markdown reports, with optional JSON output from the analyzer script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs include a 0-100 risk score, verdict band, quoted evidence, URL analysis, verification steps, and damage-control guidance when the user already clicked.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
