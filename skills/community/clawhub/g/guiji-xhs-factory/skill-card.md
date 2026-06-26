## Description: <br>
Batch-generates Xiaohongshu infographic cards and slideshow videos, then prepares video-note drafts for scheduled or manual publishing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[houdaliang](https://clawhub.ai/user/houdaliang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators and operators use this skill to define Xiaohongshu post content, generate vertical infographic images and slideshow videos, and prepare browser-assisted upload drafts for review before publishing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill automates a logged-in browser session through Chrome remote debugging. <br>
Mitigation: Use a dedicated Chrome profile or account, bind remote debugging to localhost, and review the prepared draft before manually publishing. <br>
Risk: The artifact includes hard-coded local paths that may not match the install environment. <br>
Mitigation: Inspect and adjust local paths before running generation or publishing scripts. <br>
Risk: Recurring scheduled publishing can prepare drafts repeatedly without fresh review of generated content. <br>
Mitigation: Enable scheduled jobs only after reviewing the workflow and keep manual confirmation before final publication. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/houdaliang/guiji-xhs-factory) <br>
- [Publisher profile](https://clawhub.ai/user/houdaliang) <br>
- [Post templates](references/post-templates.md) <br>
- [Publishing rules](references/publish-rules.md) <br>
- [Xiaohongshu creator publishing page](https://creator.xiaohongshu.com/publish/publish?from=homepage&target=video) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, Python and JavaScript scripts, generated PNG images, MP4 slideshow videos, and a JSON manifest.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated assets are written to local content queue and upload paths; publishing remains a human-confirmed browser action.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
