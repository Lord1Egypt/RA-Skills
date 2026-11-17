## Description:

Learn how the user actually writes — from the posts they published, and from what they approved, edited or rejected — and keep a brand profile that gets sharper with use.

This skill is ready for commercial/non-commercial use.

## Publisher:

[posteyai](https://clawhub.ai/user/posteyai)

### License/Terms of Use:

MIT-0

## Use Case:

Creators, brand teams, and agencies use this skill to learn a writing profile from published posts or supplied writing, then apply that profile to future drafts and refine it from edits and verdicts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security assessment notes that the voice-learning workflow may save drafts or upload media without a clear user request.

Mitigation: Require an explicit request before saving drafts or uploading media, and confirm the target account and action.

Risk: Profiles and ledgers may persist exact draft text and feedback, and an existing output file may be overwritten.

Mitigation: Choose the local source, profile storage, and output filename deliberately; confirm the destination before writing.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/posteyai/skills/postey-voice)
- [Brand Voice reference](artifact/references/brand-voice.md)
- [Command Reference](artifact/command-reference.md)
- [Rules Ledger](artifact/rules-ledger.md)
- [Voice Profile Schema](artifact/voice-profile-schema.md)

## Skill Output:

**Output Type(s):** [JSON, Guidance]

**Output Format:** [JSON voice profile and learning ledger, with prose guidance for applying the profile]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Profiles are account-scoped when an account is specified; otherwise the profile is explicitly unscoped.]

## Skill Version(s):

1.2.1 (source: frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
