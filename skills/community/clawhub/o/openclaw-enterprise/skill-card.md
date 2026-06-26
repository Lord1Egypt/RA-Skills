## Description: <br>
OpenClaw Enterprise orchestrates a chief-of-staff agent and specialized business agents to help teams plan procurement, production, sales, finance, compliance, reporting, and operational workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangm-a3](https://clawhub.ai/user/wangm-a3) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and operations teams use this skill to route natural-language business requests to specialized agents and generate planning guidance, workflow recommendations, reports, and risk assessments for enterprise operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad triggers and routing may send sensitive business context into an external multi-agent workflow. <br>
Mitigation: Use explicit invocation or confirmation before routing tasks, and avoid sharing confidential data unless organizational policy permits processing by configured OpenAI or Anthropic services. <br>
Risk: The skill requires API credentials for external model providers. <br>
Mitigation: Provide credentials through environment variables, scope them to approved use, and rotate them according to organizational credential policy. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/wangm-a3/openclaw-enterprise) <br>
- [Publisher Profile](https://clawhub.ai/user/wangm-a3) <br>
- [OpenClaw Homepage](https://openclaw.ai) <br>
- [GitHub Link From Metadata](https://github.com/openclaw) <br>
- [Keyword Routing Reference](references/routing_tables/keyword_routing.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Natural-language guidance, Markdown reports, JSON-like agent results, setup commands, and configuration instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include routed agent recommendations, planning summaries, risk assessments, reports, and workflow steps based on user-provided business context.] <br>

## Skill Version(s): <br>
2.0.3 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
