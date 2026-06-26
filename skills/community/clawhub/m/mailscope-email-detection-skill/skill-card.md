## Description: <br>
Mailscope Email Detection helps an agent configure a Mailscope API key, upload an .eml file to the Mailscope service, and summarize phishing, spoofing, attachment, and general email security analysis results for the user. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ddgszc](https://clawhub.ai/user/ddgszc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Security analysts, developers, and other users use this skill to scan suspicious .eml files, review authentication and sender signals, and interpret Mailscope's email threat assessment. It also guides users through local API key configuration and prerequisite checks before analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uploads the selected email file, including headers, recipients, body content, links, and attachments, to the Mailscope service. <br>
Mitigation: Use it only when policy allows that upload, and avoid confidential, regulated, or third-party-sensitive emails unless approved. <br>
Risk: The skill requires a Mailscope API key stored in config.json. <br>
Mitigation: Keep config.json private, do not hardcode or expose API keys in responses, and rotate the key if it is shared. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ddgszc/mailscope-email-detection-skill) <br>
- [Server-resolved GitHub provenance](https://github.com/ddgszc/mailscope-email-detection-skill) <br>
- [Mailscope service](https://x.lizhisec.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and terminal-oriented guidance with shell commands and human-readable security report interpretation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js 22+, a local config.json API key, and an .eml file path; uploads email content to the Mailscope service for analysis.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
