## Description:

Helps people practice short motor sequences with rotated-start drills, old-versus-new interference exercises, and spaced recall.

This skill is ready for commercial/non-commercial use.

## Publisher:

[voronindenis5](https://clawhub.ai/user/voronindenis5)

### License/Terms of Use:

MIT

## Use Case:

People learning or changing a pattern, shortcut chain, riff, or controller combo use this skill to plan brief practice sessions and assess recall, accuracy, and interference from an old sequence. Use look-alike training sequences rather than real credentials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Real unlock patterns or PINs entered for training may remain in the local practice file.

Mitigation: Practice with look-alike sequences instead of real secrets, and delete pattern_tutor.json after use if its data is sensitive.

Risk: Non-interactive sessions report simulated practice results rather than measured proficiency.

Mitigation: Assess readiness using interactive practice and real-world repetitions rather than simulated metrics.

## Reference(s):

- [Motor-sequence learning reference](references/motor-learning.md)
- [ClawHub skill release](https://clawhub.ai/voronindenis5/skills/pattern-lock-tutor)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Terminal text and Markdown with shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The trainer saves sequence and session data to pattern_tutor.json in the working directory; non-interactive practice metrics are simulated.]

## Skill Version(s):

1.0.0 (source: frontmatter and ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
