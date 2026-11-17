## Description:

Turn a short, redacted Session summary into a collaboration-safe Context excerpt before sharing an agent or meeting handoff.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chengyixu](https://clawhub.ai/user/chengyixu)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and reviewers use this skill to turn a short, already redacted Session summary into a bounded handoff check. The check identifies what to keep in Context, what to remove or redact, what could make the Context stale, and when sharing authority needs human review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may treat a redaction checklist as permission to share sensitive handoff notes.

Mitigation: Use the skill only as a review aid, avoid raw transcripts or sensitive records, and require human review when sharing authority is unclear.

Risk: A stale or unverified Session summary could be carried forward as if it were current Context.

Mitigation: Record freshness and invalidators in the checklist, and return to a person when new permission, conflicting Context, judgment, or an external commitment is involved.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chengyixu/skills/klik-session-redaction-check)
- [Klik pre-launch direction](https://pre.hiklik.ai/?utm_source=clawhub&utm_medium=companion_skill&utm_campaign=kickstarter_prelaunch&utm_content=session_redaction_check)

## Skill Output:

**Output Type(s):** [Markdown, Guidance]

**Output Format:** [Markdown checklist]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Non-executing redaction review output; it does not authorize account access, external commitments, or execution.]

## Skill Version(s):

1.0.0 (source: server release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
