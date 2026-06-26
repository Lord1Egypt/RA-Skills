## Description: <br>
Privacy Eraser helps agents scan for exposed personal information, recommend removal paths, generate privacy complaint templates, and set up periodic monitoring. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tykoo-eth](https://clawhub.ai/user/tykoo-eth) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and their agents use this skill to find public exposure of personal data, prepare removal or complaint materials, and track follow-up monitoring across platform, search, and regulator channels. <br>

### Deployment Geography for Use: <br>
Global, with China, EU, and U.S. platform and legal templates. <br>

## Known Risks and Mitigations: <br>
Risk: The skill may use logged-in browser sessions and submit platform reports on the user's behalf. <br>
Mitigation: Keep the skill in advisory or manual-review mode where possible and require user confirmation before any complaint is submitted. <br>
Risk: The skill may process sensitive identity information and evidence records. <br>
Mitigation: Redact identity documents, minimize stored case files, and keep explicit retention limits for screenshots and complaint records. <br>
Risk: Some reporting tactics may be misleading if the facts do not support the selected complaint category or DMCA claim. <br>
Mitigation: Review every generated complaint for accuracy and use only report categories and legal claims supported by the evidence. <br>
Risk: Recurring monitoring can repeatedly search for identity details using logged-in or personally identifying context. <br>
Mitigation: Set clear monitoring scope, cadence, and stop conditions before enabling scheduled scans. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/tykoo-eth/privacy-eraser) <br>
- [Platform reporting guide](artifact/platforms.md) <br>
- [Privacy legal basis guide](artifact/legal_basis.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, shell commands, configuration] <br>
**Output Format:** [Markdown guidance, complaint templates, platform steps, browser-action instructions, and monitoring configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce privacy-removal drafts, evidence checklists, browser automation steps, screenshots or case-record guidance, and recurring monitoring schedules.] <br>

## Skill Version(s): <br>
0.2.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
