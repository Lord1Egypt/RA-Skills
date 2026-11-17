## Description:

A Chinese-first prompt engineering workflow that turns natural-language requests into structured prompt templates using depth routing, reusable prompt atoms, DEPTH fingerprints, and validation utilities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kiwifruit13](https://clawhub.ai/user/kiwifruit13)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, prompt engineers, and workflow authors use this skill to generate, refine, depth-grade, and audit structured prompts for varied domains and output formats. It is most suitable when the desired result is a reusable prompt, prompt package, model-adapted prompt, or prompt-quality guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Maintenance scripts can execute code from projects being validated or documented.

Mitigation: Run maintenance scripts only against trusted repositories, or run them in an isolated environment when validating or documenting third-party content.

Risk: The workflow can produce polished prompts for high-stakes domains such as legal, medical, and financial work.

Mitigation: Use the skill's boundary routing and require qualified human review before relying on high-stakes outputs.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/kiwifruit13/skills/prompt-system-dd)
- [Usage Guide](artifact/references/usage-guide.md)
- [Routing Protocol](artifact/references/routing-protocol.md)
- [Composition Manifest](artifact/references/composition-manifest.md)
- [Depth Adaptation Protocol](artifact/references/depth-adaptation.md)
- [Quality Metrics](artifact/references/quality-metrics.md)
- [PromptIR Specification](artifact/references/prompt-ir.md)
- [Prompt Package Protocol](artifact/references/prompt-package.md)
- [Architecture](artifact/references/architecture.md)
- [Changelog](artifact/references/changelog.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown or plain text, often with DEPTH fingerprint headers and optional code or command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May adapt prompt structure for Claude, OpenAI, Gemini, DeepSeek, or Qwen when a supported model suffix is requested.]

## Skill Version(s):

1.0.2 (source: ClawHub release metadata; embedded skill frontmatter: 5.6.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
