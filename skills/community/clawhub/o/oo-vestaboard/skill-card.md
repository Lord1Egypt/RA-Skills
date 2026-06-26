## Description: <br>
Vestaboard lets an agent read the current display and transition settings, send messages, and update transition behavior through an OOMOL-connected Vestaboard account. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to operate a connected Vestaboard from an agent workflow, including reading the current board state and applying reviewed message or transition updates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can change the message or transition settings on a connected Vestaboard. <br>
Mitigation: Confirm the exact payload and expected effect with the user before running write actions. <br>
Risk: The skill depends on an OOMOL-connected Vestaboard account and server-side credential handling. <br>
Mitigation: Install and use it only when the user intends to let OOMOL operate that Vestaboard account through the oo CLI. <br>
Risk: First-time CLI setup may involve pipe-to-shell installation commands. <br>
Mitigation: Verify the installer source against OOMOL's official installation documentation before running setup commands. <br>


## Reference(s): <br>
- [ClawHub Vestaboard skill listing](https://clawhub.ai/oomol/oo-vestaboard) <br>
- [Vestaboard homepage](https://www.vestaboard.com) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [OOMOL oo CLI install guide](https://cli.oomol.com/install-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands use the oo CLI and may return JSON responses from Vestaboard connector actions.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
