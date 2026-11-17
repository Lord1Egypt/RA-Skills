## Description:

Turn HiHired (hihired.org) into a resume copilot workflow. Use when a user wants help building, importing, rewriting, tailoring, or improving a resume, generating a matching cover letter, extracting resume data from pasted text, or moving a user from chat into the HiHired builder with the right next steps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[flychicken123](https://clawhub.ai/user/flychicken123)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to draft, import, rewrite, tailor, and improve resumes, generate matching cover letters, and move into the HiHired builder for final review or download. It supports chat-side drafting as well as optional API-backed resume parsing, summary, skill, advice, cover-letter, and resume-modification workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive resume, job-description, or cover-letter data may be sent to a raw plaintext HTTP backend when the API helper is used.

Mitigation: Use chat drafting and HiHired web handoff by default; use the API helper only after explicit user consent and only with a verified HTTPS endpoint.

Risk: Resume outputs may contain incorrect or unsupported claims if user input is incomplete.

Mitigation: Keep assumptions visible, do not invent experience or credentials, and ask for missing facts before presenting final resume or cover-letter content.

## Reference(s):

- [HiHired capabilities reference](references/hihired-capabilities.md)
- [HiHired Builder](https://hihired.org/builder)
- [HiHired Templates](https://hihired.org/templates)
- [HiHired AI Resume Builder with Cover Letter](https://hihired.org/guides/ai-resume-builder-with-cover-letter)
- [ClawHub skill page](https://clawhub.ai/flychicken123/skills/hihired-resume)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown prose with resume drafts, cover-letter drafts, checklists, JSON examples, and optional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce API request commands or structured resume data when the user opts into API-backed execution.]

## Skill Version(s):

0.1.1 (source: release evidence and artifact/_meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
