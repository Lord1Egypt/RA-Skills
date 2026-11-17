## Description:

Turn meeting transcripts into operational outputs, including action items, decisions, follow-up email drafts, and ticket drafts from VTT, SRT, or plain text transcripts using multi-pass LLM extraction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tkuehnl](https://clawhub.ai/user/tkuehnl)

### License/Terms of Use:


## Use Case:

Employees, operators, and developers use this skill to convert existing meeting transcripts into operational Markdown reports containing decisions, action items, open questions, follow-up email drafts, and ticket drafts. It is intended for workflows where a human reviews meeting-derived outputs before sending emails, filing tickets, or acting on assignments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive meeting content and API credentials may be sent to configured LLM endpoints.

Mitigation: Use only approved Anthropic or OpenAI endpoints and avoid custom HTTP endpoints for confidential meetings.

Risk: Meeting-derived history is stored locally by default.

Mitigation: Use the --no-history option when processing confidential meetings or when local persistence is not approved.

Risk: Generated email and ticket drafts can be incorrect, incomplete, or unsuitable to send directly.

Mitigation: Treat generated emails and tickets as drafts that require human review before sending or filing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tkuehnl/skills/meeting-autopilot)
- [README.md](README.md)
- [SECURITY.md](SECURITY.md)
- [SKILL.md](SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports with JSON intermediate data and shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs include meeting overview tables, decisions, action item tables, open questions, parking lot items, follow-up email drafts, and ticket drafts; optional report files and local history JSON may be written.]

## Skill Version(s):

0.1.2 (source: server release metadata; artifact frontmatter and scripts show 0.1.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
