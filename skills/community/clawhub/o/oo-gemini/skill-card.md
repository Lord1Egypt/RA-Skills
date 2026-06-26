## Description: <br>
Gemini (ai.google.dev). Use this skill for ANY Gemini request - searching and reading data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to operate Gemini through an OOMOL-connected account for content generation, speech audio generation, image generation, embeddings, token counting, model discovery, and Gemini Veo video workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Gemini account connection through OOMOL and uses server-side credential injection. <br>
Mitigation: Install and use it only when the user accepts connecting Gemini through OOMOL; do not request or handle raw Gemini credentials. <br>
Risk: Media generation and Gemini Veo video workflows can create billable or long-running operations. <br>
Mitigation: Review payloads, model choices, and intended generation scope before running costly actions. <br>
Risk: First-time setup includes CLI installer commands. <br>
Mitigation: Verify the oo CLI installer source before running installation commands. <br>


## Reference(s): <br>
- [Gemini API Documentation](https://ai.google.dev/gemini-api) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [Gemini skill on ClawHub](https://clawhub.ai/oomol/oo-gemini) <br>
- [OOMOL publisher profile on ClawHub](https://clawhub.ai/user/oomol) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return Gemini connector results such as generated content, embeddings, image or video transit URLs, token counts, model lists, and operation metadata.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
