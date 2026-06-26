## Description: <br>
Takes one long-form piece of content and repurposes it into Twitter threads, LinkedIn posts, newsletter editions, and short video scripts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[marcvanstad](https://clawhub.ai/user/marcvanstad) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Creators, marketers, agencies, and content operators use this skill to turn long-form articles, transcripts, podcasts, videos, and feeds into channel-ready social posts, newsletters, and short video scripts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can fetch URLs, feeds, videos, and files supplied by the user and save generated drafts locally. <br>
Mitigation: Run it only with trusted inputs and runtime settings, and confirm where fetched content and generated drafts are stored. <br>
Risk: Generated social posts, newsletters, and scripts may misquote source material or include inaccurate claims. <br>
Mitigation: Review every draft before publishing and keep quote-accuracy, link-integrity, tone, and character-limit checks enabled. <br>
Risk: Optional scheduling, RSS watching, or publishing workflows can repeatedly process external content. <br>
Mitigation: Enable recurring jobs and posting behavior deliberately, monitor queues and outputs, and avoid confidential source material unless the runtime and API configuration meet the user's data-handling expectations. <br>


## Reference(s): <br>
- [Skill README](README.md) <br>
- [Repurpose configuration](reference/config/repurpose.yaml) <br>
- [Source configuration](reference/config/sources.yaml) <br>
- [Narrative extraction prompt](reference/prompts/extract_narrative.yaml) <br>
- [Twitter thread prompt](reference/prompts/twitter_thread.yaml) <br>
- [LinkedIn post prompt](reference/prompts/linkedin_post.yaml) <br>
- [Quality checks template](reference/templates/quality_checks.yaml) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, shell commands, guidance] <br>
**Output Format:** [Markdown drafts, text scripts, YAML configuration, and command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated drafts are organized by platform under local output folders; configured quality checks cover length, tone, quote accuracy, links, duplicate content, hashtags, and CTA presence.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
