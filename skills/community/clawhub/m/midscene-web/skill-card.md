## Description: <br>
Midscene Web enables vision-driven browser automation from screenshots without relying on DOM structure or accessibility labels. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lushi516](https://clawhub.ai/user/lushi516) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to browse websites, collect page data, fill forms, take screenshots, and validate frontend behavior through Midscene-driven browser automation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can operate logged-in Chrome sessions and act on visible account pages. <br>
Mitigation: Prefer isolated Puppeteer mode for ordinary browsing, use a dedicated Chrome profile or tab for account work, and require explicit approval before purchases, payments, posting, form submission, deletion, or account changes. <br>
Risk: Page screenshots may be sent to the configured AI model provider during automation. <br>
Mitigation: Use only approved model providers and avoid exposing sensitive pages or credentials unless the user accepts that data flow. <br>
Risk: CDP or Bridge access can keep an existing browser reachable after setup. <br>
Mitigation: Disable CDP or Bridge access when finished and disconnect sessions after completing browser automation. <br>


## Reference(s): <br>
- [Midscene.js](https://midscenejs.com) <br>
- [Midscene Model Configuration](https://midscenejs.com/model-common-config) <br>
- [Midscene Bridge Mode Documentation](https://midscenejs.com/bridge-mode-by-chrome-extension.html) <br>
- [ClawHub Skill Page](https://clawhub.ai/lushi516/midscene-web) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce browser screenshots, automation results, extracted page data, and task summaries.] <br>

## Skill Version(s): <br>
26.5.14 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
