## Description:

Unified interface to 42+ NVIDIA NIM API models for LLM chat, vision, embeddings, image generation, price comparison, and model recommendation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[534422530](https://clawhub.ai/user/534422530)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to discover NVIDIA NIM models, compare model pricing, estimate costs, and call chat, embedding, and image generation APIs through a Python interface.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, chat messages, and embedding text are sent to NVIDIA API endpoints and may contain sensitive data.

Mitigation: Avoid sending confidential or regulated data unless the deployment has approved data handling controls for the NVIDIA API use case.

Risk: The skill requires an NVIDIA API key and includes an interactive CLI path that can prompt for a key.

Mitigation: Use a limited-scope API key and provide it through a protected NVIDIA_API_KEY environment variable instead of typing it into the CLI.

Risk: The artifact contains unrelated appended learning/log content, and server-resolved provenance is unavailable.

Mitigation: Review the package contents and publisher source before installation, and do not infer GitHub provenance from the artifact text.

## Reference(s):

- [NVIDIA API Catalog](https://build.nvidia.com)
- [NVIDIA NIM API Base](https://integrate.api.nvidia.com/v1)
- [NVIDIA NIM Models Endpoint](https://integrate.api.nvidia.com/v1/models)

## Skill Output:

**Output Type(s):** [Text, Code, API Calls, Configuration]

**Output Format:** [Python objects, JSON-like API responses, and text guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an NVIDIA_API_KEY environment variable for live API calls.]

## Skill Version(s):

1.0.2 (source: server release metadata; artifact frontmatter declares 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
