## Description: <br>
Meta Debugger helps agents identify runtime errors, analyze root causes, learn from error patterns, and propose or optionally apply fixes for Python workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jason-aka-chen](https://clawhub.ai/user/jason-aka-chen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to add runtime error handling, root-cause analysis, fix suggestions, prevention checks, and metrics to Python-based agent workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill advertises autonomous code and configuration fixes that could change system behavior without enough approval controls. <br>
Mitigation: Keep safe_mode enabled and auto_fix disabled unless each proposed change is shown for human approval with target paths, diffs, tests, and rollback. <br>
Risk: The documented installation command includes standard-library modules as pip packages. <br>
Mitigation: Do not run the documented pip install command as written; review dependencies and install only required third-party packages. <br>
Risk: Error context and logs may include secrets, personal data, or other sensitive information. <br>
Mitigation: Redact secrets and personal data before recording errors, logging context, or passing context to custom handlers. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/jason-aka-chen/meta-debugger) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Guidance, Code, Configuration] <br>
**Output Format:** [Python dictionaries with analysis, suggested fixes, metrics, and optional code or configuration change proposals] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Safe mode returns proposed fixes for review before application.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
