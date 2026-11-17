## Description:

Delegates to the Qwen CLI (Alibaba)

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers can route batch processing, summarization, or multi-file analysis to Qwen when delegation-core selects it, including tasks suited to Qwen’s large context window.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: File analysis can send selected local files to an external Qwen service.

Mitigation: Review and limit the files included, and avoid sending sensitive or proprietary content unless you have authorization.

Risk: The available security evidence does not cover several unresolved referenced paths.

Mitigation: Resolve and review those referenced paths before relying on the scan's coverage.

## Reference(s):

- [Conjure project homepage](https://github.com/athola/claude-night-market/tree/master/plugins/conjure)
- [Qwen model configuration resolver](https://github.com/QwenLM/qwen-code/blob/main/packages/core/src/models/modelConfigResolver.ts)
- [Alibaba Model Studio pricing](https://www.alibabacloud.com/help/en/model-studio/model-pricing)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance]

**Output Format:** [Markdown guidance with shell command examples and delegated text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Delegated task output can be saved as a timestamped Markdown file.]

## Skill Version(s):

1.10.3 (source: frontmatter, release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
