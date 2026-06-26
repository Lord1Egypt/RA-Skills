## Description: <br>
Provides a standard workflow for uploading Markdown reports and other documents to IMA knowledge bases through note import or media upload paths. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[meta-evo-creator](https://clawhub.ai/user/meta-evo-creator) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators who maintain IMA knowledge bases use this skill to prepare Markdown or document uploads, choose the correct upload path, and avoid common mistakes such as mismatched titles, failed COS uploads, or wrong KB IDs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires sensitive IMA and COS credentials for upload workflows. <br>
Mitigation: Use least-privilege credentials, avoid exposing secrets in shell history or shared logs, and review the separate ima-skill helper before use. <br>
Risk: Documents could be uploaded to the wrong knowledge base if the KB_ID is incorrect. <br>
Mitigation: Verify the file contents and target knowledge_base_id before running add_knowledge. <br>
Risk: Continuing after a COS upload failure could create incomplete or misleading knowledge-base entries. <br>
Mitigation: Stop the workflow immediately when COS upload fails and only call add_knowledge after a verified upload. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/meta-evo-creator/ima-knowledge-upload) <br>
- [Publisher profile](https://clawhub.ai/user/meta-evo-creator) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with JavaScript and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires IMA API credentials and correct knowledge_base_id selection.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
