## Description: <br>
NVIDIA free API integration for OpenAI-compatible access to 133+ mainstream models. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[clementgu](https://clawhub.ai/user/clementgu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to configure NVIDIA's OpenAI-compatible API endpoint, choose models, and call chat, streaming, and embedding workflows with their own NVIDIA API key. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a personal NVIDIA API key and may send prompts to NVIDIA's API endpoint. <br>
Mitigation: Store the key privately, use environment variables or local-only configuration, and avoid committing real credentials. <br>
Risk: The security summary notes confusing API-key wording and the guidance says to verify the advertised CLI exists. <br>
Mitigation: Confirm the intended setup path and available nvidia-api commands before relying on the CLI examples. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/clementgu/nvidia-free-api) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/clementgu) <br>
- [NVIDIA API catalog](https://build.nvidia.com/) <br>
- [NVIDIA OpenAI-compatible API endpoint](https://integrate.api.nvidia.com/v1) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, code] <br>
**Output Format:** [Markdown with inline bash, Python, and YAML examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a user-managed NVIDIA_API_KEY credential.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence; artifact frontmatter reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
