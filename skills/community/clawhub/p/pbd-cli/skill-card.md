## Description: <br>
Command-line tool for the PaleBlueDot AI Platform that supports login, API token management, usage and balance queries, wallet balance checks, and browsing available AI models. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[derekdong-star](https://clawhub.ai/user/derekdong-star) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and PaleBlueDot users use this skill to operate pbd-cli for account authentication, API token lifecycle management, quota and wallet checks, usage review, and model discovery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill installs remote code through a shell pipeline. <br>
Mitigation: Review the installer before running it and prefer a pinned release with checksum or signature verification. <br>
Risk: The skill handles session cookies and plaintext API keys. <br>
Mitigation: Use browser login when possible and keep cookies, API keys, screenshots, logs, and shell history private. <br>
Risk: Token deletion and key-retrieval commands can expose or remove account credentials. <br>
Mitigation: Run those commands only when intended, confirm token IDs before deletion, and avoid sharing retrieved keys. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/derekdong-star/pbd-cli) <br>
- [PaleBlueDot website](https://www.palebluedot.ai) <br>
- [PaleBlueDot API base URL](https://open.palebluedot.ai) <br>
- [pbd-cli installation script](https://raw.githubusercontent.com/PaleBlueDot-AI-Open/pbd-cli/main/install.sh) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON-oriented CLI output descriptions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference local pbd-cli configuration and authenticated account state.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence; artifact frontmatter reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
