## Description: <br>
Build a complete, production-ready full-stack web application from PRD documents, prototype images, and resource files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zai-org](https://clawhub.ai/user/zai-org) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to turn PRDs, prototype images, and resource files into a working full-stack web application with backend APIs, frontend UI, seed data, verification steps, and startup documentation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can install tooling and reset local data while building or launching an application. <br>
Mitigation: Use it in disposable development workspaces, keep unrelated private files out of scope, and review generated start.sh before running it. <br>
Risk: Generated applications may touch databases or local services during setup and verification. <br>
Mitigation: Avoid production or shared databases and verify generated configuration before connecting external services. <br>
Risk: Visual verification tooling may install Playwright or Chromium if they are missing. <br>
Mitigation: Preinstall or pin Playwright and browser dependencies when dependency control matters. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zai-org/glmv-prd-to-app) <br>
- [Seed Data Generation Guide](references/seed_data_guide.md) <br>
- [Visual Verification Guide](references/visual_verification_guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, code files, shell commands, configuration files, and generated project documentation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May generate a full application workspace, seed data, API checks, screenshots, and a start.sh script.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
