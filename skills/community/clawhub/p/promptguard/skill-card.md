## Description:

Detect prompt injection attacks in text and return a risk score with detected patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mirni](https://clawhub.ai/user/mirni)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use PromptGuard to scan untrusted text for common prompt-injection patterns before the text is processed by an AI agent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Running the skill starts a local HTTP service that may receive sensitive text for scanning.

Mitigation: Run it only in trusted local environments, avoid sending secrets or private data through the scanner, and restrict service exposure as appropriate.

Risk: Unpinned runtime dependencies can change behavior across installations.

Mitigation: Pin and review dependency versions before production use.

## Reference(s):

- [PromptGuard ClawHub Skill Page](https://clawhub.ai/mirni/skills/promptguard)

## Skill Output:

**Output Type(s):** [JSON, Analysis]

**Output Format:** [JSON API response containing a risk score, detected pattern names, and input length]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Text input is constrained to 1-100,000 characters.]

## Skill Version(s):

0.1.1 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
