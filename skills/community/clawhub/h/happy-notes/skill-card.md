## Description: <br>
happy-notes helps agents manage iflow knowledge bases, import files and URLs, search stored or web content, generate reports and media, track generation status, and share notebooks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[iflow-ai-skill](https://clawhub.ai/user/iflow-ai-skill) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill with AI agents to organize notes and research in iflow, add local or web sources to notebooks, generate reports, presentations, podcasts, mind maps, or videos, and share read-only notebook links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can store, share, generate from, and delete knowledge-base content using the user's iflow API key. <br>
Mitigation: Install only from a trusted publisher, prefer an environment variable for the API key, and require explicit confirmation before share-link creation, delete actions, bulk imports, or broad generation requests. <br>
Risk: Broad triggers and automated workflows may act on more notebook content than the user intended. <br>
Mitigation: Have the agent confirm the target notebook, source files or URLs, and output type before running bulk imports, use-all-files generation, or destructive file-management actions. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/iflow-ai-skill/happy-notes) <br>
- [iflow API key management](https://iflow.cn/?open=api-key) <br>
- [API reference](references/api.md) <br>
- [Pipeline reference](references/pipelines.md) <br>
- [Knowledge base matching reference](references/kb-matching.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Markdown, Files] <br>
**Output Format:** [Markdown guidance with shell commands and JSON pipeline outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a user-provided IFLOW_API_KEY. Pipeline actions may create, import into, generate from, share, rename, or delete notebook content, and some generation tasks complete asynchronously.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
