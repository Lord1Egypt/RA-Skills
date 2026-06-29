## Description: <br>
RedFoxHub (redfox.hk) lets an agent search and read RedFoxHub data through OOMOL's `redfox` connector instead of calling the API directly. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to fetch account, work, article, and search result payloads from Douyin, WeChat Official Accounts, Xiaohongshu, TikTok, and RedFoxHub AI creation datasets through an OOMOL-connected account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill queries RedFoxHub through the user's OOMOL-connected account. <br>
Mitigation: Install and use it only when the agent is expected to access RedFoxHub data for that account. <br>
Risk: One-time CLI installation, login, or connection setup can affect the local environment or account connection state. <br>
Mitigation: Run setup only after an auth or connection failure, and verify the OOMOL CLI and RedFoxHub connection pages before proceeding. <br>
Risk: Future connector actions marked write or destructive could change or remove RedFoxHub data. <br>
Mitigation: Require explicit user approval and confirm the exact payload and target before running any action marked write or destructive. <br>


## Reference(s): <br>
- [RedFoxHub homepage](https://redfox.hk) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [OOMOL CLI install guide](https://cli.oomol.com/install-guide.md) <br>
- [ClawHub RedFoxHub skill page](https://clawhub.ai/oomol/skills/oo-redfox) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, JSON] <br>
**Output Format:** [Markdown guidance with bash commands and JSON connector responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Connector responses include a data payload and meta.executionId.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
