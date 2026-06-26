## Description: <br>
Read, write, and analyze Google Sheets with AI-powered insights, formula generation, and data summarization. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[evolinkai](https://clawhub.ai/user/evolinkai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and spreadsheet operators use this skill to connect a Google account through Maton, read or modify Google Sheets, manage spreadsheet formatting, and optionally request AI analysis, summaries, or formula suggestions through EvoLink. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Crafted spreadsheet data or command input could trigger unsafe local command construction. <br>
Mitigation: Review before installing, avoid untrusted spreadsheets or crafted inputs, and fix the script to pass data through stdin, files, or encoded arguments instead of embedding it into Python source. <br>
Risk: Google Sheets operations are routed through Maton, and optional AI commands send spreadsheet data to EvoLink. <br>
Mitigation: Use only with Google accounts and Sheets data approved for Maton processing, and avoid AI commands for confidential sheets unless EvoLink processing is approved. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/evolinkai/google-sheets-assistant) <br>
- [Project homepage](https://github.com/EvoLinkAI/google-sheets-skill-for-openclaw) <br>
- [EvoLink API documentation](https://docs.evolink.ai/en/api-manual/language-series/claude/claude-messages-api?utm_source=clawhub&utm_medium=skill&utm_campaign=google-sheets) <br>
- [Maton](https://maton.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Terminal text and Markdown guidance with shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3, curl, MATON_API_KEY, and optional EVOLINK_API_KEY for AI features.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
