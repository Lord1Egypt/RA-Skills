## Description: <br>
Gr Blog Post helps agents draft and publish Jekyll blog posts in Iris's style with SEO frontmatter, multilingual variants, internal links, and FAQ schema. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gingiris-1031](https://clawhub.ai/user/gingiris-1031) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content marketers, bloggers, and site maintainers use this skill to create Jekyll blog drafts, SEO metadata, multilingual variants, internal links, and publication steps for a GitHub-backed site. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Drafts may be sent to external translation services. <br>
Mitigation: Use draft-only mode by default, require explicit confirmation before translation, and review translated posts before publication. <br>
Risk: The workflow can update a GitHub-backed site when credentials are available. <br>
Mitigation: Restrict GitHub tokens to the intended repository and paths, require explicit confirmation before writes, and review commits before publication. <br>
Risk: Generated or translated posts may contain inaccurate content or SEO claims. <br>
Mitigation: Review every generated post, frontmatter field, and translated variant before publication. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gingiris-1031/gr-blog-post) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with YAML frontmatter examples and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose GitHub Contents API updates and translation workflows that require user-supplied credentials and review.] <br>

## Skill Version(s): <br>
1.0.2 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
