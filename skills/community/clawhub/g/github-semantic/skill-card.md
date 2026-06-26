## Description: <br>
AI-native GitHub assistant for indexing repositories, searching issues and pull requests semantically, and monitoring repository activity with alerts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ultracold-molecule](https://clawhub.ai/user/ultracold-molecule) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers use this skill to build a local semantic index of GitHub repository issues, pull requests, and metadata, then query it with natural language. It also supports monitoring repositories for issue, pull request, and CI activity that matches configured keywords. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Authenticated GitHub data may be indexed locally. <br>
Mitigation: Use only GitHub accounts and repositories that are appropriate to index on the local machine. <br>
Risk: Subprocess command construction is review-worthy before shared or untrusted use. <br>
Mitigation: Review and harden subprocess calls before using the scripts in shared automation or untrusted workflows. <br>
Risk: The monitor includes a hard-coded Feishu alert recipient. <br>
Mitigation: Replace or remove the recipient before relying on Feishu alerts. <br>
Risk: Index initialization and removal commands can destructively modify the local Qdrant collection. <br>
Mitigation: Treat init and rm operations as destructive local index operations and run them only after confirming the target collection or repository. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ultracold-molecule/github-semantic) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and terminal text output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires authenticated GitHub CLI, local Ollama embeddings, and a local Qdrant service for the scripted workflows.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence and target metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
