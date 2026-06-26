## Description: <br>
Fetches Terms of Service documents, stores snapshots, and performs semantic diffing to identify meaningful legal changes across Privacy Risks, Financial Changes, and User Rights categories. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liverock](https://clawhub.ai/user/liverock) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, compliance reviewers, and policy monitors use this skill to track public legal documents, capture local snapshots, and surface semantic changes that may affect privacy, financial terms, or user rights. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Fetched webpage text is untrusted input and generated legal-change analysis may be incomplete or misleading. <br>
Mitigation: Use the skill for public legal documents or documents acceptable for local storage, and review generated analyses before relying on them. <br>
Risk: Snapshots are stored locally and the remove command deletes tracked snapshot data. <br>
Mitigation: Set TOS_DATA_DIR to a dedicated folder and back up snapshots that need to be retained before using remove_url. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/liverock/legal-tos-differ) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, files] <br>
**Output Format:** [Markdown status messages and analysis prompts, with local JSON snapshot files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses tracked URLs, optional labels, local snapshot storage, and TOS_DATA_DIR for storage location.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence release and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
