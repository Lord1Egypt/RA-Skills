## Description:

Scans personal to-do lists, meeting notes, and message summaries to identify upcoming deadlines, scheduling conflicts, risky omissions, and items that need confirmation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[52yuanchangxing](https://clawhub.ai/user/52yuanchangxing)

### License/Terms of Use:

MIT-0

## Use Case:

External users and personal productivity agents use this skill to review local task lists, calendar summaries, message summaries, and deadline notes. It produces a draft-first deadline radar with conflicts, high-risk omissions, rescheduling suggestions, deferrable items, today's list, and explicit confirmation gaps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Inputs may contain personal scheduling details or sensitive message summaries.

Mitigation: Provide only the specific task, calendar, or message-summary files needed for the review and redact sensitive exports where possible.

Risk: Deadline and conflict summaries can be incomplete or misleading when the provided information is missing, ambiguous, or stale.

Mitigation: Treat the output as a review draft, check the listed confirmation items, and verify dates before making calendar changes.

Risk: The bundled script contains unused generic audit helpers.

Mitigation: Clean up or document those helpers before broader deployment so the skill behavior remains easy to review.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/52yuanchangxing/skills/personal-deadline-radar)
- [Publisher profile](https://clawhub.ai/user/52yuanchangxing)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Structured Markdown or JSON summaries generated from local task, calendar, or message-summary inputs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Draft-first, reviewable outputs; the local Python script can write results to a user-specified output file.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
