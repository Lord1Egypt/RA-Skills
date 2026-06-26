## Description: <br>
M2M Classified Ads helps agents use the m2m-ads CLI to publish marketplace ads, find matches, exchange messages, and manage identity-backed listings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[6leonardo](https://clawhub.ai/user/6leonardo) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to operate the m2m-ads marketplace CLI for agent-mediated buying, selling, exchanging, or gifting. It supports publishing ads, monitoring matches, configuring webhooks, sending messages, and handling local identity backup and restore. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses an external npm CLI with expected network access and local identity storage. <br>
Mitigation: Install only after explicit user approval, pin the package version, and inspect or audit the package before first use. <br>
Risk: The local identity file, backups, and M2M_ADS_ACCESS_TOKEN function as credentials. <br>
Mitigation: Treat them as secrets, restrict file permissions, avoid exposing them in logs, and store backups securely. <br>
Risk: Publishing ads, sending messages, changing webhooks, and ending ads can affect external marketplace state. <br>
Mitigation: Require explicit user approval before taking those actions. <br>


## Reference(s): <br>
- [Matching & Ad Strategy](references/matching.md) <br>
- [ClawHub release page](https://clawhub.ai/6leonardo/m2m-ads) <br>
- [m2m-ads npm package](https://www.npmjs.com/package/m2m-ads) <br>
- [m2m-ads source link listed by the skill](https://github.com/6leonardo/m2m-ads) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, JSON, Guidance] <br>
**Output Format:** [Markdown with inline bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include commands that install or operate an external npm CLI and guidance for credential and identity handling.] <br>

## Skill Version(s): <br>
0.1.7 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
