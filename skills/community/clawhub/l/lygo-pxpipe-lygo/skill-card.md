## Description:

Multi-tool vision context compression for LYGO (Anthropic, OpenAI, Grok/xAI, Gemini). Use before stuffing huge prompts or logs into pay-to-go APIs. Requires lygo-protocol-stack; read references/SECURITY.md. Agents run pxpipe_lygo_for_agent.py or local proxy - no auto publish/git push.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deepseekoracle](https://clawhub.ai/user/deepseekoracle)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to reduce large prompt or tool-output context into pxpipe-style vision payloads before using Anthropic, OpenAI, Grok/xAI, or Gemini APIs. It is intended for large non-secret context where lossy compression is acceptable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup can run mutable external code from lygo-protocol-stack with access to local files and environment API keys.

Mitigation: Use a trusted, pinned checkout, review the proxy code before execution, avoid @latest installs where possible, and run in an isolated environment.

Risk: The local proxy can forward upstream API calls using environment API keys when the user starts it.

Mitigation: Start the proxy only when needed, bind it to localhost, and provide API keys only after confirming the local code path.

Risk: Vision PNG compression is lossy and may not preserve exact identifiers, secrets, hashes, or line-precise diffs.

Mitigation: Do not compress secrets or credential files, and keep exact identifiers or hashes as separate verbatim text.

## Reference(s):

- [Security guidance](references/SECURITY.md)
- [lygo-protocol-stack](https://github.com/DeepSeekOracle/lygo-protocol-stack)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides use of local LYGO stack tools that can create PNG context payloads and JSON manifests.]

## Skill Version(s):

1.0.1 (source: release evidence and frontmatter metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
