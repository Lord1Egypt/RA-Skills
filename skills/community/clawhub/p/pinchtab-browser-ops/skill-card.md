## Description: <br>
Browser automation via PinchTab CLI (nav/snap/find/click/fill/press/text) with low-token accessibility-tree flow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[WisZhou](https://clawhub.ai/user/WisZhou) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to drive browser workflows through PinchTab, including navigation, form filling, page text collection, and repeatable browser tasks. It is especially oriented toward low-token browser control and Xiaohongshu draft preparation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can operate inside a browser profile that is already logged into websites. <br>
Mitigation: Use a dedicated browser profile when possible, handle login and 2FA manually, and review browser state before automation continues. <br>
Risk: Browser automation may create drafts, submit content, or change account state if used without clear confirmation. <br>
Mitigation: Require explicit confirmation before submissions, saved drafts, purchases, account changes, public posts, or approved eval use. <br>
Risk: A missing or untrusted PinchTab CLI could make browser actions unreliable. <br>
Mitigation: Verify the PinchTab CLI separately before installation or use. <br>


## Reference(s): <br>
- [小红书长文发布](references/xiaohongshu-longform.md) <br>
- [ClawHub skill page](https://clawhub.ai/WisZhou/pinchtab-browser-ops) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and concise status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses page text, fresh snapshots, URLs, and visible UI markers to verify browser outcomes.] <br>

## Skill Version(s): <br>
0.1.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
