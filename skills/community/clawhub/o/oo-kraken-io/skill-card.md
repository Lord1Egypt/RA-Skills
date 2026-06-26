## Description: <br>
Kraken.io lets agents check Kraken.io account status and optimize images through an OOMOL-connected account. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to operate Kraken.io from an agent session, including checking plan and monthly optimization quota status and optimizing images from a public URL or upload. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Image optimization can send image content to OOMOL/Kraken.io and store optimized results in connector transit. <br>
Mitigation: Run optimization only for image sources the user has confirmed are appropriate for external processing and storage. <br>
Risk: The optimize_image action is under-labeled as read-safe even though it processes image data. <br>
Mitigation: Treat optimize_image as a data-processing action and confirm the exact source and intended output before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-kraken-io) <br>
- [OOMOL publisher profile](https://clawhub.ai/user/oomol) <br>
- [Kraken.io homepage](https://kraken.io) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON connector payloads or responses.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May process image URLs or uploaded image content through Kraken.io and store optimized image results in connector transit.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
