## Description: <br>
HTML/CSS to Image helps an agent create images from raw HTML/CSS or public webpages, delete generated images, and retrieve usage through the OOMOL `oo` CLI connector. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to turn HTML/CSS or webpage URLs into images through a connected HTML/CSS to Image account, manage generated images, and review usage. It is intended for agents that need guided CLI commands and payload construction rather than direct API access. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill operates a connected HTML/CSS to Image account through OOMOL and requires trusted credential handling. <br>
Mitigation: Install and use it only when the OOMOL connection is intended, and review authentication or connection steps before running them. <br>
Risk: Image creation actions can change account state and may affect usage or billing. <br>
Mitigation: Review the exact action payload and expected effect with the user before approving write actions. <br>
Risk: Delete actions can remove generated images and clear CDN cache. <br>
Mitigation: Confirm the target image or batch explicitly before running destructive actions. <br>
Risk: The optional `oo` CLI installer runs remote installation scripts. <br>
Mitigation: Run the installer only if the CLI is needed and the user trusts OOMOL's installer source. <br>


## Reference(s): <br>
- [HTML/CSS to Image homepage](https://htmlcsstoimage.com) <br>
- [OOMOL CLI install guide](https://cli.oomol.com/install-guide.md) <br>
- [HTML/CSS to Image connection settings](https://console.oomol.com/app-connections?provider=htmlcsstoimage) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include `oo connector schema` and `oo connector run` commands; connector responses are JSON when executed.] <br>

## Skill Version(s): <br>
1.0.1 (source: server evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
