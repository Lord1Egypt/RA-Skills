## Description: <br>
Access and manage a self-hosted Open Notebook research system (NotebookLM alternative), including notebook creation, text/URL/file sources, cross-notebook search, and RAG chat with stored research notes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[crabsticksalad](https://clawhub.ai/user/crabsticksalad) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to manage self-hosted research notebooks through a local bridge: creating notebooks, adding sources, searching saved content, and asking cited RAG questions over stored notes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create, retrieve, search, and delete notebook data available to its API key. <br>
Mitigation: Install only with a trusted local bridge setup, restrict allowed_notebooks where possible, and keep backups when delete commands are enabled. <br>
Risk: Notebook content may include sensitive research data and is stored unencrypted at rest in the upstream Open Notebook stack. <br>
Mitigation: Do not store secrets, credentials, or sensitive PII in notebooks. <br>
Risk: Credential exposure could allow unauthorized bridge access. <br>
Mitigation: Keep OPEN_NOTEBOOK_API_KEY and OPEN_NOTEBOOK_PASSWORD private and configure per-agent API keys through the bridge. <br>


## Reference(s): <br>
- [ClawHub Open Notebook skill page](https://clawhub.ai/crabsticksalad/open-notebook) <br>
- [Open Notebook deployment guide](https://github.com/lfnovo/open-notebook) <br>
- [Open Notebook skill homepage](https://github.com/Crabsticksalad/open-notebook-skill) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [JSON command responses and Markdown guidance with shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a running local bridge, OPEN_NOTEBOOK_API_KEY, and OPEN_NOTEBOOK_BRIDGE_URL; commands may create, retrieve, search, or delete notebook data available to the API key.] <br>

## Skill Version(s): <br>
1.3.2 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
