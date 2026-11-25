## Description:

Helps developers set up automated Google Play deployment workflows, including Android project analysis, keystore generation, service account configuration, and GitHub Actions workflow generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alinklab](https://clawhub.ai/user/alinklab)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and release engineers use this skill to prepare Android projects for Play Store deployment, generate signing and CI/CD configuration, validate GitHub secrets and Play service account setup, and test deployment workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive Android release-signing data, GitHub tokens, project metadata, and the XBY API key may be sent to a third-party remote service.

Mitigation: Use the skill only when the Xiaobenyang service is trusted for this data; prefer least-privilege tokens and avoid repo-scope PATs or signing passwords where possible.

Risk: The skill persists the XBY API key in a local .env file.

Mitigation: Keep generated .env files out of source control, rotate any exposed secrets, and remove local credentials when they are no longer needed.

Risk: The security evidence reports weak disclosure and confusing unrelated project identity markers.

Mitigation: Review the skill behavior and remote-service trust boundary before installing or using it in a release workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alinklab/skills/hitoshura25-android-playstore-deploy)
- [Xiaobenyang service](https://xiaobenyang.com)
- [Xiaobenyang MCP API endpoint](https://mcp.xiaobenyang.com)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown summaries with generated configuration, workflow, and command snippets; remote API responses are returned as JSON-like data.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an XBY API key and may route Android deployment details to the Xiaobenyang service.]

## Skill Version(s):

1.0.1 (source: server release evidence; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
