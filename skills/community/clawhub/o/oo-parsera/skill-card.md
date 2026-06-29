## Description: <br>
Parsera helps agents extract structured data or clean Markdown from webpages and parse attributes from supplied HTML or text through the OOMOL `oo` CLI connector. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill when they need Parsera-backed webpage extraction, Markdown extraction, or structured parsing while keeping Parsera credentials behind an OOMOL-connected account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: First-time setup includes a remote shell installer for the `oo` CLI. <br>
Mitigation: Install the `oo` CLI from official documentation using any available integrity checks before using the skill, rather than asking an agent to pipe a remote installer directly into the shell. <br>
Risk: Parsera requests are brokered through OOMOL and require a connected account for credentials. <br>
Mitigation: Use the skill only after intentionally signing in and connecting Parsera in OOMOL, and only if that credential-broker model is acceptable for the deployment. <br>


## Reference(s): <br>
- [Parsera homepage](https://parsera.org) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [ClawHub Parsera skill page](https://clawhub.ai/oomol/oo-parsera) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with `oo` CLI shell commands and JSON payloads or responses.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live connector schemas before constructing Parsera action payloads.] <br>

## Skill Version(s): <br>
1.0.2 (source: release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
