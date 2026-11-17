## Description:

Square (squareup.com). Use this skill for ANY Square request — reading, creating, and updating data. Whenever a task involves Square, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to read and manage Square customer profiles and retrieve seller locations through their connected OOMOL account. It provides guidance for choosing an action, checking its input schema, and reviewing changes before writes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Fallback setup runs downloaded installer code without a clear approval step.

Mitigation: Review and explicitly approve a pinned, verified oo CLI installation before setup. Confirm the exact payload and effect before running customer creation or update actions.

## Reference(s):

- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [Square](https://squareup.com)
- [Square API reference](https://developer.squareup.com/reference/square)

## Skill Output:

**Output Type(s):** [API calls, Shell commands, JSON, Guidance]

**Output Format:** [Shell commands with JSON inputs and Square connector results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results vary by action and may include Square customer or location data.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
