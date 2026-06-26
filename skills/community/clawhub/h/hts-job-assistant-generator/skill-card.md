## Description: <br>
Generates OpenClaw-ready AI assistant profiles, behavior guidelines, and configuration files from enterprise job descriptions for management, technical, business, and functional roles. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiangdong-3](https://clawhub.ai/user/jiangdong-3) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Enterprise employees and managers use this skill to turn role descriptions into tailored AI assistant profiles, operating boundaries, communication norms, and reusable OpenClaw configuration files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Job descriptions can contain names, contact details, compensation, staffing plans, reporting lines, proprietary project details, or regulated HR information. <br>
Mitigation: Review and redact job descriptions before use, keeping only details needed to draft the assistant profile and configuration. <br>
Risk: Generated assistant files may not fully match internal policy or the intended operating boundaries for a role. <br>
Mitigation: Treat generated files as drafts and review the assistant identity, behavior boundaries, and reuse constraints before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jiangdong-3/hts-job-assistant-generator) <br>
- [README.md](README.md) <br>
- [IDENTITY.md](references/IDENTITY.md) <br>
- [SOUL.md](references/SOUL.md) <br>
- [AGENTS.md](references/AGENTS.md) <br>
- [USER.md](references/USER.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Configuration, Guidance] <br>
**Output Format:** [Markdown documents and OpenClaw configuration files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a role owner profile, assistant job description, behavior specification, and IDENTITY.md, SOUL.md, AGENTS.md, and USER.md drafts.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
