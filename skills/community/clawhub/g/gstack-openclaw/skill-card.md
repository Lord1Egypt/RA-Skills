## Description: <br>
Gstack Openclaw is a documentation-only OpenClaw workflow pack that gives agents structured engineering roles for product planning, architecture, design review, testing, security review, deployment guidance, and retrospectives. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leo-jiqimao](https://clawhub.ai/user/leo-jiqimao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to guide software projects through role-specific prompts for planning, architecture, implementation review, QA, release preparation, incident investigation, and retrospectives. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow guidance covers high-impact actions such as PR merging, production deployment, rollback, telemetry review, and code changes. <br>
Mitigation: Require per-action confirmation, least-privilege credentials, and human review of diffs, commands, deployment plans, and rollback decisions before execution. <br>
Risk: The skill mentions external services such as GitHub, CI/CD, cloud platforms, monitoring, notifications, and browser tooling, which could be mistaken for direct authority to call those services. <br>
Mitigation: Use separate authorized tools or skills for service access, require explicit user consent, and review credentials and scopes before any external action. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/leo-jiqimao/gstack-openclaw) <br>
- [README](artifact/README.md) <br>
- [Security Policy](artifact/SECURITY.md) <br>
- [Workflow Guide](artifact/docs/workflow.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with code snippets, command examples, checklists, reports, and configuration guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only prompt outputs; high-impact actions require separate user authorization and appropriate tool access.] <br>

## Skill Version(s): <br>
2.5.10 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
