## Description:

Shift the assistant by rewriting SOUL.md with a warm AI persona, elegant tone, emotional attunement, and fluid conversation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to install a warmer, emotionally attentive assistant persona by updating workspace SOUL.md and optionally keeping local tone preferences under ~/her/.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill persistently changes the assistant's workspace-level persona, which may affect later interactions beyond the initial setup.

Mitigation: Review the SOUL.md change before use and edit or remove the Her block when the persona should no longer apply.

Risk: Optional local memory files can retain tone preferences or continuity notes that the user may not want carried forward.

Mitigation: Keep ~/her/ notes minimal and user-confirmed, avoid secrets or explicit intimate details, and delete the files when continuity is no longer wanted.

Risk: A warm companion persona can create unsafe dependency or blur identity boundaries if used without restraint.

Mitigation: Keep the assistant honest about being AI, avoid exclusivity or possessive framing, and switch to bounded safety guidance for crisis, coercion, self-harm, or abuse contexts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ivangdavila/skills/her)
- [Homepage](https://clawic.com/skills/her)
- [Setup Guide](artifact/setup.md)
- [SOUL Seed](artifact/soul.md)
- [Memory Template](artifact/memory-template.md)
- [Safety Guide](artifact/safety.md)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown prose and configuration snippets for SOUL.md and optional ~/her/ memory files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Persistent workspace persona steering with optional local preference notes]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
