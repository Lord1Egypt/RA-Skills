## Description: <br>
Browser automation CLI for AI agents. Use when the user needs to interact with websites, including navigating pages, filling forms, clicking buttons, taking screenshots, extracting data, or automating any browser task. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[handongpu16](https://clawhub.ai/user/handongpu16) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to control a browser from the command line for navigation, form entry, clicking, screenshots, content extraction, downloads, tabs, dialogs, and page state checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agents receive broad browser control and can perform sensitive or state-changing actions. <br>
Mitigation: Use explicit instructions and review before submitting forms, logging in, accepting dialogs, downloading files, taking screenshots, or extracting content from private or account pages. <br>
Risk: Page element indices can become stale after navigation, form submissions, or dynamic content loading. <br>
Mitigation: Take a fresh browser snapshot after page changes before clicking, filling, or selecting indexed elements. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/handongpu16/my-browser-bot) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with command examples and browser state text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Browser commands can return page snapshots, element indices, screenshots, downloaded file paths, page metadata, element state, or task completion status.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
