## Description: <br>
Drop coral-gradient pins on any HTML page, write feedback in an inline glass note popup, and copy annotations as Markdown, plain text, or JSON for design review. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xuxinmaxen](https://clawhub.ai/user/xuxinmaxen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, designers, and product reviewers use this skill to add an annotation overlay to HTML prototypes or authorized web pages, collect point-specific feedback, and export review notes for handoff. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Running page-injected JavaScript on arbitrary, competitor, or sensitive authenticated sites may expose the reviewer to unwanted page manipulation or data-handling risk. <br>
Mitigation: Use the skill only on local prototypes, staging pages, or sites you own or are authorized to test; avoid banking, admin, healthcare, enterprise, customer-data, and other sensitive authenticated pages. <br>
Risk: A hosted or CDN bookmarklet can execute mutable external JavaScript if it is loaded from an unpinned or unreviewed URL. <br>
Mitigation: Prefer the self-contained local script or bookmarklet; if hosting is required, pin to a reviewed immutable version instead of a moving branch or generic hosted URL. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xuxinmaxen/html-mark) <br>
- [README](README.md) <br>
- [Basic HTML injection example](examples/basic.md) <br>
- [Advanced bookmarklet example](examples/advanced.md) <br>
- [Manual smoke test](tests/test.md) <br>


## Skill Output: <br>
**Output Type(s):** [code, shell commands, markdown, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline HTML, JavaScript, and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce a self-contained script injection pattern, external script tag, or bookmarklet instructions depending on the target workflow.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
