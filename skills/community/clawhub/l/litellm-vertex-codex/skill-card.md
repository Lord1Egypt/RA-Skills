## Description: <br>
Configure OpenAI Codex CLI to use Vertex AI Gemini models via LiteLLM. A guide for translating strict Codex requests for Gemini compatibility. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bhrum](https://clawhub.ai/user/bhrum) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to configure Codex CLI to route requests through a local LiteLLM proxy to Vertex AI Gemini models and verify the setup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup routes Codex through LiteLLM to Vertex AI and requires Google Cloud credentials. <br>
Mitigation: Use least-privileged Google Cloud credentials and enable only the Vertex AI access needed for this workflow. <br>
Risk: Persistent Codex trust settings or shell profile changes can affect future agent sessions beyond the intended workspace. <br>
Mitigation: Apply trusted-workspace settings only to repositories you intend to trust and set the dummy OPENAI_API_KEY only for this workflow when possible. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/bhrum/litellm-vertex-codex) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with YAML, TOML, and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Provides setup, verification, and troubleshooting guidance for a local LiteLLM-to-Vertex AI Codex workflow.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, package.json, release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
