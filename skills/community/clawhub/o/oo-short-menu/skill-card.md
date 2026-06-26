## Description: <br>
Short Menu (shortmenu.com). Use this skill for any Short Menu request, including creating, updating, and deleting short links through an OOMOL-connected account. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to manage Short Menu short links from an agent through the OOMOL oo CLI connector. It supports create, update, and delete workflows while requiring live schema inspection and explicit confirmation for write or destructive actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create, update, or delete Short Menu links. <br>
Mitigation: Confirm the exact target, payload, and expected effect with the user before running write or destructive actions. <br>
Risk: The skill depends on the OOMOL oo CLI and a connected Short Menu account. <br>
Mitigation: Install and use it only when the user trusts OOMOL's CLI and account connection, and follow setup steps only after an auth or connection failure. <br>
Risk: Remote installer commands are referenced for first-time setup. <br>
Mitigation: Review installer commands before execution and avoid running setup commands proactively. <br>


## Reference(s): <br>
- [Short Menu homepage](https://shortmenu.com) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [OOMOL CLI install guide](https://cli.oomol.com/install-guide.md) <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-short-menu) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May execute OOMOL connector actions that return JSON responses containing data and an execution ID.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
