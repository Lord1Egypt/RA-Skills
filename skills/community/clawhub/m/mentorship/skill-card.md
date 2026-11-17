## Description:

Finding, maintaining, and providing mentorship relationships. Use when someone wants guidance in career or skill development, wants to find a mentor, has been asked to mentor someone, or values cross-generational knowledge transfer.

This skill is ready for commercial/non-commercial use.

## Publisher:

[howtousehumans](https://clawhub.ai/user/howtousehumans)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to get practical guidance for finding mentors, running productive mentor conversations, becoming a mentor, and transferring career or trade knowledge.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release evidence reports suspicious packaging because the skill declares filesystem access even though the mentorship guidance should not need it.

Mitigation: Install and run only in a constrained environment after confirming requested permissions are acceptable.

Risk: The release evidence notes an unpinned npx install command.

Mitigation: Verify the package source and prefer a pinned or otherwise authenticated install before deployment.

Risk: Mentorship advice can be inappropriate when a mentor crosses professional or personal boundaries.

Mitigation: Follow the skill's rule to flag boundary issues and help the user assess whether the relationship should continue.

## Reference(s):

- [Harvard Business Review](https://hbr.org)

## Skill Output:

**Output Type(s):** [guidance, markdown]

**Output Format:** [Markdown with structured advice, scripts, checklists, and conversation frameworks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May tailor mentorship guidance to the user's role, industry context, and mentorship stage.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
