## Description: <br>
Research competitors, analyze top-ranking content, and generate a fully SEO-optimized 2000+ word blog post with headings, FAQ, meta description, and internal linking suggestions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dreamsarts](https://clawhub.ai/user/dreamsarts) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, marketers, and content teams use this skill to research search competitors and generate publication-ready SEO blog posts with metadata, headings, FAQ content, and internal-link suggestions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a live Chrome session to browse Google search results and competitor sites from the user's machine. <br>
Mitigation: Run it with an isolated Chrome profile or test account, and confirm that automated browsing is acceptable for the target environment. <br>
Risk: The skill sends researched competitor context and the generated prompt to Gemini for content generation. <br>
Mitigation: Avoid confidential campaign, client, or unpublished business data in prompts, and review generated articles before publishing. <br>
Risk: The artifact references a hard-coded local .env path for the Gemini API key. <br>
Mitigation: Provide a dedicated Gemini API key through a controlled environment variable or deployment secret instead of relying on a personal local path. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dreamsarts/openclaw-seo-content-engine) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown article with YAML frontmatter, plus CLI and Python usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated articles can include title, meta description, target and secondary keywords, estimated word count, reading time, FAQ sections, and internal-link suggestions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
