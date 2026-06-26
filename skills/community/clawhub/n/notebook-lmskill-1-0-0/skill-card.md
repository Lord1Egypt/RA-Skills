## Description: <br>
Use this skill to query Google NotebookLM notebooks from Claude Code for source-grounded, citation-backed answers, with browser automation, library management, and persistent authentication. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[1215656](https://clawhub.ai/user/1215656) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to connect Claude Code to Google NotebookLM notebooks, manage notebook metadata, and ask document-grounded questions that return citation-backed answers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores reusable Google session cookies and browser state on disk. <br>
Mitigation: Use a dedicated low-risk Google account, protect local browser_state files, and delete browser_state/state.json when the skill is no longer needed. <br>
Risk: The skill installs Python packages and browser automation components automatically. <br>
Mitigation: Review requirements.txt and run the skill in an isolated local environment before enabling it for regular use. <br>
Risk: The skill automates a logged-in Google session and uses stealth-like browser settings. <br>
Mitigation: Use it only for permitted NotebookLM workflows and do not use account rotation or automation to bypass service limits. <br>
Risk: Questions and notebook context may be sent to Google NotebookLM and Gemini. <br>
Mitigation: Avoid sensitive notebooks or accounts unless the data handling is approved for that use. <br>
Risk: The artifact includes misleading raw download and help links. <br>
Mitigation: Prefer the validated ClawHub release artifact and avoid raw ZIP links unless independently verified. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/1215656/notebook-lmskill-1-0-0) <br>
- [README](README.md) <br>
- [Authentication architecture](AUTHENTICATION.md) <br>
- [API reference](references/api_reference.md) <br>
- [Usage patterns](references/usage_patterns.md) <br>
- [Troubleshooting](references/troubleshooting.md) <br>
- [Playwright session-cookie persistence issue](https://github.com/microsoft/playwright/issues/36139) <br>
- [Playwright Python persistent-context storage state issue](https://github.com/microsoft/playwright/issues/14949) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and citation-backed answer text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a logged-in Google NotebookLM session and local browser automation; responses are grounded in uploaded notebook documents.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
