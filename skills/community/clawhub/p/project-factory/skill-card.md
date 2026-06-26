## Description: <br>
Bootstraps new OpenClaw automation projects from a plain-language description through flow design, node configuration, and scaffold generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lcking](https://clawhub.ai/user/lcking) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation operators use this skill to turn a proposed workflow into an OpenClaw project scaffold with a confirmed flowchart, node configuration, routing, cron setup, and starter scripts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can modify global OpenClaw configuration, shared Telegram routing, assistant registry entries, and cron jobs. <br>
Mitigation: Run the scaffold with --plan or --dry-run first, then review planned changes before allowing writes. <br>
Risk: Generated project files can store Telegram bot credentials and may inherit main-agent authorization profiles. <br>
Mitigation: Use project-specific bot credentials that can be rotated, and avoid inheriting main-agent auth profiles unless that access is intentional. <br>
Risk: Generated bot logic is a stub placeholder and requires manual implementation before production use. <br>
Mitigation: Review and implement each generated node handler, then run the skill's validation and self-check scripts before enabling cron. <br>


## Reference(s): <br>
- [ClawHub project-factory release page](https://clawhub.ai/lcking/project-factory) <br>
- [README](README.md) <br>
- [Flow Design Language](references/flow_design_language.md) <br>
- [Architecture](references/architecture.md) <br>
- [Onboarding Checklist](references/onboarding_checklist.md) <br>
- [Shared Routing Group Schema](references/shared_routing_group_schema.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON snippets, Mermaid flowcharts, shell commands, and generated project files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces project scaffolds that may include workflow documentation, scripts, routing configuration, cron registration, and token-bearing runtime configuration.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
