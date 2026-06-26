## Description: <br>
Use this skill to query Google NotebookLM notebooks from Claude Code for source-grounded, citation-backed answers with browser automation, library management, and persistent authentication. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[guccidgi](https://clawhub.ai/user/guccidgi) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External developers and Claude Code users use this skill to ask questions against their Google NotebookLM notebooks, manage a local notebook library, and retrieve source-grounded research answers for coding and documentation tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores reusable Google session data and local notebook metadata. <br>
Mitigation: Protect the skill data directory, avoid storing sensitive notebooks, and regularly clear local session data when it is no longer needed. <br>
Risk: The skill automates a logged-in Google NotebookLM browser session. <br>
Mitigation: Use a dedicated Google account for automation and confirm that browser automation is acceptable for the intended account and workspace. <br>
Risk: Automatic follow-up queries and NotebookLM usage may hit service limits or exceed the user's intended scope. <br>
Mitigation: Set limits before allowing automatic follow-up queries and monitor account query limits during use. <br>


## Reference(s): <br>
- [NotebookLM Skill API Reference](references/api_reference.md) <br>
- [NotebookLM Skill Usage Patterns](references/usage_patterns.md) <br>
- [NotebookLM Skill Troubleshooting Guide](references/troubleshooting.md) <br>
- [Authentication Architecture](AUTHENTICATION.md) <br>
- [Google NotebookLM](https://notebooklm.google/) <br>
- [Claude Code](https://github.com/anthropics/claude-code) <br>
- [Playwright session cookie persistence issue](https://github.com/microsoft/playwright/issues/36139) <br>
- [Playwright Python persistent context storage state issue](https://github.com/microsoft/playwright/issues/14949) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and plain text with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [NotebookLM answers may include source citations; follow-up prompts encourage additional queries when more context is needed.] <br>

## Skill Version(s): <br>
0.1.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
