## Description:

Creates and runs a text-only pet adventure diary driven by real-world locations, local time, weather, D20-style event checks, and emergency phone calls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jichengkai](https://clawhub.ai/user/jichengkai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to maintain a persistent Chinese-language text pet that travels through real-world locations, writes daily diary entries, and asks the user to resolve D20-style phone events.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill persists diary, state, world, event, and call files in a pet-life folder inside the selected workspace.

Mitigation: Run it only in a workspace where those local files are expected, and review or remove the pet-life folder when the simulation is no longer needed.

Risk: Daily advancement may request local weather from Open-Meteo for the simulated location.

Mitigation: Use the documented --offline option when external weather requests are not desired.

Risk: Urgent fictional phone events can auto-resolve after their deadline if the user does not choose a response.

Mitigation: Check status before advancing the simulation and answer pending calls when user choice should determine the outcome.

## Reference(s):

- [宠物冒险生活规则](references/rules.md)
- [OpenClaw Integration](references/openclaw.md)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, guidance]

**Output Format:** [JSON command results and Markdown diary entries with Chinese user-facing prose.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates persistent pet-life workspace files; weather lookup can be disabled with --offline.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
