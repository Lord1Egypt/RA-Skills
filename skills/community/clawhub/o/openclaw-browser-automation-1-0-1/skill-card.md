## Description: <br>
Automates web browser interactions through CLI commands for navigating pages, extracting data, taking screenshots, filling forms, clicking buttons, and interacting with web applications. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[q262045312-ui](https://clawhub.ai/user/q262045312-ui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to drive browser sessions from natural-language CLI commands for authorized browsing, data extraction, screenshots, form interactions, and web application workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automate sensitive browser actions such as form entry, authenticated navigation, and downloads. <br>
Mitigation: Use it only on authorized sites, avoid sensitive accounts, and confirm intent before submitting forms or downloading files. <br>
Risk: Browser sessions, screenshots, and downloads may persist after use. <br>
Mitigation: Clear the Chrome profile and agent output folders after completing a task. <br>
Risk: Setup runs npm install and npm link against CLI source that was not independently reviewed here. <br>
Mitigation: Review the actual package and source before installation, preferably in an isolated environment. <br>
Risk: Remote Browserbase mode may route browsing through external infrastructure when Browserbase keys are configured. <br>
Mitigation: Remove Browserbase keys unless remote browsing is intended and approved. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/q262045312-ui/openclaw-browser-automation-1-0-1) <br>
- [Publisher profile](https://clawhub.ai/user/q262045312-ui) <br>
- [Browser Automation CLI Reference](artifact/REFERENCE.md) <br>
- [Browser Automation Examples](artifact/EXAMPLES.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Files, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands; browser CLI commands return JSON and file paths.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands can create PNG screenshots and downloaded files in agent output folders.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact _meta.json reports 1.0.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
