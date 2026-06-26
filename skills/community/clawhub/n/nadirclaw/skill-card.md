## Description: <br>
Install, configure, and run NadirClaw LLM router to cut AI API costs by 40-70%. Use when the user wants to reduce LLM spending, route prompts to cheaper models, set up cost-saving proxy, or optimize API usage across providers (OpenAI, Anthropic, Google, Ollama). Also use when asked about model routing, LLM cost optimization, or setting up NadirClaw with OpenClaw. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[doramirdor](https://clawhub.ai/user/doramirdor) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to install and configure NadirClaw as a local LLM routing proxy for OpenClaw, Claude Code, or OpenAI-compatible tools. It helps route prompts across cheaper, local, and premium model providers while monitoring savings and routing behavior. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The installer can automatically change OpenClaw routing and leave a background local proxy running. <br>
Mitigation: Review the install behavior before execution, confirm that routing through NadirClaw is intended, and identify how to stop the service and remove the OpenClaw provider change. <br>
Risk: LLM prompts may pass through a local proxy and upstream package behavior is outside the skill card evidence. <br>
Mitigation: Use only when the upstream nadirclaw Python package is trusted, and inspect credential handling, prompt logging, and local log storage before routing sensitive traffic. <br>


## Reference(s): <br>
- [NadirClaw ClawHub release](https://clawhub.ai/doramirdor/nadirclaw) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include local service commands, OpenClaw onboarding steps, routing profile choices, and troubleshooting guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
