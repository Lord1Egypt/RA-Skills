## Description:

Search, rewrite, and generate Seedance 2.0 video prompts with cinematic variants and bilingual output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[x-rayluan](https://clawhub.ai/user/x-rayluan)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, developers, and agent users use this skill to find, adapt, translate, and generate concise Seedance-ready video prompts from a curated prompt-library workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional helper script contacts GitHub raw README URLs to search upstream prompt entries.

Mitigation: Review network access expectations before installation or use the skill without the optional helper script in restricted environments.

Risk: The skill may return both Chinese and English prompt variants when bilingual output is useful.

Mitigation: Ask for a single output language when only one language should be produced.

Risk: Some prompt material is adapted from an upstream CC BY 4.0 collection and may require attribution when reused or redistributed.

Mitigation: Keep attribution to the upstream YouMind-OpenLab Seedance prompt collection when quoting, bundling, or prominently adapting source prompts.

## Reference(s):

- [OpenClaw Seedance Prompt Library](https://clawhub.ai/x-rayluan/skills/openclaw-seedance-prompt-library)
- [Source Attribution](references/source-attribution.md)
- [Usage Patterns](references/usage-patterns.md)
- [Upstream Seedance prompt collection](https://github.com/YouMind-OpenLab/awesome-seedance-2-prompts)
- [Upstream English README](https://raw.githubusercontent.com/YouMind-OpenLab/awesome-seedance-2-prompts/main/README.md)
- [Upstream Chinese README](https://raw.githubusercontent.com/YouMind-OpenLab/awesome-seedance-2-prompts/main/README_zh.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with curated prompt examples, rewritten prompts, bilingual prompt variants, and optional shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are intentionally small and curated, typically returning 3-8 examples or safe, stylized, and experimental prompt variants.]

## Skill Version(s):

1.0.2 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
