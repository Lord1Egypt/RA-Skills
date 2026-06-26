## Description: <br>
Manage Google NotebookLM notebooks, sources, chats, artifacts, and exports through the notebooklm-py CLI with safe workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[suidge](https://clawhub.ai/user/suidge) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to operate Google NotebookLM through the local notebooklm-py CLI, including authentication checks, notebook and source management, source-grounded questions, artifact generation, downloads, and exports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can operate a user's NotebookLM account, including private document uploads, downloads, deletes, sharing changes, language changes, login changes, and generation jobs. <br>
Mitigation: Confirm account-visible, destructive, long-running, file-writing, sharing, login, generation, wait, and doctor --fix actions before execution. <br>
Risk: Shared CLI notebook context can cause actions to target the wrong notebook or profile during automation. <br>
Mitigation: Use explicit notebook IDs for workflows and isolate account state with NOTEBOOKLM_PROFILE or NOTEBOOKLM_HOME when needed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/suidge/notebooklm-py-skill) <br>
- [notebooklm-py CLI Reference](references/notebooklm-py-cli.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and JSON-oriented command output guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Prefers explicit notebook IDs and --json output; requires confirmation before destructive, long-running, file-writing, sharing, login, or doctor --fix actions.] <br>

## Skill Version(s): <br>
1.0.1 (source: evidence release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
