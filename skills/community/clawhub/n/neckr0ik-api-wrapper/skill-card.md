## Description: <br>
Convert any REST API into an OpenClaw skill automatically. Generates SKILL.md, scripts, and claw.json from OpenAPI spec or URL. Use when you want to quickly create a skill for any API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Neckr0ik](https://clawhub.ai/user/Neckr0ik) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers use this skill to generate OpenClaw skill packages from OpenAPI specifications or discoverable REST API URLs. It helps create initial SKILL.md documentation, package metadata, API client code, and endpoint references for review and integration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Review before execution as proposals could introduce incorrect or misleading guidance into skills. <br>
Mitigation: Review and scan skill before deployment. <br>

## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Neckr0ik/neckr0ik-api-wrapper) <br>
- [Skill definition](artifact/SKILL.md) <br>
- [Generator script](artifact/scripts/generator.py) <br>
- [Package metadata](artifact/claw.json) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Files] <br>
**Output Format:** [Generated skill directory with Markdown documentation, JSON configuration, and Python code; CLI output is plain text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated code, target base URLs, and credentials should be reviewed before running; use trusted OpenAPI specifications, scoped credentials, and a dedicated output directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, claw.json, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
