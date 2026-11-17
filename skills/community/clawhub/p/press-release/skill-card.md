## Description:

Generates press-release and public-relations drafts for product launches, funding announcements, events, and crisis statements.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xueyetianya](https://clawhub.ai/user/xueyetianya)

### License/Terms of Use:

MIT-0

## Use Case:

External communications teams, founders, and developers use this skill to draft press-release and PR templates for launches, financing announcements, events, and crisis responses. The generated drafts are primarily Chinese and include placeholders intended for user review and completion.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled utility can retain user-supplied text and command arguments in plaintext under the user's data directory.

Mitigation: Do not enter secrets, confidential announcements, financing details, incident-response drafts, or contact data unless local retention is acceptable; use a controlled PRESS_RELEASE_DIR and clear stored logs when needed.

Risk: Generated press releases and crisis statements may affect legal, financial, or public communications.

Mitigation: Have communications, legal, and business owners review and complete all placeholders before publication.

Risk: The generated output is primarily Chinese, which may not match English-only workflows.

Mitigation: Confirm language requirements before use and review or translate generated drafts for the intended audience.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xueyetianya/skills/press-release)
- [Publisher profile](https://clawhub.ai/user/xueyetianya)
- [BytesAgain homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown and terminal-oriented text templates, primarily Chinese]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes bracketed placeholders for user-supplied details; one bundled utility can log command arguments and stored entries locally in plaintext.]

## Skill Version(s):

2.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
