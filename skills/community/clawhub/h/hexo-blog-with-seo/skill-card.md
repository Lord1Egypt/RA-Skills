## Description:

Draft and publish Hexo posts end-to-end with front matter, SEO polish, and deployment support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jarxi](https://clawhub.ai/user/jarxi)

### License/Terms of Use:


## Use Case:

Developers and content maintainers use this skill to draft unpublished Hexo posts, polish existing Markdown for SEO, and publish through the Hexo deployment workflow after explicit approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can deploy live site changes using configured git or hosting credentials.

Mitigation: Require fresh explicit approval after reviewing the target remote and pending changes before running deployment.

Risk: The workflow uses unpinned npx Hexo commands.

Mitigation: Prefer a pinned, lockfile-backed local Hexo command or a vetted repository script.

Risk: The skill may edit existing Markdown, configuration, or generated output in a Hexo repository.

Mitigation: Review diffs before publishing and keep changes scoped to the requested post or deployment step.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jarxi/skills/hexo-blog-with-seo)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown posts with YAML front matter, status updates, and Hexo shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May modify Hexo blog files and run deployment commands when explicitly approved.]

## Skill Version(s):

1.0.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
