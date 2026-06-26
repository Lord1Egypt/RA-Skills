## Description: <br>
NotebookLM Skill lets agents query and manage Google NotebookLM notebooks for source-grounded answers, source uploads, notebook management, and generated media artifacts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[magicseek](https://clawhub.ai/user/magicseek) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill to authenticate with Google NotebookLM, query notebooks for cited answers, upload or sync sources, manage notebooks, and generate downloadable media from notebook content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires access to authenticated Google NotebookLM sessions and local documents. <br>
Mitigation: Use a dedicated Google account, review stored auth files under data/auth, and install only when this access is acceptable. <br>
Risk: Z-Library workflows may involve material the user is not authorized to download or upload. <br>
Mitigation: Avoid Z-Library commands unless you have rights to the material being used. <br>
Risk: Notebook and folder synchronization commands can change local files and NotebookLM data. <br>
Mitigation: Use dry-run or review prompts before sync, delete, download, or media-management commands. <br>
Risk: Account rotation and rate-limit workarounds can violate service expectations. <br>
Mitigation: Do not use account rotation to bypass limits; pause or reduce activity when rate limits are encountered. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/magicseek/nblm) <br>
- [nblm API Reference](references/api_reference.md) <br>
- [nblm Usage Patterns](references/usage_patterns.md) <br>
- [nblm Troubleshooting Guide](references/troubleshooting.md) <br>
- [Authentication Notes](AUTHENTICATION.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown and terminal output, with optional downloaded media files such as MP3, PDF, and PNG.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs depend on the selected NotebookLM command and authenticated account state.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
