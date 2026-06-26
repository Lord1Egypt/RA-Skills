## Description: <br>
Integrates Google NotebookLM workflows through the unofficial notebooklm-py library so agents can manage notebooks, import sources, query content, generate NotebookLM artifacts, and download outputs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oki3505F](https://clawhub.ai/user/oki3505F) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and research teams use this skill to have an agent create and manage NotebookLM notebooks, import sources, ask questions, and generate or download NotebookLM artifacts through notebooklm-py. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide broad Google-account actions, including deletion, sharing, Drive import, export, and permission-changing workflows. <br>
Mitigation: Use a dedicated or low-sensitivity Google account, avoid secrets or regulated documents, and require explicit confirmation before destructive, sharing, Drive, export, or permission-changing actions. <br>
Risk: The skill depends on an unofficial NotebookLM library and undocumented Google APIs that may change or behave unexpectedly. <br>
Mitigation: Review and pin the package before use, retest workflows after NotebookLM or library updates, and keep fallback and retry behavior explicit. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/oki3505F/notebooklm-integration) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, shell commands, configuration] <br>
**Output Format:** [Markdown with Python and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide an agent to create notebooks, import sources, change sharing permissions, export content, and download generated files through Google-account-backed NotebookLM workflows.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
