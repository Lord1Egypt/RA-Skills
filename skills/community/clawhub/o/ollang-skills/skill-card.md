## Description: <br>
Master skill for the Ollang translation platform. Routes to the right Ollang sub-skill based on intent: upload files, create orders, check status, manage revisions, run QC, browse projects and folders. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mazizulak](https://clawhub.ai/user/mazizulak) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to operate Ollang translation, captioning, dubbing, revision, human review, QC, project, and folder workflows from an agent using the Ollang API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can upload user files to Ollang and may expose confidential content to the Ollang service. <br>
Mitigation: Use it only for files intended for Ollang processing, and require the agent to show the exact file, destination, and settings before upload. <br>
Risk: The skill can create, rerun, cancel, or request human review for orders, which may affect billing, credits, or active work. <br>
Mitigation: Require explicit approval after the agent shows the order ID, action, settings, and any billing or credit impact. <br>
Risk: The skill uses an Ollang API key from the environment. <br>
Mitigation: Prefer a revocable or limited API key when available and rotate the key if it may have been exposed. <br>
Risk: Document links, callback URLs, and order details may reveal account or project information. <br>
Mitigation: Review displayed links and callback destinations before sharing them or allowing the agent to submit them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mazizulak/ollang-skills) <br>
- [Publisher profile](https://clawhub.ai/user/mazizulak) <br>
- [Ollang API documentation](https://api-docs.ollang.com) <br>
- [Ollang platform](https://ollang.com) <br>
- [Ollang account and API key portal](https://lab.ollang.com) <br>
- [Ollang API base URL](https://api-integration.ollang.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, API calls] <br>
**Output Format:** [Markdown with inline shell commands and API response summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include order IDs, project IDs, folder IDs, status values, document links, QC scores, and confirmation prompts for account-affecting actions.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
