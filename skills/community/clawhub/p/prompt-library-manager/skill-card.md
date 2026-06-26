## Description: <br>
Curated prompt template library for OpenClaw agents that stores, searches, versions, tags, and reuses prompt templates across sessions and agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[stevojarvisai-star](https://clawhub.ai/user/stevojarvisai-star) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to create, find, fill, update, import, and export reusable prompt templates. Teams can use it to standardize common prompt workflows across OpenClaw sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompt templates are stored locally and may contain sensitive content if users save secrets, regulated data, or confidential customer information. <br>
Mitigation: Do not store passwords, API keys, regulated data, or confidential customer content in prompt templates. <br>
Risk: Deletes and overwrites are immediate, which can remove important prompt templates. <br>
Mitigation: Keep backups of important prompt libraries and review destructive operations before confirming them. <br>
Risk: Imported or reused prompt templates can introduce misleading or inappropriate guidance into agent workflows. <br>
Mitigation: Review templates before reuse and scan shared libraries before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/stevojarvisai-star/prompt-library-manager) <br>
- [Publisher profile](https://clawhub.ai/user/stevojarvisai-star) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, guidance] <br>
**Output Format:** [CLI text output, filled prompt text, JSON exports, and Markdown exports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores prompt library data locally and can read, write, import, export, update, and delete user-selected prompt library files.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
