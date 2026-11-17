## Description:

Run a persistent Linux Chrome session with VNC/noVNC human takeover and capture an existing tab through CDP. Use for remote browser workflows that need manual login, MFA, or operator inspection followed by automation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[waylonsong](https://clawhub.ai/user/waylonsong)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to run a persistent Linux Chrome session, hand control to an operator over VNC for login, MFA, or inspection, and capture a specific existing tab for later automation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Explicit cookie or storage-state exports may contain authentication data.

Mitigation: Request these exports only when needed and restrict access to the resulting private files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/waylonsong/skills/headful-browser-vnc)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, HTML, PNG]

**Output Format:** [Shell commands with JSON status and manifest data; captured HTML and PNG files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Session-scoped browser captures; cookie or storage-state exports are available only when explicitly requested.]

## Skill Version(s):

2.0.0 (source: server metadata, SKILL.md frontmatter, package.json, CHANGELOG)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
