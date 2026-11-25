## Description:

Delegates to the Qwen CLI (Alibaba).

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill when the shared delegation workflow selects Qwen, including for batch processing, summarization, and multi-file analysis through the Qwen CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected local files may be sent to an external AI provider, and automatic provider selection may not match the Qwen-specific purpose.

Mitigation: Confirm which provider will receive the request and review the selected files; exclude confidential or sensitive material unless you have authorization to send it.

Risk: The security scan was partial because the delegation executor and other local paths were unavailable for inspection.

Mitigation: Review those paths before relying on the skill's behavior.

## Reference(s):

- [Night Market Conjure plugin](https://github.com/athola/claude-night-market/tree/master/plugins/conjure)
- [Qwen model configuration resolver](https://github.com/QwenLM/qwen-code/blob/main/packages/core/src/models/modelConfigResolver.ts)
- [Alibaba Cloud Model Studio pricing](https://www.alibabacloud.com/help/en/model-studio/model-pricing)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON]

**Output Format:** [Text or Markdown; JSON when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Delegated results can be saved to timestamped Markdown files.]

## Skill Version(s):

1.10.4 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
