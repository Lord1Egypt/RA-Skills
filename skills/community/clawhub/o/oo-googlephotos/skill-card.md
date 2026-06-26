## Description: <br>
Google Photos (google.com). Use this skill for ANY Google Photos request: reading, creating, updating, and deleting data through the OOMOL Google Photos connector. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an agent operate Google Photos through an OOMOL-connected account, including album, media item, upload, download, picker session, and metadata workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can perform sensitive Google Photos write actions such as uploads, album updates, description changes, and picker session creation. <br>
Mitigation: Confirm the exact payload and expected effect with the user before running any action tagged as write. <br>
Risk: The skill includes a destructive action for deleting picker sessions. <br>
Mitigation: Require explicit user approval for the target session before running destructive actions. <br>
Risk: The skill can download media items from Google Photos through connector file transit. <br>
Mitigation: Treat downloaded media as sensitive user data and verify that the requested item and destination are intended. <br>


## Reference(s): <br>
- [ClawHub Google Photos skill](https://clawhub.ai/oomol/oo-googlephotos) <br>
- [OOMOL publisher profile](https://clawhub.ai/user/oomol) <br>
- [Google Photos homepage](https://www.google.com/photos/about/) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Agent actions call the OOMOL Google Photos connector and may return JSON data with execution metadata.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
