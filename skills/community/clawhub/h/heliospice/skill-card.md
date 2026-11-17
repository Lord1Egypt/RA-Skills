## Description:

Query positions of spacecraft, planets, moons, and asteroids in the solar system.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huangzesen](https://clawhub.ai/user/huangzesen)

### License/Terms of Use:


## Use Case:

Developers, researchers, and analysts use this skill to query solar-system ephemeris data, compute distances between bodies, transform coordinate frames, and manage SPICE kernel cache state.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup installs an unpinned external Python package and the skill may use network or storage during SPICE kernel cache operations.

Mitigation: Install only in a virtual environment or container, pin and review the heliospice package version, and review upstream package provenance before use in sensitive environments.

## Reference(s):

- [Heliospice Skill Page](https://clawhub.ai/huangzesen/skills/heliospice)
- [Publisher Profile](https://clawhub.ai/user/huangzesen)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and code-oriented guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose Python package installation and SPICE kernel cache operations.]

## Skill Version(s):

0.4.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
