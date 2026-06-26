## Description: <br>
Use for JumpServer V4 preflight, `.env.local` initialization, org selection, and read-only asset, permission, audit, and access queries through the bundled `jms_*.py` CLIs; not for business mutations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liqiang-fit2cloud](https://clawhub.ai/user/liqiang-fit2cloud) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operations engineers, and security reviewers use this skill to initialize JumpServer V4 access, select organization context, and run read-only asset, permission, audit, and access-analysis queries for troubleshooting, permission review, and audit investigation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles JumpServer infrastructure credentials through `.env.local` and process environment variables. <br>
Mitigation: Install only in a trusted local environment, protect `.env.local` as a secret file, avoid shared workspaces, and rerun the full preflight flow after changing targets, accounts, organizations, or local configuration. <br>
Risk: The runtime constructs the JumpServer client with TLS certificate verification disabled and suppresses HTTPS certificate warnings. <br>
Mitigation: Prefer network paths where certificate verification can be restored or independently controlled before using the skill against sensitive infrastructure. <br>
Risk: Custom SDK module and client factory settings or dependency bootstrap behavior can change code loaded by the skill. <br>
Mitigation: Review `JMS_SDK_MODULE`, `JMS_SDK_GET_CLIENT`, and any `--confirm-install` use before allowing an agent to run the skill. <br>


## Reference(s): <br>
- [README.en.md](README.en.md) <br>
- [Runtime](references/runtime-behavior.md) <br>
- [Safety Rules](references/query-boundaries.md) <br>
- [Diagnose](references/preflight-and-diagnostics.md) <br>
- [Assets](references/object-queries.md) <br>
- [Permissions](references/permission-queries.md) <br>
- [Audit](references/audit-queries.md) <br>
- [Object Map](references/object-mapping.md) <br>
- [Troubleshooting](references/troubleshooting-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON CLI output summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide confirmed local `.env.local` and `JMS_ORG_ID` writes during initialization; business object, permission, and audit operations remain query-only.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
