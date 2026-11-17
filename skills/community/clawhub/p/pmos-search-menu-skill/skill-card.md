## Description:

Automates navigation through menu paths on the Gansu Electric Power Trading PMOS platform by opening pages, handling tabs, and capturing browser snapshots.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xu-oliver](https://clawhub.ai/user/xu-oliver)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators with authorized PMOS access use this skill to navigate the PMOS information disclosure and market-operation menu path, switch to the relevant tab, and collect page snapshots or element references for follow-on browser actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Node.js helper can run unintended local commands if a malicious element reference is entered.

Mitigation: Review before installing, avoid element references from untrusted sources, and prefer manual browser commands or the quoted shell workflow until argument-array process execution and reference validation are added.

Risk: The workflow acts inside an authenticated PMOS browser session.

Mitigation: Use only with an authorized PMOS account and confirm the active browser tab before executing navigation or snapshot commands.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/xu-oliver/skills/pmos-search-menu-skill)
- [OpenClaw Browser Tool Documentation](https://docs.openclaw.ai/tools/browser)
- [OpenClaw CLI Browser Reference](https://docs.openclaw.ai/cli/browser)
- [Navigation Path Reference](artifact/pmos-search-menu-skill/references/NAVIGATION_PATH.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with inline shell commands and browser-navigation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include PMOS menu paths, browser snapshot instructions, tab handling steps, and element reference guidance.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
