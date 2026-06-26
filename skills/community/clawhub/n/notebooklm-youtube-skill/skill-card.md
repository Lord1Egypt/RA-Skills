## Description: <br>
Automate NotebookLM notebook creation from YouTube videos by extracting people featured in a video, researching them online, adding the video and research as NotebookLM sources, and generating an audio overview. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[x-rayluan](https://clawhub.ai/user/x-rayluan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to turn YouTube interviews, talks, and documentaries into NotebookLM notebooks with added research context and an Audio Overview. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill controls Chrome while the user is logged into NotebookLM, so actions occur inside the user's Google session. <br>
Mitigation: Use a dedicated browser profile or test Google account, supervise the first run, and confirm each NotebookLM action before relying on the result. <br>
Risk: Uploaded video content and generated research may include confidential, private, or unauthorized material. <br>
Mitigation: Avoid confidential videos, private research, and content the user is not allowed to upload to NotebookLM. <br>
Risk: NotebookLM has multiple similar text areas, and automation can target the wrong field if UI state is not verified. <br>
Mitigation: Follow the screenshot-first workflow, use the documented specific selectors, and verify source insertion after each browser action. <br>


## Reference(s): <br>
- [NotebookLM UI Quick Reference](references/notebooklm_ui_guide.md) <br>
- [ClawHub release page](https://clawhub.ai/x-rayluan/notebooklm-youtube-skill) <br>
- [NotebookLM](https://notebooklm.google.com/) <br>
- [Claude skills documentation](https://support.claude.com/en/articles/12512180-using-skills-in-claude) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code] <br>
**Output Format:** [Markdown guidance with browser-automation steps and JavaScript snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create NotebookLM notebooks, add YouTube and copied-text sources, and start Audio Overview generation in a logged-in browser session.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
