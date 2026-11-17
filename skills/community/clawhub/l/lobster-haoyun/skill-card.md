## Description:

Lobster Haoyun analyzes local conversation and memory patterns across five behavioral dimensions to generate Chinese personality readings, daily fortunes, cultivation reminders, and optional community recommendations through OceanBus.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ryanbihai](https://clawhub.ai/user/ryanbihai)

### License/Terms of Use:

MIT-0

## Use Case:

External ClawHub users use this skill for Chinese-language self-reflection, daily fortune generation, and lightweight behavioral guidance based on their agent conversation context. It is suited to users who accept local profile storage and limited OceanBus metadata exchange for calendar, story, and recommendation features.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill analyzes agent conversation context and memory to derive a behavioral profile.

Mitigation: Use it only after explicit first-run consent, and review the consent disclosure before allowing profile analysis.

Risk: The skill stores derived profile data, history, preferences, consent state, and OceanBus credentials locally under ~/.lucky-lobster.

Mitigation: Treat that directory as user data; delete ~/.lucky-lobster to clear the anonymous identity and locally stored profile state.

Risk: The skill sends limited profile metadata, city-level location when provided, date, and anonymous OpenID through OceanBus for calendar, story, and recommendation features.

Mitigation: Do not use the network-backed features unless that metadata exchange is acceptable for the user and deployment environment.

Risk: The security guidance notes supply-chain caveats around dependency pinning and downloaded font verification.

Mitigation: Prefer deployments that pin dependencies, verify downloaded assets, and document remote fields in the consent prompt.

## Reference(s):

- [ClawHub listing](https://clawhub.ai/ryanbihai/skills/lobster-haoyun)
- [Artifact README](artifact/README.md)
- [Skill definition](artifact/SKILL.md)
- [OceanBus npm package](https://www.npmjs.com/package/oceanbus)
- [Project homepage listed in artifact](https://github.com/ryanbihai/lobster-haoyun)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files]

**Output Format:** [Markdown fortune or personality reading with optional generated PNG card and local JSON state]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses Node.js commands, optional OceanBus environment variables, and local state under ~/.lucky-lobster.]

## Skill Version(s):

0.8.0 (source: SKILL.md frontmatter and server release metadata; package.json reports 0.5.12 and manifest.yaml reports 0.5.11)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
