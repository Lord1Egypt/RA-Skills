## Description:

Improves a voice profile by learning from manual edits. Use after editing generated text to refine registers and close voice drift over time

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Writers and developers use this skill after manually editing generated text to identify recurring changes and propose focused updates to a voice profile.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review was partial because two local references could not be resolved.

Mitigation: Review those references before installation if they are important to the skill's use.

Risk: A one-off edit or contradictory edits could lead to an unsuitable voice-profile rule.

Mitigation: Apply the documented recurrence threshold, check for contradictions, and get user approval before changing the profile.

Risk: Learning snapshots contain generated, reviewed, and manually edited text.

Mitigation: Keep the voice-profile snapshot directory private and archive or remove completed snapshots when they are no longer needed.

## Reference(s):

- [Scribe plugin homepage](https://github.com/athola/claude-night-market/tree/master/plugins/scribe)
- [ClawHub release page](https://clawhub.ai/athola/skills/nm-scribe-voice-learn)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Configuration instructions]

**Output Format:** [Structured pattern analysis and proposed voice profile edits in Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses recurring-edit evidence thresholds; profile changes require user approval.]

## Skill Version(s):

1.10.3 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
