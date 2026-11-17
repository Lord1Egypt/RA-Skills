## Description:

Transform vague user requests into precise, high-quality prompts. Two engines: template matching (3300+ library) + LLM meta-prompting (host AI as optimizer). Only activates when the user explicitly turns it on.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thomaszhou22](https://clawhub.ai/user/thomaszhou22)

### License/Terms of Use:

MIT

## Use Case:

Developers and other AI assistant users use Prompt Optimizer to turn rough requests into clearer, structured prompts, choose template-based or direct LLM rewriting, and optionally assess prompt quality. It activates only after the user explicitly enables it.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Activation intent can be ambiguous.

Mitigation: Enable optimization only in response to an explicit prompt-optimization command.

Risk: Rewritten prompts may contain incorrect or misleading guidance.

Mitigation: Review each rewrite before accepting or using it.

Risk: Optional template libraries were not assessed in the release security review.

Mitigation: Review their content and applicable licenses before downloading or adding them.

Risk: Preferences and activation state may persist locally.

Mitigation: Inspect or clear the saved state when preferences should not persist.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/thomaszhou22/skills/mega-prompt-optimizer)
- [Lite prompt template library](https://raw.githubusercontent.com/Thomaszhou22/prompt-optimizer-skill/main/references/prompt_library_lite.json)
- [Full prompt template library](https://raw.githubusercontent.com/Thomaszhou22/prompt-optimizer-skill/main/references/prompt_library_full.json)
- [Template category reference](https://github.com/Thomaszhou22/prompt-optimizer-skill/tree/main/references/categories)

## Skill Output:

**Output Type(s):** [Text, Markdown, XML]

**Output Format:** [Optimized prompts in the selected text, Markdown, or XML format; optional Markdown quality assessment]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The user selects the output format; optimization is opt-in.]

## Skill Version(s):

4.1.2 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
