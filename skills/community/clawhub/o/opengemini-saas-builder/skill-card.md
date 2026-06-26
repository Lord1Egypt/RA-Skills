## Description: <br>
Build SaaS projects end-to-end with OpenClaw as orchestrator and Gemini CLI as a local planning and generation copilot. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hiromps](https://clawhub.ai/user/hiromps) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to plan, scaffold, implement, document, publish, and optionally deploy SaaS products, MVPs, dashboards, internal tools, and web applications. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts sent to Gemini helpers could expose secrets or confidential customer or business data. <br>
Mitigation: Remove secrets and confidential information from prompts before using Gemini-assisted planning, generation, or review. <br>
Risk: GitHub or Vercel steps can publish code, configuration, or unfinished files outside the local workspace. <br>
Mitigation: Confirm the current directory, account, repository name, visibility, environment variables, and deployment intent before creating repositories, pushing code, or deploying. <br>


## Reference(s): <br>
- [SaaS Build Modes](references/saas-build-modes.md) <br>
- [SaaS Doc Templates](references/saas-doc-templates.md) <br>
- [Repo and Deploy Checklist](references/repo-and-deploy-checklist.md) <br>
- [OpenGemini SaaS Builder on ClawHub](https://clawhub.ai/hiromps/opengemini-saas-builder) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, code snippets, shell commands, configuration notes, and generated project files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce local project documentation, scaffolds, repository setup commands, and deployment notes depending on user intent and available CLI authentication.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
