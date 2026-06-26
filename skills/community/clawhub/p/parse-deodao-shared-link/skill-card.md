## Description: <br>
Parses Dedao note share links to extract cleaned article text and optionally download article images. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ymsha88](https://clawhub.ai/user/ymsha88) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents assisting users with Dedao note links use this skill to open a supplied dedao.cn share URL, extract the note title and body text, and optionally save referenced images for local Markdown notes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can browse arbitrary supplied URLs and fetch remote images. <br>
Mitigation: Restrict accepted input to trusted Dedao share links before execution. <br>
Risk: The runner writes scraped content and images to a fixed local folder by default. <br>
Mitigation: Change the output directory to a user-approved workspace path and add overwrite protection before use. <br>
Risk: Chromium is launched with sandboxing disabled. <br>
Mitigation: Avoid running it on a normal desktop environment unless the scripts have been reviewed and sandbox settings are appropriate. <br>
Risk: Image downloads may consume unexpected local storage. <br>
Mitigation: Add image size and count limits before processing unreviewed links. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ymsha88/parse-deodao-shared-link) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, files] <br>
**Output Format:** [Markdown notes and JavaScript result objects containing extracted title, content, image metadata, and saved image files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write scraped content and downloaded images to a local output directory.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
