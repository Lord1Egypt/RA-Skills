## Description: <br>
Render Markdown as a shareable browser page by uploading selected .md files to a user-configured S3-compatible bucket where Docsify serves the public page. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rockbenben](https://clawhub.ai/user/rockbenben) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and documentation authors use this skill when they want an agent to publish selected Markdown as a public, shareable web page instead of returning long Markdown directly in chat. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Uploaded Markdown is publicly accessible at the returned URL. <br>
Mitigation: Use the skill only for content intended for public sharing, and avoid secrets, credentials, PII, confidential material, or untrusted Markdown. <br>
Risk: S3-compatible storage credentials are stored in plaintext in ~/.md-web/config.json. <br>
Mitigation: Protect the config file, avoid committing or sharing it, and restrict the storage token to the dedicated bucket where possible. <br>
Risk: Setting expire_days to 0 can clear the bucket lifecycle configuration. <br>
Mitigation: Use a dedicated bucket for this skill and review lifecycle settings before disabling automatic expiration. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/rockbenben/md-web) <br>
- [Skill homepage](https://github.com/rockbenben/aishort-skills/tree/main/skills/md-web) <br>
- [README.md](README.md) <br>
- [Docsify server README](docsify-server/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown response with a filename and clickable URL, plus setup guidance or shell commands when configuration or upload execution is needed.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Publishes selected Markdown to a public S3-compatible bucket and returns a Docsify-rendered URL; falls back to direct chat text if upload fails.] <br>

## Skill Version(s): <br>
1.1.0 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
