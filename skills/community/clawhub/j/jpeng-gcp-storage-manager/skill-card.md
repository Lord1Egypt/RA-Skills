## Description: <br>
Manage Google Cloud Storage for command-line cloud operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jpengcheng523-netizen](https://clawhub.ai/user/jpengcheng523-netizen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and cloud operators use this skill to manage Google Cloud Storage tasks from command-line workflows and automate storage operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can operate on Google Cloud Storage resources using cloud credentials. <br>
Mitigation: Use a least-privilege key limited to the specific project and buckets needed. <br>
Risk: Storage write, overwrite, delete, or public-access changes can affect cloud data and exposure. <br>
Mitigation: Manually confirm any write, overwrite, delete, or public-access changes before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jpengcheng523-netizen/jpeng-gcp-storage-manager) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, JSON] <br>
**Output Format:** [Markdown with bash commands and JSON result examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires STORAGE_API_KEY for authenticated Google Cloud Storage operations.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
