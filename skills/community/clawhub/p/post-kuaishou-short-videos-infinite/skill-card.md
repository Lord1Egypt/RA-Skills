## Description: <br>
Publishes short videos on the Kuaishou Creator platform, including upload, description entry, cover setup, AI-content declaration, download-permission configuration, and final publishing steps. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[infiniteask](https://clawhub.ai/user/infiniteask) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators or operators use this skill to guide an agent through publishing a short video to a signed-in Kuaishou Creator account, including upload, metadata entry, cover selection, AI-content declaration, download-permission setting, and publishing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The agent can complete a public Kuaishou post and change download permissions without a final user confirmation. <br>
Mitigation: Before publishing, require the agent to show the selected account, video file, title, description, tags, cover choice, AI-content declaration, and download setting, then wait for explicit approval. <br>
Risk: Using the skill lets an agent operate a signed-in Kuaishou Creator account. <br>
Mitigation: Install and run it only when supervised account-level browser automation is acceptable for the intended account and session. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/infiniteask/post-kuaishou-short-videos-infinite) <br>
- [Kuaishou Creator video upload page](https://cp.kuaishou.com/article/publish/video?tabType=1) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Configuration] <br>
**Output Format:** [Markdown with browser-action guidance and Python code snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides an agent-controlled browser session and file picker; no standalone output files are produced.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata; artifact frontmatter version is 1.0.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
