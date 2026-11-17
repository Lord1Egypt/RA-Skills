## Description:

MTTSports guides an agent through MTT Sports poker workflows using the mttsports CLI, including authentication, balance checks, room management, session watching, and table actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[songlairui](https://clawhub.ai/user/songlairui)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to play or observe MTT Sports poker through the installed CLI. It supports account status, room discovery and creation, table joining, session daemon lifecycle, event watching, and constrained autonomous gameplay decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can authorize login, room joins, chip add-ons, and poker decisions through the CLI.

Mitigation: Use a dedicated or limited-balance account and require explicit session-level approval and spending limits before joins, add-ons, auto mode, or high-risk actions.

Risk: Credentials or session tokens may be exposed if passed directly in visible commands or copied into files.

Mitigation: Avoid visible raw passwords and tokens where possible, never write extra token copies to disk, and confirm login state through structured status commands.

Risk: Autonomous gameplay can make chip-backed decisions with weak safeguards.

Mitigation: Define strategy boundaries before play, require confirmation for actions outside those boundaries, and base in-hand actions only on current session watch events.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/songlairui/skills/mttsports)
- [MTT Sports CLI npm package](https://www.npmjs.com/package/@mtt-open/mttsports-cli)
- [MTT Sports platform](https://sports.mtt.xyz)
- [Session lifecycle reference](artifact/session/references/lifecycle.md)
- [Session watch reference](artifact/session/references/watch.md)
- [Session operate reference](artifact/session/references/operate.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, JSON, NDJSON]

**Output Format:** [Markdown guidance with shell command examples and structured JSON or NDJSON command outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prefers --output json for stable CLI responses; session watch emits machine-facing NDJSON.]

## Skill Version(s):

0.0.5 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
