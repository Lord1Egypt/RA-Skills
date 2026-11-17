## Description:

Triage inbound calls to an AI agent line: classify caller intent, define screening questions, set escalate-vs-handle rules, draft message-taking scripts, and identify spam signals before the agent picks up.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ruti3](https://clawhub.ai/user/ruti3)

### License/Terms of Use:

MIT-0

## Use Case:

Customer support teams, receptionists, and builders of AI phone lines use this skill to create an inbound-call playbook. The brief helps classify caller intent, ask minimal screening questions, take messages, identify spam, and define clear handoff rules for urgent or regulated situations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Call handling rules may conflict with jurisdiction-specific recording, privacy, emergency, or regulated-industry requirements.

Mitigation: Review call scripts against applicable business policy and local law before deployment, especially recording disclosures, emergency routing, and health, legal, or financial handoffs.

Risk: Callers may offer sensitive credentials or high-risk personal information during triage.

Mitigation: Keep the skill's credential and PII boundaries in the deployed script: do not collect passwords, OTP codes, full card numbers, SSNs, or unnecessary caller data.

Risk: AI-only handling of emergencies or advice-seeking calls can delay appropriate human response.

Mitigation: Preserve explicit escalation rules for immediate danger, legal threats, VIP or urgent callers, and regulated advice requests.

## Reference(s):


## Skill Output:

**Output Type(s):** [Markdown, Guidance, Configuration]

**Output Format:** [Markdown brief with scripts, routing tables, screening questions, and escalation criteria]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prompt-only, document-only output; no code execution, network access, credentials, or telephony API access.]

## Skill Version(s):

1.0.0 (source: frontmatter, skill.json, release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
