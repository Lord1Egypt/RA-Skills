## Description: <br>
ShortPixel connector skill for reading, creating, updating, and deleting ShortPixel domain and CDN data through the OOMOL oo CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to operate a connected ShortPixel account from an agent, including domain association, CDN usage lookup, and cache or optimized-storage purge actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can operate an OOMOL-connected ShortPixel account and requires sensitive credentials managed outside the skill. <br>
Mitigation: Install only when the agent should operate that account, and rely on the documented OOMOL connection flow rather than exposing raw tokens. <br>
Risk: State-changing actions can add, set, or revoke domains, and destructive actions can purge CDN cache or stored optimized variants. <br>
Mitigation: Review exact domains and payloads before approval, and require explicit confirmation for write or destructive actions. <br>
Risk: First-time setup may ask the user to install or authenticate the oo CLI. <br>
Mitigation: Use setup steps only after a relevant command failure and verify the oo CLI installer source before running installation commands. <br>


## Reference(s): <br>
- [ClawHub ShortPixel Skill](https://clawhub.ai/oomol/oo-shortpixel) <br>
- [ShortPixel Homepage](https://shortpixel.com) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [oo CLI Install Guide](https://cli.oomol.com/install-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands operate through the OOMOL oo CLI and return JSON responses from the connector.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
