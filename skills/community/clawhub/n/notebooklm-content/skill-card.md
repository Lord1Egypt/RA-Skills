## Description: <br>
Generates slides, audio overviews, and documents from text, URLs, and files using Google NotebookLM through Chrome browser automation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aoaibiz](https://clawhub.ai/user/aoaibiz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to automate NotebookLM workflows that create learning and presentation assets from user-provided text, URLs, and files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The browser relay can act in a logged-in Chrome tab and operate NotebookLM on the user's behalf. <br>
Mitigation: Enable the relay only on the intended NotebookLM tab and review the browser state before returning or sharing generated links. <br>
Risk: NotebookLM sources may be sent to Google NotebookLM during content generation. <br>
Mitigation: Avoid sensitive or regulated material unless approved, and review NotebookLM sharing settings before sending any returned link. <br>
Risk: The local gateway token grants access to the browser relay. <br>
Mitigation: Keep the gateway token private and do not paste it into chat or generated content. <br>


## Reference(s): <br>
- [Chrome Relay Setup Guide](references/chrome-relay-setup.md) <br>
- [Google NotebookLM](https://notebooklm.google.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and returned NotebookLM links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an active Chrome relay, a logged-in NotebookLM session, and fresh browser snapshots before actions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
