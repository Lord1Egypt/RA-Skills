## Description: <br>
Journalism Agent researches, drafts, edits, and fact-checks publication-quality articles and image-supported newsletters for OpenClaw. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[defineagain](https://clawhub.ai/user/defineagain) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and content teams use this skill to research topics, draft attributed longform articles, curate event listings, and assemble mixed newsletters with images, captions, and source checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Image search or generation prompts may expose sensitive newsroom, client, investigative, or embargoed context to nkimages.com. <br>
Mitigation: Use sanitized image queries, provide approved images, or avoid the external image-generation path for sensitive work. <br>
Risk: Generated articles and event listings can contain unverified, weakly sourced, or stale claims. <br>
Mitigation: Follow the source-quality guide, verify factual claims and live event links, and remove unsupported claims before publication. <br>


## Reference(s): <br>
- [Journalism Agent ClawHub Page](https://clawhub.ai/defineagain/journalism-agent) <br>
- [Source Quality Guide](artifact/references/source-quality.md) <br>
- [NK Images Search API](https://nkimages.com/api/public/images?source=clawhub&q={query}&per_page=6) <br>
- [NK Images Generation Quota API](https://nkimages.com/api/public/generate/quota) <br>
- [NK Images Anonymous Generation API](https://nkimages.com/api/public/generate/anonymous) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, html, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown article drafts with YAML frontmatter, HTML email newsletters, shell commands, configuration values, and editorial guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include inline source citations, image credits, alt text, curated listing details, and local newsletter HTML assembled from provided parts.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence, released 2026-04-15) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
