## Description: <br>
iflow-nb helps agents manage iflow knowledge bases, import files or URLs, run web and academic searches, and generate reports, PPTs, podcasts, mind maps, or videos. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[iflow-ai-skill](https://clawhub.ai/user/iflow-ai-skill) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to route notebook, knowledge-base, search, import, sharing, file-management, and content-generation requests through iflow workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persist selected files, URLs, notes, and generated outputs to iflow. <br>
Mitigation: Use it only for content you are comfortable sending to iflow, and review the selected notebook, files, URLs, and notes before upload or import. <br>
Risk: The skill can delete notebooks, delete files, or batch-delete files. <br>
Mitigation: Require explicit confirmation of the exact notebook and file names before destructive operations. <br>
Risk: The skill can share notebook content through iflow share links. <br>
Mitigation: Confirm the target notebook and sharing intent before creating or distributing a share link. <br>
Risk: Setting IFLOW_BASE_URL changes the endpoint that receives credentials and content. <br>
Mitigation: Leave IFLOW_BASE_URL unset unless the endpoint is fully trusted. <br>
Risk: Generation may use all files in a knowledge base when the user does not select specific files. <br>
Mitigation: For large or sensitive notebooks, show the candidate notebook and file scope and wait for user approval before generation. <br>


## Reference(s): <br>
- [iflow API Reference](references/api.md) <br>
- [iflow API Key Management](https://platform.iflow.cn/profile?tab=apiKey) <br>
- [iflow](https://iflow.cn) <br>
- [ClawHub skill page](https://clawhub.ai/iflow-ai-skill/iflow-nb) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON API examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill can submit asynchronous iflow creation tasks and returns task identifiers, status records, search results, share links, or generated-output metadata.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
