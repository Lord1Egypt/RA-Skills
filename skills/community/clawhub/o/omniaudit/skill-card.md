## Description: <br>
OmniAudit scans OpenClaw skills, SKILL.md files, code, and repo ZIPs for prompt injection, credential theft, malware, reverse shells, and other threat patterns before installation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[legarams](https://clawhub.ai/user/legarams) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use OmniAudit before installing ClawHub or OpenClaw skills, running shared code, or reviewing security-sensitive files to request a remote security scan with explicit consent for local content and paid scans. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Scans may transmit selected code, local files, or ZIP contents to OmniAudit. <br>
Mitigation: Only approve scans for content you are comfortable sharing, and require explicit consent before sending local file or ZIP contents. <br>
Risk: Paid scans can spend USDC through x402 on Base. <br>
Mitigation: Verify the quoted USDC cost and obtain a clear approval before initiating any paid scan. <br>


## Reference(s): <br>
- [OmniAudit Homepage](https://omniaudit.fly.dev) <br>
- [ClawHub Skill Page](https://clawhub.ai/legarams/omniaudit) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Guidance] <br>
**Output Format:** [Markdown security report and consent/payment guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May involve remote scans of URLs, code snippets, local files, or ZIPs after required consent; paid scans require explicit approval.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata; artifact frontmatter states 1.0.3) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
