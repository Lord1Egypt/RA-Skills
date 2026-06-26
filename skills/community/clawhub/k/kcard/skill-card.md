## Description: <br>
Knowledge Card generator that extracts key knowledge from user-provided text, files, URLs, or images; chooses a concept, memo, process, or comparison card; outputs structured Markdown; and renders it as a PNG image. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[goog](https://clawhub.ai/user/goog) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to turn notes, articles, URLs, files, or images into concise knowledge cards for learning, reference, and memorization. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads user-provided text, files, URLs, or images and saves generated Markdown and PNG outputs locally. <br>
Mitigation: Use only material and output paths appropriate for the environment, and avoid confidential notes unless local storage is controlled. <br>
Risk: The rendering workflow can run a local browser-based renderer and load Google Fonts during rendering. <br>
Mitigation: Review the renderer before use in restricted environments and block or disable external asset loading when network contact is not acceptable. <br>
Risk: Security evidence marks the release as suspicious because of local file handling, browser rendering, and an undisclosed third-party font request. <br>
Mitigation: Perform security review and scan before deployment, and install only when those behaviors are acceptable. <br>


## Reference(s): <br>
- [Card Templates](artifact/references/card-templates.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/goog/kcard) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Files, Shell commands, Guidance] <br>
**Output Format:** [Markdown source file, rendered PNG image, and one-line summary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Cards are intended to stay concise, with one concept per card and a maximum of 195 words.] <br>

## Skill Version(s): <br>
1.6.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
