## Description: <br>
GitHub Action for automated security scanning of agent workspaces. Detects exposed secrets, prompt/shell injection, and data exfiltration patterns in PRs and commits. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AtlasPA](https://clawhub.ai/user/AtlasPA) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and security engineers use this GitHub Action in CI to scan agent workspaces for exposed secrets, prompt or shell injection patterns, and potential data exfiltration before changes land. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release downloads and runs mutable external Python scanner code in CI. <br>
Mitigation: Prefer a version that vendors the scanners or pins immutable commits with checksum verification before running it in production CI. <br>
Risk: The security review notes misleading local/no-network assurances compared with the action's runtime scanner downloads. <br>
Mitigation: Review the action workflow and scanner repositories as executable CI dependencies, and only use it when those repositories are trusted. <br>
Risk: Running scanner code in CI can expose repository contents, tokens, or secrets available to the workflow. <br>
Mitigation: Run with least-privilege GitHub token permissions, limited secrets exposure, and narrow workflow triggers. <br>


## Reference(s): <br>
- [OpenClaw Action on ClawHub](https://clawhub.ai/AtlasPA/openclaw-action) <br>
- [OpenClaw Security Suite](https://github.com/AtlasPA/openclaw-security) <br>
- [openclaw-sentry](https://github.com/AtlasPA/openclaw-sentry) <br>
- [openclaw-bastion](https://github.com/AtlasPA/openclaw-bastion) <br>
- [openclaw-egress](https://github.com/AtlasPA/openclaw-egress) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Configuration] <br>
**Output Format:** [GitHub Actions annotations, job summary Markdown, and CI output variables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs finding counts and critical finding status; can fail CI when configured.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
