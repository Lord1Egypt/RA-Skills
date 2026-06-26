## Description: <br>
Universal LLM gateway with intelligent routing, Graphify code intelligence, Distill compression, routing telemetry, Code Mode, and 12+ provider support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vishalveerareddy123](https://clawhub.ai/user/vishalveerareddy123) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to configure Lynkr as an OpenAI-compatible routing proxy for AI coding tools, with tiered model routing, provider failover, token optimization, and routing telemetry. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Coding prompts, tool outputs, and source snippets may be routed to configured cloud providers. <br>
Mitigation: Use local-only providers for sensitive work and review provider routing settings before connecting private repositories. <br>
Risk: The proxy may log routing telemetry or maintain memory related to coding requests. <br>
Mitigation: Review runtime settings for telemetry and memory, and disable or limit them where confidentiality requirements apply. <br>
Risk: The skill can require sensitive provider credentials for cloud model access. <br>
Mitigation: Use scoped provider credentials, store them outside source control, and rotate them if exposed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/vishalveerareddy123/lynkr) <br>
- [Publisher profile](https://clawhub.ai/user/vishalveerareddy123) <br>
- [Project homepage](https://github.com/Fast-Editor/Lynkr) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with bash, environment, and JSON code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance targets Node.js 20 or newer and OpenAI-compatible provider configuration.] <br>

## Skill Version(s): <br>
8.0.1 (source: release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
