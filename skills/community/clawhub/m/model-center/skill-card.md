## Description: <br>
Unified interface to 42+ NVIDIA NIM API models - LLM chat, vision, embeddings, image generation, with price comparison and model recommendation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[534422530](https://clawhub.ai/user/534422530) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to inspect NVIDIA NIM model options, compare costs, request model recommendations, and call chat, embedding, and image-generation APIs from Python. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The documentation contains unrelated merged learning-history records with user-like identifiers. <br>
Mitigation: Review and remove unrelated records before reuse or redistribution. <br>
Risk: Prompts and inputs sent through the skill are transmitted to NVIDIA API endpoints. <br>
Mitigation: Avoid sending secrets, proprietary text, personal data, or regulated content unless the user has approved that disclosure. <br>
Risk: Live API calls require a sensitive NVIDIA_API_KEY credential. <br>
Mitigation: Store the key in the environment, avoid committing it to files, and rotate it if exposure is suspected. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/534422530/model-center) <br>
- [NVIDIA API catalog](https://build.nvidia.com) <br>
- [NVIDIA API base endpoint](https://integrate.api.nvidia.com/v1) <br>
- [NVIDIA model listing endpoint](https://integrate.api.nvidia.com/v1/models) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Python return values and Markdown usage guidance, including JSON-like API responses and setup commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python, the requests package, and an NVIDIA_API_KEY for live NVIDIA API calls.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
