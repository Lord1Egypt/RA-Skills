## Description: <br>
pageclaw converts structured page-story markdown files into polished single-file static HTML pages through a guided design, planning, build, and quality-review pipeline. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[XY-Showing](https://clawhub.ai/user/XY-Showing) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, designers, researchers, and profile-page authors use this skill to turn structured markdown briefs into static personal, academic, portfolio, or project pages while preserving the source story structure. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create or update local project files, including page-story.md, docs/plans files, and index.html. <br>
Mitigation: Run it in the intended workspace, keep the project under version control, and review generated file diffs before committing or publishing. <br>
Risk: Reference URLs may be fetched during design analysis, and generated pages may load fonts or icons from third-party CDNs. <br>
Mitigation: Use trusted reference URLs and vendor or inline external assets when third-party runtime requests are not acceptable. <br>


## Reference(s): <br>
- [ClawHub pageclaw release](https://clawhub.ai/XY-Showing/pageclaw) <br>
- [pageclaw GitHub repository](https://github.com/XY-Showing/pageclaw) <br>
- [pageclaw README](skills/page-claw/README.md) <br>
- [page-story starter template](skills/page-claw/page-story-starter.md) <br>
- [Simple Icons](https://simpleicons.org/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Files, Guidance] <br>
**Output Format:** [Markdown plans plus a single-file static HTML page] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates or updates page-story.md when missing, docs/plans design and implementation markdown files, and index.html in the project root.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
