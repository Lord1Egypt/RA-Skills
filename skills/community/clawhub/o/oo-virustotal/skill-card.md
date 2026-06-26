## Description: <br>
VirusTotal (virustotal.com). Use this skill for VirusTotal requests, including reading, creating, and updating data through the OOMOL connector instead of calling the API directly. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts use this skill to inspect VirusTotal reports and relationships, search VirusTotal objects, and submit URLs, files, comments, votes, or rescans through an OOMOL-connected VirusTotal account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires an OOMOL-connected VirusTotal account and can use sensitive account capabilities. <br>
Mitigation: Install it only when VirusTotal access through that account is intended, and keep connector authentication scoped to the needed account. <br>
Risk: URL scans, file uploads, rescans, comments, and votes may submit data to VirusTotal or affect community-visible state, quota, or credits. <br>
Mitigation: Confirm the exact target, payload, and intended effect before running those actions. <br>
Risk: Security evidence notes a documentation mismatch around confirmation for URL scans and file rescans. <br>
Mitigation: Treat URL scans and file rescans as confirmation-required actions even when the source text is less explicit. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/oomol/oo-virustotal) <br>
- [VirusTotal Homepage](https://www.virustotal.com) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [OOMOL CLI Install Guide](https://cli.oomol.com/install-guide.md) <br>
- [OOMOL VirusTotal Connection](https://console.oomol.com/app-connections?provider=virustotal) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live connector schemas before execution and returns connector responses as JSON when actions run.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
