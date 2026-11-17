## Description:

PowPow Financing Plan OpenClaw runs an interactive investor challenge for PowPow's angel/Pre-A financing plan, using Q&A to explain the project, build an investment style profile, and optionally prepare a previewed investor email.

This skill is ready for commercial/non-commercial use.

## Publisher:

[durenzidu](https://clawhub.ai/user/durenzidu)

### License/Terms of Use:

MIT-0

## Use Case:

External investors and PowPow prospects use this skill to learn about the PowPow project, answer a 13-question investor challenge, and receive a qualitative investment style profile. The skill can also prepare an optional outreach email for the founder after preview and explicit confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Investor answers and optional contact details may be placed into an email to the PowPow founder.

Mitigation: Show the full email preview before sending, allow profile removal and redacted-copy handling, keep contact fields optional, and send only after explicit user confirmation.

Risk: Memory personalization may surface prior conversation context during the investor flow.

Mitigation: Ask for consent before accessing memory; if the user declines or does not respond, skip memory access for the session and do not include memory content in email.

Risk: Industry or market answers may depend on web lookup and can be incomplete or time-sensitive.

Mitigation: Prefer official PowPow sources for project claims, use web lookup only for relevant industry questions, and state when official materials do not cover an answer.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/durenzidu/skills/powpow-financing-plan-openclaw)
- [PowPow homepage](https://www.powpow.online/)
- [PowPow landing page](https://global.powpow.online/landing)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Conversational Markdown with structured Q&A, investment style profile summaries, optional email drafts, and link references.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Memory personalization is consent-gated; optional email content requires full preview, optional redaction/removal of profile content, and explicit send confirmation.]

## Skill Version(s):

1.2.2 (source: SKILL.md frontmatter, artifact/skill.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
