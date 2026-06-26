## Description: <br>
A stable native browser (WKWebView) for OpenClaw agents. Opens a visible window with tab management, URL bar, and login helpers \u2014 every website works, including Perplexity, Grok, Claude, and ChatGPT. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yungookim](https://clawhub.ai/user/yungookim) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill to browse websites through a visible native macOS WKWebView, including authenticated sites, form interactions, JavaScript execution, screenshots, and tab management. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks users to install external code before use. <br>
Mitigation: Review and pin the external repository code before installation. <br>
Risk: Agents may access persistent logged-in browser sessions. <br>
Mitigation: Use isolated or disposable accounts, avoid sensitive personal logins unless necessary, and clear cookies and tabs after use. <br>
Risk: Disabling built-in web tools can route future web tasks through this persistent browser session. <br>
Mitigation: Disable built-in web tools only when that routing behavior is intended. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/yungookim/openclaw-browser-2) <br>
- [OpenClaw Browser Repository](https://github.com/yungookim/openclaw-browser) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline Python, shell, and JSON code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces browser-control guidance and example commands; runtime behavior can create persistent web sessions and screenshots when the referenced browser package is installed.] <br>

## Skill Version(s): <br>
0.1.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
