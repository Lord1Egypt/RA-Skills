## Description:

Safely configure Google Vertex AI for a fresh OpenClaw setup using a Google Cloud project, service-account JSON auth, minimal-cost verification, and explicit billing checks to avoid accidental Gemini API or extra spend.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guoma970](https://clawhub.ai/user/guoma970)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to configure Google Vertex AI for OpenClaw from a fresh or mostly fresh setup while reducing billing, credential, and provider-routing mistakes. It guides a minimal first verification request before broader rollout.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow involves Google Cloud billing configuration and could lead to unexpected spend if the wrong project, provider path, or billing account is used.

Mitigation: Confirm the target project and billing credits in Google Cloud, keep model routing on google-vertex paths, run one minimal verification request, and check billing before broader rollout.

Risk: The workflow uses a service-account JSON credential that could expose cloud access if stored or reused carelessly.

Mitigation: Use a dedicated low-privilege service account and store the JSON credential carefully at an explicit local path.

## Reference(s):

- [Vertex First-Setup Checklist](references/vertex-first-setup-checklist.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with setup checks, command suggestions, configuration guidance, and billing verification steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes a required report covering machine state, Google provider path, target project, auth method, JSON path, configured google-vertex models, minimal test result, and billing checks.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
