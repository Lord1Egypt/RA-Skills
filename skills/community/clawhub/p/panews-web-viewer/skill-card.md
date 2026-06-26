## Description: <br>
Read public PANews website pages as Markdown for homepage, article-page, and column-page reads. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[medz](https://clawhub.ai/user/medz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to retrieve rendered PANews homepage, article, or column content as Markdown with page metadata when they have or imply a PANews page URL. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A PANews path without a language prefix defaults to Chinese, which may not match the user's intended locale. <br>
Mitigation: Specify a supported locale prefix such as /en, /ja, /ko, /zh, or /zh-hant before fetching. <br>
Risk: Unavailable pages can return 404 responses. <br>
Mitigation: Report 404 pages as unavailable rather than synthesizing content from other endpoints. <br>


## Reference(s): <br>
- [PANews website](https://www.panewslab.com) <br>
- [PANews English homepage](https://www.panewslab.com/en) <br>
- [ClawHub skill page](https://clawhub.ai/medz/panews-web-viewer) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown response with YAML frontmatter metadata] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Preserves rendered page structure and reports 404 pages as unavailable.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
