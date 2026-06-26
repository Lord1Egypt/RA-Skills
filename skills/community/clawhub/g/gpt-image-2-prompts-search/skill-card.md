## Description: <br>
Recommends suitable prompts from a curated library of 1,000+ GPT Image 2 image-generation prompts based on user needs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mindy-youmind](https://clawhub.ai/user/mindy-youmind) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Creators, marketers, designers, and developers use this skill to find image-generation prompt templates with sample images and adapt selected prompts for articles, videos, product visuals, social posts, and related creative work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill downloads and refreshes prompt reference data from GitHub and agents may fetch sample images from downloaded prompt records. <br>
Mitigation: Install only in environments where this network access is acceptable; review or pin reference data and disable automatic install scripts where stricter change control is required. <br>
Risk: Users may paste confidential drafts, credentials, or sensitive personal data into prompt remix requests. <br>
Mitigation: Avoid submitting confidential, credential-bearing, or sensitive personal data; sanitize source content before asking for prompt customization. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mindy-youmind/gpt-image-2-prompts-search) <br>
- [YouMind GPT Image 2 prompt gallery](https://youmind.com/gpt-image-2-prompts) <br>
- [Reference data location described by the skill](https://github.com/YouMind-OpenLab/gpt-image-2-prompts-search/tree/main/references) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown responses with prompt previews, links, sample image references, and optional shell commands for refreshing local reference data] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Recommendations are capped to at most three prompts per request; full prompt text is preserved for customization when a prompt is selected.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence, SKILL.md frontmatter, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
