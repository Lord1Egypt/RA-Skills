## Description:

Find, read, summarize, and save insights from a user's ParrotNotes meeting notes through the ParrotNotes connector.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ascetx](https://clawhub.ai/user/ascetx)

### License/Terms of Use:

MIT-0

## Use Case:

ParrotNotes users can find and summarize their meeting notes and transcripts, extract action items, and save requested insights back to a note.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad invocation may expose sensitive meeting notes or transcripts when the user did not mean ParrotNotes.

Mitigation: Confirm ambiguous requests refer to ParrotNotes before opening notes or transcripts, and quote their contents sparingly.

Risk: Saving an insight can replace an existing insight for the same note and type.

Mitigation: Check for an existing insight and obtain confirmation before overwriting it.

## Reference(s):

- [ParrotNotes skill on ClawHub](https://clawhub.ai/ascetx/skills/parrotnotes)
- [ParrotNotes connector setup](https://parrotnotes.app/docs/mcp)

## Skill Output:

**Output Type(s):** [Text, Markdown]

**Output Format:** [Natural-language responses and requested insights saved to ParrotNotes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a ParrotNotes account and connector; saves insights only on request.]

## Skill Version(s):

1.2.1 (source: release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
