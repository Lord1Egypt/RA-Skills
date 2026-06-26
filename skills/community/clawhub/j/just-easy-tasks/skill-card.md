## Description: <br>
Use when an agent needs to work with Just Easy Tasks (JET) via the jet CLI or API: configure API key/context, find, create, update, complete, comment on, link, reference, or inspect tasks and project metadata. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ryan-w-s](https://clawhub.ai/user/ryan-w-s) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to manage Just Easy Tasks work items through the JET CLI or API, including task discovery, creation, updates, completion, comments, links, references, and project metadata inspection. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires sensitive JET credentials and workspace/project context. <br>
Mitigation: Use a limited API key when available, keep credentials out of source control, and verify the selected workspace and project before making changes. <br>
Risk: Destructive or admin-level JET commands can change or remove shared task-management data. <br>
Mitigation: Use --force or --dangerously-enable-admin-commands only when the user explicitly requests the intended destructive or administrative change. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ryan-w-s/just-easy-tasks) <br>
- [Just Easy Tasks service](https://justeasytasks.com) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, API calls, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use JSON CLI output for non-interactive agent workflows.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
