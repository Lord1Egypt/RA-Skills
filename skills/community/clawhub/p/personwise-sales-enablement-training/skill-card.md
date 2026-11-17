## Description:

Turns approved messaging into an askable digital-human sales-readiness course.

This skill is ready for commercial/non-commercial use.

## Publisher:

[personwiseai](https://clawhub.ai/user/personwiseai)

### License/Terms of Use:

MIT-0

## Use Case:

Sales and enablement teams use this skill to build an interactive digital-human readiness course from approved positioning, messaging, and launch materials. The course is intended to help reps learn the buyer story, approved proof points, objection handling, and readiness checks without introducing unsupported commercial claims.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The update workflow can ask the agent to run a command that modifies the PersonWise CLI or installed skill.

Mitigation: Approve only explicit PersonWise install or upgrade commands that match the intended action, and reject opaque commands, unexpected origins, or unexpected destinations.

Risk: A generated sales-readiness course could include unsupported commercial claims if source materials are incomplete or ambiguous.

Mitigation: Keep the course evidence-locked to user-approved materials and route pricing, discounting, unsupported customer claims, and out-of-scope contract questions back to the user's deal desk or leadership.

Risk: The workflow uses browser OAuth and may upload user-selected source materials to PersonWise.

Mitigation: Do not request or handle passwords, tokens, cookies, or secrets; upload only user-named or explicitly approved files and avoid exposing upload grants or signed URLs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/personwiseai/skills/personwise-sales-enablement-training)
- [PersonWise publisher profile](https://clawhub.ai/user/personwiseai)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown summaries with CLI commands and JSON course-blueprint configuration.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces an interactive digital-human course through PersonWise, with run and project identifiers, source statuses, review results, access state, and the final course URL when available.]

## Skill Version(s):

2.1.9 (source: server release evidence and skill invocation attribution)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
