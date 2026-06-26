## Description: <br>
Safely configure Google Vertex AI for a fresh OpenClaw setup using a Google Cloud project, service-account JSON auth, minimal-cost verification, and explicit billing checks to avoid accidental Gemini API or extra spend. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[guoma970](https://clawhub.ai/user/guoma970) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to set up OpenClaw with Google Vertex AI on a fresh or mostly fresh machine while limiting billing mistakes. It guides project, service-account JSON, model-route, minimal-test, and billing-verification steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Service-account JSON credentials can expose Google Cloud access if stored or shared carelessly. <br>
Mitigation: Use a dedicated least-privilege Google service account, keep the service-account JSON private, and review OpenClaw config paths before use. <br>
Risk: Wrong provider routing or project selection can create unexpected Google Cloud charges. <br>
Mitigation: Keep models on google-vertex routes, run one tiny verification request, then manually confirm the charged project and Vertex AI billing line. <br>


## Reference(s): <br>
- [Vertex First-Setup Checklist](references/vertex-first-setup-checklist.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown report with shell commands and configuration steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes current-state audit, target project, auth method, JSON path, configured google-vertex models, minimal test result, and billing checks.] <br>

## Skill Version(s): <br>
1.0.3 (source: ClawHub release metadata; artifact frontmatter lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
