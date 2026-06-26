## Description: <br>
Generates prompts, shell commands, and configuration guidance for browser-based AI image and video generation through Google Gemini and Google Flow. <br>

This skill is for demonstration purposes and not for production usage. <br>

## Publisher: <br>
[pbseiya](https://clawhub.ai/user/pbseiya) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and content creators use this skill to draft and run browser-automation workflows for generating AI images, thumbnails, covers, banners, and short videos while tracking free-tier quotas. The bundled scripts currently present a demonstration skeleton that requires review and implementation before real automation is enabled. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill relies on a logged-in Google browser session for browser-based media generation. <br>
Mitigation: Use a dedicated Google account or isolated browser profile, avoid private prompts or media, and delete stored cookies, quota logs, and generated metadata when finished. <br>
Risk: The bundled scripts are demonstration skeletons and require browser automation code to be completed before they can produce real media. <br>
Mitigation: Review and implement the automation code with Puppeteer or Playwright, confirm current UI selectors, and test in an isolated environment before operational use. <br>
Risk: Free-tier quota and website UI behavior can change, which may break automation or produce unreliable results. <br>
Mitigation: Check quota before each run, monitor generated logs, and revalidate selectors and service behavior after provider UI changes. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/pbseiya/google-free-media-skill) <br>
- [Google Gemini](https://gemini.google.com) <br>
- [Google Flow](https://labs.google/flow) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with bash commands, JSON quota configuration, and generated media or metadata file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Scripts require a local browser environment and, as shipped, use demo placeholders unless browser automation code is completed and reviewed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
