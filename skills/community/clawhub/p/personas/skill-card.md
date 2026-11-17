## Description:

Provides 20 specialized OpenClaw persona modes that an assistant can list, activate, inspect, switch between, and exit while loading only the active persona.

This skill is ready for commercial/non-commercial use.

## Publisher:

[robbyczgw-cla](https://clawhub.ai/user/robbyczgw-cla)

### License/Terms of Use:

MIT

## Use Case:

External OpenClaw users use this skill to switch an assistant into one of 20 bundled persona modes for coding, writing, learning, lifestyle, and professional guidance. Medical and legal personas are educational or orientation-only and do not replace licensed professionals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persona mode can persist and make later assistant responses appear unusual or domain-biased.

Mitigation: Prefer explicit /personas commands, check the active persona when responses seem unexpected, and use /personas exit or the CLI reset command to return to the default mode.

Risk: Broad activation phrases such as use persona, switch to, or activate can trigger persona switching unintentionally.

Mitigation: Confirm the intended active persona after activation and reset persona mode when the specialized style is no longer needed.

Risk: Medical and legal personas can be mistaken for professional advice.

Mitigation: Treat those personas as educational or orientation-only and consult licensed professionals for medical or legal decisions.

Risk: Several bundled personas may answer in German.

Mitigation: Select personas intentionally and ask for a different response language or exit the persona if the language does not match the user's needs.

Risk: The CLI writes active-persona state to the local ~/.openclaw/persona-state.json file.

Mitigation: Use the reset command to clear active persona state and review local state handling before deploying in shared or managed environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/robbyczgw-cla/skills/personas)
- [Publisher profile](https://clawhub.ai/user/robbyczgw-cla)
- [README](README.md)
- [FAQ](FAQ.md)
- [Changelog](CHANGELOG.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown persona prompts and short text status output, with optional shell commands for the bundled CLI.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Loads one active persona at a time; the CLI stores local active-persona state in ~/.openclaw/persona-state.json.]

## Skill Version(s):

2.3.0 (source: SKILL.md frontmatter and changelog released 2026-08-31)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
