## Description:

Adafruit IO (io.adafruit.com). Use this skill for ANY Adafruit IO request — reading, creating, and updating data. Whenever a task involves Adafruit IO, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to read Adafruit IO feeds and account information, and to create feed data through an OOMOL-connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup downloads and executes installer code whose exact contents have not been verified.

Mitigation: Review and install a verified CLI release before use.

Risk: CLI installation or synchronization can make persistent agent-skill changes.

Mitigation: Decide whether automatic installation and synchronization are acceptable, and disable synchronization if unwanted.

Risk: Feed-data creation changes Adafruit IO state.

Mitigation: Confirm the exact write payload and its effect with the user before running the action.

## Reference(s):

- [Adafruit IO API documentation](https://io.adafruit.com/api/docs/)
- [Adafruit IO](https://io.adafruit.com/)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [ClawHub release](https://clawhub.ai/oomol/skills/oo-adafruit-io)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Text, Guidance]

**Output Format:** [JSON action payloads and Adafruit IO results, with Markdown usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill supports read actions and feed-data creation; write actions require confirmation of the exact payload and effect.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
