## Description: <br>
BigPicture.io (bigpicture.io). Use this skill for ANY BigPicture.io request - searching and reading data. Whenever a task involves BigPicture.io, use this skill instead of calling the API directly. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to query BigPicture.io company intelligence from an OOMOL-connected account, including company lookup by domain and company identification from IPv4 or IPv6 addresses. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill relies on OOMOL-connected BigPicture.io credentials handled server-side. <br>
Mitigation: Confirm trust in OOMOL and BigPicture.io before installation and use only the intended connected account. <br>
Risk: First-time setup includes optional pipe-to-shell installer commands for the oo CLI. <br>
Mitigation: Review OOMOL's install guide or installer script before running the installer, especially in managed environments. <br>
Risk: Connector payloads can drift if the live BigPicture.io action schema changes. <br>
Mitigation: Fetch the live connector schema before each action and build payloads to match the current contract. <br>


## Reference(s): <br>
- [BigPicture.io homepage](https://bigpicture.io) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [OOMOL oo CLI install guide](https://cli.oomol.com/install-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON connector responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live connector schemas before execution and returns BigPicture.io results through the oo CLI.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
