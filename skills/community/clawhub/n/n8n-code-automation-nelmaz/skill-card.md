## Description: <br>
Integrates n8n workflow automation into coding tasks for building, executing, modifying, and managing automation workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nelmaz](https://clawhub.ai/user/nelmaz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to integrate n8n workflow operations into coding tasks, including inspecting, executing, cloning, updating, and documenting workflows for development pipelines, data processing, and API integrations. Mutating and execution actions should be reviewed against the connected n8n instance before use. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide agents to execute, modify, clone, or delete workflows on a remote n8n instance when an API key is available. <br>
Mitigation: Use a dedicated least-privilege API key, start in read-only mode where possible, and require manual review before workflow execution, update, clone, webhook trigger, or deletion. <br>
Risk: The artifact contains conflicting old and new instructions, including older examples that reference a fixed n8n host and configuration-file credentials. <br>
Mitigation: Verify which SKILL.md is active, keep credentials out of shared config files, use environment variables or a secrets manager, and require HTTPS for the target n8n URL. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nelmaz/n8n-code-automation-nelmaz) <br>
- [n8n Documentation](https://docs.n8n.io) <br>
- [n8n API Reference](https://docs.n8n.io/api/) <br>
- [n8n Webhooks](https://docs.n8n.io/workflows/webhooks/) <br>
- [n8n Node Reference](https://docs.n8n.io/nodes/) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code, Configuration] <br>
**Output Format:** [Markdown with inline shell, JSON, YAML, and JavaScript examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include n8n API calls and workflow examples that require user-supplied n8n URLs, workflow IDs, and API keys.] <br>

## Skill Version(s): <br>
1.1.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
