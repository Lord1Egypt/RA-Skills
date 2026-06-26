## Description: <br>
Autonomous journal content pipeline for UniqueStaysUSA that researches keywords, writes editorial content, publishes to Payload CMS, and tracks results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jhigh1594](https://clawhub.ai/user/jhigh1594) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and editorial operators use this skill to run an end-to-end travel journal workflow: select the next content-calendar topic, research keywords and stays, draft and optimize an article, publish it to Payload CMS, and sync progress tracking. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automatically publish to Payload CMS. <br>
Mitigation: Use staging or draft-only CMS credentials where possible and require manual review before publishing. <br>
Risk: The skill can edit project files and create git commits. <br>
Mitigation: Require manual review before git commits and inspect the planned file changes before allowing autonomous sync. <br>
Risk: The skill can continue looping from broad prompts without a clear approval gate. <br>
Mitigation: Inspect the content calendar, scripts/ralph state files, and .claude loop files before running autonomous mode. <br>
Risk: The workflow depends on the /elite-copywriter skill for draft generation. <br>
Mitigation: Verify the /elite-copywriter dependency before enabling the pipeline. <br>


## Reference(s): <br>
- [Journal Pipeline README](artifact/README.md) <br>
- [Article Templates](artifact/references/article-templates.md) <br>
- [Quality Checklist](artifact/references/quality-checklist.md) <br>
- [SEO Requirements](artifact/references/seo-requirements.md) <br>
- [ClawHub Release Page](https://clawhub.ai/jhigh1594/journal-pipeline) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline code blocks, API request examples, CMS publishing instructions, and generated content files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May publish CMS records, update local tracking files, and create git commits when run in full autonomous mode.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
