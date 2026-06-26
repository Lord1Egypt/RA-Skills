## Description: <br>
Multi-agent workflow examples to work together on the OpenServ Platform. Covers agent discovery, multi-agent workspaces, task dependencies, and workflow orchestration using the Platform Client. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[issa-me-sush](https://clawhub.ai/user/issa-me-sush) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and external builders use this skill to design OpenServ multi-agent workflows with marketplace agent discovery, task dependencies, triggers, and explicit workflow graph edges. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Examples use wallet private keys and paid workflow triggers, which can expose funds if copied into an unsafe environment. <br>
Mitigation: Use a dedicated low-balance development wallet, keep private keys in local environment files, and keep those files out of version control. <br>
Risk: Webhook trigger URLs and tokens can start persistent workflows if shared through logs, screenshots, or public repositories. <br>
Mitigation: Avoid sharing webhook URLs, disable unused workflows and triggers, and rotate exposed trigger tokens. <br>
Risk: Marketplace agents and dependency packages can change behavior or introduce unwanted data handling. <br>
Mitigation: Vet marketplace agents before use, pin and review dependencies, and test workflows with non-sensitive sample inputs first. <br>
Risk: Some examples involve personal, client, financial, or coaching data that may require consent and controls. <br>
Mitigation: Do not submit real client or sensitive personal data without consent, minimization, and appropriate data-handling controls. <br>


## Reference(s): <br>
- [OpenServ Multi Agent Workflows on ClawHub](https://clawhub.ai/issa-me-sush/openserv-multi-agent-workflows) <br>
- [Multi-Agent Workflows Reference](reference.md) <br>
- [Multi-Agent Workflows Troubleshooting](troubleshooting.md) <br>
- [Blog Pipeline Example](examples/blog-pipeline.md) <br>
- [Content Creation Pipeline Example](examples/content-creation-pipeline.md) <br>
- [Life Coaching Pipeline Example](examples/life-coaching-pipeline.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown documentation with TypeScript examples, shell commands, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Examples may reference wallet private keys, webhook URLs, OpenServ marketplace agents, and persistent workflow triggers.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
