## Description: <br>
Manage Kibana Saved Objects, including dashboards, Lens visualizations, imports, exports, references, and related troubleshooting via the Kibana Saved Objects REST API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chunkin616-hue](https://clawhub.ai/user/chunkin616-hue) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to list, create, update, export, import, and troubleshoot Kibana dashboards, Lens visualizations, and other saved objects through REST API calls and helper scripts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can change, overwrite, or delete Kibana dashboards and saved objects. <br>
Mitigation: Require explicit human approval for delete, overwrite, and bulk operations, and export backups before imports or destructive changes. <br>
Risk: Running against the wrong Kibana host can alter the wrong environment. <br>
Mitigation: Verify the target Kibana host before execution and prefer HTTPS or a trusted internal network. <br>
Risk: Broad credentials can expand the impact of an accidental or incorrect saved-object operation. <br>
Mitigation: Use least-privilege Kibana access scoped to the saved-object operations the agent is expected to perform. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chunkin616-hue/kibana-saved-objects) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, code, configuration, text] <br>
**Output Format:** [Markdown with REST endpoint examples, JSON snippets, Python script usage, and operational guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce or consume Kibana saved object NDJSON exports and JSON API payloads.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
